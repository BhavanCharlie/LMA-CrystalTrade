"""
LMA Deviation Engine
Compares extracted clauses against LMA baseline templates
"""
from typing import Dict, List, Any
import re


class LMADeviationEngine:
    def __init__(self):
        self.baseline_templates = self._load_baseline_templates()

    async def analyze_deviations(
        self, analysis_id: str, document_id: str, extracted_terms: Dict, document_text: str
    ) -> Dict[str, Any]:
        """
        Analyze deviations from LMA standards
        
        Returns:
            {
                "deviations": [...],
                "deviation_count": int,
                "severity_breakdown": {...},
                "heatmap": {...}
            }
        """
        deviations = []
        
        # Analyze transfer clauses
        transfer_deviations = self._analyze_transfer_clauses(
            analysis_id, document_id, extracted_terms, document_text
        )
        deviations.extend(transfer_deviations)
        
        # Analyze covenant clauses
        covenant_deviations = self._analyze_covenant_clauses(
            analysis_id, document_id, extracted_terms, document_text
        )
        deviations.extend(covenant_deviations)
        
        # Analyze payment clauses
        payment_deviations = self._analyze_payment_clauses(
            analysis_id, document_id, extracted_terms, document_text
        )
        deviations.extend(payment_deviations)
        
        # Calculate severity breakdown
        severity_breakdown = {
            "high": len([d for d in deviations if d.get("deviation_severity") == "high"]),
            "medium": len([d for d in deviations if d.get("deviation_severity") == "medium"]),
            "low": len([d for d in deviations if d.get("deviation_severity") == "low"]),
        }
        
        # Generate heatmap by clause type
        heatmap = {}
        for deviation in deviations:
            clause_type = deviation.get("clause_type", "other")
            if clause_type not in heatmap:
                heatmap[clause_type] = {
                    "count": 0,
                    "high_severity": 0,
                    "medium_severity": 0,
                    "low_severity": 0,
                }
            heatmap[clause_type]["count"] += 1
            severity = deviation.get("deviation_severity", "low")
            heatmap[clause_type][f"{severity}_severity"] += 1
        
        return {
            "deviations": deviations,
            "deviation_count": len(deviations),
            "severity_breakdown": severity_breakdown,
            "heatmap": heatmap,
        }

    def _analyze_transfer_clauses(
        self, analysis_id: str, document_id: str, extracted_terms: Dict, document_text: str
    ) -> List[Dict]:
        """Analyze transfer-related clauses"""
        deviations = []
        
        transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
        baseline_transfer = self.baseline_templates.get("transfer", "")
        
        # Check for non-standard restrictions
        if "prohibited" in transfer_restrictions:
            deviations.append({
                "id": f"{analysis_id}_transfer_1",
                "analysis_id": analysis_id,
                "document_id": document_id,
                "clause_type": "transfer",
                "clause_text": extracted_terms.get("transfer_restrictions", ""),
                "deviation_severity": "high",
                "market_impact": "Significantly reduces liquidity - transfers may be prohibited entirely",
                "baseline_template": baseline_transfer,
                "confidence": 0.9,
                "page_reference": "N/A",
                "section_reference": "Transfer Provisions",
            })
        elif "assignment" not in transfer_restrictions and "participation" not in transfer_restrictions:
            deviations.append({
                "id": f"{analysis_id}_transfer_2",
                "analysis_id": analysis_id,
                "document_id": document_id,
                "clause_type": "transfer",
                "clause_text": extracted_terms.get("transfer_restrictions", ""),
                "deviation_severity": "medium",
                "market_impact": "Unclear transfer provisions may delay closing or require legal clarification",
                "baseline_template": baseline_transfer,
                "confidence": 0.7,
                "page_reference": "N/A",
                "section_reference": "Transfer Provisions",
            })
        
        return deviations

    def _analyze_covenant_clauses(
        self, analysis_id: str, document_id: str, extracted_terms: Dict, document_text: str
    ) -> List[Dict]:
        """Analyze covenant-related clauses"""
        deviations = []
        
        covenants = extracted_terms.get("financial_covenants", [])
        if not isinstance(covenants, list):
            covenants = []
        
        baseline_covenant = self.baseline_templates.get("covenant", "")
        
        # Check for unusual covenant structures
        if len(covenants) == 0:
            deviations.append({
                "id": f"{analysis_id}_covenant_1",
                "analysis_id": analysis_id,
                "document_id": document_id,
                "clause_type": "covenant",
                "clause_text": "No financial covenants identified",
                "deviation_severity": "medium",
                "market_impact": "Lack of covenants may indicate covenant-lite structure - verify with Agent",
                "baseline_template": baseline_covenant,
                "confidence": 0.6,
                "page_reference": "N/A",
                "section_reference": "Covenants",
            })
        elif len(covenants) > 5:
            deviations.append({
                "id": f"{analysis_id}_covenant_2",
                "analysis_id": analysis_id,
                "document_id": document_id,
                "clause_type": "covenant",
                "clause_text": f"{len(covenants)} financial covenants identified",
                "deviation_severity": "low",
                "market_impact": "High number of covenants may indicate tighter structure - monitor closely",
                "baseline_template": baseline_covenant,
                "confidence": 0.7,
                "page_reference": "N/A",
                "section_reference": "Covenants",
            })
        
        return deviations

    def _analyze_payment_clauses(
        self, analysis_id: str, document_id: str, extracted_terms: Dict, document_text: str
    ) -> List[Dict]:
        """Analyze payment-related clauses"""
        deviations = []
        
        # Check for unusual payment terms
        payment_keywords = ["payment", "interest", "principal", "default"]
        payment_mentions = sum(1 for keyword in payment_keywords if keyword in document_text.lower())
        
        if payment_mentions == 0:
            deviations.append({
                "id": f"{analysis_id}_payment_1",
                "analysis_id": analysis_id,
                "document_id": document_id,
                "clause_type": "payment",
                "clause_text": "Payment terms not clearly identified",
                "deviation_severity": "medium",
                "market_impact": "Unclear payment terms may require clarification with Agent",
                "baseline_template": self.baseline_templates.get("payment", ""),
                "confidence": 0.6,
                "page_reference": "N/A",
                "section_reference": "Payment Provisions",
            })
        
        return deviations

    def _load_baseline_templates(self) -> Dict[str, str]:
        """Load LMA baseline templates"""
        return {
            "transfer": """
Standard LMA Transfer Provision:
- Assignments: Permitted with Agent consent (not to be unreasonably withheld)
- Participations: Permitted without consent
- Minimum transfer amount: Typically $1M or higher
- Restrictions: No transfers to competitors or restricted parties
""",
            "covenant": """
Standard LMA Financial Covenants:
- Debt-to-EBITDA ratio
- Interest Coverage Ratio
- Leverage ratio
- Typically tested quarterly
""",
            "payment": """
Standard LMA Payment Provisions:
- Interest payments: Quarterly or semi-annual
- Principal: Bullet at maturity or amortizing schedule
- Default: Payment default after grace period
""",
            "consent": """
Standard LMA Consent Requirements:
- Agent consent for assignments (not to be unreasonably withheld)
- Borrower consent typically not required for assignments
- Majority lender consent for material amendments
""",
        }

