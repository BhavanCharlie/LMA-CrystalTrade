# CrystalTrade

**CrystalTrade** - Transparent Loan Trading Platform for the LMA Edge Hackathon.

CrystalTrade automates due diligence checks for secondary loan market transactions, bringing transparency and efficiency to loan trading.

## Overview

This desktop application automates and streamlines due diligence checks for secondary loan market transactions using AI/ML to analyze loan documents, assess risks, verify compliance, and generate comprehensive reports.

## Features

- **Document Upload & Processing**: Drag-and-drop interface for loan documents with automatic classification
- **AI-Powered Analysis**: Extracts key loan terms, identifies risks, and flags unusual clauses
- **Automated Due Diligence**: Checks transfer restrictions, consent requirements, financial covenants, and regulatory compliance
- **Risk Assessment**: Visual risk scoring with breakdown by category (credit, legal, operational)
- **Compliance Checklist**: Automated compliance verification against LMA standards
- **Report Generation**: Automated PDF report generation with executive summaries
- **Trade Readiness Scoring**: Assesses loan tradeability with explainable breakdown
- **Transfer Simulation**: Simulates assignment and participation pathways
- **LMA Deviation Detection**: Identifies deviations from LMA standard templates
- **Buyer Fit Analysis**: Matches loans to suitable buyer types (CLO, Bank, Distressed Fund)
- **Negotiation Insights**: Predicts negotiation points and suggests redlines
- **Post-Trade Monitoring**: Rule-based alerting for covenants and obligations
- **Auction Room**: English and sealed-bid auction functionality for loan trading

## Technology Stack

### Frontend
- Electron (desktop framework)
- React + TypeScript
- Tailwind CSS
- Recharts (data visualization)
- React Router DOM (routing)
- Axios (HTTP client)
- React Hot Toast (notifications)

### Backend
- Python FastAPI
- OpenAI GPT-4 (document analysis)
- LangChain (document processing)
- SQLite/PostgreSQL (data storage)
- SQLAlchemy (ORM)
- ReportLab (PDF generation)
- Pydantic (data validation)
- JWT (authentication)
- Bcrypt (password hashing)

## Architecture

### System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Electron[Electron Desktop App]
        Browser[Web Browser<br/>React SPA]
        Mobile[Mobile App<br/>Future]
    end
    
    subgraph "Frontend Application"
        Pages[Pages<br/>Dashboard, Analysis, Upload]
        Components[Components<br/>RiskScore, TradeReadiness, Auction]
        Services[API Services<br/>Axios Client, Auth Context]
    end
    
    subgraph "API Layer - FastAPI"
        AuthAPI[Auth Endpoints<br/>/signup, /login, /me]
        DocAPI[Document API<br/>/upload]
        AnalysisAPI[Analysis API<br/>/start, /get, /trade-readiness]
        AuctionAPI[Auction API<br/>/create, /bids, /close]
        MonitorAPI[Monitoring API<br/>/rules, /alerts]
    end
    
    subgraph "Service Layer"
        DocProcessor[Document Processor<br/>PDF/Word/Excel Parsing]
        AIAnalyzer[AI Analyzer<br/>OpenAI GPT-4]
        DueDiligence[Due Diligence Engine<br/>Compliance & Risk]
        TradeReadiness[Trade Readiness Engine]
        TransferSim[Transfer Simulator]
        LMADev[LMA Deviation Engine]
        BuyerFit[Buyer Fit Analyzer]
        Negotiation[Negotiation Insights]
        Monitoring[Monitoring Service]
        Auction[Auction Service]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database<br/>SQLAlchemy ORM)]
        FileStorage[File Storage<br/>uploads/, reports/]
        ExternalAPI[External APIs<br/>OpenAI API]
    end
    
    Electron --> Pages
    Browser --> Pages
    Mobile --> Pages
    Pages --> Components
    Components --> Services
    
    Services -->|HTTP/REST| AuthAPI
    Services -->|HTTP/REST| DocAPI
    Services -->|HTTP/REST| AnalysisAPI
    Services -->|HTTP/REST| AuctionAPI
    Services -->|HTTP/REST| MonitorAPI
    
    DocAPI --> DocProcessor
    AnalysisAPI --> AIAnalyzer
    AnalysisAPI --> DueDiligence
    AnalysisAPI --> TradeReadiness
    AnalysisAPI --> TransferSim
    AnalysisAPI --> LMADev
    AnalysisAPI --> BuyerFit
    AnalysisAPI --> Negotiation
    MonitorAPI --> Monitoring
    AuctionAPI --> Auction
    
    DocProcessor --> FileStorage
    AIAnalyzer --> ExternalAPI
    TradeReadiness --> DB
    DueDiligence --> DB
    TransferSim --> DB
    LMADev --> DB
    BuyerFit --> DB
    Negotiation --> DB
    Monitoring --> DB
    Auction --> DB
    
    style Electron fill:#61dafb
    style Browser fill:#61dafb
    style Pages fill:#61dafb
    style Components fill:#61dafb
    style Services fill:#61dafb
    style AuthAPI fill:#009688
    style DocAPI fill:#009688
    style AnalysisAPI fill:#009688
    style AuctionAPI fill:#009688
    style AIAnalyzer fill:#ff9800
    style DB fill:#336791
    style ExternalAPI fill:#ffd700
```

### Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Auth
    participant Service
    participant Database
    
    User->>Frontend: User Action
    Frontend->>Frontend: Update State
    Frontend->>API: HTTP Request<br/>(with JWT token)
    
    API->>Auth: Verify JWT Token
    Auth->>Database: Get User
    Database-->>Auth: User Data
    Auth-->>API: Token Valid
    
    API->>Service: Call Service Layer
    Service->>Service: Business Logic
    Service->>Database: Query/Update Data
    Database-->>Service: Results
    
    Service-->>API: Processed Data
    API-->>Frontend: HTTP Response (JSON)
    Frontend->>Frontend: Update State
    Frontend-->>User: Display Results
```

