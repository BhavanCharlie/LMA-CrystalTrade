"""
Trade Readiness Score Engine
Computes a 0-100 score and Green/Amber/Red label based on multiple factors
"""
from typing import Dict, List, Any
from datetime import datetime
import uuid


class TradeReadinessEngine:
    def __init__(self):
        self.weights = {
            "documentation_completeness": 0.20,
            "transferability_friction": 0.25,
            "consent_complexity": 0.20,
            "covenant_tightness": 0.15,
            "non_standard_deviations": 0.15,
            "regulatory_flags": 0.05,
        }

    async def calculate_trade_readiness(
        self, analysis_data: Dict, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """
        Calculate trade readiness score with explainable breakdown
        
        Returns:
            {
                "score": 0-100,
                "label": "Green" | "Amber" | "Red",
                "breakdown": {...},
                "confidence": 0.0-1.0,
                "evidence_links": [...]
            }
        """
        evidence_links = []
        
        # 1. Documentation Completeness (0-100)
        doc_completeness = self._assess_documentation_completeness(
            analysis_data, extracted_terms, evidence_links
        )
        
        # 2. Transferability Friction (0-100, higher = more friction = worse)
        transfer_friction = self._assess_transferability_friction(
            extracted_terms, compliance_checks, evidence_links
        )
        transfer_score = 100 - transfer_friction  # Invert: less friction = higher score
        
        # 3. Consent Complexity (0-100, higher complexity = worse)
        consent_complexity = self._assess_consent_complexity(
            extracted_terms, compliance_checks, evidence_links
        )
        consent_score = 100 - consent_complexity
        
        # 4. Covenant Tightness / Headroom (0-100)
        covenant_score = self._assess_covenant_tightness(
            extracted_terms, evidence_links
        )
        
        # 5. Non-standard Clause Deviations (0-100, more deviations = worse)
        deviation_score = self._assess_non_standard_deviations(
            extracted_terms, evidence_links
        )
        
        # 6. Regulatory/Compliance Flags (0-100)
        regulatory_score = self._assess_regulatory_flags(
            compliance_checks, evidence_links
        )
        
        # Calculate weighted score
        score = (
            doc_completeness * self.weights["documentation_completeness"] +
            transfer_score * self.weights["transferability_friction"] +
            consent_score * self.weights["consent_complexity"] +
            covenant_score * self.weights["covenant_tightness"] +
            deviation_score * self.weights["non_standard_deviations"] +
            regulatory_score * self.weights["regulatory_flags"]
        )
        
        score = max(0, min(100, int(score)))
        
        # Determine label
        if score >= 75:
            label = "Green"
        elif score >= 50:
            label = "Amber"
        else:
            label = "Red"
        
        # Calculate confidence based on data quality
        confidence = self._calculate_confidence(extracted_terms, compliance_checks)
        
        return {
            "score": score,
            "label": label,
            "breakdown": {
                "documentation_completeness": {
                    "score": doc_completeness,
                    "weight": self.weights["documentation_completeness"],
                    "contribution": doc_completeness * self.weights["documentation_completeness"],
                },
                "transferability_friction": {
                    "score": transfer_score,
                    "friction_level": transfer_friction,
                    "weight": self.weights["transferability_friction"],
                    "contribution": transfer_score * self.weights["transferability_friction"],
                },
                "consent_complexity": {
                    "score": consent_score,
                    "complexity_level": consent_complexity,
                    "weight": self.weights["consent_complexity"],
                    "contribution": consent_score * self.weights["consent_complexity"],
                },
                "covenant_tightness": {
                    "score": covenant_score,
                    "weight": self.weights["covenant_tightness"],
                    "contribution": covenant_score * self.weights["covenant_tightness"],
                },
                "non_standard_deviations": {
                    "score": deviation_score,
                    "weight": self.weights["non_standard_deviations"],
                    "contribution": deviation_score * self.weights["non_standard_deviations"],
                },
                "regulatory_flags": {
                    "score": regulatory_score,
                    "weight": self.weights["regulatory_flags"],
                    "contribution": regulatory_score * self.weights["regulatory_flags"],
                },
            },
            "confidence": confidence,
            "evidence_links": evidence_links,
        }

    def _assess_documentation_completeness(
        self, analysis_data: Dict, extracted_terms: Dict, evidence_links: List[Dict]
    ) -> int:
        """Assess documentation completeness (0-100)"""
        score = 50  # Base score
        
        # Check for key document types
        doc_type = analysis_data.get("document_type", "")
        if "credit_agreement" in doc_type.lower() or "loan_agreement" in doc_type.lower():
            score += 20
        
        # Check for extracted key terms
        required_terms = [
            "interest_rate",
            "maturity_date",
            "principal_amount",
            "transfer_restrictions",
            "consent_requirements",
            "financial_covenants",
        ]
        
        extracted_count = sum(1 for term in required_terms if extracted_terms.get(term))
        completeness_ratio = extracted_count / len(required_terms)
        score += int(completeness_ratio * 30)
        
        evidence_links.append({
            "type": "documentation_completeness",
            "document": analysis_data.get("document_path", ""),
            "extracted_terms_count": extracted_count,
            "total_required": len(required_terms),
        })
        
        return min(100, score)

    def _assess_transferability_friction(
        self, extracted_terms: Dict, compliance_checks: List[Dict], evidence_links: List[Dict]
    ) -> int:
        """Assess transferability friction (0-100, higher = more friction)"""
        friction = 0
        
        # Check transfer restrictions
        transfer_restrictions = extracted_terms.get("transfer_restrictions", "")
        if transfer_restrictions:
            if "prohibited" in transfer_restrictions.lower():
                friction += 40
            elif "restricted" in transfer_restrictions.lower():
                friction += 25
            elif "consent" in transfer_restrictions.lower():
                friction += 15
        
        # Check assignment vs participation
        assignment_allowed = "assignment" in str(extracted_terms.get("transfer_restrictions", "")).lower()
        participation_allowed = "participation" in str(extracted_terms.get("transfer_restrictions", "")).lower()
        
        if not assignment_allowed and not participation_allowed:
            friction += 30
        elif not assignment_allowed:
            friction += 20  # Assignment typically preferred
        
        # Check compliance checks
        for check in compliance_checks:
            if check.get("category") == "Transfer Restrictions" and check.get("status") == "fail":
                friction += 20
        
        evidence_links.append({
            "type": "transferability_friction",
            "transfer_restrictions": transfer_restrictions,
            "assignment_allowed": assignment_allowed,
            "participation_allowed": participation_allowed,
        })
        
        return min(100, friction)

    def _assess_consent_complexity(
        self, extracted_terms: Dict, compliance_checks: List[Dict], evidence_links: List[Dict]
    ) -> int:
        """Assess consent complexity (0-100, higher = more complex)"""
        complexity = 0
        
        consent_reqs = extracted_terms.get("consent_requirements", [])
        if isinstance(consent_reqs, str):
            consent_reqs = [consent_reqs] if consent_reqs else []
        
        # Number of parties requiring consent
        num_parties = len(consent_reqs)
        complexity += min(num_parties * 15, 40)
        
        # Check for specific consent requirements
        consent_text = str(extracted_terms.get("consent_requirements", "")).lower()
        if "borrower" in consent_text:
            complexity += 20
        if "agent" in consent_text:
            complexity += 15
        if "majority" in consent_text or "threshold" in consent_text:
            complexity += 15
        
        # Check compliance
        for check in compliance_checks:
            if check.get("category") == "Consent Requirements" and check.get("status") == "warning":
                complexity += 10
        
        evidence_links.append({
            "type": "consent_complexity",
            "num_parties": num_parties,
            "consent_requirements": consent_reqs,
        })
        
        return min(100, complexity)

    def _assess_covenant_tightness(
        self, extracted_terms: Dict, evidence_links: List[Dict]
    ) -> int:
        """Assess covenant tightness/headroom (0-100, higher = more headroom = better)"""
        score = 70  # Base score assuming moderate covenants
        
        covenants = extracted_terms.get("financial_covenants", [])
        if isinstance(covenants, list):
            num_covenants = len(covenants)
            # More covenants = potentially tighter, but also more structured
            if num_covenants == 0:
                score = 60  # No covenants = uncertainty
            elif num_covenants <= 3:
                score = 75  # Moderate covenants
            elif num_covenants <= 5:
                score = 65  # Many covenants
            else:
                score = 50  # Very tight
        
        # Check for current values vs requirements (if available)
        for covenant in covenants if isinstance(covenants, list) else []:
            if isinstance(covenant, dict):
                current = covenant.get("current_value")
                requirement = covenant.get("requirement")
                if current and requirement:
                    # This would need actual financial data - placeholder logic
                    score += 5  # Having data is good
        
        evidence_links.append({
            "type": "covenant_tightness",
            "num_covenants": len(covenants) if isinstance(covenants, list) else 0,
        })
        
        return min(100, max(0, score))

    def _assess_non_standard_deviations(
        self, extracted_terms: Dict, evidence_links: List[Dict]
    ) -> int:
        """Assess non-standard clause deviations (0-100, higher = fewer deviations = better)"""
        score = 80  # Base score
        
        # This would be enhanced by LMA deviation engine
        # For now, check for unusual terms
        unusual_indicators = [
            "unusual",
            "non-standard",
            "atypical",
            "custom",
            "bespoke",
        ]
        
        terms_text = str(extracted_terms).lower()
        deviation_count = sum(1 for indicator in unusual_indicators if indicator in terms_text)
        
        score -= deviation_count * 10
        
        evidence_links.append({
            "type": "non_standard_deviations",
            "deviation_indicators": deviation_count,
        })
        
        return min(100, max(0, score))

    def _assess_regulatory_flags(
        self, compliance_checks: List[Dict], evidence_links: List[Dict]
    ) -> int:
        """Assess regulatory/compliance flags (0-100)"""
        score = 90  # Base score
        
        for check in compliance_checks:
            if check.get("category") == "Regulatory Compliance":
                if check.get("status") == "fail":
                    score -= 30
                elif check.get("status") == "warning":
                    score -= 15
        
        evidence_links.append({
            "type": "regulatory_flags",
            "compliance_status": [c.get("status") for c in compliance_checks],
        })
        
        return min(100, max(0, score))

    def _calculate_confidence(
        self, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> float:
        """Calculate confidence in the score (0.0-1.0)"""
        confidence = 0.5  # Base confidence
        
        # More extracted terms = higher confidence
        term_count = len([k for k, v in extracted_terms.items() if v])
        if term_count >= 5:
            confidence += 0.2
        elif term_count >= 3:
            confidence += 0.1
        
        # More compliance checks = higher confidence
        if len(compliance_checks) >= 5:
            confidence += 0.2
        elif len(compliance_checks) >= 3:
            confidence += 0.1
        
        return min(1.0, confidence)

