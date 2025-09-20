<template>
  <div
    class="min-h-screen"
    style="
      background: linear-gradient(
        135deg,
        #2caae9 0%,
        #1a5581 50%,
        #1f826b 100%
      );
    "
  >
    <!-- Animated Background -->

    <div class="relative container mx-auto px-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- Epic Header -->
        <div class="text-center mb-12 animate-fade-in-down">
    

          <h1
            class="text-5xl md:text-7xl font-bold text-transparent bg-clip-text mb-6"
            style="
              background: linear-gradient(45deg, #e0edfb, #6fb4ad, #2caae9);
              -webkit-background-clip: text;
            "
          >
            PhishEye Scanner
          </h1>
          <p
            class="text-xl md:text-2xl max-w-3xl mx-auto animate-fade-in-up animation-delay-300"
            style="color: #e0edfb"
          >
            Advanced phishing detection analysed by a fine-tuned XLM-RoBERTa model
          </p>
        </div>
        <!-- Vervang de hele "Analysis Interface" sectie met dit: -->

        <!-- Analysis Interface -->
        <div class="grid lg:grid-cols-3 gap-8 mb-8">
          <!-- Input Panel Component -->
          <InputPanel
            v-model:emailText="emailText"
            :isAnalyzing="isAnalyzing"
            :selectedFile="selectedFile"
            :isProcessingFile="isProcessingFile"
            :fileError="fileError"
            @analyze="analyzeEmail"
            @clear-text="clearText"
            @load-example="loadExample"
            @file-processed="handleFileProcessed"
            @file-cleared="handleFileCleared"
          />

          <!-- Quick Stats Panel (blijft hetzelfde) -->
          <div class="space-y-4 animate-slide-in-right">
            <div
              class="rounded-2xl p-6 shadow-xl transition-all duration-300 transform hover:scale-105"
              style="
                background-color: rgba(224, 237, 251, 0.1);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(224, 237, 251, 0.2);
              "
            >
              <h3
                class="font-semibold mb-4 flex items-center"
                style="color: #e0edfb"
              >
                <span class="mr-2 animate-pulse"></span>
                System Status
              </h3>
              <div class="space-y-3">
                <div
                  class="flex justify-between text-sm animate-fade-in animation-delay-100"
                >
                  <span style="color: #6fb4ad">Model Status</span>
                  <span
                    class="font-semibold animate-pulse"
                    style="color: #6fb4ad"
                    >● ONLINE</span
                  >
                </div>
                <div
                  class="flex justify-between text-sm animate-fade-in animation-delay-200"
                >
                  <span style="color: #6fb4ad">Accuracy Rate</span>
                  <span class="font-bold" style="color: #e0edfb">99.58%</span>
                </div>
                <div
                  class="flex justify-between text-sm animate-fade-in animation-delay-300"
                >
                  <span style="color: #6fb4ad">Response Time</span>
                  <span class="font-bold" style="color: #e0edfb"> < 2s</span>
                </div>
                <div
                  class="flex justify-between text-sm animate-fade-in animation-delay-400"
                >
                  <span style="color: #6fb4ad">Training Data</span>
                  <span class="font-bold" style="color: #e0edfb">142K+</span>
                </div>
              </div>
            </div>

            <div
              class="rounded-2xl p-6 shadow-xl transition-all duration-300 transform hover:scale-105"
              style="
                background-color: rgba(224, 237, 251, 0.1);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(224, 237, 251, 0.2);
              "
            >
              <h3
                class="font-semibold mb-4 flex items-center"
                style="color: #e0edfb"
              >
                <span class="mr-2 animate-pulse"></span>
                Detection Modes
              </h3>
              <div class="space-y-2 text-sm">
                <div
                  class="animate-slide-in-right animation-delay-100"
                  style="color: #6fb4ad"
                >
                  ✓ Semantic Analysis
                </div>
                <div
                  class="animate-slide-in-right animation-delay-200"
                  style="color: #6fb4ad"
                >
                  ✓ URL Inspection
                </div>
                <div
                  class="animate-slide-in-right animation-delay-300"
                  style="color: #6fb4ad"
                >
                  ✓ Authority Validation
                </div>
                <div
                  class="animate-slide-in-right animation-delay-400"
                  style="color: #6fb4ad"
                >
                  ✓ Urgency Detection
                </div>
                <div
                  class="animate-slide-in-right animation-delay-500"
                  style="color: #6fb4ad"
                >
                  ✓ Social Engineering
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Display -->
        <AnalysisResults
          v-if="analysisResults"
          :analysis-results="analysisResults"
          :animated-overall-risk="animatedOverallRisk"
          :animated-urgency="animatedUrgency"
          :animated-financial-risk="animatedFinancialRisk"
          :animated-phishing="animatedPhishing"
          :animated-confidence="animatedConfidence"
        />

        <!-- Error Display -->
        <div
          v-if="errorMessage"
          class="rounded-2xl p-6 bg-red-900/20 backdrop-blur-sm border border-red-500/30 shadow-2xl"
        >
          <div class="flex items-center">
            <div
              class="w-10 h-10 rounded-lg bg-red-500/20 flex items-center justify-center mr-4"
            >
              <span class="text-xl">⚠️</span>
            </div>
            <div>
              <div class="font-bold text-red-200">System Error</div>
              <div class="text-red-300 text-sm mt-1">{{ errorMessage }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AnalyzeView from "../scripts/AnalyzeView.js";
import InputPanel from "../components/input/InputPanel.vue";
import AnalysisResults from '../components/output/AnalysisResults.vue';

export default {
  mixins: [AnalyzeView],
  components: {
    InputPanel,
    AnalysisResults
  },
};
</script>

<style scoped>
.animation-delay-100 {
  animation-delay: 0.1s;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-300 {
  animation-delay: 0.3s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}

.animation-delay-500 {
  animation-delay: 0.5s;
}

.animation-delay-600 {
  animation-delay: 0.6s;
}

.animation-delay-700 {
  animation-delay: 0.7s;
}

.animation-delay-800 {
  animation-delay: 0.8s;
}

.animation-delay-900 {
  animation-delay: 0.9s;
}

.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-1100 {
  animation-delay: 1.1s;
}

.animation-delay-1200 {
  animation-delay: 1.2s;
}

.animation-delay-1300 {
  animation-delay: 1.3s;
}

.animation-delay-1400 {
  animation-delay: 1.4s;
}

.animation-delay-1500 {
  animation-delay: 1.5s;
}

.animation-delay-1600 {
  animation-delay: 1.6s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) skewX(-12deg);
  }

  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

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

@keyframes fade-in-down {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-in-left {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slide-in-right {
  from {
    opacity: 0;
    transform: translateX(30px);
  }

  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slide-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }

  50% {
    opacity: 1;
    transform: scale(1.05);
  }

  70% {
    transform: scale(0.9);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes bounce-slow {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-10px);
  }

  60% {
    transform: translateY(-5px);
  }
}

@keyframes title-glow {
  0%,
  100% {
    text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
  }

  50% {
    text-shadow: 0 0 30px rgba(59, 130, 246, 0.8),
      0 0 40px rgba(168, 85, 247, 0.4);
  }
}

@keyframes pulse-glow {
  0%,
  100% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
  }

  50% {
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.6),
      0 0 40px rgba(168, 85, 247, 0.4);
  }
}

@keyframes pulse-subtle {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.7;
  }
}

