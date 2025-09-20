<template>
  <div class="rounded-2xl p-6 bg-white/10 backdrop-blur-sm border border-white/20 shadow-xl mb-8">
    <!-- Percentage Labels -->
    <div class="flex justify-between items-center mb-4">
      <div class="text-lg font-bold text-green-400">
        {{ legitimatePercentage }}% Legitimate
      </div>
      <div class="text-lg font-bold text-red-400">
        {{ phishingPercentage }}% Phishing
      </div>
    </div>

    <!-- Progress Bar Container -->
    <div class="relative w-full h-4 bg-gray-700/50 rounded-full overflow-hidden border border-white/10 mb-4">
      <!-- Green (Legitimate) section - always starts from left -->
      <div 
        class="absolute left-0 top-0 h-full bg-gradient-to-r from-green-500 to-green-400 transition-all duration-2000 ease-out"
        :style="{ width: animatedLegitimate + '%' }"
      >
        <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
      </div>
      
      <!-- Red (Phishing) section - always on the right -->
      <div 
        class="absolute right-0 top-0 h-full bg-gradient-to-l from-red-500 to-red-400 transition-all duration-2000 ease-out"
        :style="{ width: animatedPhishing + '%' }"
      >
        <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
      </div>

    </div>

    <!-- Risk Assessment -->
    <div class="text-center">
      <!-- <div class="text-sm text-gray-300 mb-1">
        Risk: <span class="font-semibold text-blue-300">[{{ riskLevel.toUpperCase() }}]</span>
      </div> -->
      <div class="text-md text-gray-200">
        Classification: {{ attackType }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClassificationSlider',
  props: {
    analysisResults: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      animatedLegitimate: 0,
      animatedPhishing: 0
    }
  },
  computed: {
    phishingScore() {
      return this.analysisResults?.analysis?.score || 0
    },
    
    legitimateScore() {
      return 1 - this.phishingScore
    },
    
    phishingPercentage() {
      return (this.phishingScore * 100).toFixed(3) 
    },
    
    legitimatePercentage() {
      return (this.legitimateScore * 100).toFixed(3)
    },
    
    // Slider position (0-100%) based on the phishing score
    sliderPosition() {
      return this.phishingScore * 100
    },
    
    sliderBorderClass() {
      if (this.phishingScore > 0.7) return 'border-red-500'
      if (this.phishingScore > 0.3) return 'border-yellow-500'
      return 'border-green-500'
    },
    
    sliderIndicatorClass() {
      if (this.phishingScore > 0.7) return 'bg-red-500'
      if (this.phishingScore > 0.3) return 'bg-yellow-500'
      return 'bg-green-500'
    },
    
    riskLevel() {
      return this.analysisResults?.enhanced_metadata?.threat_level || 'unknown'
    },
    
    attackType() {
      return this.analysisResults?.analysis?.threat_analysis?.technique_classification || 'Unknown'
    }
  },
  mounted() {
    // Start animation after component mounts
    this.startAnimation()
  },
  watch: {
    analysisResults() {
      this.startAnimation()
    }
  },
  methods: {
    startAnimation() {
      // Reset values
      this.animatedLegitimate = 0
      this.animatedPhishing = 0
      
      // Start animations with slight delay for smooth effect
      setTimeout(() => {
        this.animateValue('animatedLegitimate', this.legitimatePercentage, 1800)
      }, 300)
      
      setTimeout(() => {
        this.animateValue('animatedPhishing', this.phishingPercentage, 1800)
      }, 600)
    },
    
    animateValue(property, targetValue, duration) {
      const startValue = 0
      const startTime = performance.now()
      
      const animate = (currentTime) => {
        const elapsed = currentTime - startTime
        const progress = Math.min(elapsed / duration, 1)
        
        // Smooth easing function
        const easeOutCubic = 1 - Math.pow(1 - progress, 3)
        
        this[property] = startValue + (targetValue - startValue) * easeOutCubic
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          this[property] = targetValue
        }
      }
      
      requestAnimationFrame(animate)
    }
  }
}
</script>

<style scoped>
/* Ensure smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Pulse animation for the progress bars */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>