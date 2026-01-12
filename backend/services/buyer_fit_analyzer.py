"""
Buyer Fit Analyzer
Rule-based heuristics to identify buyer types (CLO, Bank, Distressed Fund) and fit scores
"""
from typing import Dict, List, Any


class BuyerFitAnalyzer:
    def __init__(self):
        self.buyer_profiles = self._load_buyer_profiles()

    async def analyze_buyer_fit(
        self, analysis_id: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """
        Analyze buyer fit for different buyer types
        
        Returns:
            {
                "buyer_fits": [
                    {
                        "buyer_type": str,
                        "fit_score": int (0-100),
                        "indicators": [...],
                        "reasoning": str,
                        "diligence_summary": str
                    }
                ]
            }
        """
        buyer_fits = []
        
        for buyer_type in ["CLO", "Bank", "DistressedFund"]:
            fit_analysis = await self._analyze_buyer_type(
                buyer_type, extracted_terms, compliance_checks
            )
            buyer_fits.append({
                "buyer_type": buyer_type,
                "fit_score": fit_analysis["score"],
                "indicators": fit_analysis["indicators"],
                "reasoning": fit_analysis["reasoning"],
                "diligence_summary": fit_analysis["diligence_summary"],
            })
        
        return {
            "buyer_fits": buyer_fits,
            "analysis_id": analysis_id,
        }

    async def _analyze_buyer_type(
        self, buyer_type: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """Analyze fit for a specific buyer type"""
        profile = self.buyer_profiles.get(buyer_type, {})
        score = 50  # Base score
        indicators = []
        reasoning_parts = []
        
        # CLO-specific analysis
        if buyer_type == "CLO":
            # CLOs prefer covenant-lite or moderate covenants
            covenants = extracted_terms.get("financial_covenants", [])
            covenant_count = len(covenants) if isinstance(covenants, list) else 0
            
            if covenant_count <= 3:
                score += 20
                indicators.append("Covenant-lite structure")
                reasoning_parts.append("Low covenant count aligns with CLO preferences")
            elif covenant_count <= 5:
                score += 10
                indicators.append("Moderate covenants")
            else:
                score -= 15
                indicators.append("High covenant count - may be restrictive for CLOs")
                reasoning_parts.append("High number of covenants may limit CLO flexibility")
            
            # CLOs prefer transferable loans
            transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
            if "prohibited" in transfer_restrictions:
                score -= 30
                indicators.append("Transfer prohibited - major blocker")
                reasoning_parts.append("Transfer prohibition is a critical issue for CLOs")
            elif "assignment" in transfer_restrictions or "participation" in transfer_restrictions:
                score += 15
                indicators.append("Transfer provisions present")
                reasoning_parts.append("Transfer provisions allow CLO flexibility")
            
            # CLOs prefer standard LMA terms
            if not any(check.get("status") == "fail" for check in compliance_checks):
                score += 10
                indicators.append("Standard LMA compliance")
        
        # Bank-specific analysis
        elif buyer_type == "Bank":
            # Banks prefer strong covenants
            covenants = extracted_terms.get("financial_covenants", [])
            covenant_count = len(covenants) if isinstance(covenants, list) else 0
            
            if covenant_count >= 3:
                score += 20
                indicators.append("Strong covenant package")
                reasoning_parts.append("Covenants provide bank with monitoring tools")
            elif covenant_count > 0:
                score += 10
                indicators.append("Some covenants present")
            else:
                score -= 10
                indicators.append("Covenant-lite - may be less attractive to banks")
                reasoning_parts.append("Banks typically prefer covenant protection")
            
            # Banks are more flexible on transfer restrictions
            transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
            if "prohibited" not in transfer_restrictions:
                score += 10
                indicators.append("Transferable structure")
        
        # Distressed Fund-specific analysis
        elif buyer_type == "DistressedFund":
            # Distressed funds are more flexible on terms
            score += 15  # Base advantage - more flexible
            
            # Check for default/restructuring provisions
            document_text = str(extracted_terms).lower()
            if "default" in document_text or "restructuring" in document_text:
                score += 15
                indicators.append("Default/restructuring provisions present")
                reasoning_parts.append("Distressed funds specialize in these situations")
            
            # Transfer restrictions less critical
            transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
            if "prohibited" not in transfer_restrictions:
                score += 10
                indicators.append("Transferable")
        
        # Common factors
        # Interest rate attractiveness
        interest_rate = extracted_terms.get("interest_rate", "")
        if interest_rate:
            # Higher rates more attractive (simplified heuristic)
            try:
                rate_value = float(str(interest_rate).replace("%", "").strip())
                if rate_value >= 5.0:
                    score += 5
                    indicators.append("Attractive interest rate")
            except:
                pass
        
        # Maturity
        maturity = extracted_terms.get("maturity_date", "")
        if maturity:
            indicators.append("Maturity date identified")
        
        # Generate reasoning
        if not reasoning_parts:
            reasoning_parts.append(f"Standard analysis for {buyer_type} buyer type")
        
        reasoning = " | ".join(reasoning_parts)
        
        # Generate diligence summary
        diligence_summary = self._generate_diligence_summary(
            buyer_type, extracted_terms, indicators
        )
        
        score = max(0, min(100, score))
        
        return {
            "score": score,
            "indicators": indicators,
            "reasoning": reasoning,
            "diligence_summary": diligence_summary,
        }

    def _generate_diligence_summary(
        self, buyer_type: str, extracted_terms: Dict, indicators: List[str]
    ) -> str:
        """Generate buyer-specific diligence summary"""
        summary = f"""
# {buyer_type} Buyer Diligence Summary

## Key Considerations for {buyer_type} Buyers

### Transfer Provisions
"""
        
        transfer_restrictions = extracted_terms.get("transfer_restrictions", "")
        if transfer_restrictions:
            summary += f"- Transfer restrictions: {transfer_restrictions}\n"
        else:
            summary += "- Transfer provisions: Standard\n"
        
        summary += "\n### Covenants\n"
        covenants = extracted_terms.get("financial_covenants", [])
        if isinstance(covenants, list) and covenants:
            summary += f"- {len(covenants)} financial covenants identified\n"
            for covenant in covenants[:3]:  # Show first 3
                if isinstance(covenant, dict):
                    summary += f"  - {covenant.get('name', 'Covenant')}: {covenant.get('requirement', 'N/A')}\n"
        else:
            summary += "- Covenant structure: Verify with Agent\n"
        
        summary += "\n### Key Indicators\n"
        for indicator in indicators:
            summary += f"- {indicator}\n"
        
        if buyer_type == "CLO":
            summary += "\n### CLO-Specific Notes\n"
            summary += "- Verify eligibility for CLO portfolio\n"
            summary += "- Check rating agency requirements\n"
            summary += "- Confirm transfer mechanics with Agent\n"
        elif buyer_type == "Bank":
            summary += "\n### Bank-Specific Notes\n"
            summary += "- Verify regulatory capital treatment\n"
            summary += "- Check internal credit policies\n"
            summary += "- Confirm documentation standards\n"
        elif buyer_type == "DistressedFund":
            summary += "\n### Distressed Fund-Specific Notes\n"
            summary += "- Assess restructuring potential\n"
            summary += "- Review default provisions\n"
            summary += "- Evaluate workout scenarios\n"
        
        return summary.strip()

    def _load_buyer_profiles(self) -> Dict[str, Dict]:
        """Load buyer type profiles"""
        return {
            "CLO": {
                "preferences": ["covenant_lite", "transferable", "standard_terms"],
                "avoid": ["high_covenants", "transfer_prohibited"],
            },
            "Bank": {
                "preferences": ["strong_covenants", "standard_terms", "regulatory_compliant"],
                "avoid": ["covenant_lite", "non_standard"],
            },
            "DistressedFund": {
                "preferences": ["flexible_terms", "default_provisions"],
                "avoid": [],
            },
        }

