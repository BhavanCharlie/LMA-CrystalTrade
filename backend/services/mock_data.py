"""
Mock data generator for testing and demo purposes
"""
from models import Analysis
from datetime import datetime, timedelta
import random


def create_mock_analysis(loan_name: str = "Sample Loan Agreement") -> dict:
    """Create mock analysis data for testing"""
    risk_score = random.randint(20, 85)
    
    return {
        "id": f"analysis_{random.randint(1000, 9999)}",
        "loan_name": loan_name,
        "status": "completed",
        "risk_score": risk_score,
        "risk_breakdown": {
            "credit_risk": random.randint(10, 80),
            "legal_risk": random.randint(10, 80),
            "operational_risk": random.randint(10, 80),
        },
        "compliance_checks": [
            {
                "category": "Transfer Restrictions",
                "status": random.choice(["pass", "warning", "fail"]),
                "description": "Standard transfer provisions identified",
                "details": "No significant restrictions found",
            },
            {
                "category": "Consent Requirements",
                "status": random.choice(["pass", "warning"]),
                "description": "Consent required from lender",
                "details": "Standard consent provisions",
            },
            {
                "category": "Financial Covenants",
                "status": "pass",
                "description": "3 financial covenants identified",
                "details": "Debt-to-equity ratio, interest coverage, minimum liquidity",
            },
            {
                "category": "Payment Obligations",
                "status": "pass",
                "description": "Payment terms identified",
                "details": "Monthly interest payments, quarterly principal",
            },
            {
                "category": "Lien Verification",
                "status": random.choice(["pass", "warning"]),
                "description": "No explicit lien mentions",
                "details": "Requires external verification",
            },
            {
                "category": "Regulatory Compliance",
                "status": "pass",
                "description": "KYC/AML provisions identified",
                "details": "Standard compliance requirements",
            },
        ],
        "extracted_terms": {
            "interest_rate": f"{random.uniform(2.5, 8.5):.2f}%",
            "maturity_date": (datetime.now() + timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d"),
            "principal_amount": f"${random.randint(1, 100)}M",
            "transfer_restrictions": "Standard assignment provisions apply",
            "consent_requirements": ["Lender", "Administrative Agent"],
            "financial_covenants": [
                {
                    "name": "Debt-to-Equity Ratio",
                    "requirement": "Not to exceed 3.0:1.0",
                    "current_value": f"{random.uniform(1.5, 2.8):.2f}:1.0",
                },
                {
                    "name": "Interest Coverage Ratio",
                    "requirement": "Not less than 2.5:1.0",
                    "current_value": f"{random.uniform(2.6, 4.0):.2f}:1.0",
                },
            ],
        },
        "recommendations": [
            "Standard due diligence procedures recommended",
            "Verify payment history with borrower records",
            "Confirm lien status with registry",
        ] if risk_score < 50 else [
            "High risk detected. Recommend thorough review by legal and credit teams.",
            "Elevated credit risk identified. Consider additional credit analysis.",
            "Significant legal risks present. Recommend legal counsel review.",
        ],
        "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
        "updated_at": datetime.now().isoformat(),
    }


