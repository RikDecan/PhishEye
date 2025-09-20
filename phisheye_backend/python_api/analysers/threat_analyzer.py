"""
Enhanced Threat Analyzer - Main orchestrator for threat analysis
"""

import re
from typing import Dict, List
import logging
from .url_analyzer import EnhancedURLAnalyzer
from .linguistic_analyzer import LinguisticAnalyzer
from .keyword_analyzer import ContextualKeywordAnalyzer


logger = logging.getLogger(__name__)

# Import keyword lists from main module or define here
URGENCY_KEYWORDS = [
    'urgent', 'immediate', 'expires', 'deadline', 'limited time', 'act now',
    'hurry', 'quickly', 'asap', 'emergency', 'critical', 'alert', 'final notice',
    'last chance', 'expires today', 'expires soon', 'time sensitive'
]

FINANCIAL_KEYWORDS = [
    'account suspended', 'verify payment', 'update payment', 'billing issue',
    'refund', 'transaction', 'bank account', 'credit card', 'paypal', 'bitcoin',
    'wire transfer', 'money', 'payment failed', 'subscription', 'unauthorized charge',
    'security breach', 'fraud alert', 'unusual activity', 'locked account'
]

AUTHORITY_KEYWORDS = [
    'irs', 'fbi', 'police', 'government', 'tax', 'legal action', 'court',
    'lawsuit', 'attorney', 'investigation', 'compliance', 'regulation',
    'customs', 'immigration', 'social security', 'medicare'
]

SOCIAL_ENGINEERING = [
    'congratulations', 'winner', 'selected', 'prize', 'lottery', 'inheritance',
    'beneficiary', 'claim', 'reward', 'gift', 'free', 'exclusive',
    'limited offer', 'special deal', 'once in lifetime'
]

CREDENTIAL_HARVESTING = [
    'login', 'password', 'username', 'verify identity', 'confirm account',
    'update information', 'security check', 'authentication', 'validate',
    'two factor', 'confirm identity', 'account verification'
]


class ThreatAnalysis:
    """Data class for threat analysis results"""

    def __init__(self, urgency_score: float, financial_risk: float,
                 suspicious_urls: List[str], threat_keywords: List[str],
                 impersonation_indicators: List[str], risk_factors: Dict[str, int],
                 technique_classification: str, overall_risk_score: float):
        self.urgency_score = urgency_score
        self.financial_risk = financial_risk
        self.suspicious_urls = suspicious_urls
        self.threat_keywords = threat_keywords
        self.impersonation_indicators = impersonation_indicators
        self.risk_factors = risk_factors
        self.technique_classification = technique_classification
        self.overall_risk_score = overall_risk_score


