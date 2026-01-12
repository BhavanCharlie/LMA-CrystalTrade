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

### System Architecture Diagram (Mermaid)

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

### Request Flow (Mermaid)

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

### Request Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. User Action (click, form submit)
     │
┌────▼────────────────────────────────────┐
│  React Frontend                        │
│  ┌──────────────────────────────────┐  │
│  │ Component/Page                   │  │
│  │  • useState/useEffect            │  │
│  │  • Event Handler                 │  │
│  └────────────┬─────────────────────┘  │
│               │                         │
│  ┌────────────▼─────────────────────┐  │
│  │ API Service (api.ts)            │  │
│  │  • Axios instance                │  │
│  │  • JWT token injection          │  │
│  │  • Request formatting            │  │
│  └────────────┬─────────────────────┘  │
└───────────────┼─────────────────────────┘
                │
                │ 2. HTTP Request (JSON)
                │    Headers: Authorization: Bearer <token>
                │
┌───────────────▼─────────────────────────┐
│  FastAPI Backend                       │
│  ┌──────────────────────────────────┐  │
│  │ CORS Middleware                  │  │
│  └────────────┬─────────────────────┘  │
│               │                         │
│  ┌────────────▼─────────────────────┐  │
│  │ JWT Auth Middleware               │  │
│  │  • Verify token                    │  │
│  │  • Extract user info               │  │
│  └────────────┬─────────────────────┘  │
│               │                         │
│  ┌────────────▼─────────────────────┐  │
│  │ Route Handler                    │  │
│  │  • Validate request               │  │
│  │  • Parse parameters              │  │
│  │  • Call service layer            │  │
│  └────────────┬─────────────────────┘  │
│               │                         │
│  ┌────────────▼─────────────────────┐  │
│  │ Service Layer                    │  │
│  │  • Business logic                │  │
│  │  • Data processing               │  │
│  │  • External API calls            │  │
│  └────────────┬─────────────────────┘  │
│               │                         │
│  ┌────────────▼─────────────────────┐  │
│  │ Database Layer (SQLAlchemy)     │  │
│  │  • ORM queries                   │  │
│  │  • Transactions                  │  │
│  │  • Data persistence              │  │
│  └────────────┬─────────────────────┘  │
└───────────────┼─────────────────────────┘
                │
                │ 3. SQL Query
                │
┌───────────────▼─────────────────────────┐
│  SQLite Database                        │
│  • Execute query                        │
│  • Return results                       │
└───────────────┬─────────────────────────┘
                │
                │ 4. Query Results
                │
┌───────────────▼─────────────────────────┐
│  FastAPI Backend                       │
│  • Format response                     │
│  • Add status code                     │
│  • Serialize data                      │
└───────────────┬─────────────────────────┘
                │
                │ 5. HTTP Response (JSON)
                │    Status: 200 OK
                │
┌───────────────▼─────────────────────────┐
│  React Frontend                        │
│  • Update state                        │
│  • Re-render components                │
│  • Show notifications                  │
└─────────────────────────────────────────┘
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

### Document Upload and Analysis Flow (Mermaid)

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

### Loan Markets Feature Data Flow (Mermaid)

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

### Entity Relationship Diagram (Mermaid)

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

### Deployment Architecture Diagram (Mermaid)

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

### Deployment Options

**Development:**
- Frontend: Vite dev server (localhost:5173)
- Backend: Uvicorn (localhost:8000)
- Database: SQLite (local file)
- File Storage: Local filesystem

**Production:**
- Frontend: Static hosting (Vercel, Netlify, or S3+CloudFront)
- Backend: Cloud platform (Render, Railway, AWS, GCP)
- Database: PostgreSQL (managed service)
- File Storage: S3, GCS, or Azure Blob

## Workflow Diagram

### Document Analysis Workflow (Mermaid)

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


### Authentication Flow (Mermaid)

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

### Authentication Flow (Detailed)

User fills Signup Form
    │
    └─► POST /api/v1/auth/signup
        Body: { email, username, password, full_name }
        │
        ├─► Backend Validation
        │   • Check email format
        │   • Check username uniqueness
        │   • Check password strength
        │
        ├─► Hash Password
        │   └─► bcrypt.hash(password)
        │
        ├─► Create User Record
        │   • id: UUID
        │   • email: validated
        │   • username: unique
        │   • hashed_password: bcrypt hash
        │   • is_active: true
        │   • is_admin: false
        │
        └─► Return User (without password)
            │
            └─► Frontend: Auto-login or redirect to login

┌─────────────────────────────────────────────────────────────────────┐
│                    USER LOGIN FLOW                                   │
└─────────────────────────────────────────────────────────────────────┘

User fills Login Form
    │
    └─► POST /api/v1/auth/login
        Body: { username/email, password }
        │
        ├─► Backend: Find User
        │   • Try username first (indexed lookup)
        │   • If not found, try email (indexed lookup)
        │   • Check if user exists and is_active
        │
        ├─► Verify Password
        │   └─► bcrypt.checkpw(password, hashed_password)
        │       • Returns True/False
        │
        ├─► Generate JWT Token
        │   └─► jwt.encode({
        │         "sub": user.id,
        │         "username": user.username,
        │         "exp": datetime.utcnow() + timedelta(days=30)
        │       }, SECRET_KEY)
        │
        └─► Return Token
            │
            └─► Frontend: Store in localStorage
                │
                └─► Set Authorization header for all requests
                    Header: Authorization: Bearer <token>

