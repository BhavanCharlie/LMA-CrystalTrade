#!/usr/bin/env python3
"""
Populate Apple credit agreement analysis with rich test data
"""
from database import get_db, init_db
from models import Analysis, TradeReadiness, TransferSimulation, LMADeviation, BuyerFit, NegotiationInsight
from datetime import datetime
import json

def populate_apple_analysis():
    """Populate Apple analysis with comprehensive test data"""
    print("Populating Apple credit agreement analysis...")
    
    init_db()
    db = next(get_db())
    
    # Find Apple analyses
    apple_analyses = db.query(Analysis).filter(Analysis.loan_name.like('%Apple%')).all()
    
    if not apple_analyses:
        print("No Apple analyses found. Please upload the document first.")
        return
    
    print(f"Found {len(apple_analyses)} Apple analysis(es)\n")
    
    # Rich Apple credit agreement scenario
    scenario = {
        "risk_score": 25,  # Very low risk - Apple is highly creditworthy
        "risk_breakdown": {"credit_risk": 15, "legal_risk": 20, "operational_risk": 30},
        "extracted_terms": {
            "interest_rate": "SOFR + 0.50%",
            "maturity_date": "2029-09-28",
            "principal_amount": "$6,000,000,000",
            "transfer_restrictions": "Assignment permitted with Administrative Agent consent (standard)",
            "consent_requirements": ["Administrative Agent"],
            "financial_covenants": [
                {"name": "Leverage Ratio", "requirement": "Not to exceed 3.5x", "current_value": "1.2x"},
                {"name": "Interest Coverage", "requirement": "Not less than 3.0x", "current_value": "45.8x"},
            ],
        },
        "trade_readiness": 92,
        "lma_deviations_count": 1,
        "buyer_fit": {"clo": 95, "bank": 90, "distressed": 20},
    }
    
    for analysis in apple_analyses:
        print(f"Populating: {analysis.loan_name}")
        
        # Update analysis
        analysis.risk_score = scenario["risk_score"]
        analysis.risk_breakdown = scenario["risk_breakdown"]
        analysis.extracted_terms = scenario["extracted_terms"]
        analysis.compliance_checks = [
            {
                "category": "Transfer Restrictions",
                "status": "pass",
                "description": "Standard assignment provisions",
                "details": "Assignment permitted with Administrative Agent consent - standard LMA terms",
            },
            {
                "category": "Consent Requirements",
                "status": "pass",
                "description": "Only Administrative Agent consent required",
                "details": "Minimal consent complexity - standard for investment grade facilities",
            },
            {
                "category": "Financial Covenants",
                "status": "pass",
                "description": "2 financial covenants - both well within limits",
                "details": "Apple's strong credit profile exceeds all covenant requirements",
            },
            {
                "category": "Payment Obligations",
                "status": "pass",
                "description": "Standard payment terms",
                "details": "Quarterly interest payments, bullet maturity",
            },
            {
                "category": "Lien Verification",
                "status": "pass",
                "description": "Unsecured facility",
                "details": "No liens or security interests",
            },
            {
                "category": "Regulatory Compliance",
                "status": "pass",
                "description": "Full compliance with regulatory requirements",
                "details": "Standard KYC/AML provisions, no regulatory flags",
            },
        ]
        analysis.recommendations = [
            "Excellent credit quality - minimal due diligence required",
            "Standard LMA terms - no unusual provisions",
            "Highly liquid and tradeable facility",
            "Ideal for CLO and bank buyers",
        ]
        
        # Create Trade Readiness
        existing_tr = db.query(TradeReadiness).filter(TradeReadiness.analysis_id == analysis.id).first()
        if not existing_tr:
            trade_readiness = TradeReadiness(
                id=f"tr-{analysis.id}",
                analysis_id=analysis.id,
                score=scenario["trade_readiness"],
                label="Green",
                breakdown={
                    "documentation": 95,
                    "transferability": 95,
                    "consent_complexity": 100,
                    "covenant_tightness": 85,
                    "lma_deviation": 95,
                    "regulatory_compliance": 100,
                },
                confidence=0.95,
                evidence_links=[],
            )
            db.add(trade_readiness)
        
        # Create Transfer Simulation
        existing_ts = db.query(TransferSimulation).filter(TransferSimulation.analysis_id == analysis.id).first()
        if not existing_ts:
            transfer_sim = TransferSimulation(
                id=f"ts-{analysis.id}",
                analysis_id=analysis.id,
                pathway_type="assignment",
                required_consents=["Administrative Agent"],
                estimated_timeline_days=3,
                blockers=[],
                recommended_actions=["Obtain Administrative Agent consent", "Prepare standard transfer documentation"],
                playbook="Standard assignment process. Obtain Administrative Agent consent (typically same-day), prepare transfer documentation, execute assignment. Minimal friction due to standard terms and strong credit quality.",
            )
            db.add(transfer_sim)
        
        # Create LMA Deviations (minimal for Apple - very standard)
        existing_deviations = db.query(LMADeviation).filter(LMADeviation.analysis_id == analysis.id).all()
        if not existing_deviations:
            lma_dev = LMADeviation(
                id=f"lma-{analysis.id}-0",
                analysis_id=analysis.id,
                document_id=analysis.id,
                clause_text="Minor variation in interest rate calculation methodology",
                clause_type="payment",
                deviation_severity="low",
                market_impact="Negligible - standard market practice",
                baseline_template="Standard LMA interest rate calculation",
            )
            db.add(lma_dev)
        
        # Create Buyer Fit
        existing_bf = db.query(BuyerFit).filter(BuyerFit.analysis_id == analysis.id).all()
        if not existing_bf:
            buyer_types = ["CLO", "Bank", "DistressedFund"]
            buyer_scores = [scenario["buyer_fit"]["clo"], scenario["buyer_fit"]["bank"], scenario["buyer_fit"]["distressed"]]
            for buyer_type, fit_score in zip(buyer_types, buyer_scores):
                buyer_fit = BuyerFit(
                    id=f"bf-{analysis.id}-{buyer_type.lower()}",
                    analysis_id=analysis.id,
                    buyer_type=buyer_type,
                    fit_score=fit_score,
                    indicators=["Investment grade credit", "Standard terms", "High liquidity"] if fit_score > 80 else ["Not suitable for distressed strategies"],
                    reasoning="Excellent fit for institutional buyers due to strong credit quality and standard terms" if fit_score > 80 else "Not aligned with distressed debt investment strategy",
                    diligence_summary=f"Perfect fit for {buyer_type} buyers - strong credit profile, standard terms, high liquidity" if fit_score > 80 else f"Not suitable for {buyer_type} investment criteria",
                )
                db.add(buyer_fit)
        
        # Create Negotiation Insights
        existing_ni = db.query(NegotiationInsight).filter(NegotiationInsight.analysis_id == analysis.id).all()
        if not existing_ni:
            insights = [
                {
                    "clause": "Interest Rate",
                    "text": "Interest rate is at market - SOFR + 0.50%",
                    "likelihood": "low",
                    "redlines": ["Accept as-is"],
                    "questions": [],
                    "risk": "No negotiation expected - market rate",
                },
                {
                    "clause": "Transfer Provisions",
                    "text": "Standard transfer provisions",
                    "likelihood": "low",
                    "redlines": ["Accept as-is"],
                    "questions": [],
                    "risk": "No negotiation expected",
                },
            ]
            for j, insight in enumerate(insights):
                ni = NegotiationInsight(
                    id=f"ni-{analysis.id}-{j}",
                    analysis_id=analysis.id,
                    clause_reference=f"Section {j+1}.{j+2}",
                    clause_text=insight["text"],
                    negotiation_likelihood=insight["likelihood"],
                    suggested_redlines=insight["redlines"],
                    questions_for_agent=insight["questions"],
                    risk_basis=insight["risk"],
                )
                db.add(ni)
        
        print(f"  ✓ Populated with Apple credit agreement scenario")
        print(f"    Risk Score: {scenario['risk_score']} (Very Low - Investment Grade)")
        print(f"    Principal: {scenario['extracted_terms']['principal_amount']}")
        print(f"    Trade Readiness: {scenario['trade_readiness']} (Excellent)")
        print()
    
    db.commit()
    print(f"✅ Successfully populated {len(apple_analyses)} Apple analysis(es) with comprehensive data!")
    print("\n📊 Apple Credit Agreement Features:")
    print("  ✓ Investment grade credit quality")
    print("  ✓ Standard LMA terms")
    print("  ✓ Excellent trade readiness")
    print("  ✓ High CLO and Bank fit scores")
    print("  ✓ Minimal LMA deviations")


if __name__ == "__main__":
    populate_apple_analysis()
