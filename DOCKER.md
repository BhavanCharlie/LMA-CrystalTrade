# Docker Setup for CrystalTrade

This guide explains how to run CrystalTrade using Docker and Docker Compose.

## Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Docker version 20.10 or higher
- At least 2GB of available RAM

## Quick Start

### Production Build

**Option 1: Use the startup script (Recommended)**
```bash
./docker-start.sh
```

**Option 2: Manual setup**

1. **Create environment file:**
```bash
# Create .env file in backend directory
echo "OPENAI_API_KEY=your_key_here" > backend/.env
echo "DATABASE_URL=sqlite:///./crystal_trade.db" >> backend/.env
```

2. **Start all services:**
```bash
docker-compose up -d
```

3. **Initialize database:**
```bash
docker-compose exec backend python -c "from database import init_db; init_db()"
```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development Mode (Hot Reload)

For development with automatic hot-reload:

**Option 1: Use the dev script (Recommended)**
```bash
./docker-dev.sh
```

**Option 2: Manual command**
```bash
docker compose -f docker-compose.dev.yml up
```

This will:
- Run backend with auto-reload on code changes (FastAPI --reload)
- Run frontend dev server with hot-reload (Vite HMR)
- Mount source code as volumes for live updates
- Watch for file changes and automatically refresh

**Access:**
- Frontend: http://localhost:5173 (with hot-reload)
- Backend: http://localhost:8000 (with auto-reload)
- API Docs: http://localhost:8000/docs

**Note:** Changes to your code files will be automatically reflected without rebuilding containers!

## Docker Commands

### Start services
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild containers
```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build backend
```

### Execute commands in containers
```bash
# Backend shell
docker-compose exec backend bash

# Run Python script
docker-compose exec backend python init_db.py

# Frontend shell
docker-compose exec frontend sh
```

### Stop and remove volumes
```bash
docker-compose down -v
```

## Environment Variables

Create a `.env` file in the project root or set environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Or set in `docker-compose.yml`:

```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## Volumes

The following directories are mounted as volumes:
- `./backend/uploads` - Uploaded documents
- `./backend/reports` - Generated reports
- `./backend/crystal_trade.db` - Database file

## Troubleshooting

### Port already in use
If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "3001:80"  # Change frontend port
  - "8001:8000"  # Change backend port
```

### Database initialization
If database errors occur:
```bash
docker-compose exec backend python init_db.py
```

### View container status
```bash
docker-compose ps
```

### Check container health
```bash
docker-compose ps
# Look for "healthy" status
```

### Reset everything
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Architecture

```
┌─────────────────────────────────────┐
│  Frontend Container (Nginx)         │
│  Port: 3000                         │
│  Serves React app                   │
└──────────────┬──────────────────────┘
               │
               │ HTTP
               │
┌──────────────▼──────────────────────┐
│  Backend Container (FastAPI)         │
│  Port: 8000                         │
│  Python + Uvicorn                   │
└─────────────────────────────────────┘
```

## Production Deployment

For production, consider:

1. **Use environment-specific compose file:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

2. **Set up reverse proxy** (nginx/traefik) in front of containers

3. **Use PostgreSQL** instead of SQLite:
   - Add PostgreSQL service to docker-compose.yml
   - Update DATABASE_URL environment variable

4. **Enable HTTPS** with SSL certificates

5. **Set resource limits:**
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

## Notes

- Electron desktop app cannot run in Docker. Use the web version or run Electron locally connecting to Dockerized backend.
- For local Electron development, run backend in Docker and Electron locally:
  ```bash
  docker-compose up backend -d
  npm run dev:electron
  ```

