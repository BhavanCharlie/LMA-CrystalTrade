#!/bin/bash

# CrystalTrade Docker Development Mode Script
# This script starts Docker in development mode with hot-reload enabled

echo "🚀 Starting CrystalTrade in Development Mode (Hot Reload)..."
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
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check for docker-compose or docker compose
DOCKER_COMPOSE_CMD=""
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
    echo "✅ Found: docker compose (plugin)"
elif command -v docker-compose > /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
    echo "✅ Found: docker-compose (standalone)"
else
    echo "❌ Neither 'docker compose' nor 'docker-compose' is available."
    exit 1
fi

# Verify Docker Compose can connect
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
        echo "❌ Docker Compose cannot connect to Docker daemon."
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

# Build and start containers in dev mode
echo "📦 Building Docker images for development..."
if ! $DOCKER_COMPOSE_CMD -f docker-compose.dev.yml build; then
    echo "❌ Failed to build Docker images"
    exit 1
fi

echo ""
echo "🚀 Starting containers in development mode..."
echo "   Changes to your code will be automatically reflected!"
echo ""

# Start in foreground so user can see logs
$DOCKER_COMPOSE_CMD -f docker-compose.dev.yml up


