# OpenClaw Feishu Workflow

中文｜English

用于两类事情：
1. 安装、配置、修复 OpenClaw 的飞书 / Lark 接入
2. 将本地 Markdown 待办同步到 Feishu Tasks

This repository covers two main jobs:
1. Install, configure, or repair Feishu / Lark integration for OpenClaw
2. Sync local Markdown todos into Feishu Tasks

---

## 仓库定位 | Positioning

这不是在重复实现飞书插件本身。
底层能力来自 OpenClaw 社区维护的 `@openclaw/feishu`；本仓库负责的是更上层的 workflow：
- setup / repair
- pairing guidance
- todo → Feishu Task sync
- cron-based auto sync

This repo does **not** replace the Feishu plugin itself.
Core Feishu capability comes from the community-maintained `@openclaw/feishu` plugin.
This repo focuses on the workflow layer above it:
- setup / repair
- pairing guidance
- todo → Feishu Task sync
- cron-based auto sync

---

## 快速开始 | Quick Start

### 1. 飞书接入安装 | Install Feishu integration

```bash
chmod +x setup.sh
./setup.sh
```

### 2. 本地待办同步到 Feishu Task | Sync local todos to Feishu Tasks

```bash
python3 scripts/feishu_task_sync.py \
  --todo-file "$HOME/.openclaw/workspace/mandala/生活系统/待办事项/当前.md" \
  --section-title "## 飞书同步优先清单" \
  --tasklist-name "我的待办同步" \
  --user-open-id "ou_xxx" \
  --state-file "./feishu_task_sync_state.local.json"
```

---

## 主要能力 | Main Capabilities

- 安装并配置 OpenClaw 飞书通道
- 修复常见 Feishu / Lark 接入问题
- 引导 pairing 流程
- 将本地 Markdown 待办同步到 Feishu Tasklist
- 通过本地 state 文件做去重和映射
- 支持配合 OpenClaw cron 做自动同步

- Install and configure the OpenClaw Feishu channel
- Repair common Feishu / Lark integration issues
- Guide pairing flow
- Sync local Markdown todos into a Feishu tasklist
- Maintain deduplication and task mapping through a local state file
- Support automatic sync via OpenClaw cron

---

## 参考链接 | References

- 飞书官方教程 | Official Feishu tutorial: https://www.feishu.cn/content/article/7613711414611463386
- 飞书开放平台 | Feishu Open Platform: https://open.feishu.cn
- OpenClaw 文档 | OpenClaw docs: https://docs.openclaw.ai
- OpenClaw Feishu 插件源码 | OpenClaw Feishu plugin source: https://github.com/openclaw/openclaw/tree/main/extensions/feishu

---

## 注意事项 | Notes

- 不要提交真实 state 文件
- 不要提交真实 token / secret / open_id
- 更详细的 skill 用法见 `SKILL.md`
- 更详细的 task sync 说明见 `references/task-sync.md`

- Do not commit real state files
- Do not commit real tokens / secrets / open_id values
- See `SKILL.md` for skill-oriented usage
- See `references/task-sync.md` for detailed task sync behavior
