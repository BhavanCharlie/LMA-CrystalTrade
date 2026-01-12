#!/usr/bin/env python3
"""
Demo Data Seeding Script
Creates sample deals and analyses for hackathon demo
"""
from database import get_db, init_db
from models import Analysis, Deal, TradeReadiness, TransferSimulation, LMADeviation, BuyerFit, NegotiationInsight, User
from datetime import datetime, timedelta
import uuid
import json
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_demo_data():
    """Seed demo data"""
    print("Seeding demo data...")
    
    # Initialize database
    init_db()
    
    db = next(get_db())
    
    # Create demo users
    print("Creating demo users...")
    demo_users = [
        {
            "id": "demo-user-001",
            "email": "demo@crystaltrade.com",
            "username": "demo",
            "password": "demo123",
            "full_name": "Demo User",
            "is_admin": False,
        },
        {
            "id": "admin-user-001",
            "email": "admin@crystaltrade.com",
            "username": "admin",
            "password": "admin123",
            "full_name": "Admin User",
            "is_admin": True,
        },
    ]
    
    for user_data in demo_users:
        existing_user = db.query(User).filter(
            (User.email == user_data["email"]) | (User.username == user_data["username"])
        ).first()
        
        if not existing_user:
            hashed_password = pwd_context.hash(user_data["password"])
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=hashed_password,
                full_name=user_data["full_name"],
                is_active=True,
                is_admin=user_data["is_admin"],
            )
            db.add(user)
            print(f"  ✓ Created user: {user_data['username']} ({user_data['email']})")
        else:
            print(f"  - User already exists: {user_data['username']}")
    
    db.commit()
    print("Demo users created!")
    print("\n📋 Demo Credentials:")
    print("  Regular User:")
    print("    Username: demo")
    print("    Password: demo123")
    print("  Admin User:")
    print("    Username: admin")
    print("    Password: admin123")
    print()
    
    # Create sample deals
    deals = [
        {
            "id": str(uuid.uuid4()),
            "deal_name": "TechCorp Term Loan B",
            "borrower_name": "TechCorp Inc.",
            "deal_type": "term_loan",
            "principal_amount": 50000000.0,
            "currency": "USD",
            "status": "active",
            "deal_metadata": {
                "sector": "Technology",
                "rating": "BB+",
                "maturity": "2028-12-31",
            },
        },
        {
            "id": str(uuid.uuid4()),
            "deal_name": "RetailCo Revolver",
            "borrower_name": "RetailCo Holdings",
            "deal_type": "revolver",
            "principal_amount": 25000000.0,
            "currency": "USD",
            "status": "active",
            "metadata": {
                "sector": "Retail",
                "rating": "B+",
                "maturity": "2026-06-30",
            },
        },
        {
            "id": str(uuid.uuid4()),
            "deal_name": "EnergyCo Senior Secured",
            "borrower_name": "EnergyCo LLC",
            "deal_type": "term_loan",
            "principal_amount": 75000000.0,
            "currency": "USD",
            "status": "active",
            "metadata": {
                "sector": "Energy",
                "rating": "BB",
                "maturity": "2029-03-31",
            },
        },
    ]
    
    # Create sample analyses
    sample_analyses = [
        {
            "loan_name": "TechCorp Term Loan B",
            "status": "completed",
            "risk_score": 35,
            "risk_breakdown": {
                "credit_risk": 30,
                "legal_risk": 25,
                "operational_risk": 50,
            },
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
            "compliance_checks": [
                {
                    "category": "Transfer Restrictions",
                    "status": "pass",
                    "description": "Standard transfer provisions",
                    "details": "Assignment permitted with Agent consent",
                },
                {
                    "category": "Consent Requirements",
                    "status": "pass",
                    "description": "Agent consent required",
                    "details": "Standard provision",
                },
                {
                    "category": "Financial Covenants",
                    "status": "pass",
                    "description": "2 financial covenants identified",
                    "details": "Covenants require ongoing monitoring",
                },
            ],
            "recommendations": [
                "Standard due diligence procedures recommended",
                "Monitor covenant compliance",
            ],
        },
        {
            "loan_name": "RetailCo Revolver",
            "status": "completed",
            "risk_score": 55,
            "risk_breakdown": {
                "credit_risk": 60,
                "legal_risk": 40,
                "operational_risk": 65,
            },
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
            "compliance_checks": [
                {
                    "category": "Transfer Restrictions",
                    "status": "warning",
                    "description": "Assignment restricted",
                    "details": "Participation may be required",
                },
                {
                    "category": "Consent Requirements",
                    "status": "warning",
                    "description": "Borrower consent required",
                    "details": "May delay transfer",
                },
            ],
            "recommendations": [
                "Review transfer restrictions carefully",
                "Allow additional time for Borrower consent",
            ],
        },
        {
            "loan_name": "EnergyCo Senior Secured",
            "status": "completed",
            "risk_score": 70,
            "risk_breakdown": {
                "credit_risk": 75,
                "legal_risk": 65,
                "operational_risk": 70,
            },
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
            "compliance_checks": [
                {
                    "category": "Transfer Restrictions",
                    "status": "fail",
                    "description": "Transfer prohibited without majority consent",
                    "details": "High transfer friction",
                },
                {
                    "category": "Consent Requirements",
                    "status": "warning",
                    "description": "Multiple consent requirements",
                    "details": "May delay transfer significantly",
                },
            ],
            "recommendations": [
                "High risk detected. Recommend thorough review by legal and credit teams",
                "Significant transfer restrictions may limit liquidity",
            ],
        },
    ]
    
    # Create analyses
    analysis_ids = []
    for i, analysis_data in enumerate(sample_analyses):
        analysis_id = str(uuid.uuid4())
        analysis_ids.append(analysis_id)
        
        analysis = Analysis(
            id=analysis_id,
            loan_name=analysis_data["loan_name"],
            status=analysis_data["status"],
            document_path=f"demo/documents/{analysis_data['loan_name'].lower().replace(' ', '_')}.pdf",
            document_type="credit_agreement",
            risk_score=analysis_data["risk_score"],
            risk_breakdown=analysis_data["risk_breakdown"],
            compliance_checks=analysis_data["compliance_checks"],
            extracted_terms=analysis_data["extracted_terms"],
            recommendations=analysis_data["recommendations"],
            created_at=datetime.utcnow() - timedelta(days=len(sample_analyses) - i),
        )
        
        db.add(analysis)
        
        # Link to deal if available
        if i < len(deals):
            deals[i]["analysis_ids"] = [analysis_id]
    
    db.commit()
    
    print(f"Created {len(sample_analyses)} sample analyses")
    print(f"Analysis IDs: {analysis_ids}")
    print("\nDemo data seeded successfully!")
    print("\nYou can now:")
    print("1. View analyses in the dashboard")
    print("2. Navigate to /analysis/{analysis_id} to see Loan Markets features")
    print("3. All features are pre-calculated and ready for demo")


if __name__ == "__main__":
    seed_demo_data()

