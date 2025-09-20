import axios from 'axios'

export default {
  name: 'AnalyzeView',
  data() {
    return {
      emailText: '',
      isAnalyzing: false,
      analysisResults: null,
      errorMessage: null,
      // File upload state
      selectedFile: null,
      isProcessingFile: false,
      fileError: null,
      // Animation state for progress bars
      animatedOverallRisk: 0,
      animatedUrgency: 0,
      animatedFinancialRisk: 0,
      animatedPhishing: 0,
      animatedConfidence: 0
    }
  },
  computed: {
    confidencePercentage() {
      return this.analysisResults ? (this.analysisResults.analysis.confidence * 100).toFixed(3) : 0
    },
    phishingPercentage() {
      return this.analysisResults ? (this.analysisResults.analysis.score * 100).toFixed(3) : 0
    },
    overallRiskPercentage() {
      return this.analysisResults?.analysis?.threat_analysis ? 
        (this.analysisResults.analysis.threat_analysis.overall_risk_score * 100).toFixed(3) : 0
    },
    urgencyPercentage() {
      return this.analysisResults?.analysis?.threat_analysis ? 
        (this.analysisResults.analysis.threat_analysis.urgency_score * 100).toFixed(3) : 0
    },
    financialRiskPercentage() {
      return this.analysisResults?.analysis?.threat_analysis ? 
        (this.analysisResults.analysis.threat_analysis.financial_risk * 100).toFixed(3) : 0
    },
    resultIcon() {
      return this.analysisResults?.analysis.label === 'phishing' ? '⚠️' : '✅'
    },
    epicResultClass() {
      if (!this.analysisResults) return ''
      return this.analysisResults.analysis.label === 'phishing' 
        ? 'bg-gradient-to-br from-red-900 via-red-800 to-red-900 border-red-500 text-white shadow-red-500/20' 
        : 'bg-gradient-to-br from-green-900 via-green-800 to-green-900 border-green-500 text-white shadow-green-500/20'
    },
    threatLevel() {
      return this.analysisResults?.enhanced_metadata?.threat_level || 'unknown'
    },
    threatLevelText() {
      const level = this.threatLevel
      const levelMap = {
        'critical': 'CRITICAL THREAT DETECTED',
        'high': 'HIGH RISK EMAIL IDENTIFIED', 
        'medium': 'MEDIUM RISK ASSESSMENT',
        'low': 'LOW RISK DETECTED',
        'minimal': 'MINIMAL THREAT LEVEL',
        'unknown': 'Risk Assessment Unavailable'
      }
      return levelMap[level] || 'Assessment Complete'
    },
    threatLevelBadgeClass() {
      const level = this.threatLevel
      const classMap = {
        'critical': 'bg-red-600 text-white',
        'high': 'bg-red-500 text-white',
        'medium': 'bg-yellow-500 text-black',
        'low': 'bg-green-500 text-white',
        'minimal': 'bg-green-600 text-white',
        'unknown': 'bg-gray-500 text-white'
      }
      return classMap[level] || 'bg-gray-500 text-white'
    },
    attackType() {
      return this.analysisResults?.analysis?.threat_analysis?.technique_classification || 'Unknown'
    },
    riskFactors() {
      return this.analysisResults?.analysis?.threat_analysis?.risk_factors || {}
    },
    hasRiskFactors() {
      return Object.values(this.riskFactors).some(value => value > 0)
    },
    suspiciousUrls() {
      return this.analysisResults?.analysis?.threat_analysis?.suspicious_urls || []
    },
    threatKeywords() {
      return this.analysisResults?.analysis?.threat_analysis?.threat_keywords || []
    },
    threatSummary() {
      return this.analysisResults?.threat_summary || []
    },
    textStats() {
      return this.analysisResults?.analysis?.text_stats || {
        character_count: 0,
        word_count: 0, 
        sentence_count: 0,
        url_count: 0
      }
    }
  },
  watch: {
    analysisResults(newVal) {
      if (newVal) {
        this.animateProgressBars()
      }
    }
  },
  methods: {
    // Example loading methods
    loadExample(type) {
      const examples = {
        phishing: "URGENT! Your PayPal account has been suspended due to suspicious activity. Click here immediately to verify your identity or your account will be permanently closed within 24 hours! We detected unauthorized access from Nigeria. Please update your payment information now: http://bit.ly/paypal-verify-now",
        legitimate: "Hi team, please find attached the quarterly report for your review. The meeting is scheduled for tomorrow at 2 PM in conference room A. Best regards, John from Finance Department. If you have any questions, feel free to reach out.",
        sophisticated: "Dear Valued Customer, We have noticed some unusual activity on your account and want to ensure your security. As part of our regular security review, please verify your account information within 48 hours. Our team is available to assist you. Thank you for choosing our services. Customer Service Team"
      }
      
      this.emailText = examples[type] || ''
      this.clearResults()
    },

    clearText() {
      this.emailText = ''
      this.clearResults()
    },

    // File handling methods
    handleFileProcessed(result) {
      if (result.processing) {
        this.isProcessingFile = true
        this.fileError = null
      } else if (result.success) {
        this.selectedFile = result.file
        this.emailText = result.content
        this.isProcessingFile = false
        this.fileError = null
        this.clearResults()
      } else if (result.error) {
        this.fileError = result.error
        this.isProcessingFile = false
        this.selectedFile = null
      }
    },

    handleFileCleared() {
      this.selectedFile = null
      this.fileError = null
      this.isProcessingFile = false
    },

    // Results and animation methods
    clearResults() {
      this.analysisResults = null
      this.errorMessage = null
      this.resetAnimatedValues()
    },

    resetAnimatedValues() {
      this.animatedOverallRisk = 0
      this.animatedUrgency = 0
      this.animatedFinancialRisk = 0
      this.animatedPhishing = 0
      this.animatedConfidence = 0
    },

    animateProgressBars() {
      this.resetAnimatedValues()
      
      setTimeout(() => {
        this.animateValue('animatedOverallRisk', this.overallRiskPercentage, 2000)
      }, 500)
      
      setTimeout(() => {
        this.animateValue('animatedUrgency', this.urgencyPercentage, 1800)
      }, 800)
      
      setTimeout(() => {
        this.animateValue('animatedFinancialRisk', this.financialRiskPercentage, 2000)
      }, 1100)
      
      setTimeout(() => {
        this.animateValue('animatedPhishing', this.phishingPercentage, 2200)
      }, 1400)
      
      setTimeout(() => {
        this.animateValue('animatedConfidence', this.confidencePercentage, 1600)
      }, 1700)
    },

    animateValue(property, targetValue, duration) {
      const startValue = 0
      const startTime = performance.now()
      
      const animate = (currentTime) => {
        const elapsed = currentTime - startTime
        const progress = Math.min(elapsed / duration, 1)
        const easeOutCubic = 1 - Math.pow(1 - progress, 3)
        
        this[property] = startValue + (targetValue - startValue) * easeOutCubic
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          this[property] = targetValue
        }
      }
      
      requestAnimationFrame(animate)
    },

    // Analysis method
    async analyzeEmail() {
      if (!this.emailText.trim()) return

      this.isAnalyzing = true
      this.errorMessage = null
      this.analysisResults = null

      try {
        const response = await axios.post('http://127.0.0.1:8090/api/predict', {
          text: this.emailText
        })

        if (response.data.success) {
          this.analysisResults = response.data
        } else {
          this.errorMessage = response.data.error || 'Analysis failed'
        }
      } catch (error) {
        console.error('Analysis error:', error)
        this.errorMessage = 'Failed to connect to analysis service. Make sure your Laravel backend is running on port 8090.'
      } finally {
        this.isAnalyzing = false
      }
    },

    // Utility methods
    getRiskBarColor(score) {
      if (score >= 0.7) return 'bg-gradient-to-r from-red-600 to-red-700'
      if (score >= 0.5) return 'bg-gradient-to-r from-orange-500 to-orange-600'
      if (score >= 0.3) return 'bg-gradient-to-r from-yellow-500 to-yellow-600'
      return 'bg-gradient-to-r from-green-500 to-green-600'
    },

    formatRiskFactor(key) {
      const factorMap = {
        'urgency_indicators': 'Urgency',
        'financial_threats': 'Financial',
        'authority_impersonation': 'Authority',
        'suspicious_urls': 'URLs',
        'grammar_errors': 'Grammar',
        'excessive_punctuation': 'Punctuation'
      }
      return factorMap[key] || key
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}