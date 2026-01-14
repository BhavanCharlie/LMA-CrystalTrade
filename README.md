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

## AI Modules Used

| Category | Technology | Purpose |
|----------|------------|---------|
| **Language Model** | OpenAI GPT-4 Turbo | Document analysis, term extraction, risk assessment |
| **AI Framework** | LangChain | Document processing orchestration, text chunking |
| **NLP** | spaCy | Named entity recognition, text analysis |
| **ML** | scikit-learn | Classification algorithms, pattern matching |
| **Vector DB** | ChromaDB | Document embeddings storage |
| **Numerical** | NumPy | Array operations, calculations |

### Document Processing

| Format | Library | Capability |
|--------|---------|------------|
| PDF | pdfplumber, PyPDF2 | Text extraction with fallback |
| Word | python-docx | .docx file parsing |
| Excel | openpyxl | Spreadsheet data extraction |
| Images | Pytesseract, Pillow | OCR for scanned documents |

### AI-Powered Services

| Service | Function | Technology |
|---------|----------|------------|
| AI Analyzer | Extract loan terms and clauses | GPT-4 + LangChain |
| Trade Readiness Engine | Assess loan transferability | Rule-based + ML scoring |
| LMA Deviation Engine | Compare against LMA standards | Template matching |
| Buyer Fit Analyzer | Match loans to buyer types | Classification algorithms |
| Negotiation Insights | Generate redlines and talking points | Pattern recognition |
| Risk Scorer | Calculate risk breakdown | Weighted scoring model |

### Configuration

| Parameter | Value |
|-----------|-------|
| Model | GPT-4 Turbo Preview |
| Temperature | 0 (deterministic) |
| Chunk Size | 4,000 characters |
| Chunk Overlap | 200 characters |

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
