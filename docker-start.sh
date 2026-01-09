#!/bin/bash

# CrystalTrade Docker Startup Script

echo "🚀 Starting CrystalTrade with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo "   Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running."
    echo ""
    echo "   Please start Docker Desktop and wait for it to be ready."
    echo "   Then run this script again."
    echo ""
    echo "   On macOS: Open Docker Desktop from Applications"
    echo "   On Linux: sudo systemctl start docker"
    echo ""
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check for docker-compose or docker compose
# Try docker compose (plugin) first as it's more reliable on Docker Desktop
DOCKER_COMPOSE_CMD=""
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
    echo "✅ Found: docker compose (plugin)"
elif command -v docker-compose > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
    echo "✅ Found: docker-compose (standalone)"
else
    echo "❌ Neither 'docker compose' nor 'docker-compose' is available."
    echo "   Please install Docker Desktop which includes Docker Compose."
    exit 1
fi

# Verify Docker Compose can actually connect to the daemon
echo "🔍 Verifying Docker Compose connection..."
max_retries=5
retry=0
while [ $retry -lt $max_retries ]; do
    if $DOCKER_COMPOSE_CMD ps > /dev/null 2>&1; then
        echo "✅ Docker Compose connection verified"
        echo "✅ Using: $DOCKER_COMPOSE_CMD"
        echo ""
        break
    fi
    retry=$((retry + 1))
    if [ $retry -lt $max_retries ]; then
        echo "   Waiting for Docker Compose to be ready... ($retry/$max_retries)"
        sleep 2
    else
        # Try the other command if available
        if [ "$DOCKER_COMPOSE_CMD" = "docker compose" ] && command -v docker-compose > /dev/null 2>&1; then
            echo "⚠️  'docker compose' failed, trying 'docker-compose'..."
            DOCKER_COMPOSE_CMD="docker-compose"
            if $DOCKER_COMPOSE_CMD ps > /dev/null 2>&1; then
                echo "✅ Docker Compose connection verified with docker-compose"
                echo "✅ Using: $DOCKER_COMPOSE_CMD"
                echo ""
                break
            fi
        elif [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ] && docker compose version > /dev/null 2>&1; then
            echo "⚠️  'docker-compose' failed, trying 'docker compose'..."
            DOCKER_COMPOSE_CMD="docker compose"
            if $DOCKER_COMPOSE_CMD ps > /dev/null 2>&1; then
                echo "✅ Docker Compose connection verified with docker compose"
                echo "✅ Using: $DOCKER_COMPOSE_CMD"
                echo ""
                break
            fi
        fi
        
        echo "❌ Docker Compose cannot connect to Docker daemon."
        echo ""
        echo "   Diagnostic information:"
        echo "   - Docker info: $(docker info > /dev/null 2>&1 && echo '✅ Works' || echo '❌ Fails')"
        echo "   - Docker ps: $(docker ps > /dev/null 2>&1 && echo '✅ Works' || echo '❌ Fails')"
        echo ""
        echo "   This usually means Docker Desktop is still starting up."
        echo "   Please try these steps:"
        echo "   1. Open Docker Desktop and wait for it to fully start (whale icon steady)"
        echo "   2. Test manually: docker ps"
        echo "   3. Test compose: docker compose ps (or docker-compose ps)"
        echo "   4. Restart Docker Desktop if the issue persists"
        echo ""
        exit 1
    fi
done

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No backend/.env file found. Creating from template..."
    echo "OPENAI_API_KEY=your_key_here" > backend/.env
    echo "DATABASE_URL=sqlite:///./crystal_trade.db" >> backend/.env
    echo "📝 Please update backend/.env with your OpenAI API key"
fi

# Build and start containers
echo "📦 Building Docker images..."
if ! $DOCKER_COMPOSE_CMD build; then
    echo "❌ Failed to build Docker images"
    echo "   Try: docker system prune -a (this will remove unused images)"
    exit 1
fi

echo ""
echo "🚀 Starting containers..."
if ! $DOCKER_COMPOSE_CMD up -d; then
    echo "❌ Failed to start containers"
    echo "   Check logs: $DOCKER_COMPOSE_CMD logs"
    exit 1
fi

# Wait for backend to be ready
echo ""
echo "⏳ Waiting for backend to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    # Check if backend is responding
    if $DOCKER_COMPOSE_CMD exec -T backend python -c "import requests; requests.get('http://localhost:8000/')" > /dev/null 2>&1 || \
       $DOCKER_COMPOSE_CMD exec -T backend curl -f http://localhost:8000/ > /dev/null 2>&1 || \
       curl -f http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Backend is ready"
        break
    fi
    attempt=$((attempt + 1))
    if [ $((attempt % 5)) -eq 0 ]; then
        echo "   Attempt $attempt/$max_attempts... (still waiting)"
    fi
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "⚠️  Backend took longer than expected to start"
    echo "   You can check logs with: $DOCKER_COMPOSE_CMD logs backend"
fi

# Initialize database
echo ""
echo "🗄️  Initializing database..."
if $DOCKER_COMPOSE_CMD exec -T backend python -c "from database import init_db; init_db()" 2>/dev/null; then
    echo "✅ Database initialized"
else
    echo "⚠️  Database initialization failed. Trying again..."
    sleep 3
    if $DOCKER_COMPOSE_CMD exec -T backend python -c "from database import init_db; init_db()" 2>/dev/null; then
        echo "✅ Database initialized"
    else
        echo "❌ Failed to initialize database"
        echo "   You can try manually: $DOCKER_COMPOSE_CMD exec backend python init_db.py"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ CrystalTrade is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 Access the application:"
echo "   🌐 Frontend:  http://localhost:3000"
echo "   🔧 Backend:   http://localhost:8000"
echo "   📚 API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 Useful commands:"
echo "   View logs:    $DOCKER_COMPOSE_CMD logs -f"
echo "   View backend: $DOCKER_COMPOSE_CMD logs -f backend"
echo "   View frontend: $DOCKER_COMPOSE_CMD logs -f frontend"
echo "   Stop:         $DOCKER_COMPOSE_CMD down"
echo "   Restart:      $DOCKER_COMPOSE_CMD restart"
echo ""
echo "💡 Tip: If you need to update backend/.env, restart with:"
echo "   $DOCKER_COMPOSE_CMD restart backend"
echo ""

