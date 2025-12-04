<p align="center">
  <img src="public/logo.svg" alt="pyplots.ai" width="250">
</p>

# pyplots Frontend

Minimal React + TypeScript + Vite + MUI frontend for the pyplots platform.

## Features

- **Python-colored branding** - Logo with Python blue (#3776AB) and yellow (#FFD43B)
- **JetBrains Mono font** - Monospace font for the pythonic developer vibe
- **Spec search & filter** - Click on spec ID to search/filter all available specs
- **Keyboard shortcuts**:
  - `Space` - Random shuffle to another spec
  - `Enter` - Open spec selector with search
  - `↑↓` - Navigate through specs in dropdown
  - `Escape` - Close modal or dropdown
- **URL sharing** - Specs are shareable via `?spec=scatter-basic` URL parameter
- **Fullscreen modal** - Click any plot to view in fullscreen
- **Responsive grid** - 1/2/3 columns based on screen size

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite 7** - Build tool
- **MUI 7** - Material UI components
- **JetBrains Mono** - Google Fonts
- **nginx** - Production web server

## Development

### Prerequisites

- Node.js 20+
- Yarn package manager

### Local Development

1. Install dependencies:
   ```bash
   cd app
   yarn install
   ```

2. Create `.env` file (optional):
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. Start development server:
   ```bash
   yarn dev
   ```

   The app will be available at `http://localhost:3000`

### Build

```bash
yarn build
```

Built files will be in the `dist/` directory.

## Docker

### Build Docker Image

```bash
docker build -t pyplots-frontend \
  --build-arg VITE_API_URL=https://your-backend-url.run.app \
  .
```

### Run Docker Container

```bash
docker run -p 8080:8080 pyplots-frontend
```

## Cloud Run Deployment

### Prerequisites

- Google Cloud Project with Cloud Run enabled
- `gcloud` CLI configured

### Deploy

From the project root:

```bash
gcloud builds submit \
  --config=app/cloudbuild.yaml \
  --substitutions=_VITE_API_URL=https://pyplots-backend-YOUR-PROJECT.run.app
```

Replace `YOUR-PROJECT` with your Google Cloud project ID.

### Update Backend URL

To update the backend URL after initial deployment:

1. Edit `app/cloudbuild.yaml`
2. Update the `_VITE_API_URL` substitution
3. Redeploy with the command above

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: `http://localhost:8000`)

## Project Structure

```
app/
├── src/
│   ├── App.tsx          # Main application component
│   ├── main.tsx         # React entry point
│   └── vite-env.d.ts    # Vite type definitions
├── public/
│   ├── favicon.svg      # Python-colored "pp" favicon
│   └── logo.svg         # Python-colored "pyplots.ai" logo
├── index.html           # HTML template (fonts, favicon)
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
├── Dockerfile           # Multi-stage Docker build
├── nginx.conf           # nginx configuration for production
├── cloudbuild.yaml      # Google Cloud Build configuration
└── package.json         # Dependencies and scripts
```

## Available Scripts

- `yarn dev` - Start development server
- `yarn build` - Build for production
- `yarn preview` - Preview production build locally
- `yarn lint` - Run ESLint
