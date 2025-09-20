<template>
  <div class="space-y-6">
    <!-- Attack Classification -->
    <div class="rounded-2xl p-6 bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
      <div class="flex items-center mb-4">
        <div class="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center mr-3">
          <span class="text-lg"><PhHeadCircuit :size="24" color="#ffffff" /></span>
        </div>
        <h4 class="font-bold text-white">Threat Intelligence</h4>
      </div>

      <div class="space-y-4">
        <div class="flex justify-between items-center p-4 rounded-lg bg-black/20 border border-white/5">
          <span class="text-sm text-gray-300">Attack Vector:</span>
          <span class="px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-200 border border-blue-400/30">
            {{ attackType }}
          </span>
        </div>

        <div class="flex justify-between items-center p-4 rounded-lg bg-black/20 border border-white/5">
          <span class="text-sm text-gray-300">Risk Level:</span>
          <span :class="threatLevelBadgeClass" class="px-3 py-1 rounded-full text-xs font-bold">
            {{ threatLevel.toUpperCase() }}
          </span>
        </div>
      </div>
    </div>

    <!-- Risk Factors -->
    <!-- <div v-if="hasRiskFactors" class="rounded-2xl p-6 bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
      <div class="flex items-center mb-4">
        <div class="w-8 h-8 rounded-lg bg-yellow-500/20 flex items-center justify-center mr-3">
          <span class="text-lg">⚡</span>
        </div>
        <h4 class="font-bold text-white">Risk Factors</h4>
      </div>
      
      <div class="space-y-3">
        <div v-for="(value, key) in riskFactors" :key="key" v-if="value > 0"
          class="flex justify-between items-center p-3 rounded-lg bg-black/20 border border-white/5">
          <span class="text-sm text-gray-300">{{ formatRiskFactor(key) }}:</span>
          <span class="font-bold text-white px-2 py-1 rounded bg-red-500/20 text-red-200">{{ value }}</span>
        </div>
      </div>
    </div> -->

    <!-- Text Statistics -->
    <div class="rounded-2xl p-6 bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
      <div class="flex items-center mb-4">
        <div class="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center mr-3">
          <span class="text-lg"><PhArticleMedium :size="24" color="#ffffff" /></span>
        </div>
        <h4 class="font-bold text-white">Text Analysis</h4>
      </div>
      
      <div class="grid grid-cols-2 gap-3">
        <div class="text-center p-4 rounded-lg bg-black/20 border border-white/5">
          <div class="text-2xl font-bold text-blue-400 mb-1">{{ textStats.character_count }}</div>
          <div class="text-xs text-gray-400">Characters</div>
        </div>
        
        <div class="text-center p-4 rounded-lg bg-black/20 border border-white/5">
          <div class="text-2xl font-bold text-green-400 mb-1">{{ textStats.word_count }}</div>
          <div class="text-xs text-gray-400">Words</div>
        </div>
        
        <div class="text-center p-4 rounded-lg bg-black/20 border border-white/5">
          <div class="text-2xl font-bold text-purple-400 mb-1">{{ textStats.sentence_count }}</div>
          <div class="text-xs text-gray-400">Sentences</div>
        </div>
        
        <div class="text-center p-4 rounded-lg bg-black/20 border border-white/5">
          <div class="text-2xl font-bold text-red-400 mb-1">{{ textStats.url_count }}</div>
          <div class="text-xs text-gray-400">URLs</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { PhHeadCircuit, PhArticleMedium   } from "@phosphor-icons/vue";



export default {
  name: 'ThreatIntelligencePanel',
  props: {
    analysisResults: {
      type: Object,
      required: true
    }
  },
    components: {
    PhHeadCircuit,
    PhArticleMedium
  },
  computed: {
    attackType() {
      return this.analysisResults?.analysis?.threat_analysis?.technique_classification || 'Unknown'
    },
    
    threatLevel() {
      return this.analysisResults?.enhanced_metadata?.threat_level || 'unknown'
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
    
    riskFactors() {
      return this.analysisResults?.analysis?.threat_analysis?.risk_factors || {}
    },
    
    hasRiskFactors() {
      return Object.values(this.riskFactors).some(value => value > 0)
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
  methods: {
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
    }
  }
}
</script>