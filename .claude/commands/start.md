# Start Development Servers

Start both backend and frontend development servers.

## Instructions

1. Start the FastAPI backend server in background:
```bash
uv run uvicorn api.main:app --reload --port 8000 &
```

2. Start the React frontend dev server:
```bash
cd app && yarn dev
```

## Notes
- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:3000
- Use `pkill -f uvicorn` to stop the backend
- Use `pkill -f vite` to stop the frontend