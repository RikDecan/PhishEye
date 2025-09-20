<template>
  <div class="space-y-8 animate-fade-in">
    <!-- Classification Slider -->
    <ClassificationSlider :analysis-results="analysisResults" />
    
    <!-- Main Threat Detection Card -->
    <ThreatDetectionCard :analysis-results="analysisResults" />

    <!-- Analytics Dashboard -->
    <div class="grid lg:grid-cols-3 gap-8">
      <!-- Risk Assessment Panel -->
      <RiskAssessmentPanel 
        :analysis-results="analysisResults"
        :animated-overall-risk="animatedOverallRisk"
        :animated-urgency="animatedUrgency"
        :animated-financial-risk="animatedFinancialRisk"
        :animated-phishing="animatedPhishing"
        :animated-confidence="animatedConfidence"
      />

      <!-- Threat Intelligence Panel -->
      <ThreatIntelligencePanel :analysis-results="analysisResults" />
    </div>

    <!-- Threat Details -->
    <ThreatDetailsSection :analysis-results="analysisResults" />

    <!-- Processing Metadata -->
    <div class="rounded-xl p-6 bg-white/5 backdrop-blur-sm border border-white/10">
      <div class="grid md:grid-cols-4 gap-6">
        <div class="flex items-center text-sm text-gray-300">
          <div>
            <div class="font-medium text-white">Processed</div>
            <div class="text-xs">{{ formatDate(analysisResults.metadata.processed_at) }}</div>
          </div>
        </div>
        
        <div class="flex items-center text-sm text-gray-300">
     
          <div>
            <div class="font-medium text-white">Model</div>
            <div class="text-xs">XLM-RoBERTa</div>
          </div>
        </div>
        
        <div v-if="analysisResults.enhanced_metadata" class="flex items-center text-sm text-gray-300">
         zzzzzzzzzzzzzzzzzzzz
          <div>
            <div class="font-medium text-white">Category</div>
            <div class="text-xs">{{ analysisResults.enhanced_metadata.risk_category || 'Unknown' }}</div>
          </div>
        </div>
        
        <div class="flex items-center text-sm text-gray-300">

          <div>
            <div class="font-medium text-white">Status</div>
            <div class="text-xs text-green-400">Complete</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import ThreatDetectionCard from './ThreatDetectionCard.vue'
import RiskAssessmentPanel from './RiskAssessmentPanel.vue'
import ThreatIntelligencePanel from './ThreatIntelligencePanel.vue'
import ThreatDetailsSection from './ThreatDetailsSection.vue'
import ClassificationSlider from './ClassificationSlider.vue'

export default {
  name: 'AnalysisResults',
  components: {
    ClassificationSlider,
    // ThreatDetectionCard,
    RiskAssessmentPanel,
    ThreatIntelligencePanel,
    ThreatDetailsSection
  },
  props: {
    analysisResults: {
      type: Object,
      required: true
    },
    animatedOverallRisk: {
      type: Number,
      default: 0
    },
    animatedUrgency: {
      type: Number,
      default: 0
    },
    animatedFinancialRisk: {
      type: Number,
      default: 0
    },
    animatedPhishing: {
      type: Number,
      default: 0
    },
    animatedConfidence: {
      type: Number,
      default: 0
    }
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}
</style>