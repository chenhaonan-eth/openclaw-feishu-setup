# Feishu Setup Skill for OpenClaw

一键安装和配置飞书/Lark 频道插件，使用 WebSocket 长连接模式（无需公网 URL）。

## 功能

- 自动安装 `@openclaw/feishu` 插件
- 自动配置 WebSocket 长连接模式
- 自动更新 OpenClaw 配置文件
- 自动重启 gateway
- 提供配对指引

## 使用方法

### 自动安装（推荐）

```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/openclaw-feishu-setup/main/setup.sh)
```

### 手动安装

1. 克隆仓库到 OpenClaw skills 目录：

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/openclaw-feishu-setup.git feishu-setup
```

2. 运行安装脚本：

```bash
cd feishu-setup
chmod +x setup.sh
./setup.sh
```

3. 按提示输入：
   - Feishu App ID (cli_xxx)
   - Feishu App Secret

### 通过 OpenClaw Agent

直接告诉 agent：

```
帮我安装飞书插件
```

Agent 会自动读取 SKILL.md 并执行安装流程。

## 前置要求

- OpenClaw 已安装
- Node.js 和 npm 可用
- 已在飞书开放平台创建应用并获取 App ID 和 App Secret

## 获取飞书凭证

1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 启用机器人能力
5. 配置权限：
   - 接收消息
   - 发送消息
   - 获取用户信息

## 配对流程

安装完成后：

1. 在飞书中找到你的 bot
2. 发送任意消息
3. Bot 会返回配对码，例如：`W8YR3K5Q`
4. 在终端运行：

```bash
openclaw pairing approve feishu W8YR3K5Q
```

5. 完成！现在可以正常对话了

## 配置说明

脚本会自动修改 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "connectionMode": "websocket",
      "accounts": {
        "default": {
          "appId": "cli_xxx",
          "appSecret": "xxx"
        }
      }
    }
  }
}
```

- `connectionMode: "websocket"` - 使用长连接，无需公网 URL
- `dmPolicy: "pairing"` - 需要配对才能使用（安全）

## 故障排查

### 插件加载失败

```bash
# 检查依赖
cd $(npm root -g)/openclaw/extensions/feishu
npm install
```

### Gateway 未启动

```bash
# 检查进程
ps aux | grep "openclaw gateway"

# 重启
openclaw gateway &
```

### 飞书未显示在状态中

```bash
# 验证配置
openclaw channels status
openclaw channels capabilities | grep -i feishu
```

## 功能特性

安装后可用的工具：

- `feishu_doc` - 飞书文档操作
- `feishu_chat` - 群聊管理
- `feishu_wiki` - 知识库操作
- `feishu_drive` - 云空间管理
- `feishu_bitable` - 多维表格操作

## 参考链接

- [飞书开放平台](https://open.feishu.cn)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [飞书插件源码](https://github.com/openclaw/openclaw/tree/main/extensions/feishu)

## License

MIT
