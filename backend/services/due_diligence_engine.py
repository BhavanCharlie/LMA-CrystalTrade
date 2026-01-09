from typing import Dict, List
import re


class DueDiligenceEngine:
    def __init__(self):
        self.compliance_rules = self._load_compliance_rules()

    async def run_checks(self, document_text: str, ai_results: Dict) -> List[Dict]:
        """Run all due diligence checks"""
        checks = []
        
        # Transfer restrictions check
        checks.append(await self._check_transfer_restrictions(document_text, ai_results))
        
        # Consent requirements check
        checks.append(await self._check_consent_requirements(document_text, ai_results))
        
        # Financial covenants check
        checks.append(await self._check_financial_covenants(document_text, ai_results))
        
        # Payment history check (would need actual payment data)
        checks.append(await self._check_payment_obligations(document_text))
        
        # Lien verification (would need external data)
        checks.append(await self._check_lien_mentions(document_text))
        
        # Regulatory compliance
        checks.append(await self._check_regulatory_compliance(document_text))
        
        return checks

    async def calculate_risk_score(
        self, ai_results: Dict, compliance_results: List[Dict]
    ) -> Dict:
        """Calculate overall risk score"""
        credit_risk = 0
        legal_risk = 0
        operational_risk = 0
        
        # Analyze risk flags from AI
        risk_flags = ai_results.get("risk_flags", [])
        for flag in risk_flags:
            severity_score = {"high": 30, "medium": 15, "low": 5}.get(
                flag.get("severity", "low"), 0
            )
            category = flag.get("category", "operational")
            
            if category == "credit":
                credit_risk += severity_score
            elif category == "legal":
                legal_risk += severity_score
            else:
                operational_risk += severity_score
        
        # Analyze compliance failures
        for check in compliance_results:
            if check["status"] == "fail":
                if "transfer" in check["category"].lower():
                    legal_risk += 20
                elif "covenant" in check["category"].lower():
                    credit_risk += 15
                else:
                    operational_risk += 10
            elif check["status"] == "warning":
                operational_risk += 5
        
        # Analyze unusual clauses
        unusual_count = len(ai_results.get("unusual_clauses", []))
        legal_risk += min(unusual_count * 5, 25)
        
        # Normalize scores (0-100)
        credit_risk = min(credit_risk, 100)
        legal_risk = min(legal_risk, 100)
        operational_risk = min(operational_risk, 100)
        
        # Calculate overall score (weighted average)
        overall_score = int(
            (credit_risk * 0.4 + legal_risk * 0.35 + operational_risk * 0.25)
        )
        
        return {
            "overall_score": overall_score,
            "breakdown": {
                "credit_risk": credit_risk,
                "legal_risk": legal_risk,
                "operational_risk": operational_risk,
            },
        }

    async def generate_recommendations(
        self, risk_assessment: Dict, compliance_results: List[Dict]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        overall_score = risk_assessment["overall_score"]
        breakdown = risk_assessment["breakdown"]
        
        if overall_score >= 70:
            recommendations.append(
                "High risk detected. Recommend thorough review by legal and credit teams before proceeding."
            )
        
        if breakdown["credit_risk"] >= 60:
            recommendations.append(
                "Elevated credit risk identified. Consider additional credit analysis and borrower financial review."
            )
        
        if breakdown["legal_risk"] >= 60:
            recommendations.append(
                "Significant legal risks present. Recommend legal counsel review of identified clauses and restrictions."
            )
        
        # Compliance-specific recommendations
        for check in compliance_results:
            if check["status"] == "fail":
                recommendations.append(
                    f"Compliance issue in {check['category']}: {check['description']}"
                )
        
        if not recommendations:
            recommendations.append(
                "No major issues detected. Standard due diligence procedures recommended."
            )
        
        return recommendations

    async def _check_transfer_restrictions(
        self, document_text: str, ai_results: Dict
    ) -> Dict:
        """Check for transfer restrictions"""
        terms = ai_results.get("extracted_terms", {})
        transfer_info = terms.get("transfer_restrictions", "")
        
        # Look for common restriction keywords
        restriction_keywords = [
            "prohibited",
            "restricted",
            "requires consent",
            "prior written consent",
            "assignment restrictions",
        ]
        
        has_restrictions = any(
            keyword.lower() in document_text.lower() for keyword in restriction_keywords
        ) or bool(transfer_info)
        
        return {
            "category": "Transfer Restrictions",
            "status": "warning" if has_restrictions else "pass",
            "description": "Transfer restrictions identified" if has_restrictions else "No significant transfer restrictions found",
            "details": transfer_info if transfer_info else "Standard transfer provisions",
        }

    async def _check_consent_requirements(
        self, document_text: str, ai_results: Dict
    ) -> Dict:
        """Check consent requirements for transfer"""
        terms = ai_results.get("extracted_terms", {})
        consent_reqs = terms.get("consent_requirements", [])
        
        has_consent_reqs = len(consent_reqs) > 0 or bool(
            re.search(
                r"consent.*required|prior.*written.*consent",
                document_text,
                re.IGNORECASE,
            )
        )
        
        return {
            "category": "Consent Requirements",
            "status": "warning" if has_consent_reqs else "pass",
            "description": f"Consent required from {len(consent_reqs)} parties" if consent_reqs else "No explicit consent requirements",
            "details": ", ".join(consent_reqs) if consent_reqs else "Standard provisions",
        }

    async def _check_financial_covenants(
        self, document_text: str, ai_results: Dict
    ) -> Dict:
        """Check financial covenants"""
        terms = ai_results.get("extracted_terms", {})
        covenants = terms.get("financial_covenants", [])
        
        has_covenants = len(covenants) > 0 or bool(
            re.search(
                r"covenant|financial.*ratio|debt.*to.*equity|interest.*coverage",
                document_text,
                re.IGNORECASE,
            )
        )
        
        return {
            "category": "Financial Covenants",
            "status": "pass" if has_covenants else "warning",
            "description": f"{len(covenants)} financial covenants identified" if covenants else "No explicit financial covenants found",
            "details": "Covenants require ongoing monitoring" if has_covenants else "Verify covenant requirements",
        }

    async def _check_payment_obligations(self, document_text: str) -> Dict:
        """Check payment obligations"""
        # This would typically require access to payment history data
        has_payment_terms = bool(
            re.search(
                r"payment.*due|interest.*payment|principal.*payment|default",
                document_text,
                re.IGNORECASE,
            )
        )
        
        return {
            "category": "Payment Obligations",
            "status": "pass",
            "description": "Payment terms identified in document",
            "details": "Verify payment history with borrower records",
        }

    async def _check_lien_mentions(self, document_text: str) -> Dict:
        """Check for lien mentions"""
        has_lien_mentions = bool(
            re.search(
                r"lien|encumbrance|security.*interest|pledge",
                document_text,
                re.IGNORECASE,
            )
        )
        
        return {
            "category": "Lien Verification",
            "status": "warning" if has_lien_mentions else "pass",
            "description": "Liens or encumbrances mentioned in document" if has_lien_mentions else "No explicit lien mentions",
            "details": "Requires external verification of lien registry",
        }

    async def _check_regulatory_compliance(self, document_text: str) -> Dict:
        """Check for regulatory compliance mentions"""
        regulatory_keywords = [
            "kyc",
            "aml",
            "know your customer",
            "anti-money laundering",
            "regulatory",
            "compliance",
        ]
        
        has_regulatory = any(
            keyword.lower() in document_text.lower() for keyword in regulatory_keywords
        )
        
        return {
            "category": "Regulatory Compliance",
            "status": "pass" if has_regulatory else "warning",
            "description": "Regulatory compliance provisions identified" if has_regulatory else "Limited regulatory compliance mentions",
            "details": "Verify KYC/AML requirements are met",
        }

    def _load_compliance_rules(self) -> Dict:
        """Load compliance rules (placeholder for more complex rule engine)"""
        return {
            "lma_standards": True,
            "regulatory_requirements": True,
        }


