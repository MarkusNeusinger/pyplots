# 🚀 Deployment Guide

## Overview

pyplots is deployed on **Google Cloud Platform** with a focus on cost-efficiency and scalability. This guide covers production deployment, CI/CD, and operational best practices.

**Production URL**: `https://pyplots.ai`

---

## Google Cloud Infrastructure

### Services Used

| Service | Purpose | Instance Type | Cost Estimate |
|---------|---------|---------------|---------------|
| **Cloud Run** (API) | FastAPI backend | Auto-scaling (0-10) | ~$10-30/month |
| **Cloud Run** (Frontend) | Next.js app | Auto-scaling (0-5) | ~$5-15/month |
| **n8n Cloud** | Automation workflows | Pro subscription | Already paid |
| **Cloud SQL** | PostgreSQL database | db-f1-micro | ~$10/month |
| **Cloud Storage** | Preview images | Standard storage | ~$1-5/month |
| **Cloud Build** | CI/CD | Free tier | $0 |
| **Secret Manager** | Secrets storage | Per secret | ~$1/month |

**Total**: ~$25-60/month (with optimization)
**Note**: n8n Pro subscription already paid separately

---

## Prerequisites

### 1. GCP Account Setup

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Login
gcloud auth login

# Create project
gcloud projects create pyplots-prod --name="pyplots"

# Set project
gcloud config set project pyplots-prod

# Enable APIs
gcloud services enable \
  run.googleapis.com \
  sql-component.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  compute.googleapis.com
```

### 2. Domain Configuration

**Domain**: `pyplots.ai` (already purchased)

**DNS Setup** (at domain registrar):
```
Type  Name  Value
A     @     [Cloud Run IP]
A     www   [Cloud Run IP]
CNAME api   api.run.app
```

**SSL Certificate**: Auto-provisioned by Cloud Run (Let's Encrypt)

---

## Cloud SQL Setup

### Create Database Instance

```bash
# Create instance (minimal for start)
gcloud sql instances create pyplots-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=europe-west4 \
  --network=default \
  --no-assign-ip \
  --availability-type=zonal

# Create database
gcloud sql databases create pyplots \
  --instance=pyplots-db

# Create user
gcloud sql users create pyplots \
  --instance=pyplots-db \
  --password=[SECURE_PASSWORD]
```

**Important**:
- `--no-assign-ip`: Private IP only (no public access)
- `db-f1-micro`: Cheapest tier (upgrade later if needed)
- `europe-west4`: Close to users, cost-effective

### Database Connection

**Connection Name**: `pyplots-prod:europe-west4:pyplots-db`

**Internal IP**: Retrieved via:
```bash
gcloud sql instances describe pyplots-db \
  --format="value(ipAddresses[0].ipAddress)"
```

**Database Schema**: For tables, migrations, and data model, see [Database Architecture](architecture/database.md)

---

## Cloud Storage Setup

### Create Bucket

```bash
# Create bucket
gsutil mb -p pyplots-prod -c STANDARD -l europe-west4 gs://pyplots-images

# Set public access for preview images
gsutil iam ch allUsers:objectViewer gs://pyplots-images

# Set CORS
cat > cors.json << EOF
[
  {
    "origin": ["https://pyplots.ai", "https://www.pyplots.ai"],
    "method": ["GET"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
EOF

gsutil cors set cors.json gs://pyplots-images
```

### Lifecycle Policy (Auto-delete old previews)

```bash
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "daysSinceNoncurrentTime": 30,
          "matchesPrefix": ["previews/"]
        }
      },
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 1,
          "matchesPrefix": ["generated/"]
        }
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://pyplots-images
```

**Policy**:
- Old preview versions deleted 30 days after new version uploaded
- User-generated plots deleted after 1 day

---

## Secret Manager

### Store Secrets

```bash
# Database password
echo -n "SECURE_DB_PASSWORD" | \
  gcloud secrets create db-password --data-file=-

# Anthropic API key
echo -n "sk-ant-..." | \
  gcloud secrets create anthropic-api-key --data-file=-

# GitHub token (for Actions)
echo -n "ghp_..." | \
  gcloud secrets create github-token --data-file=-

# Service account for API
gcloud secrets create api-service-account \
  --data-file=service-account.json
```

### Grant Access

```bash
# Allow Cloud Run to access secrets
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:pyplots-api@pyplots-prod.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## Cloud Run Deployment

### Backend (FastAPI)

**Dockerfile**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-dev

# Copy application
COPY . .

# Run migrations and start server
CMD uv run alembic upgrade head && \
    uv run uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Deploy**:
```bash
# Build and deploy
gcloud run deploy pyplots-api \
  --source . \
  --region europe-west4 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1 \
  --concurrency 80 \
  --set-env-vars="ENVIRONMENT=production" \
  --set-secrets="DATABASE_URL=db-connection-string:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest" \
  --add-cloudsql-instances="pyplots-prod:europe-west4:pyplots-db"

# Map custom domain
gcloud run domain-mappings create \
  --service pyplots-api \
  --domain api.pyplots.ai \
  --region europe-west4
```

