from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import uvicorn
from typing import Dict, List
import logging
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse

# Load environment variables FIRST
load_dotenv()

# Configure logging BEFORE trying imports
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

# Now try to import enhanced modules with proper error handling
try:
    from analyzers.threat_analyzer import EnhancedThreatAnalyzer, ThreatAnalysis
    from utils.threat_calculator import ThreatLevelCalculator
    from utils.summary_generator import ThreatSummaryGenerator

    ENHANCED_MODULES_AVAILABLE = True
    logger.info("Enhanced modules loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced modules not available: {e}")
    logger.info("Using fallback analyzer")
    ENHANCED_MODULES_AVAILABLE = False

app = FastAPI(title="PhishEye Threat Intelligence API", version="2.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:8090').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class EmailRequest(BaseModel):
    text: str
    max_length: int = int(os.getenv('MAX_SEQUENCE_LENGTH', 512))


class ThreatAnalysis(BaseModel):
    urgency_score: float
    financial_risk: float
    suspicious_urls: List[str]
    threat_keywords: List[str]
    impersonation_indicators: List[str]
    risk_factors: Dict[str, int]
    technique_classification: str
    overall_risk_score: float


class EnhancedPredictionResponse(BaseModel):
    label: str
    score: float
    confidence: float
    threat_analysis: ThreatAnalysis
    text_stats: Dict[str, int]


# Global model variables
model = None
tokenizer = None

# Fallback analyzer - always available
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
    'lawsuit', 'attorney', 'investigation', 'compliance', 'regulation'
]


class FallbackThreatAnalyzer:
    @staticmethod
    async def analyze_text_enhanced(text: str) -> dict:
        """Fallback analyzer when enhanced modules aren't available"""
        try:
            text_lower = text.lower()

            # Basic keyword matching
            urgency_matches = [kw for kw in URGENCY_KEYWORDS if kw in text_lower]
            financial_matches = [kw for kw in FINANCIAL_KEYWORDS if kw in text_lower]
            authority_matches = [kw for kw in AUTHORITY_KEYWORDS if kw in text_lower]

            # Basic URL analysis
            urls = re.findall(r'http[s]?://\S+', text)
            suspicious_urls = []
            for url in urls:
                if any(suspicious in url.lower() for suspicious in ['bit.ly', 'tinyurl', 't.co']) or len(url) > 50:
                    suspicious_urls.append(url)

            # Basic scoring
            urgency_score = min(len(urgency_matches) / 3.0, 1.0)
            financial_risk = min(len(financial_matches) / 2.0, 1.0)

            # Enhanced grammar analysis
            grammar_errors = len(re.findall(r'[A-Z]{3,}', text))  # All caps words
            grammar_errors += len(re.findall(r'[!]{2,}', text))  # Multiple exclamations

            # Overall risk calculation
            overall_risk = (
                    urgency_score * 0.3 +
                    financial_risk * 0.4 +
                    (len(suspicious_urls) > 0) * 0.2 +
                    min(grammar_errors / 5.0, 1.0) * 0.1
            )

            # Technique classification
            if len(financial_matches) >= 2:
                technique = "Financial Phishing"
            elif len(authority_matches) >= 1:
                technique = "Authority Impersonation"
            elif len(urgency_matches) >= 3:
                technique = "Urgency-Based Phishing"
            else:
                technique = "Generic Phishing"

            return {
                'urgency_score': urgency_score,
                'financial_risk': financial_risk,
                'suspicious_urls': suspicious_urls,
                'threat_keywords': list(set(urgency_matches + financial_matches + authority_matches))[:10],
                'impersonation_indicators': authority_matches,
                'risk_factors': {
                    'urgency_indicators': len(urgency_matches),
                    'financial_threats': len(financial_matches),
                    'authority_impersonation': len(authority_matches),
                    'suspicious_urls': len(suspicious_urls),
                    'grammar_errors': grammar_errors,
                    'excessive_punctuation': len(re.findall(r'[!]{2,}', text))
                },
                'technique_classification': technique,
                'overall_risk_score': min(overall_risk, 1.0)
            }
        except Exception as e:
            logger.error(f"Fallback analyzer failed: {e}")
            # Ultra-basic fallback
            return {
                'urgency_score': 0.5,
                'financial_risk': 0.5,
                'suspicious_urls': [],
                'threat_keywords': [],
                'impersonation_indicators': [],
                'risk_factors': {
                    'urgency_indicators': 0,
                    'financial_threats': 0,
                    'authority_impersonation': 0,
                    'suspicious_urls': 0,
                    'grammar_errors': 0,
                    'excessive_punctuation': 0
                },
                'technique_classification': 'Generic Phishing',
                'overall_risk_score': 0.5
            }


@app.on_event("startup")
async def load_model():
    """Load the fine-tuned model on startup"""
    global model, tokenizer
    try:
        model_path = os.getenv('MODEL_PATH', '../../model/')
        logger.info(f"Loading model from {model_path}")

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        model.eval()
        logger.info("model loaded successfuly")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "2.1.0",
        "enhanced_modules": ENHANCED_MODULES_AVAILABLE,
        "analyzer_type": "enhanced" if ENHANCED_MODULES_AVAILABLE else "fallback",
        "enhancements": [
            "contextual_keyword_analysis" if ENHANCED_MODULES_AVAILABLE else "basic_keyword_analysis",
            "enhanced_url_detection",
            "adaptive_risk_weights" if ENHANCED_MODULES_AVAILABLE else "static_risk_weights",
            "improved_grammar_detection",
            "threat_categorization"
        ]
    }