┌─────────────────────────────────────────────────────────────────────┐
│                    PROTECTED ROUTE ACCESS                           │
└─────────────────────────────────────────────────────────────────────┘

User navigates to protected route
    │
    └─► ProtectedRoute Component
        │
        ├─► Check AuthContext
        │   • Is user authenticated?
        │   • Is token valid?
        │
        ├─► If not authenticated
        │   └─► Redirect to /login
        │
        └─► If authenticated
            │
            └─► API Request with Token
                │
                └─► Backend: Verify Token
                    • Extract token from header
                    • jwt.decode(token, SECRET_KEY)
                    • Verify expiration
                    • Get user from database
                    │
                    └─► Allow request or return 401
```

### Auction Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AUCTION CREATION FLOW                             │
└─────────────────────────────────────────────────────────────────────┘

Seller creates auction
    │
    └─► POST /api/v1/auctions
        Body: {
          analysis_id,
          loan_name,
          auction_type: "english" | "sealed_bid",
          lot_size,
          min_bid,
          bid_increment,
          reserve_price,
          end_time
        }
        │
        ├─► Backend Validation
        │   • Check analysis exists
        │   • Validate auction parameters
        │   • Check user permissions
        │
        ├─► Create Auction Record
        │   • id: UUID
        │   • status: "pending"
        │   • start_time: now
        │   • created_by: user_id
        │
        └─► Create AuditEvent
            • event_type: "auction_created"
            • entity_type: "auction"
            • entity_id: auction.id

┌─────────────────────────────────────────────────────────────────────┐
│                    BIDDING FLOW                                      │
└─────────────────────────────────────────────────────────────────────┘

Buyer places bid
    │
    └─► POST /api/v1/auctions/{id}/bids
        Body: { bid_amount }
        │
        ├─► Backend Validation
        │   • Check auction is active
        │   • Check bid >= min_bid
        │   • Check bid >= current_highest + increment
        │   • Check auction hasn't ended
        │
        ├─► Create Bid Record
        │   • id: UUID
        │   • auction_id: FK
        │   • bidder_id: user_id
        │   • bid_amount: validated
        │   • is_locked: true
        │   • timestamp: now
        │
        ├─► Update Auction
        │   • Set current highest bid
        │
        └─► Create AuditEvent
            • event_type: "bid_placed"
            • entity_type: "bid"
            • entity_id: bid.id

┌─────────────────────────────────────────────────────────────────────┐
│                    AUCTION CLOSURE FLOW                              │
└─────────────────────────────────────────────────────────────────────┘

Seller closes auction
    │
    └─► POST /api/v1/auctions/{id}/close
        │
        ├─► Backend Validation
        │   • Check user is auction creator
        │   • Check auction is active
        │
        ├─► Determine Winner
        │   • Find highest bid
        │   • Check if >= reserve_price
        │
        ├─► Update Auction
        │   • status: "closed"
        │   • winning_bid_id: highest_bid.id
        │
        ├─► Update Winning Bid
        │   • is_winning: true
        │
        └─► Create AuditEvent
            • event_type: "auction_closed"
            • entity_type: "auction"
            • entity_id: auction.id
```

### API Request Flow with Error Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUCCESSFUL REQUEST FLOW                           │
└─────────────────────────────────────────────────────────────────────┘

Frontend API Call
    │
    └─► Axios Request
        │
        ├─► Add Authorization Header (if authenticated)
        │   Header: Authorization: Bearer <token>
        │
        ├─► Send HTTP Request
        │   Method: GET/POST/PUT/DELETE
        │   URL: http://localhost:8000/api/v1/...
        │   Body: JSON (if POST/PUT)
        │
        └─► Backend Processing
            │
            ├─► CORS Middleware
            │   • Check origin
            │   • Add CORS headers
            │
            ├─► JWT Middleware (if protected route)
            │   • Extract token
            │   • Verify token
            │   • Get user
            │
            ├─► Route Handler
            │   • Validate request
            │   • Parse parameters
            │   • Call service
            │
            ├─► Service Layer
            │   • Business logic
            │   • Database operations
            │
            └─► Response
                Status: 200 OK
                Body: { data: {...} }
                │
                └─► Frontend: Update state, show success

┌─────────────────────────────────────────────────────────────────────┐
│                    ERROR HANDLING FLOW                               │
└─────────────────────────────────────────────────────────────────────┘

Request with Error
    │
    └─► Backend Error Occurs
        │
        ├─► Validation Error (400)
        │   └─► Return: { "detail": "Validation error" }
        │       │
        │       └─► Frontend: Show error message
        │
        ├─► Authentication Error (401)
        │   └─► Return: { "detail": "Not authenticated" }
        │       │
        │       └─► Frontend: Redirect to login
        │
        ├─► Not Found Error (404)
        │   └─► Return: { "detail": "Resource not found" }
        │       │
        │       └─► Frontend: Show 404 message
        │
        ├─► Server Error (500)
        │   └─► Return: { "detail": "Internal server error" }
        │       │
        │       └─► Frontend: Show error toast
        │
        └─► Network Error
            └─► Frontend: Show connection error
                • Retry button
                • Check connection status
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
