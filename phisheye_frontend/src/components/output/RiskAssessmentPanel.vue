<template>
  <div class="lg:col-span-2 rounded-2xl p-6 shadow-2xl bg-white/5 backdrop-blur-sm border border-white/10">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">

        <div>
          <h3 class="text-xl font-bold text-white">Scanning Results</h3>
          <p class="text-gray-400 text-sm">{{
            formatDate(analysisResults?.analysis?.enhanced_metadata?.analysis_timestamp) }}</p>
        </div>
      </div>

      <!-- Threat Level Badge -->
      <div class="flex items-center space-x-2">
        <div :class="getThreatLevelBadgeClass()"
          class="px-3 py-1 rounded-full font-bold text-xs uppercase tracking-wider">
          {{ getThreatLevel() }}
        </div>
        <div class="text-2xl">{{ getResultIcon() }}</div>
      </div>
    </div>

    <!-- Main Risk Scores -->
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-2">
          <span class="text-gray-300 font-medium text-sm">Overall Risk</span>
          <span class="text-lg font-bold text-white">{{ overallRiskPercentage }}%</span>
        </div>
        <div class="w-full bg-gray-800/50 rounded-full h-2 relative overflow-hidden">
          <div :class="getRiskBarColor(overallRiskScore) + ' rounded-full transition-all duration-2000 ease-out h-full'"
            :style="{ width: animatedOverallRisk + '%' }"></div>
        </div>
      </div>

      <div>
       

   <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-2">
          <span class="text-gray-300 font-medium text-sm">Confidence</span>
          <span class="text-lg font-bold text-white">{{ confidencePercentage }}%</span>
        </div>
        <div class="w-full bg-gray-800/50 rounded-full h-2 relative overflow-hidden">
          <div
            class="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-2000 ease-out h-full"
            :style="{ width: animatedConfidence + '%' }"></div>
        </div>
      </div>
      </div>

 <!--Lege div  -->
          <div class="bg-black/20 rounded-lg p-3 border border-red/5 cursor-pointer" @click="downloadPDF">
            <div class="flex items-center justify-between mb-2">
            <span class="text-white font-medium text-md">Download Results </span>
            <span class="text-lg font-bold"><PhFilePdf :size="32" color="#ffffff" /></span>
          </div>
        </div>
        <!--Lege div  -->
   

    </div>

    <!-- Risk Factors Grid -->
    <div class="grid grid-cols-2 gap-3 mb-4">
      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center">
            <span class="text-sm mr-2"></span>
            <span class="text-gray-300 font-medium text-xs">Urgency indicators</span>
          </div>
          <span class="text-white font-bold text-sm">{{ getRiskFactorValue('urgency_indicators') }}</span>
        </div>

      </div>

      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center">
            <span class="text-sm mr-2"></span>
            <span class="text-gray-300 font-medium text-xs">Financial Thread count</span>
          </div>
          <span class="text-white font-bold text-sm">{{ getRiskFactorValue('financial_threats') }}</span>
        </div>
      </div>

      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center">
            <span class="text-sm mr-2"></span>
            <span class="text-gray-300 font-medium text-xs">URL Count</span>
          </div>
          <span class="text-white font-bold text-sm">{{ getRiskFactorValue('suspicious_urls') }}</span>
        </div>

      </div>

      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center">
            <span class="text-sm mr-2"></span>
            <span class="text-gray-300 font-medium text-sm">Authority impersonations</span>
          </div>
          <span class="text-white font-bold text-sm">{{ getRiskFactorValue('authority_impersonation') }}</span>
        </div>

      </div>
    </div>

    <!-- Attack Type & Category -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between">
          <span class="text-gray-300 font-medium text-xs">Attack Type</span>
          <span class="px-2 py-1 bg-red-500/20 text-red-300 rounded text-xs font-medium border border-red-500/30">
            {{ getAttackTypeShort() }}
          </span>
        </div>
      </div>

      <div class="bg-black/20 rounded-lg p-3 border border-white/5">
        <div class="flex items-center justify-between">
          <span class="text-gray-300 font-medium text-xs">Processing time</span>
          <span class="text-white font-mono text-xs">~ {{ getProcessingTime() }} ms</span>
        </div>
      </div>
    </div>

    <!-- Threat Keywords (if any) -->
    <div v-if="threatKeywords.length > 0" class="mt-4">
      <div class="text-gray-300 font-medium text-xs mb-2">Detected Keywords:</div>
      <div class="flex flex-wrap gap-1">
        <span v-for="keyword in threatKeywords.slice(0, 6)" :key="keyword"
          class="px-2 py-1 bg-red-500/10 text-red-300 rounded text-xs font-medium border border-red-500/20">
          {{ keyword }}
        </span>
        <span v-if="threatKeywords.length > 6" class="px-2 py-1 bg-gray-500/20 text-gray-300 rounded text-xs">
          +{{ threatKeywords.length - 6 }} more
        </span>
      </div>
    </div>
  </div>
