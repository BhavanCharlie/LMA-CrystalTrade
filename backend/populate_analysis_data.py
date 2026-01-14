#!/usr/bin/env python3
"""
Populate existing analyses with rich mock data for testing
This simulates what would be extracted from real loan documents
"""
from database import get_db, init_db
from models import Analysis, TradeReadiness, TransferSimulation, LMADeviation, BuyerFit, NegotiationInsight
from datetime import datetime, timedelta
import json
import random

def populate_analysis_data():
    """Populate existing analyses with comprehensive test data"""
    print("Populating analyses with rich test data...")
    
    init_db()
    db = next(get_db())
    
    analyses = db.query(Analysis).filter(Analysis.status == "completed").all()
    
    if not analyses:
        print("No completed analyses found. Please upload and analyze documents first.")
        return
    
    print(f"Found {len(analyses)} analyses to populate\n")
    
    # Different scenarios for different documents
    scenarios = [
        {
            "name": "Standard Term Loan",
            "risk_score": 35,
            "risk_breakdown": {"credit_risk": 30, "legal_risk": 25, "operational_risk": 50},
            "extracted_terms": {
                "interest_rate": "LIBOR + 3.50%",
                "maturity_date": "2028-12-31",
                "principal_amount": "$50,000,000",
                "transfer_restrictions": "Assignment permitted with Agent consent",
                "consent_requirements": ["Agent"],
                "financial_covenants": [
                    {"name": "Leverage Ratio", "requirement": "Max 4.5x", "current_value": "3.8x"},
                    {"name": "Interest Coverage", "requirement": "Min 2.0x", "current_value": "2.5x"},
                ],
            },
            "trade_readiness": 82,
            "lma_deviations_count": 2,
            "buyer_fit": {"clo": 85, "bank": 70, "distressed": 40},
        },
        {
            "name": "Restricted Revolver",
            "risk_score": 55,
            "risk_breakdown": {"credit_risk": 60, "legal_risk": 40, "operational_risk": 65},
            "extracted_terms": {
                "interest_rate": "LIBOR + 4.25%",
                "maturity_date": "2026-06-30",
                "principal_amount": "$25,000,000",
                "transfer_restrictions": "Assignment restricted, participation permitted",
                "consent_requirements": ["Agent", "Borrower"],
                "financial_covenants": [
                    {"name": "Leverage Ratio", "requirement": "Max 5.0x", "current_value": "4.8x"},
                ],
            },
            "trade_readiness": 65,
            "lma_deviations_count": 4,
            "buyer_fit": {"clo": 60, "bank": 80, "distressed": 55},
        },
        {
            "name": "High Risk Secured Loan",
            "risk_score": 70,
            "risk_breakdown": {"credit_risk": 75, "legal_risk": 65, "operational_risk": 70},
            "extracted_terms": {
                "interest_rate": "LIBOR + 5.00%",
                "maturity_date": "2029-03-31",
                "principal_amount": "$75,000,000",
                "transfer_restrictions": "Transfer prohibited without majority lender consent",
                "consent_requirements": ["Agent", "Borrower", "Majority Lenders"],
                "financial_covenants": [
                    {"name": "Leverage Ratio", "requirement": "Max 4.0x", "current_value": "3.9x"},
                    {"name": "Interest Coverage", "requirement": "Min 2.5x", "current_value": "2.6x"},
                    {"name": "Debt Service Coverage", "requirement": "Min 1.25x", "current_value": "1.30x"},
                ],
            },
            "trade_readiness": 45,
            "lma_deviations_count": 6,
            "buyer_fit": {"clo": 35, "bank": 45, "distressed": 85},
        },
    ]
    
    for i, analysis in enumerate(analyses):
        scenario = scenarios[i % len(scenarios)]
        
        print(f"Populating: {analysis.loan_name}")
        
        # Update analysis with rich data
        analysis.risk_score = scenario["risk_score"]
        analysis.risk_breakdown = scenario["risk_breakdown"]
        analysis.extracted_terms = scenario["extracted_terms"]
        analysis.compliance_checks = [
            {
                "category": "Transfer Restrictions",
                "status": "pass" if "permitted" in scenario["extracted_terms"]["transfer_restrictions"].lower() else "warning",
                "description": scenario["extracted_terms"]["transfer_restrictions"],
                "details": "Standard provision" if "permitted" in scenario["extracted_terms"]["transfer_restrictions"].lower() else "May delay transfer",
            },
            {
                "category": "Consent Requirements",
                "status": "pass" if len(scenario["extracted_terms"]["consent_requirements"]) == 1 else "warning",
                "description": f"Consent required from: {', '.join(scenario['extracted_terms']['consent_requirements'])}",
                "details": "Standard" if len(scenario["extracted_terms"]["consent_requirements"]) == 1 else "Multiple consents may delay",
            },
            {
                "category": "Financial Covenants",
                "status": "pass",
                "description": f"{len(scenario['extracted_terms']['financial_covenants'])} financial covenants identified",
                "details": "Covenants require ongoing monitoring",
            },
            {
                "category": "Payment Obligations",
                "status": "pass",
                "description": "Payment terms identified",
                "details": "Monthly interest payments, quarterly principal",
            },
            {
                "category": "Lien Verification",
                "status": "warning",
                "description": "Security interests mentioned",
                "details": "Requires external verification",
            },
            {
                "category": "Regulatory Compliance",
                "status": "pass",
                "description": "KYC/AML provisions identified",
                "details": "Standard compliance requirements",
            },
        ]
        analysis.recommendations = [
            "Standard due diligence procedures recommended",
            "Monitor covenant compliance",
            "Verify payment history with borrower records",
        ] if scenario["risk_score"] < 50 else [
            "High risk detected. Recommend thorough review by legal and credit teams.",
            "Significant transfer restrictions may limit liquidity",
            "Multiple consent requirements may delay transfer process",
        ]
        
        # Create Trade Readiness
        existing_tr = db.query(TradeReadiness).filter(TradeReadiness.analysis_id == analysis.id).first()
        if not existing_tr:
            score = scenario["trade_readiness"]
            label = "Green" if score >= 75 else "Amber" if score >= 50 else "Red"
            trade_readiness = TradeReadiness(
                id=f"tr-{analysis.id}",
                analysis_id=analysis.id,
                score=score,
                label=label,
                breakdown={
                    "documentation": 85,
                    "transferability": score - 10,
                    "consent_complexity": 100 - (len(scenario["extracted_terms"]["consent_requirements"]) * 15),
                    "covenant_tightness": 70,
                    "lma_deviation": 100 - (scenario["lma_deviations_count"] * 10),
                    "regulatory_compliance": 90,
                },
                confidence=0.85,
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
                required_consents=scenario["extracted_terms"]["consent_requirements"],
                estimated_timeline_days=7 if len(scenario["extracted_terms"]["consent_requirements"]) == 1 else 14,
                blockers=[] if len(scenario["extracted_terms"]["consent_requirements"]) == 1 else ["Multiple consent requirements"],
                recommended_actions=["Obtain Agent consent", "Prepare transfer documentation"],
                playbook="Standard assignment process. Obtain required consents, prepare documentation, execute transfer.",
            )
            db.add(transfer_sim)
        
        # Create LMA Deviations
        existing_deviations = db.query(LMADeviation).filter(LMADeviation.analysis_id == analysis.id).all()
        if not existing_deviations:
            deviation_types = [
                {"description": "Non-standard interest rate calculation", "severity": "medium"},
                {"description": "Unusual transfer restriction language", "severity": "low"},
                {"description": "Additional consent requirement beyond standard", "severity": "high"},
                {"description": "Modified covenant structure", "severity": "medium"},
                {"description": "Custom payment terms", "severity": "low"},
                {"description": "Non-standard security provisions", "severity": "high"},
            ]
            
            for j in range(scenario["lma_deviations_count"]):
                dev = deviation_types[j % len(deviation_types)]
                lma_dev = LMADeviation(
                    id=f"lma-{analysis.id}-{j}",
                    analysis_id=analysis.id,
                    document_id=analysis.id,
                    clause_text=dev["description"],
                    clause_type="transfer" if "transfer" in dev["description"].lower() else "covenant",
                    deviation_severity=dev["severity"],
                    market_impact="May affect marketability" if dev["severity"] == "high" else "Minor impact",
                    baseline_template="Standard LMA template clause",
                )
                db.add(lma_dev)
        
        # Create Buyer Fit
        existing_bf = db.query(BuyerFit).filter(BuyerFit.analysis_id == analysis.id).all()
        if not existing_bf:
            buyer_types = ["CLO", "Bank", "DistressedFund"]
            buyer_map = {"CLO": "clo", "Bank": "bank", "DistressedFund": "distressed"}
            for buyer_type in buyer_types:
                fit_score = scenario["buyer_fit"][buyer_map[buyer_type]]
                buyer_fit = BuyerFit(
                    id=f"bf-{analysis.id}-{buyer_type.lower()}",
                    analysis_id=analysis.id,
                    buyer_type=buyer_type,
                    fit_score=fit_score,
                    indicators=["Standard terms", "Good credit profile"] if fit_score > 70 else ["Restricted transfer", "Tight covenants"],
                    reasoning="Good fit based on credit profile and transferability" if fit_score > 70 else "Limited fit due to restrictions",
                    diligence_summary=f"Loan characteristics align with {buyer_type} investment criteria" if fit_score > 60 else f"Loan may not meet {buyer_type} requirements",
                )
                db.add(buyer_fit)
        
        # Create Negotiation Insights
        existing_ni = db.query(NegotiationInsight).filter(NegotiationInsight.analysis_id == analysis.id).all()
        if not existing_ni:
            insights = [
                {"clause": "Interest Rate", "text": "Interest rate is above market", "likelihood": "high", "redlines": ["Negotiate rate reduction to LIBOR + 3.0%"], "questions": ["What is current market rate?"], "risk": "High credit risk if rate not adjusted"},
                {"clause": "Transfer Restrictions", "text": "Transfer restrictions are standard", "likelihood": "low", "redlines": ["Accept as-is"], "questions": [], "risk": "No significant risk"},
                {"clause": "Covenants", "text": "Covenant thresholds are tight", "likelihood": "medium", "redlines": ["Request covenant relief"], "questions": ["Can covenants be relaxed?"], "risk": "Medium operational risk"},
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
        
        print(f"  ✓ Populated with scenario: {scenario['name']}")
        print(f"    Risk Score: {scenario['risk_score']}")
        print(f"    Trade Readiness: {scenario['trade_readiness']}")
        print(f"    LMA Deviations: {scenario['lma_deviations_count']}")
        print()
    
    db.commit()
    print(f"✅ Successfully populated {len(analyses)} analyses with comprehensive test data!")
    print("\n📊 All features should now be visible:")
    print("  ✓ Rich extracted terms")
    print("  ✓ Trade Readiness scores")
    print("  ✓ Transfer Simulations")
    print("  ✓ LMA Deviations")
    print("  ✓ Buyer Fit analysis")
    print("  ✓ Negotiation Insights")


if __name__ == "__main__":
    populate_analysis_data()
