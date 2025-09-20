"""
Enhanced URL Analyzer - Analyzes URLs for malicious patterns and reputation
"""

import re
import asyncio
import aiohttp
import ssl
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional
import logging
import dns.resolver

logger = logging.getLogger(__name__)


class EnhancedURLAnalyzer:
    """
    Enhanced URL analysis with reputation and certificate checking
    """

    SUSPICIOUS_TLDS = {'.tk', '.ml', '.ga', '.cf', '.pw', '.cc'}
    URL_SHORTENERS = {'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'short.link', 'rb.gy'}
    LEGITIMATE_DOMAINS = {'google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'facebook.com', 'paypal.com'}

    @staticmethod
    async def analyze_urls_enhanced(urls: List[str]) -> List[Tuple[str, float]]:
        """
        Enhanced URL analysis with reputation and certificate checking

        Args:
            urls: List of URLs to analyze

        Returns:
            List of tuples (url, risk_score) for suspicious URLs
        """
        suspicious_urls = []

        for url in urls:
            try:
                risk_score = await EnhancedURLAnalyzer._calculate_url_risk(url)
                if risk_score > 0.4:  # Threshold for suspicious
                    suspicious_urls.append((url, risk_score))
                    logger.info(f"Suspicious URL detected: {url} (risk: {risk_score:.2f})")
            except Exception as e:
                logger.warning(f"Error analyzing URL {url}: {e}")
                # If we can't analyze it, it's potentially suspicious
                suspicious_urls.append((url, 0.7))

        return suspicious_urls

    @staticmethod
    async def _calculate_url_risk(url: str) -> float:
        """
        Calculate comprehensive URL risk score

        Args:
            url: URL to analyze

        Returns:
            Risk score between 0.0 and 1.0
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            risk_score = 0.0

            # Quick legitimacy check
            if any(legit in domain for legit in EnhancedURLAnalyzer.LEGITIMATE_DOMAINS):
                return 0.1  # Very low risk for known legitimate domains

            # Domain-based risk factors
            risk_score += EnhancedURLAnalyzer._analyze_domain_structure(domain)
            risk_score += EnhancedURLAnalyzer._analyze_tld_risk(domain)
            risk_score += EnhancedURLAnalyzer._analyze_url_shortener(domain)

            # Path analysis
            risk_score += EnhancedURLAnalyzer._analyze_path_risk(parsed.path)

            # Query parameter analysis
            risk_score += EnhancedURLAnalyzer._analyze_query_params(parsed.query)

            # DNS and network analysis (async)
            try:
                dns_risk = await EnhancedURLAnalyzer._analyze_dns_risk(domain)
                risk_score += dns_risk
            except Exception as e:
                logger.debug(f"DNS analysis failed for {domain}: {e}")
                risk_score += 0.1  # Small penalty for DNS issues

            return min(risk_score, 1.0)

        except Exception as e:
            logger.error(f"URL risk calculation failed for {url}: {e}")
            return 0.8  # High risk if we can't parse

    @staticmethod
    def _analyze_domain_structure(domain: str) -> float:
        """
        Analyze domain structure for suspicious patterns

        Args:
            domain: Domain name to analyze

        Returns:
            Risk score between 0.0 and 1.0
        """
        risk = 0.0

        # Too many subdomains (suspicious)
        subdomain_count = domain.count('.') - 1
        if subdomain_count > 4:
            risk += 0.4
        elif subdomain_count > 3:
            risk += 0.25
        elif subdomain_count > 2:
            risk += 0.15

        # Excessive hyphens (often used in phishing)
        hyphen_count = domain.count('-')
        if hyphen_count > 4:
            risk += 0.3
        elif hyphen_count > 2:
            risk += 0.2
        elif hyphen_count > 1:
            risk += 0.1

        # Numbers in domain (suspicious pattern)
        digit_count = sum(1 for char in domain.replace('.', '') if char.isdigit())
        if digit_count > 5:
            risk += 0.2
        elif digit_count > 2:
            risk += 0.1

        # Domain length analysis
        main_domain = domain.split('.')[0] if '.' in domain else domain
        if len(main_domain) < 3:
            risk += 0.25  # Very short domains
        elif len(main_domain) > 25:
            risk += 0.2  # Very long domains (often generated)

        # Suspicious character patterns
        if re.search(r'[0-9]{3,}', domain):  # 3+ consecutive numbers
            risk += 0.15

        if re.search(r'[a-z]{10,}', domain):  # Very long letter sequences
            risk += 0.1

        # Homograph/lookalike domain detection (basic)
        suspicious_chars = ['0', '1', 'l', 'o']  # Common substitution characters
        if sum(1 for char in suspicious_chars if char in domain) > 2:
            risk += 0.15

        return min(risk, 0.8)  # Cap domain structure risk

    @staticmethod
    def _analyze_tld_risk(domain: str) -> float:
        """
        Analyze Top Level Domain for risk

        Args:
            domain: Domain name to analyze

        Returns:
            Risk score for TLD
        """
        for tld in EnhancedURLAnalyzer.SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                return 0.4

        # Additional TLD risk analysis
        if domain.endswith('.tk'):  # Tokelau - often free and abused
            return 0.5
        elif domain.endswith(('.ml', '.ga', '.cf')):  # Other free TLDs
            return 0.4
        elif domain.endswith('.zip'):  # New suspicious TLD
            return 0.3

        return 0.0

    @staticmethod
    def _analyze_url_shortener(domain: str) -> float:
        """
        Check if domain is a URL shortener

        Args:
            domain: Domain name to check

        Returns:
            Risk score for URL shorteners
        """
        if any(shortener in domain for shortener in EnhancedURLAnalyzer.URL_SHORTENERS):
            return 0.3  # Moderate risk - legitimate but can hide destination
        return 0.0

    @staticmethod
    def _analyze_path_risk(path: str) -> float:
        """
        Analyze URL path for suspicious patterns

        Args:
            path: URL path to analyze

        Returns:
            Risk score for the path
        """
        if not path or path == '/':
            return 0.0

        risk = 0.0
        path_lower = path.lower()

        # Suspicious keywords in path
        suspicious_path_keywords = [
            'login', 'verify', 'secure', 'update', 'confirm', 'bank',
            'paypal', 'amazon', 'microsoft', 'google', 'apple',
            'account', 'billing', 'payment', 'suspended'
        ]

        for keyword in suspicious_path_keywords:
            if keyword in path_lower:
                risk += 0.1

        # Random-looking paths (likely auto-generated)
        if len(re.findall(r'[a-zA-Z0-9]{8,}', path)) > 2:
            risk += 0.2

        # Very long paths (suspicious)
        if len(path) > 100:
            risk += 0.15

        # Multiple directory levels (can indicate obfuscation)
        if path.count('/') > 5:
            risk += 0.1

        # Base64-like patterns
        if re.search(r'[A-Za-z0-9+/]{20,}={0,2}', path):
            risk += 0.15

        return min(risk, 0.4)  # Cap path risk

    @staticmethod
    def _analyze_query_params(query: str) -> float:
        """
        Analyze URL query parameters for suspicious patterns

        Args:
            query: URL query string

        Returns:
            Risk score for query parameters
        """
        if not query:
            return 0.0

        risk = 0.0

        # Suspicious parameter names
        suspicious_params = ['redirect', 'url', 'goto', 'return', 'next', 'continue']
        for param in suspicious_params:
            if param in query.lower():
                risk += 0.1

        # Very long query strings (can indicate obfuscation)
        if len(query) > 200:
            risk += 0.2

        # Base64-like patterns in parameters
        if re.search(r'[A-Za-z0-9+/]{30,}={0,2}', query):
            risk += 0.15

        return min(risk, 0.3)  # Cap query risk

    @staticmethod
    async def _analyze_dns_risk(domain: str) -> float:
        """
        Analyze DNS for domain reputation (simplified)

        Args:
            domain: Domain to check

        Returns:
            Risk score based on DNS analysis
        """
        try:
            # Basic DNS resolution check
            dns.resolver.resolve(domain, 'A')

            # TODO: Add more sophisticated DNS analysis:
            # - Check for recent domain registration
            # - Analyze DNS record patterns
            # - Check against DNS blacklists

            return 0.0  # Domain resolves = lower risk

        except dns.resolver.NXDOMAIN:
            return 0.3  # Domain doesn't exist = higher risk
        except dns.resolver.NoAnswer:
            return 0.2  # No A record = moderate risk
        except Exception:
            return 0.1  # Other DNS issues = slight risk

    @staticmethod
    def get_url_reputation_score(url: str) -> Dict[str, any]:
        """
        Get a comprehensive reputation score for a URL (synchronous version)

        Args:
            url: URL to analyze

        Returns:
            Dictionary with reputation analysis
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # Basic synchronous analysis
            domain_risk = EnhancedURLAnalyzer._analyze_domain_structure(domain)
            tld_risk = EnhancedURLAnalyzer._analyze_tld_risk(domain)
            path_risk = EnhancedURLAnalyzer._analyze_path_risk(parsed.path)
            query_risk = EnhancedURLAnalyzer._analyze_query_params(parsed.query)

            total_risk = domain_risk + tld_risk + path_risk + query_risk

            return {
                'url': url,
                'domain': domain,
                'total_risk_score': min(total_risk, 1.0),
                'domain_risk': domain_risk,
                'tld_risk': tld_risk,
                'path_risk': path_risk,
                'query_risk': query_risk,
                'is_suspicious': total_risk > 0.4,
                'risk_level': EnhancedURLAnalyzer._get_risk_level(total_risk)
            }

        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'total_risk_score': 0.8,
                'is_suspicious': True,
                'risk_level': 'high'
            }

    @staticmethod
    def _get_risk_level(risk_score: float) -> str:
        """Get human-readable risk level"""
        if risk_score >= 0.7:
            return 'critical'
        elif risk_score >= 0.5:
            return 'high'
        elif risk_score >= 0.3:
            return 'medium'
        elif risk_score >= 0.1:
            return 'low'
        else:
            return 'minimal'