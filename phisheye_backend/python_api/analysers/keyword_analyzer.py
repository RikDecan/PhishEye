"""
Contextual Keyword Analyzer - Context-aware analysis of threat keywords
"""

import re
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ContextualKeywordAnalyzer:
    """
    Analyze keywords within their context for more accurate threat detection
    """

    # Negation words that can reduce threat score
    NEGATION_WORDS = [
        'not', 'no', 'never', 'none', 'nothing', 'neither', 'nor',
        "don't", "doesn't", "didn't", "won't", "can't", "isn't", "aren't",
        "wasn't", "weren't", "haven't", "hasn't", "hadn't", "shouldn't",
        "couldn't", "wouldn't", "mustn't", "shan't"
    ]

    # Time intensifiers that increase urgency
    TIME_INTENSIFIERS = [
        'now', 'immediately', 'today', 'tonight', 'asap', 'right now',
        'within hours', 'within minutes', 'before midnight', 'by today',
        'this hour', 'right away', 'at once', 'instantly'
    ]

    # Financial action words that increase financial threat score
    FINANCIAL_ACTIONS = [
        'verify', 'update', 'confirm', 'validate', 'secure', 'protect',
        'restore', 'unlock', 'reactivate', 'recover', 'fix', 'resolve'
    ]

    @staticmethod
    def analyze_urgency_context(text: str, matches: List[str]) -> float:
        """
        Context-aware urgency analysis

        Args:
            text: Full text to analyze
            matches: List of urgency keywords found

        Returns:
            Contextual urgency score (0.0 - 1.0)
        """
        if not matches:
            return 0.0

        try:
            text_lower = text.lower()
            context_score = 0.0
            processed_matches = set()  # Avoid double-counting

            for match in matches:
                if match in processed_matches:
                    continue

                processed_matches.add(match)
                match_score = ContextualKeywordAnalyzer._analyze_urgency_match_context(
                    text_lower, match
                )
                context_score += match_score

            # Additional context analysis
            context_score += ContextualKeywordAnalyzer._analyze_time_pressure_context(text_lower)
            context_score += ContextualKeywordAnalyzer._analyze_consequence_context(text_lower)

            return min(context_score, 1.0)

        except Exception as e:
            logger.error(f"Urgency context analysis failed: {e}")
            # Fallback to simple scoring
            return min(len(matches) / 3.0, 1.0)

    @staticmethod
    def _analyze_urgency_match_context(text: str, match: str) -> float:
        """Analyze context around a specific urgency match"""
        match_positions = [m.start() for m in re.finditer(re.escape(match), text)]
        total_score = 0.0

        for pos in match_positions:
            score = 0.2  # Base score for urgency keyword

            # Check for negations before the match
            before_context = text[max(0, pos - 20):pos]
            if any(neg in before_context for neg in ContextualKeywordAnalyzer.NEGATION_WORDS):
                score = 0.0  # Negated urgency
                continue

            # Check for time intensifiers after the match
            after_context = text[pos:min(len(text), pos + 30)]
            if any(intensifier in after_context for intensifier in ContextualKeywordAnalyzer.TIME_INTENSIFIERS):
                score += 0.3

            # Check for specific urgency patterns
            context_window = text[max(0, pos - 15):min(len(text), pos + 15)]

            # Deadline patterns
            if re.search(r'(expire|deadline|end).*?(today|tomorrow|hour|minute)', context_window):
                score += 0.2

            # Account closure threats
            if re.search(r'(close|suspend|terminate|cancel).*?(account|service)', context_window):
                score += 0.25

            total_score += score

        return total_score

    @staticmethod
    def _analyze_time_pressure_context(text: str) -> float:
        """Analyze overall time pressure context"""
        score = 0.0

        # Specific time pressure patterns
        time_patterns = [
            r'within\s+\d+\s+(hour|minute|day)s?',
            r'expire[sd]?\s+(today|tomorrow|soon)',
            r'deadline.*?(today|tomorrow|tonight)',
            r'(last|final)\s+(chance|opportunity|warning)',
            r'act\s+(now|immediately|today)',
            r'limited\s+time\s+(offer|deal)',
            r'time\s+(sensitive|critical|running\s+out)'
        ]

        for pattern in time_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.15

        return min(score, 0.4)

    @staticmethod
    def _analyze_consequence_context(text: str) -> float:
        """Analyze consequence/threat context"""
        score = 0.0

        # Consequence patterns
        consequence_patterns = [
            r'(will|shall)\s+(be\s+)?(close|suspend|terminate|cancel|block)',
            r'(lose|loss)\s+(access|account|data|money)',
            r'permanent(ly)?\s+(close|suspend|delete|remove)',
            r'legal\s+(action|consequence|proceeding)',
            r'account\s+(will\s+be\s+)?(suspend|close|terminate)',
            r'service\s+(will\s+be\s+)?(discontinue|stop|end)'
        ]

        for pattern in consequence_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2

        return min(score, 0.3)

    @staticmethod
    def analyze_financial_context(text: str, matches: List[str]) -> float:
        """
        Context-aware financial threat analysis

        Args:
            text: Full text to analyze
            matches: List of financial keywords found

        Returns:
            Contextual financial risk score (0.0 - 1.0)
        """
        if not matches:
            return 0.0

        try:
            text_lower = text.lower()
            context_score = 0.0

            # Analyze each financial match in context
            for match in set(matches):  # Remove duplicates
                match_score = ContextualKeywordAnalyzer._analyze_financial_match_context(
                    text_lower, match
                )
                context_score += match_score

            # Additional financial context analysis
            context_score += ContextualKeywordAnalyzer._analyze_payment_action_context(text_lower)
            context_score += ContextualKeywordAnalyzer._analyze_account_threat_context(text_lower)
            context_score += ContextualKeywordAnalyzer._analyze_financial_urgency_context(text_lower)

            return min(context_score, 1.0)

        except Exception as e:
            logger.error(f"Financial context analysis failed: {e}")
            # Fallback to simple scoring
            return min(len(matches) / 2.0, 1.0)

    @staticmethod
    def _analyze_financial_match_context(text: str, match: str) -> float:
        """Analyze context around a specific financial match"""
        match_positions = [m.start() for m in re.finditer(re.escape(match), text)]
        total_score = 0.0

        for pos in match_positions:
            score = 0.15  # Base score for financial keyword

            # Check for negations
            before_context = text[max(0, pos - 20):pos]
            if any(neg in before_context for neg in ContextualKeywordAnalyzer.NEGATION_WORDS):
                continue  # Skip negated financial terms

            # Check for action words
            context_window = text[max(0, pos - 20):min(len(text), pos + 20)]
            if any(action in context_window for action in ContextualKeywordAnalyzer.FINANCIAL_ACTIONS):
                score += 0.2

            # Check for specific financial threat patterns
            if re.search(r'(suspend|block|freeze|lock).*?(account|card)', context_window):
                score += 0.3

            if re.search(r'(verify|update|confirm).*?(payment|billing|card)', context_window):
                score += 0.25

            if re.search(r'unauthorized.*?(transaction|charge|access)', context_window):
                score += 0.3

            total_score += score

        return total_score

    @staticmethod
    def _analyze_payment_action_context(text: str) -> float:
        """Analyze payment-related action context"""
        score = 0.0

        # Payment action patterns
        payment_patterns = [
            r'(verify|update|confirm)\s+.*?(payment|billing|card|account)',
            r'(click|tap|press)\s+.*?(verify|update|confirm)',
            r'(enter|provide|submit)\s+.*?(password|pin|code|number)',
            r'(re-enter|re-submit)\s+.*?(payment|billing)',
            r'(secure|protect)\s+.*?(account|payment|information)'
        ]

        for pattern in payment_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2

        return min(score, 0.4)

    @staticmethod
    def _analyze_account_threat_context(text: str) -> float:
        """Analyze account threat context"""
        score = 0.0

        # Account threat patterns
        threat_patterns = [
            r'account\s+(suspend|close|terminate|block|freeze)',
            r'(suspend|close|terminate)\s+.*?account',
            r'access\s+(denied|blocked|restricted|limited)',
            r'(unusual|suspicious|unauthorized)\s+.*?(activity|access|login)',
            r'security\s+(breach|violation|alert|warning)',
            r'(fraud|fraudulent)\s+(activity|transaction|attempt)'
        ]

        for pattern in threat_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.25

        return min(score, 0.5)

    @staticmethod
    def _analyze_financial_urgency_context(text: str) -> float:
        """Analyze financial urgency combination"""
        score = 0.0

        # Combined financial + urgency patterns
        combined_patterns = [
            r'(urgent|immediate).*?(payment|billing|account)',
            r'(expire|deadline).*?(payment|subscription|account)',
            r'(final|last).*?(notice|warning).*?(payment|account)',
            r'(act|respond)\s+(now|immediately).*?(payment|billing)',
            r'(limited\s+time).*?(payment|account|offer)'
        ]

        for pattern in combined_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            score += matches * 0.2

        return min(score, 0.3)

    @staticmethod
    def analyze_authority_context(text: str, matches: List[str]) -> Dict[str, float]:
        """
        Analyze authority impersonation context

        Args:
            text: Full text to analyze
            matches: List of authority keywords found

        Returns:
            Dictionary with authority analysis results
        """
        try:
            text_lower = text.lower()

            results = {
                'impersonation_score': 0.0,
                'legal_threat_score': 0.0,
                'government_score': 0.0,
                'corporate_score': 0.0
            }

            if not matches:
                return results

            # Government authority patterns
            gov_patterns = [
                r'(irs|fbi|police|government).*?(investigation|audit|notice)',
                r'(tax|legal)\s+(investigation|audit|proceeding)',
                r'(customs|immigration).*?(violation|issue)',
                r'social\s+security.*?(suspend|investigation)'
            ]

            for pattern in gov_patterns:
                matches_found = len(re.findall(pattern, text_lower))
                results['government_score'] += matches_found * 0.3

            # Legal threat patterns
            legal_patterns = [
                r'legal\s+(action|proceeding|consequence)',
                r'(lawsuit|court|attorney).*?(proceed|file|contact)',
                r'(violation|breach).*?(law|regulation|terms)',
                r'(criminal|civil)\s+(charge|proceeding)'
            ]

            for pattern in legal_patterns:
                matches_found = len(re.findall(pattern, text_lower))
                results['legal_threat_score'] += matches_found * 0.3

            # Corporate authority patterns
            corp_patterns = [
                r'(bank|paypal|amazon|microsoft|apple).*?(security|suspend)',
                r'(customer\s+service|support\s+team).*?(urgent|immediate)',
                r'(compliance|security)\s+(team|department)',
                r'(official|authorized).*?(notice|communication)'
            ]

            for pattern in corp_patterns:
                matches_found = len(re.findall(pattern, text_lower))
                results['corporate_score'] += matches_found * 0.25

            # Overall impersonation score
            results['impersonation_score'] = min(
                results['government_score'] +
                results['legal_threat_score'] +
                results['corporate_score'],
                1.0
            )

            # Cap individual scores
            for key in results:
                results[key] = min(results[key], 1.0)

            return results

        except Exception as e:
            logger.error(f"Authority context analysis failed: {e}")
            return {
                'impersonation_score': 0.0,
                'legal_threat_score': 0.0,
                'government_score': 0.0,
                'corporate_score': 0.0
            }