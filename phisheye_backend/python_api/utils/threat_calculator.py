"""
Threat Level Calculator - Determines categorical threat levels and risk categories
"""

from typing import Dict


class ThreatLevelCalculator:
    """
    Calculate threat levels and risk categories based on analysis results
    """

    @staticmethod
    def calculate_threat_level(overall_risk: float, risk_factors: Dict[str, int]) -> str:
        """
        Calculate categorical threat level based on overall risk score and factors

        Args:
            overall_risk: Overall risk score (0.0 - 1.0)
            risk_factors: Dictionary of risk factor counts

        Returns:
            Threat level string: critical, high, medium, low, minimal, unknown
        """
        try:
            # Base level calculation
            if overall_risk >= 0.8:
                base_level = "critical"
            elif overall_risk >= 0.6:
                base_level = "high"
            elif overall_risk >= 0.4:
                base_level = "medium"
            elif overall_risk >= 0.2:
                base_level = "low"
            else:
                base_level = "minimal"

            # Adjust based on risk factors
            high_risk_factors = sum(1 for count in risk_factors.values() if count > 2)

            # Escalate if multiple high-risk factors present
            if high_risk_factors >= 3 and base_level in ["medium", "low"]:
                return "high"
            elif high_risk_factors >= 2 and base_level == "low":
                return "medium"

            # Specific escalations
            if (risk_factors.get('suspicious_urls', 0) > 0 and
                    risk_factors.get('financial_threats', 0) > 1 and
                    base_level == "medium"):
                return "high"

            if (risk_factors.get('authority_impersonation', 0) > 0 and
                    risk_factors.get('urgency_indicators', 0) > 2 and
                    base_level in ["low", "minimal"]):
                return "medium"

            return base_level

        except Exception:
            return "unknown"

    @staticmethod
    def determine_risk_category(technique: str, financial_risk: float, authority_score: int) -> str:
        """
        Determine specific risk category based on analysis

        Args:
            technique: Classified attack technique
            financial_risk: Financial risk score (0.0 - 1.0)
            authority_score: Number of authority impersonation indicators

        Returns:
            Risk category string
        """
        try:
            technique_lower = technique.lower()

            # Primary categorization based on technique
            if "credential" in technique_lower:
                if financial_risk > 0.5:
                    return "credential_harvesting_financial"
                else:
                    return "credential_harvesting"

            elif "authority" in technique_lower or authority_score > 0:
                if financial_risk > 0.5:
                    return "authority_impersonation_financial"
                else:
                    return "authority_impersonation"

            elif "social engineering" in technique_lower:
                if financial_risk > 0.5:
                    return "social_engineering_financial"
                else:
                    return "social_engineering"

            elif financial_risk > 0.6:
                return "financial_phishing"

            elif "poorly crafted" in technique_lower:
                return "low_quality_phishing"

            elif "urgent" in technique_lower:
                return "urgency_based_phishing"

            else:
                return "generic_phishing"

        except Exception:
            return "unknown_threat"

    @staticmethod
    def get_risk_level_description(threat_level: str) -> str:
        """
        Get human-readable description of threat level

        Args:
            threat_level: Threat level string

        Returns:
            Description string
        """
        descriptions = {
            "critical": "Immediate action required - high confidence phishing attack",
            "high": "Likely phishing - recommend blocking and investigation",
            "medium": "Suspicious content - warrants closer inspection",
            "low": "Some risk indicators present - monitor carefully",
            "minimal": "Low risk - appears mostly legitimate",
            "unknown": "Unable to assess risk level"
        }

        return descriptions.get(threat_level, "Risk level assessment unavailable")

    @staticmethod
    def get_recommended_action(threat_level: str, risk_category: str) -> str:
        """
        Get recommended action based on threat level and category

        Args:
            threat_level: Threat level string
            risk_category: Risk category string

        Returns:
            Recommended action string
        """
        if threat_level == "critical":
            return "Block immediately and report to security team"
        elif threat_level == "high":
            return "Quarantine and investigate further"
        elif threat_level == "medium":
            return "Flag for review and user awareness"
        elif threat_level == "low":
            return "Monitor and log for pattern analysis"
        elif threat_level == "minimal":
            return "Allow with standard monitoring"
        else:
            return "Manual review required"