"""
Linguistic Analyzer - Extracts linguistic features and analyzes text patterns
"""

import re
from typing import Dict, List
import logging

# Try to import textstat, fallback if not available
try:
    from textstat import flesch_reading_ease, flesch_kincaid_grade
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False
    logging.warning("textstat not available - using simplified readability analysis")

logger = logging.getLogger(__name__)


class LinguisticAnalyzer:
    """
    Analyze linguistic patterns and extract features from text
    """

    @staticmethod
    def extract_features(text: str) -> Dict[str, float]:
        """
        Extract comprehensive linguistic features for enhanced analysis

        Args:
            text: Text to analyze

        Returns:
            Dictionary of linguistic features
        """
        try:
            if not text or not text.strip():
                return LinguisticAnalyzer._get_empty_features()

            # Basic text analysis
            sentences = re.split(r'[.!?]+', text.strip())
            sentences = [s.strip() for s in sentences if s.strip()]
            words = text.split()
            total_chars = len(text)

            if not words:
                return LinguisticAnalyzer._get_empty_features()

            # Character-based features
            punct_count = len(re.findall(r'[!?.,;:()"]', text))
            caps_count = sum(1 for c in text if c.isupper())
            digit_count = sum(1 for c in text if c.isdigit())

            # Punctuation analysis
            exclamation_count = text.count('!')
            question_count = text.count('?')
            excessive_punct = len(re.findall(r'[!]{2,}|[?]{2,}', text))

            # Word-based features
            caps_words = sum(1 for word in words if word.isupper() and len(word) > 1)
            long_words = sum(1 for word in words if len(word) > 10)

            # Sentence analysis
            sentence_count = max(len(sentences), 1)
            avg_sentence_length = len(words) / sentence_count

            # Calculate readability
            readability_score = LinguisticAnalyzer._calculate_readability(text, words, sentences)

            # Advanced pattern analysis
            repetition_score = LinguisticAnalyzer._analyze_repetition(text)
            emotional_intensity = LinguisticAnalyzer._analyze_emotional_intensity(text)

            return {
                'avg_sentence_length': avg_sentence_length,
                'punctuation_ratio': punct_count / total_chars,
                'caps_ratio': caps_count / total_chars,
                'digit_ratio': digit_count / total_chars,
                'readability_score': readability_score,
                'exclamation_ratio': exclamation_count / len(words),
                'question_ratio': question_count / len(words),
                'caps_words_ratio': caps_words / len(words),
                'long_words_ratio': long_words / len(words),
                'excessive_punctuation': excessive_punct,
                'repetition_score': repetition_score,
                'emotional_intensity': emotional_intensity,
                'word_count': len(words),
                'sentence_count': sentence_count,
                'avg_word_length': sum(len(word) for word in words) / len(words)
            }

        except Exception as e:
            logger.error(f"Linguistic feature extraction failed: {e}")
            return LinguisticAnalyzer._get_empty_features()

    @staticmethod
    def _get_empty_features() -> Dict[str, float]:
        """Return empty feature set for error cases"""
        return {
            'avg_sentence_length': 0.0,
            'punctuation_ratio': 0.0,
            'caps_ratio': 0.0,
            'digit_ratio': 0.0,
            'readability_score': 50.0,  # Neutral readability
            'exclamation_ratio': 0.0,
            'question_ratio': 0.0,
            'caps_words_ratio': 0.0,
            'long_words_ratio': 0.0,
            'excessive_punctuation': 0.0,
            'repetition_score': 0.0,
            'emotional_intensity': 0.0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0.0
        }

    @staticmethod
    def _calculate_readability(text: str, words: List[str], sentences: List[str]) -> float:
        """
        Calculate readability score (Flesch Reading Ease or simplified version)

        Args:
            text: Full text
            words: List of words
            sentences: List of sentences

        Returns:
            Readability score (0-100, higher = more readable)
        """
        try:
            if TEXTSTAT_AVAILABLE and len(words) > 5:
                return max(0, min(100, flesch_reading_ease(text)))
            else:
                # Simplified readability calculation
                avg_sentence_length = len(words) / max(len(sentences), 1)
                avg_word_length = sum(len(word) for word in words) / len(words)

                # Simple formula: shorter sentences and words = more readable
                readability = 100 - (avg_sentence_length * 2) - (avg_word_length * 5)
                return max(0, min(100, readability))

        except Exception:
            return 50.0  # Neutral score on error

    @staticmethod
    def _analyze_repetition(text: str) -> float:
        """
        Analyze text for repetitive patterns (often found in spam/phishing)

        Args:
            text: Text to analyze

        Returns:
            Repetition score (0-1, higher = more repetitive)
        """
        try:
            text_lower = text.lower()
            words = text_lower.split()

            if len(words) < 5:
                return 0.0

            repetition_score = 0.0

            # Check for repeated words
            word_counts = {}
            for word in words:
                if len(word) > 3:  # Only count substantial words
                    word_counts[word] = word_counts.get(word, 0) + 1

            # Calculate repetition based on word frequency
            total_substantial_words = sum(word_counts.values())
            if total_substantial_words > 0:
                repeated_words = sum(count - 1 for count in word_counts.values() if count > 1)
                repetition_score += repeated_words / total_substantial_words

            # Check for repeated phrases (2-3 words)
            phrases = []
            for i in range(len(words) - 1):
                if len(words[i]) > 2 and len(words[i + 1]) > 2:
                    phrases.append(f"{words[i]} {words[i + 1]}")

            if phrases:
                phrase_counts = {}
                for phrase in phrases:
                    phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1

                repeated_phrases = sum(1 for count in phrase_counts.values() if count > 1)
                repetition_score += repeated_phrases / len(phrases)

            # Check for repeated character patterns
            char_repetitions = len(re.findall(r'(.)\1{2,}', text_lower))  # 3+ repeated chars
            repetition_score += min(char_repetitions / 10, 0.3)

            return min(repetition_score, 1.0)

        except Exception:
            return 0.0

    @staticmethod
    def _analyze_emotional_intensity(text: str) -> float:
        """
        Analyze emotional intensity of text (common in phishing)

        Args:
            text: Text to analyze

        Returns:
            Emotional intensity score (0-1)
        """
        try:
            text_lower = text.lower()
            intensity_score = 0.0

            # Emotional keywords
            high_intensity_words = [
                'urgent', 'immediate', 'emergency', 'critical', 'alert',
                'warning', 'danger', 'threat', 'suspended', 'blocked',
                'expires', 'deadline', 'final', 'last chance', 'act now',
                'hurry', 'quickly', 'asap', 'important', 'serious'
            ]

            excitement_words = [
                'amazing', 'incredible', 'fantastic', 'wonderful',
                'congratulations', 'winner', 'lucky', 'selected',
                'exclusive', 'special', 'limited', 'bonus'
            ]

            fear_words = [
                'suspended', 'closed', 'terminated', 'cancelled',
                'blocked', 'restricted', 'locked', 'frozen',
                'investigation', 'violation', 'breach', 'unauthorized'
            ]

            # Count emotional words
            all_emotional_words = high_intensity_words + excitement_words + fear_words
            words = text_lower.split()

            if words:
                emotional_word_count = sum(1 for word in words if any(em_word in word for em_word in all_emotional_words))
                intensity_score += emotional_word_count / len(words)

            # Analyze punctuation for emotional emphasis
            exclamation_density = text.count('!') / max(len(text), 1) * 100
            question_density = text.count('?') / max(len(text), 1) * 100
            caps_density = sum(1 for c in text if c.isupper()) / max(len(text), 1) * 100

            intensity_score += min(exclamation_density, 0.3)
            intensity_score += min(question_density, 0.2)
            intensity_score += min(caps_density / 100, 0.3)

            # Multiple exclamation/question marks
            multiple_punct = len(re.findall(r'[!]{2,}|[?]{2,}', text))
            intensity_score += min(multiple_punct / 5, 0.2)

            return min(intensity_score, 1.0)

        except Exception:
            return 0.0

    @staticmethod
    def analyze_grammar_quality(text: str) -> Dict[str, float]:
        """
        Analyze grammar quality and common errors

        Args:
            text: Text to analyze

        Returns:
            Dictionary with grammar analysis results
        """
        try:
            grammar_issues = {
                'spelling_errors': 0.0,
                'grammar_errors': 0.0,
                'punctuation_errors': 0.0,
                'capitalization_errors': 0.0,
                'overall_quality': 1.0
            }

            # Basic spelling/grammar heuristics
            words = text.split()

            # Check for obvious spelling issues
            misspelled_patterns = [
                r'\b\w*[ck]k\w*\b',  # Double k patterns
                r'\b\w*[sz]z\w*\b',   # Double s/z patterns
                r'\b\w{15,}\b'        # Extremely long words (likely errors)
            ]

            spelling_errors = 0
            for pattern in misspelled_patterns:
                spelling_errors += len(re.findall(pattern, text, re.IGNORECASE))

            if words:
                grammar_issues['spelling_errors'] = min(spelling_errors / len(words), 1.0)

            # Capitalization errors
            sentences = re.split(r'[.!?]+', text)
            cap_errors = 0
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and not sentence[0].isupper():
                    cap_errors += 1

            if sentences:
                grammar_issues['capitalization_errors'] = cap_errors / len(sentences)

            # Random capitalization within words
            random_caps = len(re.findall(r'\b[a-z]+[A-Z]+[a-z]*\b', text))
            if words:
                grammar_issues['grammar_errors'] = min(random_caps / len(words), 1.0)

            # Punctuation errors (simplified)
            punct_errors = 0
            punct_errors += len(re.findall(r'[a-zA-Z][.!?][a-zA-Z]', text))  # Missing space after punct
            punct_errors += len(re.findall(r'\s+[.!?]', text))  # Space before punct

            grammar_issues['punctuation_errors'] = min(punct_errors / max(len(text), 1), 0.5)

            # Overall quality score
            total_errors = sum(grammar_issues[key] for key in grammar_issues if key != 'overall_quality')
            grammar_issues['overall_quality'] = max(0.0, 1.0 - total_errors)

            return grammar_issues

        except Exception as e:
            logger.error(f"Grammar analysis failed: {e}")
            return {
                'spelling_errors': 0.0,
                'grammar_errors': 0.0,
                'punctuation_errors': 0.0,
                'capitalization_errors': 0.0,
                'overall_quality': 0.5
            }

    @staticmethod
    def detect_language_patterns(text: str) -> Dict[str, any]:
        """
        Detect language patterns that might indicate machine translation or foreign origin

        Args:
            text: Text to analyze

        Returns:
            Dictionary with language pattern analysis
        """
        try:
            patterns = {
                'likely_machine_translated': False,
                'foreign_syntax_score': 0.0,
                'unusual_word_order': 0.0,
                'translation_artifacts': []
            }

            # Common machine translation artifacts
            translation_artifacts = [
                r'\bthe the\b',  # Duplicated articles
                r'\ba a\b',      # Duplicated articles
                r'\byour you\b', # Confused pronouns
                r'\bhis her\b',  # Gender confusion
                r'\bis are\b',   # Verb confusion
            ]

            artifacts_found = []
            for pattern in translation_artifacts:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    artifacts_found.extend(matches)

            patterns['translation_artifacts'] = artifacts_found

            if artifacts_found:
                patterns['likely_machine_translated'] = True
                patterns['foreign_syntax_score'] = min(len(artifacts_found) / 10, 1.0)

            # Unusual word order patterns (simplified)
            unusual_patterns = [
                r'\b(very|much|more|most)\s+(much|very)\b',  # Double intensifiers
                r'\bof\s+the\s+\w+\s+of\b',  # Unusual prepositional phrases
                r'\bwill\s+be\s+will\b',     # Repeated auxiliaries
            ]

            unusual_count = 0
            for pattern in unusual_patterns:
                unusual_count += len(re.findall(pattern, text, re.IGNORECASE))

            if unusual_count > 0:
                patterns['unusual_word_order'] = min(unusual_count / 5, 1.0)

            return patterns

        except Exception as e:
            logger.error(f"Language pattern detection failed: {e}")
            return {
                'likely_machine_translated': False,
                'foreign_syntax_score': 0.0,
                'unusual_word_order': 0.0,
                'translation_artifacts': []
            }

    @staticmethod
    def analyze_writing_style(text: str) -> Dict[str, any]:
        """
        Analyze overall writing style for authenticity

        Args:
            text: Text to analyze

        Returns:
            Dictionary with writing style analysis
        """
        try:
            style_analysis = {
                'formality_score': 0.0,
                'complexity_score': 0.0,
                'authenticity_score': 1.0,
                'style_indicators': []
            }

            words = text.split()
            if not words:
                return style_analysis

            # Formality indicators
            formal_words = [
                'please', 'kindly', 'sincerely', 'regards', 'respectfully',
                'furthermore', 'however', 'therefore', 'nevertheless'
            ]

            informal_words = [
                'hey', 'hi', 'yeah', 'ok', 'cool', 'awesome', 'gonna', 'wanna'
            ]

            formal_count = sum(1 for word in words if word.lower() in formal_words)
            informal_count = sum(1 for word in words if word.lower() in informal_words)

            if formal_count + informal_count > 0:
                style_analysis['formality_score'] = formal_count / (formal_count + informal_count)

            # Complexity indicators
            complex_words = sum(1 for word in words if len(word) > 8)
            avg_word_length = sum(len(word) for word in words) / len(words)

            style_analysis['complexity_score'] = min(
                (complex_words / len(words)) * 2 + (avg_word_length / 10), 1.0
            )

            # Authenticity red flags
            authenticity_penalties = 0.0

            # Excessive repetition
            unique_words = len(set(word.lower() for word in words))
            if len(words) > 0:
                repetition_ratio = 1 - (unique_words / len(words))
                if repetition_ratio > 0.7:
                    authenticity_penalties += 0.3
                    style_analysis['style_indicators'].append('High repetition detected')

            # Inconsistent capitalization
            cap_inconsistencies = len(re.findall(r'\b[a-z]+[A-Z]+[a-z]*\b', text))
            if cap_inconsistencies > 2:
                authenticity_penalties += 0.2
                style_analysis['style_indicators'].append('Inconsistent capitalization')

            # Excessive punctuation
            excessive_punct = len(re.findall(r'[!]{3,}|[?]{3,}|[.]{3,}', text))
            if excessive_punct > 1:
                authenticity_penalties += 0.1
                style_analysis['style_indicators'].append('Excessive punctuation')

            # Grammar inconsistencies
            grammar_errors = LinguisticAnalyzer.analyze_grammar_quality(text)
            if grammar_errors['overall_quality'] < 0.5:
                authenticity_penalties += 0.2
                style_analysis['style_indicators'].append('Poor grammar quality')

            style_analysis['authenticity_score'] = max(0.0, 1.0 - authenticity_penalties)

            return style_analysis

        except Exception as e:
            logger.error(f"Writing style analysis failed: {e}")
            return {
                'formality_score': 0.5,
                'complexity_score': 0.5,
                'authenticity_score': 0.5,
                'style_indicators': ['Analysis failed']
            }

    @staticmethod
    def get_comprehensive_analysis(text: str) -> Dict[str, any]:
        """
        Get comprehensive linguistic analysis combining all methods

        Args:
            text: Text to analyze

        Returns:
            Complete linguistic analysis
        """
        try:
            analysis = {
                'basic_features': LinguisticAnalyzer.extract_features(text),
                'grammar_quality': LinguisticAnalyzer.analyze_grammar_quality(text),
                'language_patterns': LinguisticAnalyzer.detect_language_patterns(text),
                'writing_style': LinguisticAnalyzer.analyze_writing_style(text)
            }

            # Calculate overall linguistic risk score
            risk_factors = []

            # High emotional intensity
            if analysis['basic_features']['emotional_intensity'] > 0.6:
                risk_factors.append('high_emotional_intensity')

            # Poor readability
            if analysis['basic_features']['readability_score'] < 30:
                risk_factors.append('poor_readability')

            # High repetition
            if analysis['basic_features']['repetition_score'] > 0.5:
                risk_factors.append('high_repetition')

            # Grammar issues
            if analysis['grammar_quality']['overall_quality'] < 0.5:
                risk_factors.append('poor_grammar')

            # Machine translation indicators
            if analysis['language_patterns']['likely_machine_translated']:
                risk_factors.append('machine_translation')

            # Low authenticity
            if analysis['writing_style']['authenticity_score'] < 0.5:
                risk_factors.append('low_authenticity')

            analysis['risk_factors'] = risk_factors
            analysis['overall_linguistic_risk'] = min(len(risk_factors) / 6.0, 1.0)

            return analysis

        except Exception as e:
            logger.error(f"Comprehensive linguistic analysis failed: {e}")
            return {
                'basic_features': LinguisticAnalyzer._get_empty_features(),
                'grammar_quality': {'overall_quality': 0.5},
                'language_patterns': {'likely_machine_translated': False},
                'writing_style': {'authenticity_score': 0.5},
                'risk_factors': ['analysis_failed'],
                'overall_linguistic_risk': 0.5
            }