#!/usr/bin/env python3
"""
Feishu task sync helper for OpenClaw workspaces.

What it does:
- Reads a designated section from a local todo markdown file
- Calls Feishu task tools through OpenClaw Gateway (/tools/invoke)
- Creates or reuses a Feishu tasklist
- Adds the target user as tasklist editor
- Creates missing tasks
- Tries to update changed tasks (summary / due / priority)
- Persists sync mapping in a local state JSON file

Suggested usage:
  python3 scripts/feishu_task_sync.py \
    --todo-file "$HOME/.openclaw/workspace/mandala/生活系统/待办事项/当前.md" \
    --section-title "## 飞书同步优先清单" \
    --tasklist-name "我的待办同步" \
    --user-open-id "ou_xxx"

Notes:
- Add-or-modify only. No delete behavior.
- If some Feishu historical tasks fail to update, they are recorded in pending_updates.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_GATEWAY_URL = "http://127.0.0.1:18789/tools/invoke"
DEFAULT_CONFIG_FILE = Path.home() / ".openclaw/openclaw.json"


@dataclass
class TaskItem:
    summary: str
    priority: str | None = None
    due: str | None = None

    @property
    def key(self) -> str:
        return self.summary.strip()


@dataclass
class SyncState:
    tasklist_guid: str | None
    tasklist_url: str | None
    synced_tasks: dict[str, dict[str, Any]]
    pending_updates: dict[str, dict[str, Any]]
    last_sync_at: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--todo-file", required=True)
    parser.add_argument("--section-title", required=True)
    parser.add_argument("--tasklist-name", required=True)
    parser.add_argument("--user-open-id", required=True)
    parser.add_argument("--state-file", default="./feishu_task_sync_state.json")
    parser.add_argument("--gateway-url", default=DEFAULT_GATEWAY_URL)
    parser.add_argument("--config-file", default=str(DEFAULT_CONFIG_FILE))
    return parser.parse_args()


def load_gateway_token(config_file: Path) -> str:
    data = json.loads(config_file.read_text(encoding="utf-8"))
    token = data.get("gateway", {}).get("auth", {}).get("token")
    if not token:
        raise RuntimeError(f"gateway token not found in {config_file}")
    return token


def invoke_tool(token: str, gateway_url: str, tool: str, args: dict[str, Any]) -> dict[str, Any]:
    payload = json.dumps({"tool": tool, "args": args}).encode("utf-8")
    req = urllib.request.Request(
        gateway_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not data.get("ok"):
        raise RuntimeError(f"tool call failed: {tool}: {data}")
    return data["result"].get("details", {})


def load_state(state_file: Path) -> SyncState:
    if not state_file.exists():
        return SyncState(tasklist_guid=None, tasklist_url=None, synced_tasks={}, pending_updates={}, last_sync_at=None)
    data = json.loads(state_file.read_text(encoding="utf-8"))
    return SyncState(
        tasklist_guid=data.get("tasklist_guid"),
        tasklist_url=data.get("tasklist_url"),
        synced_tasks=data.get("synced_tasks", {}),
        pending_updates=data.get("pending_updates", {}),
        last_sync_at=data.get("last_sync_at"),
    )


def save_state(state_file: Path, state: SyncState) -> None:
    state_file.write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_sync_section(todo_file: Path, section_title: str) -> list[TaskItem]:
    text = todo_file.read_text(encoding="utf-8")
    if section_title not in text:
        raise RuntimeError(f"section not found: {section_title}")
    after = text.split(section_title, 1)[1]
    lines = after.splitlines()
    tasks: list[TaskItem] = []
    current: TaskItem | None = None
    for line in lines:
        if line.startswith("## ") and line.strip() != section_title:
            break
        m = re.match(r"^- \[ \] (.+)$", line.strip())
        if m:
            if current:
                tasks.append(current)
            current = TaskItem(summary=m.group(1).strip())
            continue
        if current is None:
            continue
        p = re.match(r"^- 优先级：(.+)$", line.strip())
        if p:
            current.priority = p.group(1).strip()
            continue
        d = re.match(r"^- 截止：([0-9]{4}-[0-9]{2}-[0-9]{2})$", line.strip())
        if d:
            current.due = d.group(1).strip()
            continue
    if current:
        tasks.append(current)
    return tasks


def ensure_tasklist(token: str, gateway_url: str, state: SyncState, tasklist_name: str, user_open_id: str) -> SyncState:
    if state.tasklist_guid:
        return state
    suffix = datetime.now().strftime("%Y-%m-%d")
    detail = invoke_tool(token, gateway_url, "feishu_tasklist_create", {"name": f"{tasklist_name} {suffix}"})
    tasklist = detail["tasklist"]
    state.tasklist_guid = tasklist["guid"]
    state.tasklist_url = tasklist["url"]
    invoke_tool(token, gateway_url, "feishu_tasklist_add_members", {
        "tasklist_guid": state.tasklist_guid,
        "members": [{"id": user_open_id, "type": "user", "role": "editor"}],
        "user_id_type": "open_id",
    })
    return state


def build_description(task: TaskItem) -> str:
    parts = ["Source: local todo sync section"]
    if task.priority:
        parts.append(f"Priority: {task.priority}")
    if task.due:
        parts.append(f"Due: {task.due}")
    return "\n".join(parts)


def due_payload(due: str | None) -> dict[str, Any] | None:
    if not due:
        return None
    due_dt = datetime.strptime(due, "%Y-%m-%d")
    return {"timestamp": str(int(due_dt.timestamp() * 1000)), "is_all_day": True}


def create_task(token: str, gateway_url: str, tasklist_guid: str, task: TaskItem) -> dict[str, Any]:
    args: dict[str, Any] = {
        "summary": task.summary,
        "description": build_description(task),
        "tasklists": [{"tasklist_guid": tasklist_guid}],
    }
    due = due_payload(task.due)
    if due:
        args["due"] = due
    detail = invoke_tool(token, gateway_url, "feishu_task_create", args)
    return detail["task"]


def update_task(token: str, gateway_url: str, task_guid: str, task: TaskItem) -> dict[str, Any]:
    update_fields = ["summary", "description"]
    body: dict[str, Any] = {"summary": task.summary, "description": build_description(task)}
    due = due_payload(task.due)
    if due:
        body["due"] = due
        update_fields.append("due")
    detail = invoke_tool(token, gateway_url, "feishu_task_update", {
        "task_guid": task_guid,
        "task": body,
        "update_fields": update_fields,
    })
    task_detail = detail.get("task")
    if not task_detail:
        raise RuntimeError(f"feishu_task_update returned no task payload: {detail}")
    return task_detail


def needs_update(stored: dict[str, Any], task: TaskItem) -> bool:
    return (
        stored.get("last_summary") != task.summary
        or stored.get("last_due") != task.due
        or stored.get("last_priority") != task.priority
    )


def main() -> int:
    args = parse_args()
    todo_file = Path(args.todo_file).expanduser()
    state_file = Path(args.state_file).expanduser()
    config_file = Path(args.config_file).expanduser()

    token = load_gateway_token(config_file)
    state = load_state(state_file)
    state = ensure_tasklist(token, args.gateway_url, state, args.tasklist_name, args.user_open_id)
    tasks = parse_sync_section(todo_file, args.section_title)

    created = 0
    updated = 0
    skipped = 0
    update_failed = 0

    for task in tasks:
        stored = state.synced_tasks.get(task.key)
        if not stored or not stored.get("guid"):
            created_task = create_task(token, args.gateway_url, state.tasklist_guid, task)
            state.synced_tasks[task.key] = {
                "guid": created_task.get("guid"),
                "url": created_task.get("url"),
                "task_id": created_task.get("task_id"),
                "last_summary": task.summary,
                "last_due": task.due,
                "last_priority": task.priority,
            }
            created += 1
            continue

        if needs_update(stored, task):
            try:
                updated_task = update_task(token, args.gateway_url, stored["guid"], task)
                stored.update({
                    "url": updated_task.get("url", stored.get("url")),
                    "task_id": updated_task.get("task_id", stored.get("task_id")),
                    "last_summary": task.summary,
                    "last_due": task.due,
                    "last_priority": task.priority,
                })
                state.pending_updates.pop(task.key, None)
                updated += 1
            except Exception as exc:
                state.pending_updates[task.key] = {
                    "guid": stored.get("guid"),
                    "wanted_summary": task.summary,
                    "wanted_due": task.due,
                    "wanted_priority": task.priority,
                    "error": str(exc),
                    "recorded_at": datetime.now().isoformat(timespec="seconds"),
                }
                update_failed += 1
            continue

        skipped += 1

    state.last_sync_at = datetime.now().isoformat(timespec="seconds")
    save_state(state_file, state)
    print(json.dumps({
        "tasklist_guid": state.tasklist_guid,
        "tasklist_url": state.tasklist_url,
        "created": created,
        "updated": updated,
        "update_failed": update_failed,
        "skipped": skipped,
        "pending_updates": len(state.pending_updates),
        "total_local_tasks": len(tasks),
        "state_file": str(state_file),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
