# OpenClaw Feishu Workflow

用于两类事情：

1. 安装/配置/修复 OpenClaw 的飞书（Lark）接入
2. 将本地 Markdown 待办同步到 Feishu Tasks

## 仓库定位

这不是在重复实现飞书插件本身。

底层能力来自 OpenClaw 社区维护的 `@openclaw/feishu`，本仓库负责的是上层 workflow：
- setup / repair
- pairing guidance
- todo → Feishu Task sync
- cron-based auto sync

## 快速入口

### 1. 飞书接入安装

```bash
chmod +x setup.sh
./setup.sh
```

### 2. 本地待办同步到 Feishu Task

```bash
python3 scripts/feishu_task_sync.py \
  --todo-file "$HOME/.openclaw/workspace/mandala/生活系统/待办事项/当前.md" \
  --section-title "## 飞书同步优先清单" \
  --tasklist-name "我的待办同步" \
  --user-open-id "ou_xxx" \
  --state-file "./feishu_task_sync_state.local.json"
```

## 参考

- 官方教程（飞书）：https://www.feishu.cn/content/article/7613711414611463386
- 飞书开放平台：https://open.feishu.cn
- OpenClaw 文档：https://docs.openclaw.ai
- OpenClaw Feishu 插件源码：https://github.com/openclaw/openclaw/tree/main/extensions/feishu

## 说明

- 不要提交真实 state 文件
- 不要提交真实 token / secret / open_id
- 更详细的 skill 用法见 `SKILL.md`
- 更详细的 task sync 说明见 `references/task-sync.md`
