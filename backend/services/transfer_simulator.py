"""
Transferability Simulator
Simulates trade pathways (assignment vs participation) with consents, timeline, and blockers
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta


class TransferSimulator:
    def __init__(self):
        self.base_timeline_days = {
            "assignment": 14,  # Base days for assignment
            "participation": 7,  # Base days for participation
        }

    async def simulate_transfer_pathway(
        self, analysis_id: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """
        Simulate transfer pathways for a loan
        
        Returns:
            {
                "pathways": [
                    {
                        "type": "assignment" | "participation",
                        "required_consents": [...],
                        "estimated_timeline_days": int,
                        "blockers": [...],
                        "recommended_actions": [...],
                        "playbook": str
                    }
                ]
            }
        """
        pathways = []
        
        # Simulate Assignment pathway
        assignment_pathway = await self._simulate_pathway(
            "assignment", extracted_terms, compliance_checks
        )
        pathways.append(assignment_pathway)
        
        # Simulate Participation pathway
        participation_pathway = await self._simulate_pathway(
            "participation", extracted_terms, compliance_checks
        )
        pathways.append(participation_pathway)
        
        return {
            "pathways": pathways,
            "analysis_id": analysis_id,
            "simulated_at": datetime.utcnow().isoformat(),
        }

    async def _simulate_pathway(
        self, pathway_type: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> Dict[str, Any]:
        """Simulate a single pathway"""
        required_consents = self._identify_required_consents(
            pathway_type, extracted_terms, compliance_checks
        )
        
        blockers = self._identify_blockers(pathway_type, extracted_terms, compliance_checks)
        
        timeline_days = self._estimate_timeline(
            pathway_type, required_consents, blockers
        )
        
        recommended_actions = self._generate_recommended_actions(
            pathway_type, required_consents, blockers
        )
        
        playbook = self._generate_playbook(
            pathway_type, required_consents, blockers, timeline_days
        )
        
        return {
            "type": pathway_type,
            "required_consents": required_consents,
            "estimated_timeline_days": timeline_days,
            "blockers": blockers,
            "recommended_actions": recommended_actions,
            "playbook": playbook,
        }

    def _identify_required_consents(
        self, pathway_type: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> List[Dict]:
        """Identify required consents for the pathway"""
        consents = []
        
        consent_reqs = extracted_terms.get("consent_requirements", [])
        if isinstance(consent_reqs, str):
            consent_reqs = [consent_reqs] if consent_reqs else []
        
        # Check for Agent consent
        if any("agent" in str(req).lower() for req in consent_reqs):
            consents.append({
                "party": "Agent",
                "required": True,
                "threshold": "N/A",
                "timing": "Before transfer",
                "complexity": "Low" if pathway_type == "participation" else "Medium",
            })
        
        # Check for Borrower consent
        if any("borrower" in str(req).lower() for req in consent_reqs):
            consents.append({
                "party": "Borrower",
                "required": True,
                "threshold": "N/A",
                "timing": "Before transfer",
                "complexity": "High",
            })
        
        # Check for Lender consent (majority/minority)
        transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
        if "majority" in transfer_restrictions or "threshold" in transfer_restrictions:
            consents.append({
                "party": "Lenders",
                "required": True,
                "threshold": "Majority (typically 50%+)",
                "timing": "Before transfer",
                "complexity": "Medium",
            })
        
        # Default: Agent consent usually required for assignments
        if pathway_type == "assignment" and not consents:
            consents.append({
                "party": "Agent",
                "required": True,
                "threshold": "N/A",
                "timing": "Before transfer",
                "complexity": "Low",
            })
        
        return consents

    def _identify_blockers(
        self, pathway_type: str, extracted_terms: Dict, compliance_checks: List[Dict]
    ) -> List[Dict]:
        """Identify potential blockers"""
        blockers = []
        
        # Check transfer restrictions
        transfer_restrictions = str(extracted_terms.get("transfer_restrictions", "")).lower()
        
        if "prohibited" in transfer_restrictions:
            blockers.append({
                "type": "Transfer Prohibition",
                "severity": "Critical",
                "description": "Transfer is explicitly prohibited",
                "mitigation": "Review for exceptions or consider alternative structures",
            })
        
        if pathway_type == "assignment" and "assignment" not in transfer_restrictions:
            if "participation" in transfer_restrictions:
                blockers.append({
                    "type": "Assignment Not Allowed",
                    "severity": "High",
                    "description": "Assignment may not be permitted, participation may be required",
                    "mitigation": "Consider participation pathway instead",
                })
        
        # Check compliance failures
        for check in compliance_checks:
            if check.get("status") == "fail":
                blockers.append({
                    "type": f"Compliance Issue: {check.get('category')}",
                    "severity": "High",
                    "description": check.get("description", ""),
                    "mitigation": "Resolve compliance issue before proceeding",
                })
        
        # Check for missing documentation
        required_terms = ["interest_rate", "maturity_date", "principal_amount"]
        missing_terms = [term for term in required_terms if not extracted_terms.get(term)]
        if missing_terms:
            blockers.append({
                "type": "Missing Documentation",
                "severity": "Medium",
                "description": f"Missing key terms: {', '.join(missing_terms)}",
                "mitigation": "Obtain complete documentation",
            })
        
        return blockers

    def _estimate_timeline(
        self, pathway_type: str, required_consents: List[Dict], blockers: List[Dict]
    ) -> int:
        """Estimate timeline in days"""
        base_days = self.base_timeline_days.get(pathway_type, 14)
        
        # Add days for each consent required
        for consent in required_consents:
            complexity = consent.get("complexity", "Medium")
            if complexity == "High":
                base_days += 7
            elif complexity == "Medium":
                base_days += 3
            else:
                base_days += 1
        
        # Add days for blockers
        for blocker in blockers:
            severity = blocker.get("severity", "Medium")
            if severity == "Critical":
                base_days += 14
            elif severity == "High":
                base_days += 7
            elif severity == "Medium":
                base_days += 3
        
        return base_days

    def _generate_recommended_actions(
        self, pathway_type: str, required_consents: List[Dict], blockers: List[Dict]
    ) -> List[str]:
        """Generate recommended next actions"""
        actions = []
        
        # Pathway-specific actions
        if pathway_type == "assignment":
            actions.append("Obtain executed assignment agreement from seller")
            actions.append("Verify Agent consent requirements")
        else:
            actions.append("Execute participation agreement")
            actions.append("Confirm participation structure with Agent")
        
        # Consent-specific actions
        for consent in required_consents:
            party = consent.get("party", "")
            if party == "Borrower":
                actions.append(f"Request Borrower consent - allow 5-7 business days")
            elif party == "Agent":
                actions.append(f"Submit transfer notice to Agent - typically 2-3 business days")
            elif party == "Lenders":
                actions.append(f"Coordinate with Lenders for majority consent if required")
        
        # Blocker-specific actions
        for blocker in blockers:
            if blocker.get("severity") == "Critical":
                actions.append(f"URGENT: Resolve {blocker.get('type')} before proceeding")
            elif blocker.get("severity") == "High":
                actions.append(f"Address {blocker.get('type')}: {blocker.get('mitigation')}")
        
        # Standard actions
        actions.append("Complete KYC/AML checks")
        actions.append("Execute transfer documentation")
        actions.append("Coordinate settlement with Agent")
        
        return actions

    def _generate_playbook(
        self, pathway_type: str, required_consents: List[Dict], blockers: List[Dict], timeline_days: int
    ) -> str:
        """Generate text playbook"""
        playbook = f"""