</template>

<script>

import { PhFilePdf  } from '@phosphor-icons/vue';
import pdfGenerator from '@/scripts/pdfGenerator'

export default {
  name: 'CompactRiskAssessmentPanel',
    components: {
    PhFilePdf 
  },
  props: {
    analysisResults: {
      type: Object,
      required: true
    },
    animatedOverallRisk: { type: Number, default: 0 },
    animatedUrgency: { type: Number, default: 0 },
    animatedFinancialRisk: { type: Number, default: 0 },
    animatedPhishing: { type: Number, default: 0 },
    animatedConfidence: { type: Number, default: 0 }
  },
  computed: {
    overallRiskScore() {
      return this.analysisResults?.analysis?.threat_analysis?.overall_risk_score || 0
    },

    overallRiskPercentage() {
      return (this.overallRiskScore * 100).toFixed(3)
    },

    urgencyPercentage() {
      const score = this.analysisResults?.analysis?.threat_analysis?.urgency_score || 0
      return (score * 100).toFixed(3)
    },

    financialRiskPercentage() {
      const score = this.analysisResults?.analysis?.threat_analysis?.financial_risk || 0
      return (score * 100).toFixed(3)
    },

    phishingPercentage() {
      const score = this.analysisResults?.analysis?.score || 0
      return (score * 100).toFixed(3)
    },

    confidencePercentage() {
      const score = this.analysisResults?.analysis?.confidence || 0
      return (score * 100).toFixed(3)
    },

    threatKeywords() {
      return this.analysisResults?.analysis?.threat_analysis?.threat_keywords || []
    },

    riskFactors() {
      return this.analysisResults?.analysis?.threat_analysis?.risk_factors || {}
    },

    threatSummary() {
      return this.analysisResults?.analysis?.threat_summary || []
    },
  },
  methods: {
    getRiskBarColor(score) {
      if (score >= 0.7) return 'bg-gradient-to-r from-red-600 to-red-700'
      if (score >= 0.5) return 'bg-gradient-to-r from-orange-500 to-orange-600'
      if (score >= 0.3) return 'bg-gradient-to-r from-yellow-500 to-yellow-600'
      return 'bg-gradient-to-r from-green-500 to-green-600'
    },

    getPhishingBarColor() {
      const score = this.analysisResults?.analysis?.score || 0
      if (score >= 0.8) return 'bg-gradient-to-r from-red-600 to-red-700'
      if (score >= 0.6) return 'bg-gradient-to-r from-orange-500 to-orange-600'
      if (score >= 0.4) return 'bg-gradient-to-r from-yellow-500 to-yellow-600'
      return 'bg-gradient-to-r from-green-500 to-green-600'
    },
    downloadPDF() {
      const result = pdfGenerator.generateAnalysisReport(this.analysisResults)
      if (result.success) {
        console.log('PDF generated:', result.fileName)
      } else {
        console.error('PDF generation failed:', result.error)
      }
    },
    getThreatLevel() {
      const level = this.analysisResults?.analysis?.enhanced_metadata?.threat_level || 'unknown'
      return level.toUpperCase()
    },

    getThreatLevelBadgeClass() {
      const level = this.analysisResults?.analysis?.enhanced_metadata?.threat_level || 'unknown'
      const classMap = {
        'critical': 'bg-gradient-to-r from-red-600 to-red-700 text-white shadow-red-500/50',
        'high': 'bg-gradient-to-r from-red-500 to-orange-600 text-white shadow-red-500/40',
        'medium': 'bg-gradient-to-r from-yellow-500 to-orange-500 text-black shadow-yellow-500/40',
        'low': 'bg-gradient-to-r from-green-500 to-green-600 text-white shadow-green-500/40',
        'minimal': 'bg-gradient-to-r from-green-600 to-green-700 text-white shadow-green-500/50',
        'unknown': 'bg-gradient-to-r from-gray-500 to-gray-600 text-white shadow-gray-500/30'
      }
      return classMap[level] || classMap['unknown']
    },

    getResultIcon() {
      const label = this.analysisResults?.analysis?.label
      const level = this.analysisResults?.analysis?.enhanced_metadata?.threat_level

      if (label === 'phishing') {
        if (level === 'critical') return ''
        if (level === 'high') return ''
        return ''
      }
      return '✅'
    },

    getAttackTypeShort() {
      const type = this.analysisResults?.analysis?.threat_analysis?.technique_classification || 'Unknown'
      const shortMap = {
        'Financial Phishing': 'Financial',
        'Generic Phishing': 'Generic',
        'Credential Harvesting': 'Credential',
        'Business Email Compromise': 'BEC',
        'Unknown': 'Unknown'
      }
      return shortMap[type] || type.split(' ')[0]
    },

    getProcessingTime() {
      return this.analysisResults?.analysis?.enhanced_metadata?.processing_time_ms || 0.75
    },

    getRiskFactorValue(factor) {
      return this.riskFactors[factor] || 0
    },

    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>