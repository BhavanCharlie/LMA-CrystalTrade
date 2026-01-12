"""
Negotiation Insights Generator
Identifies clauses likely to be negotiated and suggests redlines/questions
"""
from typing import Dict, List, Any


class NegotiationInsightsGenerator:
    def __init__(self):
        self.negotiation_triggers = self._load_negotiation_triggers()

    async def generate_insights(
        self, analysis_id: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """
        Generate negotiation insights
        
        Returns:
            {
                "insights": [
                    {
                        "clause_reference": str,
                        "clause_text": str,
                        "negotiation_likelihood": str,
                        "suggested_redlines": [...],
                        "questions_for_agent": [...],
                        "risk_basis": str
                    }
                ]
            }
        """
        insights = []
        
        # Analyze transfer restrictions
        transfer_insight = self._analyze_transfer_for_negotiation(
            analysis_id, extracted_terms
        )
        if transfer_insight:
            insights.append(transfer_insight)
        
        # Analyze consent requirements
        consent_insight = self._analyze_consent_for_negotiation(
            analysis_id, extracted_terms
        )
        if consent_insight:
            insights.append(consent_insight)
        
        # Analyze covenants
        covenant_insight = self._analyze_covenants_for_negotiation(
            analysis_id, extracted_terms
        )
        if covenant_insight:
            insights.append(covenant_insight)
        
        # Analyze compliance issues
        for check in compliance_checks:
            if check.get("status") == "fail":
                compliance_insight = self._analyze_compliance_for_negotiation(
                    analysis_id, check
                )
                if compliance_insight:
                    insights.append(compliance_insight)
        
        return {
            "insights": insights,
            "analysis_id": analysis_id,
        }

    def _analyze_transfer_for_negotiation(
        self, analysis_id: str, extracted_terms: Dict
    ) -> Dict[str, Any] | None:
        """Analyze transfer provisions for negotiation"""
        transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
        
        if "prohibited" in transfer_restrictions:
            return {
                "clause_reference": "Transfer Provisions",
                "clause_text": extracted_terms.get("transfer_restrictions", ""),
                "negotiation_likelihood": "high",
                "suggested_redlines": [
                    "Remove transfer prohibition",
                    "Add standard LMA transfer provisions allowing assignments with Agent consent",
                    "Clarify participation rights",
                ],
                "questions_for_agent": [
                    "Are there any exceptions to the transfer prohibition?",
                    "Can we negotiate assignment rights?",
                    "What is the process for requesting transfer consent?",
                ],
                "risk_basis": "Transfer prohibition significantly limits liquidity and marketability",
            }
        elif "restricted" in transfer_restrictions and "consent" not in transfer_restrictions:
            return {
                "clause_reference": "Transfer Provisions",
                "clause_text": extracted_terms.get("transfer_restrictions", ""),
                "negotiation_likelihood": "medium",
                "suggested_redlines": [
                    "Clarify transfer restrictions",
                    "Specify consent requirements and thresholds",
                ],
                "questions_for_agent": [
                    "What are the specific transfer restrictions?",
                    "What consent is required for assignments?",
                ],
                "risk_basis": "Unclear transfer restrictions may delay closing",
            }
        
        return None

    def _analyze_consent_for_negotiation(
        self, analysis_id: str, extracted_terms: Dict
    ) -> Dict[str, Any] | None:
        """Analyze consent requirements for negotiation"""
        consent_reqs = extracted_terms.get("consent_requirements", [])
        if isinstance(consent_reqs, str):
            consent_reqs = [consent_reqs] if consent_reqs else []
        
        if len(consent_reqs) > 2:
            return {
                "clause_reference": "Consent Requirements",
                "clause_text": str(consent_reqs),
                "negotiation_likelihood": "medium",
                "suggested_redlines": [
                    "Limit consent requirements to Agent only for standard assignments",
                    "Clarify consent thresholds and timing",
                ],
                "questions_for_agent": [
                    "Can we reduce consent requirements for standard transfers?",
                    "What is the typical consent timeline?",
                    "Are there any consent exceptions?",
                ],
                "risk_basis": "Multiple consent requirements can delay transfers and increase complexity",
            }
        
        return None

    def _analyze_covenants_for_negotiation(
        self, analysis_id: str, extracted_terms: Dict
    ) -> Dict[str, Any] | None:
        """Analyze covenants for negotiation"""
        covenants = extracted_terms.get("financial_covenants", [])
        if not isinstance(covenants, list):
            return None
        
        if len(covenants) > 5:
            return {
                "clause_reference": "Financial Covenants",
                "clause_text": f"{len(covenants)} financial covenants",
                "negotiation_likelihood": "low",
                "suggested_redlines": [
                    "Review covenant headroom and thresholds",
                    "Consider covenant relief provisions",
                ],
                "questions_for_agent": [
                    "What is the current covenant headroom?",
                    "Are there any covenant relief provisions?",
                    "What is the covenant testing frequency?",
                ],
                "risk_basis": "High number of covenants may indicate tight structure - verify headroom",
            }
        
        return None

    def _analyze_compliance_for_negotiation(
        self, analysis_id: str, compliance_check: Dict
    ) -> Dict[str, Any] | None:
        """Analyze compliance issues for negotiation"""
        category = compliance_check.get("category", "")
        description = compliance_check.get("description", "")
        
        if compliance_check.get("status") == "fail":
            return {
                "clause_reference": category,
                "clause_text": description,
                "negotiation_likelihood": "high",
                "suggested_redlines": [
                    f"Resolve {category} compliance issue",
                    "Align with LMA standards",
                ],
                "questions_for_agent": [
                    f"Can we address the {category} issue?",
                    "What is required to bring this into compliance?",
                ],
                "risk_basis": f"Compliance failure in {category} may block transfer or require remediation",
            }
        
        return None

    def _load_negotiation_triggers(self) -> Dict[str, List[str]]:
        """Load negotiation trigger keywords"""
        return {
            "high_likelihood": [
                "prohibited",
                "restricted",
                "requires consent",
                "must obtain",
            ],
            "medium_likelihood": [
                "may require",
                "subject to",
                "at discretion",
            ],
        }

