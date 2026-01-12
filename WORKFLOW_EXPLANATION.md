# CrystalTrade Workflow & Process Explanation

## 📋 Overview

CrystalTrade is a desktop application that automates due diligence for secondary loan market transactions. It processes loan documents, extracts key information using AI, performs automated checks, and provides comprehensive analysis including trade readiness, transfer simulation, and market intelligence.

---

## 🔄 Complete Workflow

### **Phase 1: Document Upload & Initial Processing**

```
User Action → Frontend → Backend → Database
```

1. **User uploads document** (via drag-and-drop or file picker)
   - Supported formats: PDF, Word (.doc, .docx), Excel (.xls, .xlsx)
   - Location: `/upload` page

2. **Frontend sends to backend**
   - `POST /api/v1/documents/upload`
   - File is uploaded with FormData
   - Progress tracking shown to user

3. **Backend processes document**
   - **DocumentProcessor** class:
     - Saves file to `backend/uploads/` directory
     - Classifies document type (credit_agreement, amendment, financial_statement, etc.)
     - Extracts basic metadata
   - Creates **Analysis** record in database with status: `"pending"`

4. **Returns analysis_id** to frontend
   - User sees "Upload successful" message
   - Analysis ID is stored for next step

---

### **Phase 2: AI-Powered Analysis (Background Process)**

```
User clicks "Start Analysis" → Background Task → Multi-Step Processing
```

1. **User triggers analysis**
   - Clicks "Upload and Analyze" button
   - Frontend calls: `POST /api/v1/analyses/{analysis_id}/start`

