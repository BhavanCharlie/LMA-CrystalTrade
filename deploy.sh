#!/bin/bash

# CrystalTrade Quick Deployment Script
set -e

echo "🚀 CrystalTrade Deployment Script"
echo "=================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "   Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "   Install from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file..."
    cd backend
    cat > .env << EOF
# CrystalTrade Backend Environment Variables
OPENAI_API_KEY=${OPENAI_API_KEY:-}
DATABASE_URL=sqlite:///./crystal_trade.db
SECRET_KEY=$(openssl rand -hex 32)
FRONTEND_URL=http://localhost:3000
DEBUG=False
HOST=0.0.0.0
PORT=8000
EOF
    cd ..
    echo "✅ Created backend/.env"
else
    echo "✅ backend/.env already exists"
fi

echo ""
echo "🔨 Building and starting containers..."
docker-compose down 2>/dev/null || true
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "📊 Initializing database..."
docker-compose exec -T backend python -c "from database import init_db; init_db()" || echo "Database already initialized"
docker-compose exec -T backend python create_demo_users.py || echo "Demo users may already exist"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📋 Demo Credentials:"
echo "   Username: demo"
echo "   Password: demo123"
echo ""
echo "📝 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
