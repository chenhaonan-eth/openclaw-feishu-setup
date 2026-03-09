# Task Sync Reference

## Purpose

`../scripts/feishu_task_sync.py` is a workflow helper built on top of OpenClaw's built-in Feishu task tools.

It handles:
- parsing a markdown todo section
- creating/reusing a Feishu tasklist
- adding a user as tasklist editor
- creating missing tasks
- attempting incremental updates
- recording failures in `pending_updates`
- persisting local ↔ remote mapping in a state file

## Recommended command

```bash
python3 scripts/feishu_task_sync.py \
  --todo-file "$HOME/.openclaw/workspace/mandala/生活系统/待办事项/当前.md" \
  --section-title "## 飞书同步优先清单" \
  --tasklist-name "我的待办同步" \
  --user-open-id "ou_xxx" \
  --state-file "./feishu_task_sync_state.local.json"
```

## Expected markdown shape

```md
## 飞书同步优先清单
- [ ] 任务 A
  - 优先级：high
  - 截止：2026-03-10
- [ ] 任务 B
  - 优先级：medium
```

The script currently reads:
- task summary
- priority
- due date (`YYYY-MM-DD`)

## State file guidance

Do not commit real state files.

Recommended names:
- `feishu_task_sync_state.local.json`
- `.cache/feishu_task_sync_state.json`

The state file stores:
- `tasklist_guid`
- `tasklist_url`
- `synced_tasks`
- `pending_updates`
- `last_sync_at`

## Cron example

```bash
openclaw cron add \
  --name feishu-task-sync-v1 \
  --every 10m \
  --session isolated \
  --agent main \
  --no-deliver \
  --message "Run python3 /path/to/feishu_task_sync.py ...; reply NO_REPLY when nothing changed"
```

## Known edge case

Some historical Feishu tasks may fail on update and return 404.

Current handling:
- do not fail the whole sync run
- record the item into `pending_updates`
- continue syncing the rest

## Positioning

This is not a replacement for `@openclaw/feishu`.
It is a workflow layer on top of these built-in tools:

For the broader Feishu setup flow, also reference the official tutorial:
- https://www.feishu.cn/content/article/7613711414611463386

Built-in tools used here:
- `feishu_task_create`
- `feishu_task_get`
- `feishu_task_update`
- `feishu_tasklist_create`
- `feishu_tasklist_add_members`
