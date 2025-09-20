"""
Threat Summary Generator - Creates human-readable threat analysis summaries
"""

from typing import List, Dict


class ThreatSummaryGenerator:
    """
    Generate human-readable summaries of threat analysis results
    """

    @staticmethod
    def generate_summary(analysis) -> List[str]:
        """
        Generate comprehensive threat summary based on analysis results

        Args:
            analysis: ThreatAnalysis object with analysis results

        Returns:
            List of summary strings describing the threats found
        """
        summary = []

        try:
            # Urgency analysis
            if analysis.urgency_score > 0.7:
                summary.append("Extreme urgency language detected with aggressive time pressure tactics")
            elif analysis.urgency_score > 0.5:
                summary.append("High urgency language detected with time pressure tactics")
            elif analysis.urgency_score > 0.3:
                summary.append("Moderate urgency indicators present")

            # Financial threat analysis
            if analysis.financial_risk > 0.7:
                summary.append("Critical financial threat indicators - likely targeting payment/banking information")
            elif analysis.financial_risk > 0.5:
                summary.append("Financial threat indicators present")
            elif analysis.financial_risk > 0.3:
                summary.append("Potential financial-related content detected")

            # URL analysis
            url_count = len(analysis.suspicious_urls)
            if url_count > 3:
                summary.append(f"Multiple suspicious URLs detected ({url_count} URLs) - high redirect risk")
            elif url_count > 1:
                summary.append(f"Multiple suspicious URL patterns identified ({url_count} URLs)")
            elif url_count == 1:
                summary.append("Suspicious URL pattern identified")

            # Authority impersonation
            authority_count = len(analysis.impersonation_indicators)
            if authority_count > 2:
                summary.append("Multiple authority impersonation indicators detected")
            elif authority_count > 0:
                summary.append("Authority impersonation indicators detected")

            # Grammar and linguistic analysis
            grammar_errors = analysis.risk_factors.get('grammar_errors', 0)
            linguistic_anomalies = analysis.risk_factors.get('linguistic_anomalies', 0)

            if grammar_errors > 5:
                summary.append("Multiple grammar and linguistic anomalies - potentially automated translation")
            elif grammar_errors > 3:
                summary.append("Grammar and linguistic anomalies found")

            # Technique-specific summaries
            technique = analysis.technique_classification.lower()
            if "credential harvesting" in technique:
                summary.append("Credential harvesting attempt detected - likely seeking login information")
            elif "social engineering" in technique:
                summary.append("Social engineering tactics identified - psychological manipulation present")
            elif "poorly crafted" in technique:
                summary.append("Low-quality phishing attempt - amateur construction detected")

            # Overall risk assessment
            if analysis.overall_risk_score > 0.8:
                summary.append("HIGH CONFIDENCE THREAT - Multiple attack vectors identified")
            elif analysis.overall_risk_score > 0.6:
                summary.append("Significant threat indicators - recommend immediate attention")
            elif analysis.overall_risk_score > 0.4:
                summary.append("Moderate threat level - warrants investigation")

            # Keyword-based insights
            keyword_count = len(analysis.threat_keywords)
            if keyword_count > 7:
                summary.append(f"Extensive use of threat-related keywords ({keyword_count} identified)")
            elif keyword_count > 4:
                summary.append(f"Multiple threat-related keywords detected ({keyword_count} found)")

            # Punctuation analysis
            excessive_punct = analysis.risk_factors.get('excessive_punctuation', 0)
            if excessive_punct > 2:
                summary.append("Excessive punctuation usage - emotional manipulation tactics")

            # Default summary if no specific threats found
            if not summary:
                if analysis.overall_risk_score > 0.3:
                    summary.append("Basic threat patterns detected - monitor for additional indicators")
                else:
                    summary.append("Minimal threat indicators - appears largely legitimate")

            return summary[:5]  # Limit to top 5 most important findings

        except Exception as e:
            return [f"Summary generation failed - manual review recommended: {str(e)}"]

    @staticmethod
    def generate_short_summary(analysis) -> str:
        """
        Generate a single-line threat summary

        Args:
            analysis: ThreatAnalysis object

        Returns:
            Single summary string
        """
        try:
            risk_score = analysis.overall_risk_score
            technique = analysis.technique_classification

            if risk_score > 0.8:
                return f"HIGH RISK: {technique} with multiple attack vectors"
            elif risk_score > 0.6:
                return f"ELEVATED RISK: {technique} detected"
            elif risk_score > 0.4:
                return f"MODERATE RISK: {technique} indicators present"
            elif risk_score > 0.2:
                return f"LOW RISK: Minimal {technique} patterns"
            else:
                return "MINIMAL RISK: Content appears legitimate"

        except Exception:
            return "Risk assessment unavailable"

    @staticmethod
    def generate_technical_summary(analysis) -> Dict[str, str]:
        """
        Generate technical summary for security teams

        Args:
            analysis: ThreatAnalysis object

        Returns:
            Dictionary with technical analysis details
        """
        try:
            return {
                "attack_vector": analysis.technique_classification,
                "confidence_level": ThreatSummaryGenerator._get_confidence_level(analysis.overall_risk_score),
                "primary_indicators": ThreatSummaryGenerator._get_primary_indicators(analysis),
                "recommended_action": ThreatSummaryGenerator._get_recommended_action(analysis.overall_risk_score),
                "ioc_summary": ThreatSummaryGenerator._generate_ioc_summary(analysis)
            }
        except Exception as e:
            return {"error": f"Technical summary generation failed: {str(e)}"}

    @staticmethod
    def _get_confidence_level(risk_score: float) -> str:
        """Get confidence level based on risk score"""
        if risk_score > 0.8:
            return "High Confidence"
        elif risk_score > 0.6:
            return "Medium-High Confidence"
        elif risk_score > 0.4:
            return "Medium Confidence"
        elif risk_score > 0.2:
            return "Low-Medium Confidence"
        else:
            return "Low Confidence"

    @staticmethod
    def _get_primary_indicators(analysis) -> str:
        """Get primary threat indicators"""
        indicators = []

        if analysis.urgency_score > 0.5:
            indicators.append("Urgency")
        if analysis.financial_risk > 0.5:
            indicators.append("Financial")
        if len(analysis.suspicious_urls) > 0:
            indicators.append("Malicious URLs")
        if len(analysis.impersonation_indicators) > 0:
            indicators.append("Authority Impersonation")

        return ", ".join(indicators) if indicators else "Generic patterns"

    @staticmethod
    def _get_recommended_action(risk_score: float) -> str:
        """Get recommended action based on risk score"""
        if risk_score > 0.8:
            return "Block and investigate immediately"
        elif risk_score > 0.6:
            return "Quarantine and analyze"
        elif risk_score > 0.4:
            return "Flag for review"
        elif risk_score > 0.2:
            return "Monitor closely"
        else:
            return "Standard monitoring"

    @staticmethod
    def _generate_ioc_summary(analysis) -> str:
        """Generate Indicators of Compromise summary"""
        iocs = []

        if analysis.suspicious_urls:
            iocs.append(f"{len(analysis.suspicious_urls)} suspicious URL(s)")

        keyword_count = len(analysis.threat_keywords)
        if keyword_count > 0:
            iocs.append(f"{keyword_count} threat keyword(s)")

        if analysis.risk_factors.get('grammar_errors', 0) > 3:
            iocs.append("Grammar anomalies")

        return ", ".join(iocs) if iocs else "Standard content patterns"