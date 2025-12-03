# Nitan MCP Server

[论坛开发讨论贴](https://www.uscardforum.com/t/topic/450599)

This is a heavily modified version of [Discourse MCP](https://github.com/discourse/discourse-mcp). It is a dedicated MCP client for https://www.uscardforum.com/ with Cloudflare bypass capabilities.

This repository is based on the [MCP Server Template](https://github.com/InteractionCo/mcp-server-template) and configured for Render deployment with streamable HTTP transport.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/mcp-server-template)

## Prerequisites

- **Node.js 18 or higher** (required)
- Python 3.7+ (required for Cloudflare bypass)
- pip3 (for Python dependency installation)

**Check your Node.js version:**
```bash
node --version  # Should be v18.0.0 or higher
```

**If you need to upgrade Node.js:**
```bash
# Using nvm (recommended)
nvm install 18
nvm use 18

# Or download from https://nodejs.org/
```

## Local Development

### Setup

Fork the repo, then run:

```bash
git clone <your-repo-url>
cd mcp-server-template
npm install
npm run build
```

### Install Python Dependencies

The server uses Python for Cloudflare bypass. Install dependencies:

```bash
pip3 install -r requirements.txt
# Or install individually:
pip3 install cloudscraper curl-cffi
```

**If Python is installed in a virtual environment:**
```bash
# Set the python_path when running the server
node dist/index.js --python_path /path/to/python_executable
```

### Test

**Using stdio transport (default):**
```bash
npm run build
node dist/index.js
# then in another terminal run:
npx @modelcontextprotocol/inspector
```

**Using HTTP transport:**
```bash
npm run build
node dist/index.js --transport=http --port=8000
# then in another terminal run:
npx @modelcontextprotocol/inspector
```

Open http://localhost:3000 and connect to `http://localhost:8000/mcp` using "Streamable HTTP" transport (NOTE THE `/mcp`!).

The server will start even if Python dependencies are missing, but Cloudflare bypass features won't work until you install them.

## Deployment

### Option 1: One-Click Deploy to Render

Click the "Deploy to Render" button above, or visit:
```
https://render.com/deploy?repo=https://github.com/yourusername/mcp-server-template
```

### Option 2: Manual Deployment to Render

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect your forked repository
5. Render will automatically detect the `render.yaml` configuration

Your server will be available at `https://your-service-name.onrender.com/mcp` (NOTE THE `/mcp`!)

### Option 3: Using npx (for local/development use)

```bash
npx -y @nitansde/mcp@latest
```

**What happens automatically:**
1. ✅ Downloads and caches the package
2. ✅ Installs Node.js dependencies
3. ✅ Runs `postinstall` script to check/install Python dependencies
4. ✅ Checks Python dependencies at runtime and shows helpful warnings if missing

## MCP Client Configuration

**For Claude Desktop (macOS/Windows):**

**Using npx (recommended for local use):**
```json
{
  "mcpServers": {
    "nitan": {
      "command": "npx",
      "args": [
        "-y",
        "@nitansde/mcp@latest"
      ],
      "env": {
        "NITAN_USERNAME": "YOUR_USERNAME",
        "NITAN_PASSWORD": "YOUR_PASSWORD"
      }
    }
  }
}
```

**Using deployed HTTP server:**
```json
{
  "mcpServers": {
    "nitan": {
      "url": "https://your-service-name.onrender.com/mcp"
    }
  }
}
```

Use optional env `"TIME_ZONE": "America/New_York"` if you want to use a timezone different to your local clock.

**Configuration file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Cloudflare Bypass

This server uses an intelligent **dual-method Cloudflare bypass strategy**:
1. Tries `cloudscraper` first (mature, established)
2. Automatically falls back to `curl_cffi` if cloudscraper fails (better browser impersonation)
3. Remembers failures and uses the working method for subsequent requests

This provides maximum reliability against Cloudflare protection. See [CLOUDFLARE_BYPASS.md](CLOUDFLARE_BYPASS.md) for details.

## Poke Setup

You can connect your MCP server to Poke at [poke.com/settings/connections](https://poke.com/settings/connections).

To test the connection explicitly, ask poke something like: `Tell the subagent to use the "{connection name}" integration's "{tool name}" tool`.

If you run into persistent issues of poke not calling the right MCP (e.g. after you've renamed the connection) you may send `clearhistory` to poke to delete all message history and start fresh.

## Additional Documentation

- [AGENTS.md](AGENTS.md) - Information about agents
- [TOOLS.md](TOOLS.md) - Available tools documentation
- [CLOUDFLARE_BYPASS.md](CLOUDFLARE_BYPASS.md) - Cloudflare bypass details
- [CLOUDSCRAPER_INTEGRATION.md](CLOUDSCRAPER_INTEGRATION.md) - Cloudscraper integration details
- [CHANGELOG.md](CHANGELOG.md) - Version history

## Original README

Based on [Discourse MCP](https://github.com/discourse/discourse-mcp/blob/main/README.md)
