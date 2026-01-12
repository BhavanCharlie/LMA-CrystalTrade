"""
Post-Trade Monitoring Service
Monitors covenants and key dates/obligations with alerts
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta


class MonitoringService:
    def __init__(self):
        pass

    async def create_monitoring_rule(
        self, analysis_id: str, rule_config: Dict
    ) -> Dict[str, Any]:
        """Create a monitoring rule"""
        return {
            "id": f"rule_{analysis_id}_{datetime.utcnow().timestamp()}",
            "analysis_id": analysis_id,
            "rule_type": rule_config.get("rule_type", "covenant"),
            "rule_name": rule_config.get("rule_name", "Unnamed Rule"),
            "threshold_value": rule_config.get("threshold_value", 0.0),
            "current_value": rule_config.get("current_value", 0.0),
            "alert_threshold": rule_config.get("alert_threshold", 0.9),
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        }

    async def check_rules(self, rules: List[Dict]) -> List[Dict]:
        """Check all monitoring rules and generate alerts"""
        alerts = []
        
        for rule in rules:
            if not rule.get("is_active", True):
                continue
            
            threshold = rule.get("threshold_value", 0.0)
            current = rule.get("current_value", 0.0)
            alert_threshold_pct = rule.get("alert_threshold", 0.9)
            
            # Calculate breach percentage
            if threshold > 0:
                breach_pct = current / threshold
            else:
                breach_pct = 1.0
            
            # Generate alert if approaching threshold
            if breach_pct >= alert_threshold_pct:
                alert_type = "critical" if breach_pct >= 1.0 else "warning"
                
                alerts.append({
                    "rule_id": rule.get("id"),
                    "analysis_id": rule.get("analysis_id"),
                    "alert_type": alert_type,
                    "message": self._generate_alert_message(rule, breach_pct),
                    "threshold_breach_percentage": breach_pct,
                    "is_acknowledged": False,
                    "created_at": datetime.utcnow().isoformat(),
                })
        
        return alerts

    def _generate_alert_message(self, rule: Dict, breach_pct: float) -> str:
        """Generate alert message"""
        rule_name = rule.get("rule_name", "Rule")
        rule_type = rule.get("rule_type", "covenant")
        current = rule.get("current_value", 0.0)
        threshold = rule.get("threshold_value", 0.0)
        
        if breach_pct >= 1.0:
            return f"CRITICAL: {rule_name} has breached threshold. Current: {current}, Threshold: {threshold}"
        else:
            pct_remaining = (1.0 - breach_pct) * 100
            return f"WARNING: {rule_name} is at {breach_pct*100:.1f}% of threshold ({pct_remaining:.1f}% remaining). Current: {current}, Threshold: {threshold}"

    async def extract_monitoring_rules_from_analysis(
        self, analysis_id: str, extracted_terms: Dict
    ) -> List[Dict]:
        """Extract monitoring rules from analysis"""
        rules = []
        
        # Extract covenant rules
        covenants = extracted_terms.get("financial_covenants", [])
        if isinstance(covenants, list):
            for covenant in covenants:
                if isinstance(covenant, dict):
                    rule = {
                        "id": f"rule_{analysis_id}_covenant_{covenant.get('name', 'unknown')}",
                        "analysis_id": analysis_id,
                        "rule_type": "covenant",
                        "rule_name": covenant.get("name", "Financial Covenant"),
                        "threshold_value": self._parse_covenant_threshold(covenant.get("requirement", "")),
                        "current_value": self._parse_covenant_value(covenant.get("current_value", "")),
                        "alert_threshold": 0.9,
                        "is_active": True,
                    }
                    rules.append(rule)
        
        # Extract date-based rules
        maturity_date = extracted_terms.get("maturity_date", "")
        if maturity_date:
            # Create a date monitoring rule (simplified - would need actual date parsing)
            rules.append({
                "id": f"rule_{analysis_id}_maturity",
                "analysis_id": analysis_id,
                "rule_type": "date",
                "rule_name": "Maturity Date",
                "threshold_value": 0.0,  # Would be actual date
                "current_value": 0.0,
                "alert_threshold": 0.9,
                "is_active": True,
            })
        
        return rules

    def _parse_covenant_threshold(self, requirement: str) -> float:
        """Parse covenant threshold from requirement text"""
        # Simplified parsing - would need more sophisticated NLP
        try:
            # Look for numbers
            import re
            numbers = re.findall(r'\d+\.?\d*', str(requirement))
            if numbers:
                return float(numbers[0])
        except:
            pass
        return 0.0

    def _parse_covenant_value(self, current_value: str) -> float:
        """Parse current covenant value"""
        try:
            return float(str(current_value).replace(",", "").strip())
        except:
            return 0.0

