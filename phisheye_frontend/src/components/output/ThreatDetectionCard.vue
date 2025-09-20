<template>
  <div :class="cardClass" 
    class="rounded-3xl shadow-2xl p-8 border-2 relative overflow-hidden animate-result-appear">
    
    <!-- Subtle background effect -->
    <div class="absolute inset-0 opacity-5">
      <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent transform -skew-x-12 animate-shimmer"></div>
    </div>

    <div class="relative">
      <!-- Header Section -->
      <div class="flex flex-col lg:flex-row lg:items-center justify-between mb-8">
        <div class="flex items-center mb-6 lg:mb-0">
          <div class="relative mr-6">
            <div class="w-16 h-16 rounded-full flex items-center justify-center text-3xl"
              :class="iconBackgroundClass">
              {{ resultIcon }}
            </div>
            <div v-if="isPhishing" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-ping"></div>
          </div>
          
          <div>
            <h2 class="text-3xl lg:text-4xl font-black mb-2 tracking-wide text-white">
              {{ classificationLabel }}
            </h2>
            <p class="text-lg lg:text-xl opacity-90 font-medium text-gray-100">
              {{ threatLevelText }}
            </p>
            <div class="text-sm opacity-75 mt-2 text-gray-200">
              Classification: {{ attackType }}
            </div>
          </div>
        </div>

        <div class="text-center lg:text-right">
          <div class="text-4xl lg:text-5xl font-black mb-2 text-white">
            {{ confidencePercentage }}%
          </div>
          <div class="text-base lg:text-lg opacity-75 font-medium text-gray-200">
            AI Confidence
          </div>
          <div class="mt-3 inline-block px-4 py-2 rounded-full text-sm font-bold"
            :class="threatLevelBadgeClass">
            {{ threatLevel.toUpperCase() }} RISK
          </div>
        </div>
      </div>

      <!-- AI Summary Section -->
      <div v-if="threatSummary.length > 0" class="mt-8">
        <div class="rounded-2xl p-6 backdrop-blur-sm border border-white/10"
          style="background-color: rgba(0, 0, 0, 0.1);">
          <h4 class="font-bold text-lg mb-4 flex items-center text-white">
            <span class="mr-3 w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">🧠</span>
            AI Threat Analysis Summary
          </h4>
          <div class="space-y-3">
            <div v-for="(summary, index) in threatSummary" :key="summary"
              class="flex items-start text-sm text-gray-100 animate-slide-in-right"
              :style="{ animationDelay: (index * 0.2 + 0.5) + 's' }">
              <div class="w-2 h-2 bg-blue-400 rounded-full mr-3 mt-2 flex-shrink-0"></div>
              <span>{{ summary }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ThreatDetectionCard',
  props: {
    analysisResults: {
      type: Object,
      required: true
    }
  },
  computed: {
    isPhishing() {
      return this.analysisResults?.analysis?.label === 'phishing'
    },
    
    classificationLabel() {
      return this.analysisResults?.analysis?.label?.toUpperCase() || 'UNKNOWN'
    },
    
    resultIcon() {
      return this.isPhishing ? '⚠️' : '✅'
    },
    
    cardClass() {
      return this.isPhishing 
        ? 'bg-gradient-to-br from-red-800 via-red-700 to-red-800 border-red-400 text-white shadow-red-500/20' 
        : 'bg-gradient-to-br from-green-800 via-green-700 to-green-800 border-green-400 text-white shadow-green-500/20'
    },
    
    iconBackgroundClass() {
      return this.isPhishing 
        ? 'bg-red-500/20 border-2 border-red-400/30' 
        : 'bg-green-500/20 border-2 border-green-400/30'
    },
    
    confidencePercentage() {
      return this.analysisResults ? (this.analysisResults.analysis.confidence * 100).toFixed(1) : 0
    },
    
    threatLevel() {
      return this.analysisResults?.enhanced_metadata?.threat_level || 'unknown'
    },
    
    threatLevelText() {
      const level = this.threatLevel
      const levelMap = {
        'critical': 'Critical Threat Detected',
        'high': 'High Risk Email Identified', 
        'medium': 'Medium Risk Assessment',
        'low': 'Low Risk Detected',
        'minimal': 'Minimal Threat Level',
        'unknown': 'Risk Assessment Complete'
      }
      return levelMap[level] || 'Assessment Complete'
    },
    
    threatLevelBadgeClass() {
      const level = this.threatLevel
      const classMap = {
        'critical': 'bg-red-600 text-white border border-red-400',
        'high': 'bg-red-500 text-white border border-red-300',
        'medium': 'bg-yellow-500 text-black border border-yellow-300',
        'low': 'bg-green-500 text-white border border-green-300',
        'minimal': 'bg-green-600 text-white border border-green-400',
        'unknown': 'bg-gray-500 text-white border border-gray-300'
      }
      return classMap[level] || 'bg-gray-500 text-white border border-gray-300'
    },
    
    attackType() {
      return this.analysisResults?.analysis?.threat_analysis?.technique_classification || 'Unknown'
    },
    
    threatSummary() {
      return this.analysisResults?.threat_summary || []
    }
  }
}
</script>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%) skewX(-12deg); }
  100% { transform: translateX(200%) skewX(-12deg); }
}

@keyframes result-appear {
  0% { opacity: 0; transform: scale(0.95) translateY(20px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes slide-in-right {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

.animate-shimmer { animation: shimmer 3s infinite; }
.animate-result-appear { animation: result-appear 0.8s ease-out forwards; }
.animate-slide-in-right { animation: slide-in-right 0.6s ease-out forwards; }
</style>