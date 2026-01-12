# CrystalTrade Demo Script

## Overview
This document provides a step-by-step guide for demonstrating CrystalTrade's Loan Markets features at the LMA Edge Hackathon.

## Prerequisites
1. Application is running (backend on port 8000, frontend on port 5173)
2. Demo data has been seeded
3. Browser open to http://localhost:5173

## Demo Flow

### 1. Dashboard Overview (30 seconds)
- **Navigate to**: Dashboard (home page)
- **Show**: 
  - Total analyses count
  - Risk distribution chart
  - Recent analyses table
- **Say**: "CrystalTrade provides a comprehensive dashboard showing all loan analyses. We can see our portfolio at a glance."

### 2. View Existing Analysis (1 minute)
- **Navigate to**: Click on any analysis in the "Recent Analyses" table
- **Show**: 
  - Overview tab with risk score, extracted terms, compliance checklist
- **Say**: "Each analysis includes AI-powered extraction of key loan terms, risk scoring, and compliance checks."

### 3. Trade Readiness Score (2 minutes)
- **Navigate to**: "Trade Readiness" tab
- **Show**:
  - Overall score (0-100) with Green/Amber/Red label
  - Breakdown by category (documentation, transferability, consent, covenants, deviations, regulatory)
  - Evidence links
- **Say**: "The Trade Readiness Score provides a comprehensive assessment of how ready a loan is for trading. It considers documentation completeness, transferability friction, consent complexity, covenant tightness, and deviations from LMA standards."

### 4. Transfer Simulator (2 minutes)
- **Navigate to**: "Transfer Simulator" tab
- **Show**:
  - Assignment vs Participation pathways
  - Required consents for each pathway
  - Estimated timeline
  - Blockers and recommended actions
  - Playbook text
- **Say**: "The Transfer Simulator helps traders understand the practical steps needed to complete a transfer. It identifies required consents, estimates timelines, and highlights potential blockers."

### 5. LMA Deviations (1.5 minutes)
- **Navigate to**: "LMA Deviations" tab
- **Show**:
  - Deviation count and severity breakdown
  - Individual deviations with market impact
  - Heatmap by clause type
- **Say**: "The LMA Deviation Engine compares loan documents against standard LMA templates, highlighting non-standard language that could impact liquidity or closing timelines."

### 6. Buyer Fit Analysis (1.5 minutes)
- **Navigate to**: "Buyer Fit" tab
- **Show**:
  - Fit scores for CLO, Bank, and Distressed Fund buyers
  - Indicators explaining the fit
  - Buyer-specific diligence summaries
- **Say**: "Buyer Fit uses rule-based heuristics to identify which buyer types are most suitable for a loan. This helps sellers target the right buyers and helps buyers find suitable opportunities."

### 7. Negotiation Insights (1.5 minutes)
- **Navigate to**: "Negotiation" tab
- **Show**:
  - Clauses likely to be negotiated
  - Suggested redlines
  - Questions to ask the Agent/Borrower
- **Say**: "Negotiation Insights identify clauses that are likely to be negotiated and provide suggested redlines and questions to streamline the negotiation process."

### 8. Post-Trade Monitoring (1 minute)
- **Navigate to**: "Monitoring" tab
- **Show**:
  - Active monitoring rules
  - Alerts for approaching thresholds
- **Say**: "Post-Trade Monitoring allows users to set rules on covenants and key dates, with alerts when thresholds are near breach."

### 9. Auction Room (2 minutes) - If time permits
- **Navigate to**: "Auction" tab
- **Show**:
  - Create auction form
  - Place bids
  - View leaderboard
  - Close auction and see winner
- **Say**: "The Auction Room enables sellers to list loan positions for time-boxed auctions. Buyers can place bids, and the system handles both English (ascending) and sealed-bid auction types."

## Key Talking Points

### Value Proposition
- **Speed**: Reduces due diligence time from days to hours
- **Transparency**: Provides explainable, evidence-backed analysis
- **Efficiency**: Automates repetitive checks and calculations
- **Intelligence**: AI-powered extraction and analysis

### Technical Highlights
- **Offline-first**: Works without external API dependencies (for demo)
- **Evidence-based**: Every result includes citations to source documents
- **Modular**: Feature-flagged architecture allows easy enable/disable
- **Extensible**: Clean separation of concerns, easy to add new features

### Use Cases
1. **Sellers**: Quickly assess trade readiness and identify potential buyers
2. **Buyers**: Understand transfer requirements and identify suitable opportunities
3. **Traders**: Simulate transfer pathways and identify blockers early
4. **Compliance**: Automated checks against LMA standards

## Demo Tips

1. **Start with Overview**: Always show the overview tab first to establish context
2. **Use Real Examples**: Reference the seeded demo data to show realistic scenarios
3. **Highlight Evidence**: Point out evidence links and citations to show transparency
4. **Show Breakdowns**: Drill into breakdowns to show explainability
5. **Emphasize Speed**: Mention that all analysis happens automatically in the background

## Troubleshooting

### If features don't load:
- Check browser console for errors
- Verify backend is running on port 8000
- Check that analysis status is "completed"

### If demo data is missing:
- Run: `cd backend && python seed_demo_data.py`
- Refresh the dashboard

### If API errors occur:
- Check feature flags are enabled in `backend/feature_flags.py`
- Verify database is initialized: `cd backend && python init_db.py`

## Next Steps After Demo

1. **Q&A**: Be ready to discuss:
   - Architecture and scalability
   - Integration with existing systems
   - Pricing model
   - Roadmap

2. **Live Demo**: If time permits, upload a new document and show the analysis process

3. **Code Walkthrough**: Be prepared to show:
   - Service architecture
   - Evidence logging system
   - Feature flag implementation

