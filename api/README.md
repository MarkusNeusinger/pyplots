# pyplots API

FastAPI backend for the pyplots platform.

## 🚀 Quick Start

### Local Development

```bash
# From project root
uv sync --all-extras

# Start API server
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Hello World**: http://localhost:8000/

### Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check for Cloud Run
- `GET /hello/{name}` - Simple hello endpoint

## 🐳 Docker

### Build locally

```bash
# From project root
docker build -f api/Dockerfile -t pyplots-backend .
```

### Run locally

```bash
docker run -p 8000:8000 pyplots-backend
```

Visit: http://localhost:8000/docs

## ☁️ Cloud Run Deployment

### Prerequisites

1. Google Cloud Project
2. Cloud Build API enabled
3. Cloud Run API enabled
4. Appropriate IAM permissions

### Deploy

```bash
# From project root
gcloud builds submit --config=api/cloudbuild.yaml --project=YOUR_PROJECT_ID
```

### Configuration

Edit `api/cloudbuild.yaml` substitutions:
- `_SERVICE_NAME`: Cloud Run service name (default: pyplots-backend)
- `_REGION`: Deployment region (default: europe-west4)
- `_MEMORY`: Container memory (default: 512Mi)
- `_MIN_INSTANCES`: Min instances (default: 0)
- `_MAX_INSTANCES`: Max instances (default: 3)

### Environment Variables

Production env vars are set in `cloudbuild.yaml`:
- `ENVIRONMENT=production`
- `GOOGLE_CLOUD_PROJECT=<project-id>`

Add more in the deploy step:
```yaml
- "--set-env-vars=MY_VAR=value"
```

## 🧪 Testing

```bash
# Run tests
uv run pytest tests/unit/api/

# With coverage
uv run pytest tests/unit/api/ --cov=api
```

## 📝 API Development

### Adding new endpoints

1. Create router in `api/routers/`:
```python
# api/routers/plots.py
from fastapi import APIRouter

router = APIRouter(prefix="/plots", tags=["plots"])

@router.get("/")
async def list_plots():
    return {"plots": []}
```

2. Include router in `api/main.py`:
```python
from api.routers import plots

app.include_router(plots.router)
```

### Project Structure

```
api/
├── main.py              # FastAPI app
├── __init__.py
├── routers/             # API endpoints
│   ├── __init__.py
│   ├── plots.py
│   ├── specs.py
│   └── data.py
├── Dockerfile           # Container image
├── cloudbuild.yaml      # Cloud Build config
└── README.md            # This file
```

## 🔐 Security

- Non-root user in Docker container
- CORS configured for allowed origins
- Health check endpoint for Cloud Run
- Environment-based configuration

## 📊 Monitoring

### Health Check

Cloud Run uses `/health` endpoint for liveness checks.

Returns:
```json
{
  "status": "healthy",
  "service": "pyplots-api",
  "version": "0.1.0"
}
```

### Logs

View Cloud Run logs:
```bash
gcloud run services logs read pyplots-backend --region=europe-west4
```

## 🛠️ Troubleshooting

### Common Issues

**Port not binding:**
- Cloud Run sets `PORT` env var
- Dockerfile CMD uses `${PORT:-8000}`

**CORS errors:**
- Add origin to `allow_origins` in `main.py`

**Build fails:**
- Check `pyproject.toml` is in project root
- Verify Dockerfile paths are correct

### Debug locally

```bash
# Run with debug logging
uv run uvicorn api.main:app --reload --log-level debug
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [UV Package Manager](https://github.com/astral-sh/uv)