# {pathway_type.title()} Transfer Playbook

## Overview
This playbook outlines the steps required to complete a {pathway_type} transfer for this loan position.

## Estimated Timeline
{timeline_days} business days from initiation to settlement.

## Required Consents
"""
        
        if required_consents:
            for consent in required_consents:
                playbook += f"""
- **{consent.get('party')}**: {consent.get('description', 'Consent required')}
  - Threshold: {consent.get('threshold', 'N/A')}
  - Timing: {consent.get('timing', 'Before transfer')}
  - Complexity: {consent.get('complexity', 'Medium')}
"""
        else:
            playbook += "\n- No explicit consent requirements identified (verify with Agent)\n"
        
        playbook += "\n## Potential Blockers\n"
        
        if blockers:
            for blocker in blockers:
                playbook += f"""
- **{blocker.get('type')}** ({blocker.get('severity')}): {blocker.get('description')}
  - Mitigation: {blocker.get('mitigation')}
"""
        else:
            playbook += "\n- No critical blockers identified\n"
        
        playbook += f"""
## Key Steps
1. Initiate transfer request with Agent
2. Obtain required consents
3. Complete due diligence checks
4. Execute transfer documentation
5. Coordinate settlement

## Notes
- Monitor timeline closely - delays in consent can extend timeline significantly
- Maintain communication with Agent throughout process
- Document all consents and approvals
"""
        
        return playbook.strip()