## Project Structure

```
LMA-CrystalTrade/
├── backend/                          # FastAPI backend
│   ├── services/                     # Business logic
│   │   ├── ai_analyzer.py            # OpenAI GPT-4 analysis
│   │   ├── auction_service.py        # Auction management
│   │   ├── buyer_fit_analyzer.py     # Buyer matching
│   │   ├── document_processor.py    # Document parsing
│   │   ├── due_diligence_engine.py   # Compliance checks
│   │   ├── lma_deviation_engine.py   # LMA deviation detection
│   │   ├── monitoring_service.py     # Post-trade monitoring
│   │   ├── negotiation_insights.py   # Negotiation prediction
│   │   ├── report_generator.py       # PDF generation
│   │   ├── trade_readiness_engine.py # Trade readiness scoring
│   │   └── transfer_simulator.py    # Transfer pathways
│   ├── models.py                     # Database models
│   ├── main.py                       # FastAPI app
│   └── database.py                   # DB connection
├── src/                              # React frontend
│   ├── components/                   # Reusable components
│   ├── pages/                        # Page components
│   ├── services/                     # API client
│   └── contexts/                     # React contexts
├── electron/                         # Electron desktop app
└── package.json                      # Dependencies
```

## Data Models

### Core Models

- **Analysis**: Primary analysis results (risk scores, terms, compliance)
- **Document**: Uploaded document metadata
- **Report**: Generated PDF reports
- **User**: Authentication and user profiles

### Loan Markets Models

- **TradeReadiness**: Trade readiness scores and breakdowns
- **TransferSimulation**: Transfer pathway simulations
- **LMADeviation**: LMA template deviation records
- **BuyerFit**: Buyer type fit analysis
- **NegotiationInsight**: Negotiation predictions
- **MonitoringRule**: Post-trade monitoring rules
- **MonitoringAlert**: Generated alerts
- **Auction**: Auction records
- **Bid**: Bid records

### Supporting Models

- **EvidenceLog**: Evidence tracking for AI results
- **AuditEvent**: Audit trail
- **Deal**: Deal/transaction records

See `backend/models.py` for complete model definitions with fields and relationships.

## Data Flow Diagram

### Document Upload and Analysis Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant DocProcessor
    participant AIAnalyzer
    participant DueDiligence
    participant Database
    participant OpenAI
    
    User->>Frontend: Upload Document (PDF/Word/Excel)
    Frontend->>Backend: POST /api/v1/documents/upload
    Backend->>DocProcessor: save_file()
    DocProcessor->>FileStorage: Save file to disk
    Backend->>Database: Create Analysis (status: pending)
    Database-->>Backend: Return analysis_id
    Backend-->>Frontend: Return analysis_id
    Frontend-->>User: Show "Upload successful"
    
    User->>Frontend: Click "Start Analysis"
    Frontend->>Backend: POST /api/v1/analyses/{id}/start
    Backend->>Database: Update status: "processing"
    Backend->>Backend: Start Background Task
    
    par Parallel Processing
        Backend->>DocProcessor: extract_text()
        DocProcessor->>FileStorage: Read file
        DocProcessor-->>Backend: Return raw text
    and
        Backend->>AIAnalyzer: analyze_document(text)
        AIAnalyzer->>OpenAI: GPT-4 API Call
        OpenAI-->>AIAnalyzer: Extracted terms, risks, clauses
        AIAnalyzer-->>Backend: Structured JSON
    and
        Backend->>DueDiligence: run_checks(text, ai_results)
        DueDiligence->>DueDiligence: Check compliance
        DueDiligence->>DueDiligence: Calculate risk scores
        DueDiligence->>DueDiligence: Generate recommendations
        DueDiligence-->>Backend: Compliance & risk data
    end
    
    Backend->>Database: Update Analysis (status: completed)
    Database-->>Backend: Confirmation
    
    loop Polling
        Frontend->>Backend: GET /api/v1/analyses/{id}
        Backend->>Database: Query Analysis
        Database-->>Backend: Analysis data
        Backend-->>Frontend: Return results
        alt Status = "processing"
            Frontend->>Frontend: Wait 3 seconds
        else Status = "completed"
            Frontend->>Frontend: Display results
        end
    end
```

### Loan Markets Feature Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Engine
    participant Database
    participant EvidenceLog
    
    User->>Frontend: Click Feature Tab (e.g., Trade Readiness)
    Frontend->>Frontend: Check if data cached
    alt Data Not Cached
        Frontend->>Backend: GET /api/v1/analyses/{id}/feature-name
        Backend->>Database: Check if feature data exists
        alt Data Exists
            Database-->>Backend: Return cached data
            Backend-->>Frontend: Return cached results
        else Data Not Exists
            Backend->>Engine: Calculate feature data
            Engine->>Database: Fetch Analysis data
            Database-->>Engine: Analysis data
            Engine->>Engine: Process & Calculate
            Engine->>Database: Save feature results
            Engine->>EvidenceLog: Log evidence
            EvidenceLog->>Database: Save evidence logs
            Engine-->>Backend: Return calculated data
            Backend-->>Frontend: Return results
        end
    else Data Cached
        Frontend->>Frontend: Display cached data
    end
    Frontend-->>User: Display feature results
```

## Entity Relationship Diagram

### Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ ANALYSIS : creates
    USER ||--o{ AUCTION : creates
    USER ||--o{ BID : places
    
    ANALYSIS ||--o{ DOCUMENT : contains
    ANALYSIS ||--o{ REPORT : generates
    ANALYSIS ||--o{ TRADE_READINESS : has
    ANALYSIS ||--o{ TRANSFER_SIMULATION : has
    ANALYSIS ||--o{ LMA_DEVIATION : has
    ANALYSIS ||--o{ BUYER_FIT : has
    ANALYSIS ||--o{ NEGOTIATION_INSIGHT : has
    ANALYSIS ||--o{ MONITORING_RULE : has
    ANALYSIS ||--o{ AUCTION : linked_to
    ANALYSIS ||--o{ EVIDENCE_LOG : references
    
    AUCTION ||--o{ BID : receives
    MONITORING_RULE ||--o{ MONITORING_ALERT : triggers
    
    USER {
        string id PK
        string email UK
        string username UK
        string hashed_password
        string full_name
        boolean is_active
        boolean is_admin
        datetime created_at
    }
    
    ANALYSIS {
        string id PK
        string loan_name
        string status
        string document_path
        integer risk_score
        json risk_breakdown
        json compliance_checks
        json extracted_terms
        json recommendations
        datetime created_at
    }
    
    DOCUMENT {
        string id PK
        string analysis_id FK
        string file_path
        string file_name
        string file_type
        integer file_size
    }
    
    REPORT {
        string id PK
        string analysis_id FK
        string loan_name
        string report_type
        string file_path
    }
    
    TRADE_READINESS {
        string id PK
        string analysis_id FK
        integer score
        string label
        json breakdown
        float confidence
        json evidence_links
    }
    
    TRANSFER_SIMULATION {
        string id PK
        string analysis_id FK
        string pathway_type
        json required_consents
        integer estimated_timeline_days
        json blockers
        json recommended_actions
    }
    
    LMA_DEVIATION {
        string id PK
        string analysis_id FK
        string clause_text
        string clause_type
        string deviation_severity
        text market_impact
        text baseline_template
        float confidence
    }
    
    BUYER_FIT {
        string id PK
        string analysis_id FK
        string buyer_type
        integer fit_score
        json indicators
        text reasoning
    }
    
    NEGOTIATION_INSIGHT {
        string id PK
        string analysis_id FK
        string clause_reference
        text clause_text
        string negotiation_likelihood
        json suggested_redlines
        json questions_for_agent
    }
    
    MONITORING_RULE {
        string id PK
        string analysis_id FK
        string rule_type
        string rule_name
        float threshold_value
        float current_value
        boolean is_active
    }
    
    MONITORING_ALERT {
        string id PK
        string rule_id FK
        string analysis_id FK
        string alert_type
        text message
        float threshold_breach_percentage
        boolean is_acknowledged
    }
    
    AUCTION {
        string id PK
        string analysis_id FK
        string loan_name
        string auction_type
        float lot_size
        float min_bid
        float bid_increment
        float reserve_price
        datetime start_time
        datetime end_time
        string status
        string winning_bid_id FK
    }
    
    BID {
        string id PK
        string auction_id FK
        string bidder_id
        string bidder_name
        float bid_amount
        boolean is_locked
        boolean is_winning
        datetime timestamp
    }
    
    EVIDENCE_LOG {
        string id PK
        string analysis_id FK
        string document_id
        string document_name
        integer page_number
        string section
        text extraction_text
        float extraction_confidence
        string feature_type
        string feature_id
    }
    
    AUDIT_EVENT {
        string id PK
        string event_type
        string entity_type
        string entity_id
        string user_id FK
        string action
        json details
        datetime timestamp
    }
    
    DEAL {
        string id PK
        string deal_name
        string borrower_name
        string deal_type
        float principal_amount
        string currency
        string status
        json analysis_ids
        json deal_metadata
    }
```


## Deployment Architecture

### Deployment Architecture Diagram

```mermaid
graph LR
    subgraph "User Devices"
        Desktop[Desktop Browser]
        ElectronApp[Electron Desktop App]
        Mobile[Mobile Browser]
    end
    
    subgraph "Frontend Deployment"
        CDN[CDN/Edge Cache]
        Frontend[React Frontend<br/>Vite Build<br/>Static Assets]
    end
    
    subgraph "Backend Deployment"
        Backend[FastAPI Backend<br/>Uvicorn Server]
        DB[(PostgreSQL/SQLite<br/>Database)]
        FileStorage[File Storage<br/>S3/Local]
    end
    
    subgraph "External Services"
        OpenAIAPI[OpenAI API<br/>GPT-4]
        EmailService[Email Service<br/>Future]
    end
    
    Desktop --> CDN
    ElectronApp --> CDN
    Mobile --> CDN
    CDN --> Frontend
    Frontend -->|HTTPS/REST API| Backend
    Backend --> DB
    Backend --> FileStorage
    Backend -->|AI Requests| OpenAIAPI
    Backend -->|Notifications| EmailService
    
    style Frontend fill:#61dafb
    style Backend fill:#009688
    style DB fill:#336791
    style OpenAIAPI fill:#ffd700
    style CDN fill:#00d4ff
```

## Deployment Guide

> 📘 **For detailed step-by-step deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

This guide provides step-by-step instructions to deploy CrystalTrade to production environments.

## Quick Start: Step-by-Step Deployment

### Option 1: Docker Compose Deployment (Easiest - 5 Minutes)

**Step 1: Clone the Repository**
```bash
git clone <your-repository-url>
cd LMA-CrystalTrade
```

**Step 2: Create Environment File**
```bash
cd backend
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./crystal_trade.db
SECRET_KEY=$(openssl rand -hex 32)
FRONTEND_URL=http://localhost:3000
DEBUG=False
EOF
cd ..
```

**Step 3: Start Services**
```bash
docker-compose up -d --build
```

**Step 4: Initialize Database**
```bash
docker-compose exec backend python -c "from database import init_db; init_db()"
docker-compose exec backend python create_demo_users.py
```

**Step 5: Verify Deployment**
- Open browser: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Login with: `demo` / `demo123`

**Step 6: View Logs (if needed)**
```bash
docker-compose logs -f
```

**Step 7: Stop Services**
```bash
docker-compose down
```

---

### Option 2: Production Deployment on VPS/Server (30 Minutes)

#### Part A: Server Preparation

**Step 1: Connect to Your Server**
```bash
ssh user@your-server-ip
```

**Step 2: Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

**Step 3: Install Required Software**
```bash
# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y
```

**Step 4: Install PostgreSQL (Optional - for production)**
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE crystal_trade;
CREATE USER crystal_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE crystal_trade TO crystal_user;
\q
```

#### Part B: Backend Deployment

**Step 5: Clone Repository**
```bash
cd /var/www
sudo git clone <your-repository-url> crystal-trade
sudo chown -R $USER:$USER crystal-trade
cd crystal-trade/backend
```

**Step 6: Setup Python Environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 7: Configure Environment Variables**
```bash
nano .env
```

Add the following (adjust values as needed):
```bash
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://crystal_user:your_secure_password@localhost:5432/crystal_trade
# Or for SQLite: DATABASE_URL=sqlite:///./crystal_trade.db
SECRET_KEY=$(openssl rand -hex 32)
FRONTEND_URL=https://yourdomain.com
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

**Step 8: Initialize Database**
```bash
python -c "from database import init_db; init_db()"
python create_demo_users.py
```

**Step 9: Test Backend**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
# Press Ctrl+C after testing
```

**Step 10: Create Systemd Service**
```bash
sudo nano /etc/systemd/system/crystal-trade-backend.service
```

Paste the following:
```ini
[Unit]
Description=CrystalTrade Backend API
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/crystal-trade/backend
Environment="PATH=/var/www/crystal-trade/backend/venv/bin"
ExecStart=/var/www/crystal-trade/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 11: Start Backend Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable crystal-trade-backend
sudo systemctl start crystal-trade-backend
sudo systemctl status crystal-trade-backend
```

**Step 12: Configure Nginx for Backend**
```bash
sudo nano /etc/nginx/sites-available/crystal-trade-api
```

Add:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
}
```

**Step 13: Enable Backend Nginx Site**
```bash
sudo ln -s /etc/nginx/sites-available/crystal-trade-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Part C: Frontend Deployment

**Step 14: Build Frontend**
```bash
cd /var/www/crystal-trade
npm install
```

**Step 15: Create Frontend Environment File**
```bash
cat > .env.production << EOF
VITE_API_URL=https://api.yourdomain.com
EOF
```

**Step 16: Build Frontend for Production**
```bash
npm run build
```

**Step 17: Configure Nginx for Frontend**
```bash
sudo nano /etc/nginx/sites-available/crystal-trade
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/crystal-trade/dist;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Step 18: Enable Frontend Nginx Site**
```bash
sudo ln -s /etc/nginx/sites-available/crystal-trade /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 19: Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

**Step 20: Verify Deployment**
- Frontend: https://yourdomain.com
- Backend API: https://api.yourdomain.com
- API Docs: https://api.yourdomain.com/docs

---

### Option 3: Cloud Platform Deployment (Render.com - 15 Minutes)

#### Backend Deployment on Render

**Step 1: Create Render Account**
- Go to https://render.com
- Sign up with GitHub

**Step 2: Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository

**Step 3: Configure Backend Service**
- **Name**: `crystal-trade-backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 4: Add Environment Variables**
Click "Advanced" → "Add Environment Variable" and add:
```
DATABASE_URL=postgresql://... (from PostgreSQL service)
OPENAI_API_KEY=your_key
SECRET_KEY=your_secret_key_min_32_chars
FRONTEND_URL=https://your-frontend.onrender.com
DEBUG=False
```

**Step 5: Create PostgreSQL Database**
- Click "New +" → "PostgreSQL"
- **Name**: `crystal-trade-db`
- **Database**: `crystal_trade`
- Copy the "Internal Database URL"
- Paste it as `DATABASE_URL` in backend environment variables

**Step 6: Deploy Backend**
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Note the service URL (e.g., `https://crystal-trade-backend.onrender.com`)

**Step 7: Initialize Database**
- Go to backend service → "Shell"
- Run:
```bash
python -c "from database import init_db; init_db()"
python create_demo_users.py
```

#### Frontend Deployment on Render

**Step 8: Create Static Site**
- Click "New +" → "Static Site"
- Connect same GitHub repository

**Step 9: Configure Frontend**
- **Name**: `crystal-trade-frontend`
- **Root Directory**: (leave empty)
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`

**Step 10: Add Environment Variables**
```
VITE_API_URL=https://crystal-trade-backend.onrender.com
```

**Step 11: Deploy Frontend**
- Click "Create Static Site"
- Wait for deployment
- Your app will be live at the provided URL

---

### Option 4: Railway.app Deployment (10 Minutes)

**Step 1: Create Railway Account**
- Go to https://railway.app
- Sign up with GitHub

**Step 2: Create New Project**
- Click "New Project" → "Deploy from GitHub repo"
- Select your repository

**Step 3: Add Backend Service**
- Click "New" → "GitHub Repo"
- Select backend directory
- Railway auto-detects Python

**Step 4: Add PostgreSQL**
- Click "New" → "Database" → "Add PostgreSQL"
- Railway automatically sets `DATABASE_URL`

**Step 5: Configure Backend Environment**
Click on backend service → "Variables" tab, add:
```
OPENAI_API_KEY=your_key
SECRET_KEY=your_secret_key
FRONTEND_URL=https://your-app.up.railway.app
DEBUG=False
```

**Step 6: Add Frontend Service**
- Click "New" → "GitHub Repo"
- Select project root
- Set root directory to project root

**Step 7: Configure Frontend**
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npx serve -s dist -l $PORT`

**Step 8: Add Frontend Environment Variables**
```
VITE_API_URL=https://your-backend.up.railway.app
```

**Step 9: Deploy**
- Railway automatically deploys
- Get your URLs from service settings

**Step 10: Initialize Database**
- Go to backend service → "Deployments" → "View Logs"
- Or use Railway CLI:
```bash
railway run python -c "from database import init_db; init_db()"
railway run python create_demo_users.py
```

---

## Post-Deployment Steps

### Step 1: Verify All Services
```bash
# Check backend health
curl https://your-backend-url/health

# Check frontend loads
curl https://your-frontend-url
```

### Step 2: Test Authentication
- Visit frontend URL
- Try to sign up
- Try to login
- Verify JWT token is stored

### Step 3: Test Document Upload
- Upload a test PDF
- Start analysis
- Verify results appear

### Step 4: Setup Monitoring (Optional)
```bash
# Install monitoring tools
# Example: Uptime monitoring with UptimeRobot or Pingdom
```

### Step 5: Setup Backups
```bash
# For PostgreSQL
pg_dump crystal_trade > backup.sql

# Schedule daily backups with cron
crontab -e
# Add: 0 2 * * * pg_dump crystal_trade > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Step 6: Configure Domain (if using custom domain)
- Point DNS A record to your server IP
- Or configure CNAME for cloud platforms
- Wait for DNS propagation (up to 48 hours)

---

## Troubleshooting Common Issues

### Issue: Backend won't start
```bash
# Check logs
sudo journalctl -u crystal-trade-backend -n 50

# Check environment variables
sudo cat /var/www/crystal-trade/backend/.env

# Test manually
cd /var/www/crystal-trade/backend
source venv/bin/activate
python -c "from main import app; print('OK')"
```

### Issue: Frontend can't connect to backend
```bash
# Check CORS settings in backend
# Verify VITE_API_URL in frontend .env
# Check network connectivity
curl https://your-backend-url/api/v1/dashboard/stats
```

### Issue: Database connection error
```bash
# Test PostgreSQL connection
psql -h localhost -U crystal_user -d crystal_trade

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Issue: File uploads not working
```bash
# Check directory permissions
sudo chown -R www-data:www-data /var/www/crystal-trade/backend/uploads
sudo chmod -R 755 /var/www/crystal-trade/backend/uploads

# Check disk space
df -h
```

---

## Maintenance Commands

### Update Application
```bash
cd /var/www/crystal-trade
git pull origin main
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart crystal-trade-backend
cd ..
npm install
npm run build
sudo systemctl restart nginx
```

### View Logs
```bash
# Backend logs
sudo journalctl -u crystal-trade-backend -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Docker logs
docker-compose logs -f backend
```

### Restart Services
```bash
# Backend
sudo systemctl restart crystal-trade-backend

# Nginx
sudo systemctl restart nginx

# Docker
docker-compose restart
```

---

## Deployment Guide (Detailed)

This section provides detailed information about deployment options and configurations.

### Prerequisites

Before deploying, ensure you have:

- **Node.js 18+** and npm installed
- **Python 3.10+** installed
- **Docker** and Docker Compose (for containerized deployment)
- **Git** for cloning the repository
- **OpenAI API Key** (optional, for AI features)
- **Domain name** (optional, for production)
- **SSL Certificate** (for HTTPS in production)

### Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# OpenAI API (Required for AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./crystal_trade.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@host:port/dbname

# JWT Authentication
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=43200  # 30 days

# Application Settings
DEBUG=False  # Set to False in production
HOST=0.0.0.0
PORT=8000

# Frontend URL (for CORS)
FRONTEND_URL=https://your-frontend-domain.com
# For development: FRONTEND_URL=http://localhost:5173

# File Storage (Optional - for cloud storage)
# AWS_S3_BUCKET=your-bucket-name
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_REGION=us-east-1
```

### Deployment Methods

#### Method 1: Docker Compose (Recommended for Quick Deployment)

**Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd LMA-CrystalTrade
```

**Step 2: Configure Environment Variables**
```bash
cd backend
cp .env.example .env  # Or create .env manually
# Edit .env with your configuration
```

**Step 3: Build and Start Services**
```bash
# From project root
docker-compose up -d --build
```

**Step 4: Initialize Database**
```bash
docker-compose exec backend python -c "from database import init_db; init_db()"
docker-compose exec backend python create_demo_users.py
```

**Step 5: Verify Deployment**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Step 6: Stop Services**
```bash
docker-compose down
```

**Step 7: View Logs**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

#### Method 2: Manual Deployment (VPS/Server)

**Backend Deployment:**

**Step 1: Server Setup**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip nginx -y

# Install Node.js (for frontend build)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

**Step 2: Clone and Setup Backend**
```bash
cd /var/www
sudo git clone <repository-url> crystal-trade
cd crystal-trade/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env  # Add your environment variables

# Initialize database
python -c "from database import init_db; init_db()"
python create_demo_users.py
```

**Step 3: Setup Systemd Service**
```bash
sudo nano /etc/systemd/system/crystal-trade-backend.service
```

Add the following content:
```ini
[Unit]
Description=CrystalTrade Backend API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/crystal-trade/backend
Environment="PATH=/var/www/crystal-trade/backend/venv/bin"
ExecStart=/var/www/crystal-trade/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Step 4: Start Backend Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable crystal-trade-backend
sudo systemctl start crystal-trade-backend
sudo systemctl status crystal-trade-backend
```

**Step 5: Configure Nginx Reverse Proxy**
```bash
sudo nano /etc/nginx/sites-available/crystal-trade-backend
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeouts for long-running requests
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

**Step 6: Enable Nginx Configuration**
```bash
sudo ln -s /etc/nginx/sites-available/crystal-trade-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Frontend Deployment:**

**Step 1: Build Frontend**
```bash
cd /var/www/crystal-trade
npm install
npm run build
```

**Step 2: Configure Nginx for Frontend**
```bash
sudo nano /etc/nginx/sites-available/crystal-trade-frontend
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    root /var/www/crystal-trade/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Step 3: Enable Frontend Configuration**
```bash
sudo ln -s /etc/nginx/sites-available/crystal-trade-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Step 4: Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

#### Method 3: Cloud Platform Deployment

##### Option A: Render.com

**Backend Deployment:**

1. **Create New Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `crystal-trade-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

3. **Environment Variables**
   ```
   DATABASE_URL=postgresql://user:pass@host/db
   OPENAI_API_KEY=your_key
   SECRET_KEY=your_secret_key
   FRONTEND_URL=https://your-frontend.onrender.com
   DEBUG=False
   ```

4. **Add PostgreSQL Database**
   - Create new PostgreSQL database
   - Copy connection string to `DATABASE_URL`

**Frontend Deployment:**

1. **Create New Static Site**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect your GitHub repository

2. **Configure Build**
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Root Directory**: (leave empty)

3. **Environment Variables**
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

##### Option B: Railway.app

**Backend Deployment:**

1. **Create New Project**
   - Go to Railway Dashboard
   - Click "New Project" → "Deploy from GitHub repo"

2. **Configure Service**
   - Select backend directory
   - Railway auto-detects Python
   - Add environment variables in dashboard

3. **Add PostgreSQL**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

**Frontend Deployment:**

1. **Create New Service**
   - In same project, click "New" → "GitHub Repo"
   - Select frontend directory

2. **Configure Build**
   - Set root directory to project root
   - Build command: `npm install && npm run build`
   - Start command: `npx serve -s dist -l $PORT`

##### Option C: AWS (EC2 + S3 + RDS)

**Step 1: Launch EC2 Instance**
```bash
# Launch Ubuntu 22.04 LTS instance
# Security Group: Allow HTTP (80), HTTPS (443), SSH (22)
```

**Step 2: Setup Backend on EC2**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Follow Manual Deployment steps above
```

**Step 3: Setup RDS PostgreSQL**
- Go to AWS RDS Console
- Create PostgreSQL database
- Note connection string
- Update `DATABASE_URL` in backend `.env`

**Step 4: Setup S3 for File Storage**
- Create S3 bucket
- Configure IAM user with S3 access
- Add AWS credentials to backend `.env`

**Step 5: Deploy Frontend to S3 + CloudFront**
```bash
# Build frontend
npm run build

# Install AWS CLI
aws configure

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Create CloudFront distribution
# Point to S3 bucket
# Configure custom domain and SSL
```

#### Method 4: Vercel (Frontend) + Render (Backend)

**Backend on Render:**
- Follow Render.com backend deployment steps above

**Frontend on Vercel:**

1. **Import Project**
   - Go to Vercel Dashboard
   - Click "Add New" → "Project"
   - Import from GitHub

2. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: (leave empty)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

3. **Environment Variables**
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Vercel automatically deploys on every push

### Database Migration (SQLite to PostgreSQL)

If migrating from SQLite to PostgreSQL:

**Step 1: Export SQLite Data**
```bash
sqlite3 crystal_trade.db .dump > backup.sql
```

**Step 2: Create PostgreSQL Database**
```bash
createdb crystal_trade
```

**Step 3: Import Data**
```bash
# Modify backup.sql to be PostgreSQL compatible
psql crystal_trade < backup.sql
```

**Step 4: Update DATABASE_URL**
```bash
# In backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/crystal_trade
```

### Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Use strong `SECRET_KEY` (minimum 32 characters)
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up PostgreSQL database (not SQLite)
- [ ] Configure CORS with production frontend URL
- [ ] Set up file storage (S3/GCS/Azure) for uploads
- [ ] Configure backup strategy for database
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Test all API endpoints
- [ ] Verify authentication works
- [ ] Test file uploads
- [ ] Configure email notifications (if needed)
- [ ] Set up CI/CD pipeline
- [ ] Document API endpoints
- [ ] Set up health check endpoints

### Monitoring and Maintenance

**Health Check Endpoint:**
```bash
curl http://your-backend-url/health
```

**View Logs:**
```bash
# Docker
docker-compose logs -f backend

# Systemd
sudo journalctl -u crystal-trade-backend -f

# Render/Railway
# View logs in dashboard
```

**Database Backup:**
```bash
# PostgreSQL
pg_dump crystal_trade > backup_$(date +%Y%m%d).sql

# SQLite
cp crystal_trade.db backup_$(date +%Y%m%d).db
```

**Update Application:**
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Or for manual deployment
sudo systemctl restart crystal-trade-backend
```

### Troubleshooting

**Backend won't start:**
- Check environment variables are set correctly
- Verify database connection string
- Check logs: `docker-compose logs backend` or `sudo journalctl -u crystal-trade-backend`

**Frontend can't connect to backend:**
- Verify `VITE_API_URL` is set correctly
- Check CORS settings in backend
- Verify backend is accessible from frontend domain

**Database connection errors:**
- Verify `DATABASE_URL` format
- Check database is running
- Verify credentials and network access

**File upload issues:**
- Check upload directory permissions
- Verify disk space
- Check file size limits in nginx/backend config

**Performance issues:**
- Enable database connection pooling
- Use CDN for static assets
- Configure caching headers
- Consider using Redis for session storage

### Security Considerations

1. **Never commit `.env` files** to version control
2. **Use environment variables** for all secrets
3. **Enable HTTPS** in production
4. **Set up firewall rules** to restrict access
5. **Regular security updates** for dependencies
6. **Use strong passwords** for database
7. **Implement rate limiting** on API endpoints
8. **Regular backups** of database
9. **Monitor logs** for suspicious activity
10. **Keep dependencies updated** (`npm audit`, `pip check`)

### Support

For deployment issues, check:
- Application logs
- Server logs
- Database logs
- Network connectivity
- Environment variable configuration

## Workflow Diagram

### Document Analysis Workflow

```mermaid
flowchart TD
    Start([User Starts]) --> Upload[Upload Document]
    Upload --> Validate{File Valid?}
    Validate -->|No| Error1[Show Error]
    Validate -->|Yes| SaveFile[Save to Storage]
    SaveFile --> CreateAnalysis[Create Analysis Record<br/>status: pending]
    CreateAnalysis --> ShowSuccess[Show Upload Success]
    ShowSuccess --> StartAnalysis{User Clicks<br/>Start Analysis?}
    
    StartAnalysis -->|No| Wait[Wait for User]
    StartAnalysis -->|Yes| UpdateStatus[Update Status:<br/>processing]
    UpdateStatus --> BackgroundTask[Background Task]
    
    BackgroundTask --> ExtractText[Extract Text<br/>PDF/Word/Excel]
    ExtractText --> AIAnalysis[AI Analysis<br/>OpenAI GPT-4]
    AIAnalysis --> DueDiligence[Due Diligence Checks]
    DueDiligence --> RiskScoring[Calculate Risk Scores]
    RiskScoring --> Recommendations[Generate Recommendations]
    Recommendations --> SaveResults[Save Results to DB]
    SaveResults --> UpdateComplete[Update Status:<br/>completed]
    
    UpdateComplete --> Polling{Status Polling}
    Polling -->|processing| Wait3Sec[Wait 3 seconds]
    Wait3Sec --> Polling
    Polling -->|completed| DisplayResults[Display Results]
    
    DisplayResults --> OverviewTab[Overview Tab<br/>Risk, Terms, Compliance]
    DisplayResults --> LoanMarketsTabs[Loan Markets Tabs]
    
    LoanMarketsTabs --> TradeReadiness[Trade Readiness]
    LoanMarketsTabs --> TransferSim[Transfer Simulator]
    LoanMarketsTabs --> LMADev[LMA Deviations]
    LoanMarketsTabs --> BuyerFit[Buyer Fit]
    LoanMarketsTabs --> Negotiation[Negotiation Insights]
    LoanMarketsTabs --> Monitoring[Monitoring]
    LoanMarketsTabs --> Auction[Auction Room]
    
    Error1 --> Start
    Wait --> StartAnalysis
    
    style Start fill:#90EE90
    style DisplayResults fill:#87CEEB
    style Error1 fill:#FFB6C1
    style BackgroundTask fill:#FFD700
```


### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant AuthService
    participant Database
    
    Note over User,Database: Registration Flow
    User->>Frontend: Fill Signup Form
    Frontend->>Backend: POST /api/v1/auth/signup
    Backend->>AuthService: Validate Input
    AuthService->>Database: Check Email/Username Uniqueness
    Database-->>AuthService: Validation Result
    AuthService->>AuthService: Hash Password (bcrypt)
    AuthService->>Database: Create User Record
    Database-->>AuthService: User Created
    AuthService->>AuthService: Generate JWT Token
    AuthService-->>Backend: Return User + Token
    Backend-->>Frontend: Success Response
    Frontend->>Frontend: Store Token in localStorage
    Frontend-->>User: Redirect to Dashboard
    
    Note over User,Database: Login Flow
    User->>Frontend: Fill Login Form
    Frontend->>Backend: POST /api/v1/auth/login
    Backend->>AuthService: Authenticate User
    AuthService->>Database: Find User (username/email)
    Database-->>AuthService: User Data
    AuthService->>AuthService: Verify Password (bcrypt)
    alt Password Correct
        AuthService->>AuthService: Generate JWT Token
        AuthService-->>Backend: Return Token
        Backend-->>Frontend: Success + Token
        Frontend->>Frontend: Store Token
        Frontend-->>User: Redirect to Dashboard
    else Password Incorrect
        AuthService-->>Backend: Authentication Failed
        Backend-->>Frontend: 401 Unauthorized
        Frontend-->>User: Show Error Message
    end
    
    Note over User,Database: Protected Route Access
    User->>Frontend: Navigate to Protected Route
    Frontend->>Frontend: Check AuthContext
    alt Not Authenticated
        Frontend-->>User: Redirect to /login
    else Authenticated
        Frontend->>Backend: API Request + JWT Token
        Backend->>AuthService: Verify Token
        AuthService->>AuthService: Decode & Validate Token
        alt Token Valid
            AuthService->>Database: Get User
            Database-->>AuthService: User Data
            AuthService-->>Backend: User Authenticated
            Backend->>Backend: Process Request
            Backend-->>Frontend: Success Response
        else Token Invalid/Expired
            Backend-->>Frontend: 401 Unauthorized
            Frontend->>Frontend: Clear Token
            Frontend-->>User: Redirect to Login
        end
    end
```

### Auction Workflow

```mermaid
sequenceDiagram
    participant Seller
    participant Buyer
    participant Frontend
    participant Backend
    participant AuctionService
    participant Database
    participant AuditLog
    
    Note over Seller,AuditLog: Auction Creation Flow
    Seller->>Frontend: Create Auction Form
    Frontend->>Backend: POST /api/v1/auctions<br/>{analysis_id, loan_name, type, lot_size, etc.}
    Backend->>AuctionService: Validate & Create
    AuctionService->>Database: Check analysis exists
    Database-->>AuctionService: Analysis data
    AuctionService->>Database: Create Auction Record<br/>(status: pending)
    AuctionService->>AuditLog: Log auction_created event
    Database-->>AuctionService: Auction created
    AuctionService-->>Backend: Return auction_id
    Backend-->>Frontend: Success + auction_id
    Frontend-->>Seller: Show auction created
    
    Note over Seller,AuditLog: Bidding Flow
    Buyer->>Frontend: View Auction & Place Bid
    Frontend->>Backend: POST /api/v1/auctions/{id}/bids<br/>{bid_amount}
    Backend->>AuctionService: Validate Bid
    AuctionService->>Database: Check auction status
    Database-->>AuctionService: Auction data
    alt Auction Active & Bid Valid
        AuctionService->>Database: Create Bid Record<br/>(is_locked: true)
        AuctionService->>Database: Update highest bid
        AuctionService->>AuditLog: Log bid_placed event
        Database-->>AuctionService: Bid created
        AuctionService-->>Backend: Success
        Backend-->>Frontend: Bid accepted
        Frontend-->>Buyer: Show bid confirmation
    else Bid Invalid
        AuctionService-->>Backend: Validation error
        Backend-->>Frontend: Error message
        Frontend-->>Buyer: Show error
    end
    
    Note over Seller,AuditLog: Auction Closure Flow
    Seller->>Frontend: Close Auction
    Frontend->>Backend: POST /api/v1/auctions/{id}/close
    Backend->>AuctionService: Close Auction
    AuctionService->>Database: Get all bids
    Database-->>AuctionService: Bids list
    AuctionService->>AuctionService: Find highest bid<br/>Check >= reserve_price
    alt Highest Bid >= Reserve
        AuctionService->>Database: Update Auction<br/>(status: closed, winning_bid_id)
        AuctionService->>Database: Update Bid<br/>(is_winning: true)
        AuctionService->>AuditLog: Log auction_closed event
        Database-->>AuctionService: Auction closed
        AuctionService-->>Backend: Winner determined
        Backend-->>Frontend: Auction closed + winner
        Frontend-->>Seller: Show winner
    else No Valid Bid
        AuctionService->>Database: Update Auction<br/>(status: closed, no winner)
        AuctionService-->>Backend: Auction closed (no winner)
        Backend-->>Frontend: Auction closed
        Frontend-->>Seller: Show no winner message
    end
```

## AI Modules Used

### Core AI Libraries

- **OpenAI** (`openai>=1.54.0`): GPT-4 Turbo for document analysis
- **LangChain** (`langchain>=0.3.0`): Document processing framework
  - `langchain-openai`: OpenAI integration
  - `langchain-text-splitters`: Text chunking (4000 chars, 200 overlap)
  - `langchain-core`: Core components
- **spaCy** (`spacy>=3.7.5`): NLP for entity recognition
- **scikit-learn** (`scikit-learn>=1.5.0`): ML algorithms
- **numpy** (`numpy>=1.26.0`): Numerical computations
- **chromadb** (`chromadb>=0.5.0`): Vector database for embeddings

### Document Processing

- **pdfplumber** (`pdfplumber>=0.11.0`): PDF text extraction
- **pypdf2** (`pypdf2>=3.0.1`): PDF fallback
- **python-docx** (`python-docx>=1.1.2`): Word processing
- **openpyxl** (`openpyxl>=3.1.5`): Excel processing
- **pytesseract** (`pytesseract>=0.3.13`): OCR
- **pillow** (`pillow>=11.0.0`): Image processing

### AI Services

- **AIAnalyzer**: GPT-4 document analysis
- **TradeReadinessEngine**: Rule-based scoring
- **LMADeviationEngine**: Template matching
- **BuyerFitAnalyzer**: Classification algorithms
- **NegotiationInsightsGenerator**: Pattern recognition

### AI Configuration

- **Model**: GPT-4 Turbo Preview
- **Temperature**: 0 (deterministic)
- **Chunk Size**: 4000 characters
- **Chunk Overlap**: 200 characters

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- OpenAI API key (optional, for AI features)

### Installation

1. **Install frontend dependencies:**
```bash
npm install
```

2. **Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./crystal_trade.db
```

4. **Initialize database:**
```bash
cd backend
python -c "from database import init_db; init_db()"
```

### Running the Application

**Option 1: Docker (Recommended)**
```bash
# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python -c "from database import init_db; init_db()"
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

**Option 2: Docker Development Mode (Hot Reload)**
```bash
./docker-dev.sh
```

This starts containers with hot-reload enabled - code changes are automatically reflected!

**Option 3: Local Development (No Docker)**
```bash
npm run dev
```

This will start:
- React dev server on http://localhost:5173
- FastAPI backend on http://localhost:8000
- Electron desktop app

**Build for production:**
```bash
npm run build
npm start
```

## API Endpoints

- `POST /api/v1/documents/upload` - Upload document
- `POST /api/v1/analyses/{id}/start` - Start analysis
- `GET /api/v1/analyses/{id}` - Get analysis results
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/reports` - List reports
- `POST /api/v1/reports/generate` - Generate report

## Usage

1. **Upload Documents**: Navigate to the Upload page and drag-and-drop loan documents
2. **Start Analysis**: Click "Upload and Analyze" to begin AI-powered analysis
3. **View Results**: Once analysis completes, view detailed results including:
   - Risk scores and breakdown
   - Extracted loan terms
   - Compliance checklist
   - Recommendations
4. **Generate Reports**: Create PDF reports from completed analyses

## Commercial Viability

- **Target Users**: Loan traders, secondary market participants, due diligence teams
- **Value Proposition**: Reduces due diligence time from days to hours, cuts costs by 60-80%
- **Scalability**: Cloud-ready architecture, API-first design
- **Revenue Model**: Per-transaction pricing or subscription tiers

## License

MIT License

Copyright (c) 2024 CrystalTrade

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
