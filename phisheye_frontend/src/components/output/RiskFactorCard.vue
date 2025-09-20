<template>
  <div class="bg-black/20 rounded-lg p-4 border border-white/5 hover:border-white/10 transition-all duration-300">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center">
        <span class="text-lg mr-2">{{ icon }}</span>
        <span class="text-gray-300 font-medium text-sm">{{ label }}</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-white font-bold text-lg">{{ value }}</span>
        <div :class="getSeverityBadgeClass()" class="px-2 py-1 rounded text-xs font-medium">
          {{ getSeverityText() }}
        </div>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="w-full bg-gray-800/50 rounded-full h-2 relative overflow-hidden">
      <div :class="getSeverityBarColor() + ' rounded-full transition-all duration-2000 ease-out h-full'"
        :style="{ width: Math.min(animatedValue, 100) + '%' }">
        <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
      </div>
    </div>
    
    <!-- Percentage Display -->
    <div class="mt-2 text-right">
      <span class="text-gray-400 text-xs">{{ Math.min(percentage, 100).toFixed(1) }}%</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiskFactorCard',
  props: {
    icon: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    value: {
      type: Number,
      required: true
    },
    percentage: {
      type: Number,
      required: true
    },
    animatedValue: {
      type: Number,
      default: 0
    },
    severity: {
      type: String,
      default: 'low',
      validator: value => ['critical', 'high', 'medium', 'low'].includes(value)
    }
  },
  methods: {
    getSeverityText() {
      const severityMap = {
        'critical': 'CRIT',
        'high': 'HIGH',
        'medium': 'MED',
        'low': 'LOW'
      }
      return severityMap[this.severity] || 'LOW'
    },
    
    getSeverityBadgeClass() {
      const classMap = {
        'critical': 'bg-red-600 text-white',
        'high': 'bg-red-500 text-white',
        'medium': 'bg-yellow-500 text-black',
        'low': 'bg-green-500 text-white'
      }
      return classMap[this.severity] || classMap['low']
    },
    
    getSeverityBarColor() {
      if (this.value === 0) return 'bg-gradient-to-r from-green-500 to-green-600'
      
      const classMap = {
        'critical': 'bg-gradient-to-r from-red-600 to-red-700',
        'high': 'bg-gradient-to-r from-red-500 to-orange-600',
        'medium': 'bg-gradient-to-r from-yellow-500 to-orange-500',
        'low': 'bg-gradient-to-r from-yellow-400 to-yellow-500'
      }
      return classMap[this.severity] || classMap['low']
    }
  }
}
</script>