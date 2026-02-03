# The Agentic Layer

The Agentic Layer is a "ring" of code, scripts, and assets that sits around your application code. Its purpose is to
encode your engineering expertise so that AI agents can operate your codebase autonomously.

## Structure

```
agentic/
├── commands/       # Prompt templates (chore.md, implement.md, ...)
├── workflows/      # Executable workflows (uv run)
│   └── modules/    # Shared Python modules (agent.py)
├── specs/          # Generated plans and specifications
└── runs/           # Execution output (in .gitignore)
```

## Usage

```bash
# Run chore & implement workflow
uv run agentic/workflows/chore_implement.py "your task description"

# Options
--model [haiku|sonnet|opus]    # Default: opus
--cli [claude|copilot|gemini]  # Default: claude
--working-dir PATH             # Default: current directory
```