**Environment Variables** (via Cloud Run):
- `ENVIRONMENT=production`
- `DATABASE_URL` (from Secret Manager)
- `ANTHROPIC_API_KEY` (from Secret Manager)
- `GCS_BUCKET=pyplots-images`

---

### Frontend (Next.js)

**Dockerfile**:
```dockerfile
FROM node:20-slim AS builder

WORKDIR /app

COPY app/package*.json ./
RUN npm ci

COPY app/ ./
RUN npm run build

FROM node:20-slim

WORKDIR /app

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

ENV PORT=8080
CMD ["npm", "start"]
```

**Deploy**:
```bash
gcloud run deploy pyplots-frontend \
  --source ./app \
  --region europe-west4 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 5 \
  --memory 256Mi \
  --cpu 1 \
  --set-env-vars="NEXT_PUBLIC_API_URL=https://api.pyplots.ai"

# Map custom domain
gcloud run domain-mappings create \
  --service pyplots-frontend \
  --domain pyplots.ai \
  --region europe-west4
```

---

### n8n (Cloud - Already Configured)

**No deployment needed** - using n8n Cloud Pro subscription.

**Configuration**:
- Access: https://app.n8n.cloud (or custom subdomain)
- Webhooks: Configured to call API endpoints
- Credentials: API keys stored in n8n Cloud securely

**Integration with API**:
- n8n calls `https://api.pyplots.ai/internal/*` endpoints
- Authentication via API key (stored in n8n credentials)
- No need to expose n8n publicly

---

## CI/CD with GitHub Actions

### Workflow: Deploy on Merge

**.github/workflows/deploy.yml**:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy pyplots-api \
            --source . \
            --region europe-west4 \
            --project pyplots-prod

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}

      - name: Deploy Frontend
        run: |
          gcloud run deploy pyplots-frontend \
            --source ./app \
            --region europe-west4 \
            --project pyplots-prod

  sync-metadata:
    needs: [deploy-backend]
    runs-on: ubuntu-latest
    steps:
      - name: Sync repository to database
        run: |
          curl -X POST https://api.pyplots.ai/internal/sync-from-repo \
            -H "Authorization: Bearer ${{ secrets.API_TOKEN }}"
```

---

## Database Migrations

### Production Migration Strategy

**Before deploying code changes**:
```bash
# 1. Create migration locally
uv run alembic revision -m "add new column"

# 2. Test migration locally
uv run alembic upgrade head
uv run alembic downgrade -1  # Test rollback
uv run alembic upgrade head