@app.post("/predict", response_model=EnhancedPredictionResponse)
async def predict_phishing(request: EmailRequest) -> EnhancedPredictionResponse:
    """prediction with threat intelligence"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        start_time = datetime.now()

        # Tokenize input
        inputs = tokenizer(
            request.text,
            truncation=True,
            padding=True,
            max_length=request.max_length,
            return_tensors="pt"
        )

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)

        # Get prediction
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_class].item()

        # Map to labels
        label_map = {0: "legitimate", 1: "phishing"}
        predicted_label = label_map[predicted_class]
        score = probabilities[0][1].item()  # Phishing probability

        # Enhanced Threat Analysis
        if ENHANCED_MODULES_AVAILABLE:
            try:
                threat_analysis_result = await EnhancedThreatAnalyzer.analyze_text_enhanced(request.text)
                threat_analysis = ThreatAnalysis(
                    urgency_score=threat_analysis_result.urgency_score,
                    financial_risk=threat_analysis_result.financial_risk,
                    suspicious_urls=threat_analysis_result.suspicious_urls,
                    threat_keywords=threat_analysis_result.threat_keywords,
                    impersonation_indicators=threat_analysis_result.impersonation_indicators,
                    risk_factors=threat_analysis_result.risk_factors,
                    technique_classification=threat_analysis_result.technique_classification,
                    overall_risk_score=threat_analysis_result.overall_risk_score
                )
            except Exception as e:
                logger.warning(f"Enhanced analyzer failed, using fallback: {e}")
                threat_analysis_dict = await FallbackThreatAnalyzer.analyze_text_enhanced(request.text)
                threat_analysis = ThreatAnalysis(**threat_analysis_dict)
        else:
            # Use fallback analyzer
            threat_analysis_dict = await FallbackThreatAnalyzer.analyze_text_enhanced(request.text)
            threat_analysis = ThreatAnalysis(**threat_analysis_dict)

        # Text Statistics
        text_stats = {
            "character_count": len(request.text),
            "word_count": len(request.text.split()),
            "sentence_count": len(re.split(r'[.!?]+', request.text)),
            "url_count": len(re.findall(r'http[s]?://\S+', request.text))
        }

        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        logger.info(f"Analysis completed in {processing_time:.2f}ms - Label: {predicted_label}, Score: {score:.3f}")

        return EnhancedPredictionResponse(
            label=predicted_label,
            score=score,
            confidence=confidence,
            threat_analysis=threat_analysis,
            text_stats=text_stats
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# Laravel-compatible endpoint
@app.post("/api/analyze-text")
async def analyze_text_laravel_compatible(request: EmailRequest):
    """Laravel-compatible endpoint"""
    try:
        # Get enhanced prediction
        prediction = await predict_phishing(request)

        # Calculate threat level (simplified)
        overall_risk = prediction.threat_analysis.overall_risk_score
        if overall_risk >= 0.8:
            threat_level = "critical"
        elif overall_risk >= 0.6:
            threat_level = "high"
        elif overall_risk >= 0.4:
            threat_level = "medium"
        elif overall_risk >= 0.2:
            threat_level = "low"
        else:
            threat_level = "minimal"

        # Generate simple summary
        threat_summary = []
        if prediction.threat_analysis.urgency_score > 0.5:
            threat_summary.append("High urgency language detected with time pressure tactics")
        if prediction.threat_analysis.financial_risk > 0.5:
            threat_summary.append("Financial threat indicators present")
        if len(prediction.threat_analysis.suspicious_urls) > 0:
            threat_summary.append(
                f"Suspicious URL patterns identified ({len(prediction.threat_analysis.suspicious_urls)} URLs)")

        # Return exact format your Laravel backend expects
        return {
            "success": True,
            "analysis": {
                "label": prediction.label,
                "score": prediction.score,
                "confidence": prediction.confidence,
                "threat_analysis": {
                    "overall_risk_score": prediction.threat_analysis.overall_risk_score,
                    "urgency_score": prediction.threat_analysis.urgency_score,
                    "financial_risk": prediction.threat_analysis.financial_risk,
                    "technique_classification": prediction.threat_analysis.technique_classification,
                    "risk_factors": prediction.threat_analysis.risk_factors,
                    "suspicious_urls": prediction.threat_analysis.suspicious_urls,
                    "threat_keywords": prediction.threat_analysis.threat_keywords
                },
                "text_stats": prediction.text_stats
            },
            "enhanced_metadata": {
                "threat_level": threat_level,
                "risk_category": "financial_phishing" if prediction.threat_analysis.financial_risk > 0.5 else "generic_phishing"
            },
            "threat_summary": threat_summary if threat_summary else ["Basic threat patterns detected"],
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "model_version": "xlm-roberta-enhanced-v2.1",
                "processing_time_ms": 1200
            }
        }

    except Exception as e:
        logger.error(f"Laravel-compatible analysis error: {e}")
        return {
            "success": False,
            "error": f"Analysis failed: {str(e)}"
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv('API_HOST', '127.0.0.1'),
        port=int(os.getenv('API_PORT', 8000)),
        reload=True,
        log_level=os.getenv('LOG_LEVEL', 'info').lower()
    )