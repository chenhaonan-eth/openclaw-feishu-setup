---
name: feishu-workflow
description: Install, configure, or repair Feishu/Lark integration for OpenClaw, including channel setup, websocket connection mode, plugin enablement, pairing guidance, official tutorial references, and Feishu Task-based todo sync workflow. Use when the user asks to install Feishu, configure Lark, fix Feishu connection, enable Feishu task tools, read Feishu setup tutorials, or sync local markdown todos into Feishu Tasks.
---

# Feishu Setup

Use this skill to do one of two things:

1. Set up or repair the OpenClaw Feishu/Lark channel
2. Sync local markdown todos into Feishu Tasks through OpenClaw's built-in Feishu task tools

## Workflow

### A. Channel setup / repair

If the user needs Feishu/Lark connection setup:

- Use `setup.sh` for guided installation when shell execution is appropriate
- Ensure OpenClaw config enables the `feishu` channel and plugin entry
- Prefer websocket mode
- Restart gateway only when needed
- Guide pairing after the bot is reachable

### B. Todo → Feishu Task sync

If the user wants local todos synced to Feishu Tasks:

- Use `scripts/feishu_task_sync.py`
- Feed it a markdown todo file, a section title, a tasklist name, and the target user's `open_id`
- Keep the tasklist owner as the bot/app
- Add the human user as `editor`
- Store task mapping in a local state file that is NOT committed

## Read next when needed

- For detailed sync script usage and cron examples, read `references/task-sync.md`
- For installation and pairing flow details, read `README.md` only if you need repo-oriented setup context

## Rules

- Do not commit real secrets, real gateway tokens, or real local state files
- Prefer OpenClaw built-in Feishu task tools over reimplementing raw Feishu API calls
- Treat this skill as workflow glue around community-maintained Feishu plugin capabilities, not a replacement for the plugin
