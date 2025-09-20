<template>
  <div class="space-y-3">
    <div class="flex justify-between items-center">
      <span class="text-sm font-medium text-gray-200 flex items-center">
        <span class="mr-2">{{ icon }}</span>
        {{ label }}
      </span>
      <span class="text-sm font-bold text-white">{{ percentage }}%</span>
    </div>
    
    <div class="w-full bg-gray-800/50 rounded-full h-4 relative overflow-hidden border border-gray-600/30">
      <div :class="colorClass + ' rounded-full transition-all duration-1800 ease-out h-full relative'"
        :style="{ width: animatedValue + '%' }">
        <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RiskMetric',
  props: {
    icon: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    percentage: {
      type: [String, Number],
      required: true
    },
    animatedValue: {
      type: Number,
      default: 0
    },
    colorClass: {
      type: String,
      default: 'bg-gradient-to-r from-blue-500 to-blue-600'
    }
  }
}
</script>