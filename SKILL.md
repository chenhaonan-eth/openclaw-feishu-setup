# Feishu Setup Skill

Auto-install and configure Feishu/Lark channel for OpenClaw with WebSocket long-connection mode.

## Usage

User provides:
- App ID (cli_xxx)
- App Secret

Agent will:
1. Install @openclaw/feishu plugin
2. Install plugin dependencies
3. Configure openclaw.json with WebSocket mode
4. Restart gateway
5. Guide user through pairing

## Trigger

When user mentions:
- "安装飞书"
- "配置飞书"
- "setup feishu"
- "install lark"

## Prerequisites

- OpenClaw installed
- npm available
- Gateway not running or can be restarted

## Configuration

Adds to `~/.openclaw/openclaw.json`:

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
  },
  "plugins": {
    "allow": [..., "feishu"],
    "load": {
      "paths": [..., "/path/to/feishu"]
    },
    "entries": {
      "feishu": { "enabled": true }
    }
  }
}
```

## Steps

### 1. Install Plugin

```bash
npm install -g @openclaw/feishu
```

### 2. Install Dependencies

```bash
cd $(npm root -g)/openclaw/extensions/feishu
npm install
```

### 3. Update Config

Edit `~/.openclaw/openclaw.json`:
- Add feishu to channels
- Add feishu to plugins.allow
- Add feishu path to plugins.load.paths
- Add feishu to plugins.entries

### 4. Restart Gateway

```bash
pkill -f "openclaw gateway"
openclaw gateway &
```

### 5. Verify

```bash
openclaw channels status
```

Should show: `Feishu default: enabled, configured, running`

### 6. Pairing

User sends message to bot in Feishu, gets pairing code.

Agent runs:
```bash
openclaw pairing approve feishu <CODE>
```

## Troubleshooting

### Plugin fails to load

**Error**: `Cannot find module '@larksuiteoapi/node-sdk'`

**Fix**: Install dependencies in plugin directory

### Gateway not starting

**Check**: `ps aux | grep "openclaw gateway"`

**Restart**: `openclaw gateway &`

### Feishu not in status

**Check**: `openclaw channels capabilities | grep -i feishu`

**Fix**: Verify config and restart gateway

## Notes

- Uses WebSocket mode (no public URL needed)
- Default dmPolicy is "pairing" (requires approval)
- Supports direct messages and group chats
- Includes doc/wiki/drive/bitable tools

## References

- Feishu Open Platform: https://open.feishu.cn
- OpenClaw Docs: https://docs.openclaw.ai/channels/feishu
- Plugin Source: https://github.com/openclaw/openclaw (extensions/feishu)
