#!/bin/bash
set -e

echo "🦞 OpenClaw Feishu Setup"
echo ""

# Check prerequisites
if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install Node.js first."
    exit 1
fi

if ! command -v openclaw &> /dev/null; then
    echo "❌ openclaw not found. Please install OpenClaw first."
    exit 1
fi

# Get credentials
read -p "Enter Feishu App ID (cli_xxx): " APP_ID
read -sp "Enter Feishu App Secret: " APP_SECRET
echo ""

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ]; then
    echo "❌ App ID and Secret are required"
    exit 1
fi

# Install plugin
echo "📦 Installing @openclaw/feishu..."
npm install -g @openclaw/feishu

# Install dependencies
FEISHU_PATH=$(npm root -g)/openclaw/extensions/feishu
echo "📦 Installing plugin dependencies..."
cd "$FEISHU_PATH"
npm install

# Update config
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
echo "⚙️  Updating configuration..."

# Backup config
cp "$CONFIG_FILE" "$CONFIG_FILE.backup"

# Use Node.js to update JSON
node << EOF
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));

// Add feishu channel
if (!config.channels) config.channels = {};
config.channels.feishu = {
  enabled: true,
  dmPolicy: 'pairing',
  connectionMode: 'websocket',
  accounts: {
    default: {
      appId: '$APP_ID',
      appSecret: '$APP_SECRET'
    }
  }
};

// Add to plugins.allow
if (!config.plugins) config.plugins = {};
if (!config.plugins.allow) config.plugins.allow = [];
if (!config.plugins.allow.includes('feishu')) {
  config.plugins.allow.push('feishu');
}

// Add to plugins.load.paths
if (!config.plugins.load) config.plugins.load = {};
if (!config.plugins.load.paths) config.plugins.load.paths = [];
const feishuPath = '$FEISHU_PATH';
if (!config.plugins.load.paths.includes(feishuPath)) {
  config.plugins.load.paths.push(feishuPath);
}

// Add to plugins.entries
if (!config.plugins.entries) config.plugins.entries = {};
config.plugins.entries.feishu = { enabled: true };

fs.writeFileSync('$CONFIG_FILE', JSON.stringify(config, null, 2));
EOF

echo "✅ Configuration updated"

# Restart gateway
echo "🔄 Restarting gateway..."
pkill -f "openclaw gateway" 2>/dev/null || true
sleep 2
nohup openclaw gateway > /dev/null 2>&1 &

sleep 3

# Verify
echo ""
echo "🔍 Verifying installation..."
openclaw channels status | grep -i feishu

echo ""
echo "✅ Feishu setup complete!"
echo ""
echo "Next steps:"
echo "1. Open Feishu and send a message to your bot"
echo "2. You'll receive a pairing code"
echo "3. Run: openclaw pairing approve feishu <CODE>"