# 3. Commit migration files
git add migrations/versions/*.py
git commit -m "Add migration: add new column"

# 4. Deploy (migration runs automatically in Dockerfile CMD)
```

**Automatic Migration on Deploy**:
```dockerfile
# In Dockerfile
CMD uv run alembic upgrade head && \
    uv run uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Manual Migration** (if needed):
```bash
# Connect to Cloud Run instance
gcloud run services proxy pyplots-api --port=8080

# Run migration manually
uv run alembic upgrade head
```

---

## Monitoring & Logging

### Cloud Logging

View logs:
```bash
# API logs
gcloud run services logs read pyplots-api \
  --region europe-west4 \
  --limit 50

# Follow logs in real-time
gcloud run services logs tail pyplots-api \
  --region europe-west4
```

**Log Levels**:
- ERROR: Application errors
- WARNING: Deprecations, high latency
- INFO: Requests, deployments
- DEBUG: Development only (disabled in prod)

### Cloud Monitoring

**Metrics to Track**:
- Request count
- Request latency (p50, p95, p99)
- Error rate
- Instance count
- Memory usage
- Database connections

**Alerts**:
```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Error Rate" \
  --condition-threshold-value=0.05 \
  --condition-threshold-duration=300s
```

### Health Checks

Cloud Run automatic health checks:
- Endpoint: `/health`
- Interval: 10 seconds
- Unhealthy threshold: 3 consecutive failures

---

## Cost Optimization

### 1. Cloud Run Auto-scaling

```yaml
# Start from 0 instances when idle
min-instances: 0

# Scale based on concurrency (80 requests per instance)
concurrency: 80

# Limit max instances to control costs
max-instances: 10
```

**Estimated Costs** (with minimal traffic):
- 0 instances when idle: $0
- 1 instance running 24/7: ~$10/month
- Burst to 5 instances occasionally: ~$15/month

---

### 2. Database Optimization

**Start Small**:
```bash
# Minimal instance
--tier=db-f1-micro  # ~$10/month

# Upgrade when needed
gcloud sql instances patch pyplots-db \
  --tier=db-g1-small  # ~$25/month
```

**Connection Pooling** (in code):
```python
# Limit connections to avoid overloading small instance
pool_size=5
max_overflow=10
```

---

### 3. Storage Optimization

**Lifecycle Policies**:
- Old previews auto-deleted after 30 days
- User plots deleted after 24 hours

**Compression**:
```python
# Compress PNGs before upload
from PIL import Image

img.save('output.png', optimize=True, quality=85)
```

**Estimated Costs**:
- 1000 previews × 100 KB = 100 MB: $0.02/month
- 10,000 requests/month: $0.40/month

---

### 4. n8n Cloud

**Already Paid**:
- n8n Pro subscription
- Unlimited workflow executions
- No additional hosting costs

**Benefits**:
- No self-hosting maintenance
- Automatic updates
- Built-in monitoring
- Better uptime than self-hosted

---

### 5. GitHub Actions

**Leverage Free Tier**:
- 2,000 minutes/month (GitHub Pro)
- Cache dependencies between runs
- Matrix strategy for parallel tests

**Minimize Build Time**:
```yaml
# Cache dependencies
- uses: actions/cache@v3
  with:
    path: ~/.uv/cache
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

---

### 6. AI API Costs

**Use Claude Code Max Subscription**:
- Already paid: $20/month
- Unlimited code generation
- Routine quality checks

**Vertex AI (Multi-LLM)**:
- Only for critical decisions
- ~10-20 calls/month
- Estimated: $1-2/month

---

## Backup & Recovery

### Automated Backups

Cloud SQL automatic backups:
```bash
# Configure backups
gcloud sql instances patch pyplots-db \
  --backup-start-time=03:00 \
  --retained-backups-count=7
```

### Manual Backup

```bash
# Create on-demand backup
gcloud sql backups create \
  --instance=pyplots-db \
  --description="Before major migration"

# List backups
gcloud sql backups list --instance=pyplots-db

# Restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=pyplots-db \
  --backup-id=BACKUP_ID
```

### Repository Backup

Code is in GitHub (already backed up):
- Push to `main` branch = automatic backup
- Tags for releases: `git tag v1.0.0`

---

## Security

### Service Accounts

**API Service Account**:
```bash
gcloud iam service-accounts create pyplots-api \
  --display-name="pyplots API"

# Grant permissions
gcloud projects add-iam-policy-binding pyplots-prod \
  --member="serviceAccount:pyplots-api@pyplots-prod.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding pyplots-prod \
  --member="serviceAccount:pyplots-api@pyplots-prod.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### Secrets Rotation

Rotate secrets periodically:
```bash
# Generate new password
NEW_PASSWORD=$(openssl rand -base64 32)

# Update secret
echo -n "$NEW_PASSWORD" | \
  gcloud secrets versions add db-password --data-file=-

# Update database user
gcloud sql users set-password pyplots \
  --instance=pyplots-db \
  --password=$NEW_PASSWORD
```

### SSL/TLS

- HTTPS enforced (Cloud Run default)
- Let's Encrypt certificates (auto-renewed)
- HSTS headers enabled

---

## Rollback Strategy

### Code Rollback

```bash
# List revisions
gcloud run revisions list \
  --service=pyplots-api \
  --region=europe-west4

# Rollback to previous revision
gcloud run services update-traffic pyplots-api \
  --to-revisions=pyplots-api-00042-abc=100 \
  --region=europe-west4
```

### Database Rollback

```bash
# Rollback migration
uv run alembic downgrade -1

# Or restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=pyplots-db
```

---

## Production Checklist

Before going live:

- [ ] Domain configured and SSL working
- [ ] Database created with backups enabled
- [ ] Secrets stored in Secret Manager
- [ ] Cloud Run services deployed
- [ ] Health checks passing
- [ ] Monitoring and alerts configured
- [ ] Cost alerts set up
- [ ] Backup strategy tested
- [ ] Rollback procedure tested
- [ ] Load testing completed
- [ ] Security audit passed

---

## Maintenance

### Weekly Tasks

- Check error logs
- Review cost reports
- Check backup success

### Monthly Tasks

- Review and optimize costs
- Update dependencies (`uv sync --upgrade`)
- Review security alerts
- Rotate secrets (if policy requires)

### Quarterly Tasks

- Performance review and optimization
- Capacity planning
- Database maintenance (VACUUM, ANALYZE)

---

## Troubleshooting

### Service Not Responding

```bash
# Check service status
gcloud run services describe pyplots-api \
  --region europe-west4

# Check logs
gcloud run services logs read pyplots-api \
  --region europe-west4 \
  --limit 100
```

### Database Connection Issues

```bash
# Test from Cloud Shell
gcloud sql connect pyplots-db --user=pyplots

# Check Cloud SQL proxy
gcloud sql instances describe pyplots-db
```

### High Costs

```bash
# Check billing
gcloud billing accounts list

# Review costs by service
gcloud billing accounts get-spending \
  --account=BILLING_ACCOUNT_ID
```

---

*For architecture details, see [architecture/](./architecture/)*
*For development setup, see [development.md](./development.md)*