class EnhancedThreatAnalyzer:
    """
    Enhanced threat analyzer with contextual understanding and adaptive scoring
    """

    @staticmethod
    async def analyze_text_enhanced(text: str) -> ThreatAnalysis:
        """
        Enhanced threat analysis with contextual understanding
        """
        try:
            text_lower = text.lower()

            # Extract linguistic features
            linguistic_features = LinguisticAnalyzer.extract_features(text)

            # Enhanced keyword analysis
            urgency_matches = [kw for kw in URGENCY_KEYWORDS if kw in text_lower]
            financial_matches = [kw for kw in FINANCIAL_KEYWORDS if kw in text_lower]
            authority_matches = [kw for kw in AUTHORITY_KEYWORDS if kw in text_lower]

            # Context-aware scoring
            urgency_score = ContextualKeywordAnalyzer.analyze_urgency_context(text, urgency_matches)
            financial_risk = ContextualKeywordAnalyzer.analyze_financial_context(text, financial_matches)

            # Enhanced URL analysis
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            urls = re.findall(url_pattern, text)
            suspicious_url_analysis = await EnhancedURLAnalyzer.analyze_urls_enhanced(urls)
            suspicious_urls = [url for url, score in suspicious_url_analysis]

            # Enhanced grammar analysis
            grammar_risk = EnhancedThreatAnalyzer._calculate_grammar_risk(text, linguistic_features)

            # Collect all threat keywords
            all_threat_keywords = []
            all_threat_keywords.extend(urgency_matches)
            all_threat_keywords.extend(financial_matches)
            all_threat_keywords.extend(authority_matches)

            # Enhanced risk factors
            risk_factors = {
                'urgency_indicators': len(urgency_matches),
                'financial_threats': len(financial_matches),
                'authority_impersonation': len(authority_matches),
                'suspicious_urls': len(suspicious_urls),
                'grammar_errors': int(grammar_risk * 10),
                'excessive_punctuation': len(re.findall(r'[!]{2,}', text)),
                'linguistic_anomalies': EnhancedThreatAnalyzer._calculate_linguistic_anomalies(linguistic_features)
            }

            # Enhanced technique classification
            technique = EnhancedThreatAnalyzer._classify_technique_enhanced(text_lower, linguistic_features)

            # Improved overall risk score with adaptive weights
            risk_weights = EnhancedThreatAnalyzer._calculate_adaptive_weights(risk_factors)
            overall_risk = (
                    urgency_score * risk_weights['urgency'] +
                    financial_risk * risk_weights['financial'] +
                    (len(suspicious_urls) > 0) * risk_weights['url'] +
                    (len(authority_matches) > 0) * risk_weights['authority'] +
                    grammar_risk * risk_weights['grammar'] +
                    EnhancedThreatAnalyzer._calculate_linguistic_risk(linguistic_features) * risk_weights['linguistic']
            )

            return ThreatAnalysis(
                urgency_score=urgency_score,
                financial_risk=financial_risk,
                suspicious_urls=suspicious_urls,
                threat_keywords=list(set(all_threat_keywords[:10])),
                impersonation_indicators=authority_matches,
                risk_factors=risk_factors,
                technique_classification=technique,
                overall_risk_score=min(overall_risk, 1.0)
            )

        except Exception as e:
            logger.error(f"Enhanced threat analysis failed: {e}")
            # Fallback to basic analysis
            return await EnhancedThreatAnalyzer._fallback_analysis(text)

    @staticmethod
    async def _fallback_analysis(text: str) -> ThreatAnalysis:
        """Fallback to basic analysis if enhanced analysis fails"""
        logger.warning("Using fallback threat analysis")
        text_lower = text.lower()

        urgency_matches = [kw for kw in URGENCY_KEYWORDS if kw in text_lower]
        financial_matches = [kw for kw in FINANCIAL_KEYWORDS if kw in text_lower]
        authority_matches = [kw for kw in AUTHORITY_KEYWORDS if kw in text_lower]

        return ThreatAnalysis(
            urgency_score=min(len(urgency_matches) / 3.0, 1.0),
            financial_risk=min(len(financial_matches) / 2.0, 1.0),
            suspicious_urls=[],
            threat_keywords=list(set(urgency_matches + financial_matches + authority_matches)),
            impersonation_indicators=authority_matches,
            risk_factors={
                'urgency_indicators': len(urgency_matches),
                'financial_threats': len(financial_matches),
                'authority_impersonation': len(authority_matches),
                'suspicious_urls': 0,
                'grammar_errors': 0,
                'excessive_punctuation': 0
            },
            technique_classification="Generic Phishing",
            overall_risk_score=0.5
        )

    @staticmethod
    def _calculate_grammar_risk(text: str, linguistic_features: Dict[str, float]) -> float:
        """Enhanced grammar risk calculation"""
        risk = 0.0

        # Basic grammar issues
        risk += len(re.findall(r'\b[A-Z]{2,}\b', text)) * 0.05
        risk += len(re.findall(r'([a-z])[A-Z]', text)) * 0.03

        # Linguistic feature based risk
        if linguistic_features['caps_ratio'] > 0.15:
            risk += 0.2
        if linguistic_features['exclamation_ratio'] > 0.05:
            risk += 0.15
        if linguistic_features['readability_score'] < 30:
            risk += 0.1

        return min(risk, 1.0)

    @staticmethod
    def _calculate_linguistic_anomalies(linguistic_features: Dict[str, float]) -> int:
        """Calculate linguistic anomaly count"""
        anomalies = 0

        if linguistic_features['avg_sentence_length'] > 30:
            anomalies += 1
        if linguistic_features['avg_sentence_length'] < 5:
            anomalies += 1
        if linguistic_features['punctuation_ratio'] > 0.1:
            anomalies += 1
        if linguistic_features['caps_ratio'] > 0.15:
            anomalies += 1

        return anomalies

    @staticmethod
    def _calculate_adaptive_weights(risk_factors: Dict[str, int]) -> Dict[str, float]:
        """Calculate adaptive weights based on risk factor presence"""
        base_weights = {
            'urgency': 0.20,
            'financial': 0.25,
            'url': 0.20,
            'authority': 0.15,
            'grammar': 0.10,
            'linguistic': 0.10
        }

        # Increase weights for present factors
        total_factors = sum(1 for v in risk_factors.values() if v > 0)
        if total_factors > 0:
            boost_per_factor = 0.05 / total_factors
            for factor in risk_factors:
                if risk_factors[factor] > 0:
                    weight_key = {
                        'urgency_indicators': 'urgency',
                        'financial_threats': 'financial',
                        'suspicious_urls': 'url',
                        'authority_impersonation': 'authority',
                        'grammar_errors': 'grammar'
                    }.get(factor)
                    if weight_key:
                        base_weights[weight_key] += boost_per_factor

        return base_weights

    @staticmethod
    def _classify_technique_enhanced(text_lower: str, linguistic_features: Dict[str, float]) -> str:
        """Enhanced technique classification with linguistic features"""
        social_score = sum(1 for kw in SOCIAL_ENGINEERING if kw in text_lower)
        credential_score = sum(1 for kw in CREDENTIAL_HARVESTING if kw in text_lower)
        authority_score = sum(1 for kw in AUTHORITY_KEYWORDS if kw in text_lower)

        # Add linguistic indicators
        if linguistic_features['exclamation_ratio'] > 0.05 and social_score > 0:
            social_score += 1

        if credential_score >= 2:
            return "Credential Harvesting"
        elif authority_score >= 1:
            return "Authority Impersonation"
        elif social_score >= 2:
            return "Social Engineering"
        elif linguistic_features['readability_score'] < 30:
            return "Poorly Crafted Phishing"
        else:
            return "Generic Phishing"

    @staticmethod
    def _calculate_linguistic_risk(linguistic_features: Dict[str, float]) -> float:
        """Calculate risk based on linguistic features"""
        risk = 0.0

        # Poor readability might indicate automated/poor translation
        if linguistic_features['readability_score'] < 30:
            risk += 0.3
        elif linguistic_features['readability_score'] > 80:
            risk -= 0.1

        # Excessive punctuation/caps
        if linguistic_features['exclamation_ratio'] > 0.03:
            risk += 0.2
        if linguistic_features['caps_ratio'] > 0.1:
            risk += 0.2

        return max(min(risk, 1.0), 0.0)