2. **Backend starts background task**
   - Analysis status changes to `"processing"`
   - Background task runs asynchronously (doesn't block API)

3. **Step-by-step processing pipeline:**

   #### **Step 1: Text Extraction**
   - **DocumentProcessor.extract_text()**
   - Extracts text from document based on file type:
     - **PDF**: Uses `pdfplumber` (preferred) or `PyPDF2` (fallback)
     - **Word**: Uses `python-docx`
     - **Excel**: Uses `openpyxl`
   - Returns full document text

   #### **Step 2: AI Analysis**
   - **AIAnalyzer.analyze_document()**
   - Uses OpenAI GPT-4 to:
     - **Extract key terms**: Interest rate, maturity date, principal amount, transfer restrictions, consent requirements, financial covenants
     - **Identify risks**: Credit, legal, operational risks with severity levels
     - **Find unusual clauses**: Non-standard or problematic language
   - Returns structured JSON with extracted data

   #### **Step 3: Due Diligence Checks**
   - **DueDiligenceEngine.run_checks()**
   - Performs automated compliance checks:
     - Transfer restrictions analysis
     - Consent requirements verification
     - Financial covenants identification
     - Payment obligations review
     - Lien mentions check
     - Regulatory compliance verification
   - Returns list of compliance check results

   #### **Step 4: Risk Scoring**
   - **DueDiligenceEngine.calculate_risk_score()**
   - Calculates risk scores (0-100) for:
     - Credit Risk (40% weight)
     - Legal Risk (35% weight)
     - Operational Risk (25% weight)
   - Combines into overall risk score
   - Returns risk breakdown

   #### **Step 5: Generate Recommendations**
   - **DueDiligenceEngine.generate_recommendations()**
   - Creates actionable recommendations based on:
     - Overall risk score
     - Risk breakdown
     - Compliance failures
   - Returns list of recommendation strings

4. **Save results to database**
   - Analysis status → `"completed"`
   - All extracted data saved to Analysis record:
     - `risk_score`, `risk_breakdown`
     - `compliance_checks`
     - `extracted_terms`
     - `recommendations`

---

### **Phase 3: Viewing Results (Overview Tab)**

```
User navigates to analysis → Frontend fetches data → Displays results
```

1. **User navigates to analysis**
   - From Dashboard: Click "View Details" on any analysis
   - From Upload page: Click "View Analysis" after upload
   - Route: `/analysis/{analysis_id}`

2. **Frontend fetches analysis data**
   - `GET /api/v1/analyses/{analysis_id}`
   - Polls every 3 seconds if status is "processing"

3. **Overview Tab displays:**
   - **Risk Score Component**: Visual radial chart + breakdown bars
   - **Extracted Terms Component**: Key loan terms in organized cards
   - **Compliance Checklist Component**: Pass/Warning/Fail status for each check
   - **Recommendations Section**: List of actionable recommendations

---

### **Phase 4: Loan Markets Features (On-Demand)**

```
User clicks feature tab → Frontend requests feature data → Backend calculates → Returns results
```

When user clicks any Loan Markets tab, the frontend:

1. **Checks if feature is enabled** (via feature flags)
2. **Requests feature data** from backend API
3. **Backend calculates on-demand** (or retrieves cached result)
4. **Displays results** in tab-specific UI

#### **A) Trade Readiness Score**
- **API**: `GET /api/v1/analyses/{id}/trade-readiness`
- **Engine**: `TradeReadinessEngine`
- **Process**:
  1. Assesses 6 categories:
     - Documentation completeness (20% weight)
     - Transferability friction (25% weight)
     - Consent complexity (20% weight)
     - Covenant tightness (15% weight)
     - Non-standard deviations (15% weight)
     - Regulatory flags (5% weight)
  2. Calculates weighted score (0-100)
  3. Assigns label: Green (≥75), Amber (50-74), Red (<50)
  4. Generates evidence links with citations
- **UI**: Large score display + breakdown chart + evidence list

#### **B) Transfer Simulator**
- **API**: `GET /api/v1/analyses/{id}/transfer-simulation`
- **Engine**: `TransferSimulator`
- **Process**:
  1. Simulates two pathways:
     - **Assignment**: Full transfer of loan position
     - **Participation**: Partial interest transfer
  2. For each pathway:
     - Identifies required consents (Agent, Borrower, Lenders)
     - Estimates timeline (base + consent delays + blockers)
     - Lists potential blockers
     - Generates recommended actions
     - Creates text playbook
- **UI**: Side-by-side pathway cards with playbook text

#### **C) LMA Deviations**
- **API**: `GET /api/v1/analyses/{id}/lma-deviations`
- **Engine**: `LMADeviationEngine`
- **Process**:
  1. Compares extracted clauses against LMA baseline templates
  2. Identifies deviations by type:
     - Transfer clauses
     - Covenant clauses
     - Payment clauses
  3. Assigns severity (high/medium/low)
  4. Explains market impact
  5. Generates heatmap by clause type
- **UI**: Deviation list with severity indicators + heatmap

#### **D) Buyer Fit**
- **API**: `GET /api/v1/analyses/{id}/buyer-fit`
- **Engine**: `BuyerFitAnalyzer`
- **Process**:
  1. Analyzes loan against buyer type profiles:
     - **CLO**: Prefers covenant-lite, transferable
     - **Bank**: Prefers strong covenants, standard terms
     - **Distressed Fund**: More flexible, handles defaults
  2. Calculates fit score (0-100) for each buyer type
  3. Lists fit indicators
  4. Generates buyer-specific diligence summary
- **UI**: Grid of buyer type cards with scores and indicators

#### **E) Negotiation Insights**
- **API**: `GET /api/v1/analyses/{id}/negotiation-insights`
- **Engine**: `NegotiationInsightsGenerator`
- **Process**:
  1. Identifies clauses likely to be negotiated:
     - Transfer restrictions
     - Consent requirements
     - Covenants
     - Compliance issues
  2. Assesses negotiation likelihood (high/medium/low)
  3. Generates suggested redlines
  4. Creates questions for Agent/Borrower
- **UI**: List of insights with redlines and questions

#### **F) Post-Trade Monitoring**
- **API**: 
  - `POST /api/v1/analyses/{id}/monitoring/rules` (create rule)
  - `GET /api/v1/analyses/{id}/monitoring/alerts` (get alerts)
- **Engine**: `MonitoringService`
- **Process**:
  1. User creates monitoring rules (covenants, dates, obligations)
  2. System checks rules against current values
  3. Generates alerts when thresholds approached
  4. Displays in-app alerts (no external email)
- **UI**: Alert list with severity indicators

#### **G) Auction Room**
- **API**: 
  - `POST /api/v1/auctions` (create)
  - `POST /api/v1/auctions/{id}/bids` (place bid)
  - `GET /api/v1/auctions/{id}/leaderboard` (view bids)
  - `POST /api/v1/auctions/{id}/close` (close auction)
- **Engine**: `AuctionService`
- **Process**:
  1. Seller creates auction (English or Sealed-bid)
  2. Buyers place bids (validated for increments, timing)
  3. Leaderboard shown (for English auctions)
  4. At close: Winner determined, audit trail created
- **UI**: Auction creation form + bidding interface + leaderboard

---

## 🗄️ Data Flow Architecture

```
┌─────────────┐
│   Frontend  │ (React + TypeScript)
│  (Port 5173)│
└──────┬──────┘
       │ HTTP/REST API
       │
┌──────▼─────────────────────────────────────┐
│         Backend API (FastAPI)              │
│         (Port 8000)                        │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  Document Upload Endpoint            │ │
│  │  → DocumentProcessor                 │ │
│  │  → Creates Analysis (pending)        │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  Start Analysis Endpoint              │ │
│  │  → Background Task                   │ │
│  │    → DocumentProcessor.extract_text()│ │
│  │    → AIAnalyzer.analyze_document()   │ │
│  │    → DueDiligenceEngine.run_checks() │ │
│  │    → Calculate risk scores           │ │
│  │    → Generate recommendations       │ │
│  │    → Update Analysis (completed)     │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ┌──────────────────────────────────────┐ │
│  │  Loan Markets Feature Endpoints       │ │
│  │  → TradeReadinessEngine               │ │
│  │  → TransferSimulator                 │ │
│  │  → LMADeviationEngine                 │ │
│  │  → BuyerFitAnalyzer                  │ │
│  │  → NegotiationInsightsGenerator       │ │
│  │  → MonitoringService                 │ │
│  │  → AuctionService                     │ │
│  └──────────────────────────────────────┘ │
└──────┬─────────────────────────────────────┘
       │
       │ SQLAlchemy ORM
       │
┌──────▼─────────────────────────────────────┐
│         SQLite Database                    │
│         (crystal_trade.db)                 │
│                                            │
│  Tables:                                   │
│  - analyses                                │
│  - documents                                │
│  - reports                                  │
│  - trade_readiness                         │
│  - transfer_simulations                    │
│  - lma_deviations                           │
│  - buyer_fits                               │
│  - negotiation_insights                    │
│  - monitoring_rules                         │
│  - monitoring_alerts                       │
│  - auctions                                 │
│  - bids                                     │
│  - evidence_logs                            │
│  - audit_events                             │
│  - deals                                    │
└────────────────────────────────────────────┘
```

---

## 👤 User Journey

### **Scenario 1: New Document Upload**

1. **Dashboard** → User sees overview of all analyses
2. **Upload Page** → User drags & drops loan document
3. **Upload Progress** → File uploads, analysis starts
4. **Analysis View** → User navigates to see results
5. **Overview Tab** → See risk score, terms, compliance
6. **Loan Markets Tabs** → Explore trade readiness, transfer simulation, etc.
7. **Generate Report** → Create PDF report if needed

### **Scenario 2: View Existing Analysis**

1. **Dashboard** → Click on existing analysis
2. **Analysis View** → Overview tab shows basic analysis
3. **Trade Readiness Tab** → Check if loan is trade-ready
4. **Transfer Simulator Tab** → Understand transfer pathway
5. **Buyer Fit Tab** → Identify suitable buyers
6. **Negotiation Tab** → Prepare for negotiations
7. **Monitoring Tab** → Set up post-trade alerts

### **Scenario 3: Auction Workflow**

1. **Analysis View** → User has completed analysis
2. **Auction Tab** → Create new auction
3. **Configure Auction** → Set lot size, min bid, duration
4. **Auction Active** → Buyers place bids
5. **Leaderboard** → See current bids (English auction)
6. **Close Auction** → Winner determined automatically
7. **Trade Workspace** → Auto-created with due diligence package

---

## 🔧 Technical Details

### **Background Processing**
- Uses FastAPI `BackgroundTasks` for async analysis
- Analysis runs in background, doesn't block API
- Frontend polls for status updates every 3 seconds
- Status progression: `pending` → `processing` → `completed` / `failed`

### **AI Integration**
- Uses OpenAI GPT-4 for document analysis
- Falls back to mock data if API key not available
- Text is chunked (4000 chars) for processing
- Results include confidence scores

### **Evidence & Citations**
- Every AI result includes evidence links
- EvidenceLog system tracks:
  - Document name
  - Page number
  - Section reference
  - Extraction confidence
  - Feature type

### **Feature Flags**
- All Loan Markets features can be toggled
- Environment variables control features
- Allows gradual rollout or A/B testing

### **Offline-First Demo**
- Works without external API dependencies
- Uses local SQLite database
- Cached processing results
- Mock data available for demo

---

## 📊 State Management

### **Frontend State**
- React hooks (`useState`, `useEffect`)
- Local component state
- API calls via `api.ts` service
- No global state management (Redux/Zustand) - simple architecture

### **Backend State**
- SQLite database (SQLAlchemy ORM)
- In-memory caching for feature calculations
- Background task state in database

---

## 🚀 Performance Optimizations

1. **Background Processing**: Analysis doesn't block UI
2. **Lazy Loading**: Loan Markets features load on-demand
3. **Caching**: Feature results cached in database
4. **Polling**: Frontend polls for updates (could be WebSocket in production)
5. **Chunking**: Large documents split for AI processing

---

## 🔐 Security & Audit

- **Audit Trail**: All actions logged in `audit_events` table
- **Bid Locking**: Bids locked after placement
- **Validation**: Auction rules enforced (increments, timing)
- **Evidence Tracking**: All AI results have citations

---

This workflow ensures that CrystalTrade provides comprehensive, explainable, and actionable insights for loan trading decisions while maintaining transparency and auditability throughout the process.

