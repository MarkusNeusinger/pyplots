# Chore: Remove SSE MCP Transport

## Chore Description
Remove the deprecated SSE (Server-Sent Events) transport from the MCP server and keep only the modern Streamable HTTP transport. SSE was the old MCP standard before SDK 1.0, but all actively maintained MCP clients (Claude Desktop, Claude Code, Cursor, Cline, MCP Inspector) now support Streamable HTTP. Removing SSE simplifies the codebase:
- Single MCP app instead of two
- One endpoint to document (`/mcp` only)
- Simpler lifespan management
- Less code to maintain and test

The `stateless_http=True` fix has already been applied to `api/mcp/server.py`.

## Relevant Files
Use these files to resolve the chore:

- **`api/main.py`** - Contains MCP app creation, lifespan management, and route mounting. Need to remove `mcp_sse_app` creation, its lifespan context, and the `/sse` mount.
- **`api/mcp/server.py`** - MCP server definition. Already has `stateless_http=True` fix applied. No changes needed.
- **`app/src/pages/McpPage.tsx`** - Frontend MCP documentation page. Need to remove SSE endpoint row from the table.
- **`docs/reference/mcp.md`** - Full MCP documentation. Need to update protocol description from "JSON-RPC over SSE" to "Streamable HTTP".

### New Files
None required.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Remove SSE from api/main.py
- Remove the `mcp_sse_app` creation line (line ~50):
  ```python
  # Remove this line:
  mcp_sse_app = mcp_server.http_app(path="/", transport="sse")
  ```
- Update the lifespan function to remove nested SSE context:
  ```python
  # Change from:
  async with mcp_http_app.lifespan(app):
      async with mcp_sse_app.lifespan(app):
          logger.info("MCP server initialized (HTTP + SSE)")
          yield

  # To:
  async with mcp_http_app.lifespan(app):
      logger.info("MCP server initialized")
      yield
  ```
- Remove the SSE mount (line ~142):
  ```python
  # Remove this line:
  app.mount("/sse", mcp_sse_app)  # SSE transport at /sse
  ```
- Update the comment above mcp_http_app to remove SSE mention

### Step 2: Update McpPage.tsx frontend
- Remove the SSE row from the endpoints table in the "What is MCP" section
- Keep only the Streamable HTTP row
- The table should show only:
  ```
  Streamable HTTP | https://api.pyplots.ai/mcp
  ```

### Step 3: Update docs/reference/mcp.md
- Update the protocol description in the "MCP vs REST API" table:
  - Change `| **Protocol** | JSON-RPC over SSE | HTTP/JSON |`
  - To: `| **Protocol** | Streamable HTTP | HTTP/JSON |`

### Step 4: Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Validation Commands
Execute every command to validate the chore is complete with zero regressions.

- `uv run ruff check api/ && uv run ruff format api/` - Lint and format backend code
- `uv run pytest tests/unit/api/mcp/` - Run MCP unit tests
- `cd app && yarn lint` - Lint frontend code
- `cd app && yarn build` - Build frontend to verify TypeScript compiles

## Notes
- The `stateless_http=True` change in `api/mcp/server.py` was already applied in an earlier commit and should remain.
- After this change, only `/mcp` endpoint will be available for MCP clients.
- The MCP Inspector command in the documentation (`npx @modelcontextprotocol/inspector https://api.pyplots.ai/mcp`) remains valid.
- This change needs to be deployed to production for the fix to take effect on `api.pyplots.ai`.
