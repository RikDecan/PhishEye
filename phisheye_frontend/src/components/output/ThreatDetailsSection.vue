<template>
  <div class="grid md:grid-cols-2 gap-8">
    <!-- Malicious URLs -->
    <div v-if="suspiciousUrls.length > 0" 
      class="rounded-2xl p-6 border bg-gradient-to-br from-red-900/40 to-red-800/40 border-red-500/30 backdrop-blur-sm">
      
      <div class="flex items-center mb-6">
        <div class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center mr-4 border border-red-400/30">
          <span class="text-xl">⚠️</span>
        </div>
        <h4 class="font-bold text-lg text-white">Malicious URLs Detected</h4>
      </div>
      
      <div class="space-y-3">
        <div v-for="(url, index) in suspiciousUrls" :key="url"
          class="p-4 rounded-lg bg-black/30 border border-red-400/20 hover:bg-black/40 transition-all duration-300">
          <div class="flex items-start space-x-3">
            <div class="w-6 h-6 rounded bg-red-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
              <span class="text-xs">🔗</span>
            </div>
            <div class="font-mono text-sm text-red-200 break-all leading-relaxed">
              {{ url }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Suspicious Keywords -->
    <div v-if="threatKeywords.length > 0" 
      class="rounded-2xl p-6 border bg-gradient-to-br from-orange-900/40 to-orange-800/40 border-orange-500/30 backdrop-blur-sm">
      
      <div class="flex items-center mb-6">
        <div class="w-10 h-10 rounded-lg bg-orange-500/20 flex items-center justify-center mr-4 border border-orange-400/30">
          <span class="text-xl"><PhKey :size="24" color="#ffffff" /></span>
        </div>
        <h4 class="font-bold text-lg text-white">Suspicious Keywords</h4>
      </div>
      
      <div class="flex flex-wrap gap-2">
        <span v-for="(keyword, index) in threatKeywords" :key="keyword"
          class="px-3 py-2 rounded-full text-sm font-medium border bg-orange-500/20 text-orange-200 border-orange-400/40 hover:bg-orange-500/30 transition-all duration-300 cursor-default">
          {{ keyword }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { PhKey  } from '@phosphor-icons/vue';

export default {
  name: 'ThreatDetailsSection',
  props: {
    analysisResults: {
      type: Object,
      required: true
    }
  },
   components: {
    PhKey
  },
  computed: {
    suspiciousUrls() {
      return this.analysisResults?.analysis?.threat_analysis?.suspicious_urls || []
    },
    
    threatKeywords() {
      return this.analysisResults?.analysis?.threat_analysis?.threat_keywords || []
    }
  }
}
</script>