@keyframes result-appear {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }

  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes number-count {
  from {
    transform: scale(0.5);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-5px);
  }

  75% {
    transform: translateX(5px);
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

.animate-fade-in-down {
  animation: fade-in-down 0.8s ease-out forwards;
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
}

.animate-slide-in-left {
  animation: slide-in-left 0.6s ease-out forwards;
}

.animate-slide-in-right {
  animation: slide-in-right 0.6s ease-out forwards;
}

.animate-slide-in-up {
  animation: slide-in-up 0.4s ease-out forwards;
}

.animate-bounce-in {
  animation: bounce-in 0.6s ease-out forwards;
}

.animate-bounce-slow {
  animation: bounce-slow 3s ease-in-out infinite;
}

.animate-title-glow {
  animation: title-glow 3s ease-in-out infinite;
}

.animate-pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

.animate-pulse-subtle {
  animation: pulse-subtle 2s ease-in-out infinite;
}

.animate-result-appear {
  animation: result-appear 0.8s ease-out forwards;
}

.animate-number-count {
  animation: number-count 0.5s ease-out forwards;
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

/* Set initial states for animated elements */
.animate-fade-in,
.animate-fade-in-down,
.animate-fade-in-up,
.animate-slide-in-left,
.animate-slide-in-right,
.animate-slide-in-up,
.animate-bounce-in {
  opacity: 0;
}

/* Custom scrollbar for dark theme */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.custom-email-textarea::placeholder {
  color: rgba(224, 237, 251, 0.5);
}

.custom-email-textarea:hover {
  background-color: rgba(26, 85, 129, 0.6);
}

.custom-email-textarea:focus {
  background-color: rgba(26, 85, 129, 0.7);
  outline: none;
}
</style>
