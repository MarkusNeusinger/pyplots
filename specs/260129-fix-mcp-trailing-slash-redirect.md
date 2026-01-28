# Bug: MCP server 307 redirect breaks Claude CLI integration

## Bug Description
When users try to add the pyplots MCP server using the Claude CLI command:
```bash
claude mcp add pyplots --transport http https://api.pyplots.ai/mcp
```

The server is added successfully, but when Claude CLI tries to connect, it fails with "Failed to connect" status. The server shows as configured but non-functional.

**Expected behavior**: Claude CLI should successfully connect to the MCP server and list available tools.

**Actual behavior**: Connection fails silently. Running `claude mcp get pyplots` shows `Status: ✗ Failed to connect`.

## Problem Statement
The pyplots MCP endpoint at `https://api.pyplots.ai/mcp` returns a **307 Temporary Redirect** to `http://api.pyplots.ai/mcp/` when accessed without a trailing slash. This causes two issues:

1. **Claude CLI doesn't follow HTTP redirects** - MCP clients generally do not follow 307 redirects
2. **HTTPS-to-HTTP downgrade** - The redirect location uses `http://` instead of `https://`, which is a security concern

## Solution Statement
Update the documentation to instruct users to use the URL with a trailing slash: `https://api.pyplots.ai/mcp/`. This avoids the redirect issue entirely since the server responds correctly when the trailing slash is included.

This is the minimal fix that resolves the issue without requiring code changes to the MCP server or FastAPI configuration.

## Steps to Reproduce
1. Add the MCP server using Claude CLI:
   ```bash
   claude mcp add pyplots --transport http https://api.pyplots.ai/mcp
   ```
2. Check the server status:
   ```bash
   claude mcp get pyplots
   ```
3. Observe: `Status: ✗ Failed to connect`

**Verification that trailing slash works:**
```bash
# Remove and re-add with trailing slash
claude mcp remove pyplots
claude mcp add pyplots --transport http https://api.pyplots.ai/mcp/
claude mcp get pyplots
# Observe: Status should show connected with tools listed
```

## Root Cause Analysis
The root cause is a combination of factors:

1. **Starlette/FastAPI redirect behavior**: When an app is mounted at a path, Starlette's router has `redirect_slashes=True` by default. This means requests to `/mcp` are redirected to `/mcp/` with a 307 status code.

2. **MCP client behavior**: Claude CLI (and other MCP clients) do not follow HTTP redirects per the MCP protocol specification. They expect the endpoint to respond directly without redirects.

3. **HTTP downgrade in redirect**: The 307 redirect location header contains `http://` instead of `https://`, likely due to how the request is proxied through Google Cloud Run.

**Technical verification:**
```bash
# Without trailing slash - returns 307 redirect
curl -s -D - https://api.pyplots.ai/mcp 2>&1 | head -5
# HTTP/2 307
# location: http://api.pyplots.ai/mcp/

# With trailing slash - works correctly
curl -s -H "Accept: application/json, text/event-stream" -H "Content-Type: application/json" \
  -X POST -d '{"jsonrpc":"2.0","method":"initialize",...}' https://api.pyplots.ai/mcp/
# Returns 200 with MCP response
```

## Relevant Files
Use these files to fix the bug:

### Existing Files
- `docs/reference/mcp.md` - MCP documentation that needs URL updates to include trailing slash
- `app/src/pages/McpPage.tsx` - Frontend MCP page that shows configuration examples

### New Files
None required.

## Step by Step Tasks

### 1. Update MCP Documentation
Update `docs/reference/mcp.md` to use trailing slash in all URL examples:

- Change `https://api.pyplots.ai/mcp` to `https://api.pyplots.ai/mcp/` in:
  - Quick Start section (Claude Desktop config)
  - Claude Code (CLI) section
  - MCP Inspector command
  - Technical Details section
  - Troubleshooting section (curl command)
  - Any other occurrences

### 2. Update Frontend MCP Page
Update `app/src/pages/McpPage.tsx` to use trailing slash in configuration examples:

- Update the JSON configuration examples shown to users
- Ensure consistency with documentation

### 3. Verify the Fix
Manually test that the trailing slash URL works:

```bash
# Remove old config
claude mcp remove pyplots

# Add with trailing slash
claude mcp add pyplots --transport http https://api.pyplots.ai/mcp/

# Verify connection works
claude mcp get pyplots
# Should show: Status: ✓ Connected (or similar success indicator)
```

### 4. Run Validation Commands
Execute all validation commands to ensure no regressions.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- `uv run ruff check docs/reference/mcp.md && uv run ruff format docs/reference/mcp.md` - Lint documentation (will pass, md file)
- `cd app && yarn build` - Verify frontend builds without errors
- `claude mcp remove pyplots 2>/dev/null; claude mcp add pyplots --transport http https://api.pyplots.ai/mcp/; claude mcp get pyplots` - Test the fix works

## Final Check
- Use `mcp__plugin_serena_serena__think_about_whether_you_are_done` to verify all tasks are complete.

## Notes
- **Alternative solutions considered but not chosen:**
  1. **Disable redirect_slashes in FastAPI**: This would require code changes and may break other parts of the application
  2. **Register both `/mcp` and `/mcp/` routes**: More complex and requires FastMCP changes
  3. **Use a different mount pattern**: Would require significant refactoring

- **Future consideration**: If FastMCP or the MCP protocol adds better redirect handling, the server-side fix could be revisited. For now, the documentation fix is the safest and quickest solution.

- **Related issues**:
  - https://github.com/jlowin/fastmcp/issues/1544
  - https://github.com/jlowin/fastmcp/issues/1364
  - https://github.com/modelcontextprotocol/python-sdk/issues/1168
