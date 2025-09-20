<template>
  <div class="lg:col-span-2 animate-slide-in-left">
    <div class="rounded-2xl p-8 shadow-2xl transition-all duration-300 hover:scale-[1.01]"
      style="background-color: rgba(224, 237, 251, 0.1); backdrop-filter: blur(16px); border: 1px solid rgba(224, 237, 251, 0.2);">
      
      <!-- Terminal Header -->
      <!-- <div class="flex items-center mb-6">
        <div class="w-3 h-3 bg-red-500 rounded-full mr-2 animate-pulse"></div>
        <div class="w-3 h-3 bg-yellow-500 rounded-full mr-2 animate-pulse animation-delay-200"></div>
        <div class="w-3 h-3 rounded-full mr-2 animate-pulse animation-delay-400"
          style="background-color: #6fb4ad;"></div>
        <span class="ml-4 font-mono text-sm"
          style="color: rgba(224, 237, 251, 0.75);">phisheye-terminal</span>
      </div> -->

      <div class="mb-6">
    

        <!-- File Upload Component -->
        <FileUpload 
          :selectedFile="selectedFile"
          :isProcessingFile="isProcessingFile"
          :fileError="fileError"
          @file-processed="handleFileProcessed"
          @file-cleared="handleFileCleared"
        />

        <!-- Divider -->
        <div class="flex items-center mb-6">
          <div class="flex-1 h-px" style="background-color: rgba(224, 237, 251, 0.2);"></div>
          <span class="px-4 text-xs" style="color: rgba(224, 237, 251, 0.5);">OR</span>
          <div class="flex-1 h-px" style="background-color: rgba(224, 237, 251, 0.2);"></div>
        </div>

        <!-- Text Area -->
        <div class="relative">
          <textarea 
            id="emailText" 
            :value="emailText"
            @input="$emit('update:emailText', $event.target.value)"
            class="w-full h-48 px-4 py-4 border rounded-xl resize-none font-mono text-sm backdrop-blur-sm transition-all duration-300 focus:ring-2 custom-email-textarea"
            style="background-color: rgba(26, 85, 129, 0.5); border-color: rgba(224, 237, 251, 0.3); color: #e0edfb;"
            placeholder="Paste suspicious email content here or click an example below..."
          ></textarea>
          <div class="absolute top-3 right-3 text-xs animate-fade-in" style="color: rgba(224, 237, 251, 0.6);">
            {{ emailText.length }}/5000 chars
          </div>
        </div>
      </div>

      <!-- Example Buttons -->
      <ExampleButtons 
        @load-example="handleLoadExample"
        @clear-text="$emit('clear-text')"
      />

      <!-- Analyze Button -->
      <div class="text-center">
        <button 
          @click="$emit('analyze')" 
          :disabled="!emailText.trim() || isAnalyzing"
          class="group relative inline-flex items-center px-12 py-4 text-lg font-bold rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-2xl overflow-hidden"
          style="background: #7bbda4; color: #e0edfb;">
          
          <div class="absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity duration-300"
            style="background:  #7bbda4;"></div>

          <span v-if="isAnalyzing" class="relative mr-3 animate-spin text-2xl"><PhArrowsClockwise :size="24" color="#ffffff" /></span>
          <span v-else class="relative mr-3 text-2xl"><PhMagnifyingGlass :size="24" color="#ffffff" /></span>
          <span class="relative">{{ isAnalyzing ? 'Scanning Patterns...' : 'Initiate Scan' }}</span>

          <div class="absolute inset-0 blur-lg opacity-30 group-hover:opacity-50 transition-opacity"
            style="background:  #7bbda4;"></div>
        </button>


      </div>
    </div>
  </div>
</template>

<script>
import FileUpload from './FileUpload.vue'
import ExampleButtons from './ExampleButtons.vue'
import { PhArrowsClockwise, PhMagnifyingGlass   } from "@phosphor-icons/vue";


export default {
  name: 'InputPanel',
  components: {
    FileUpload,
    ExampleButtons,
    PhArrowsClockwise,
    PhMagnifyingGlass 

  },
  props: {
    emailText: String,
    isAnalyzing: Boolean,
    selectedFile: Object,
    isProcessingFile: Boolean,
    fileError: String
  },
  emits: ['update:emailText', 'analyze', 'clear-text', 'load-example', 'file-processed', 'file-cleared'],
  methods: {
    handleLoadExample(type) {
      this.$emit('load-example', type)
    },
    
    handleFileProcessed(result) {
      this.$emit('file-processed', result)
    },
    
    handleFileCleared() {
      this.$emit('file-cleared')
    }
  }
}
</script>

<style scoped>
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

.animation-delay-200 {
  animation-delay: 0.2s;
}
.animation-delay-400 {
  animation-delay: 0.4s;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-in-left {
  from { opacity: 0; transform: translateX(-30px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); }
  50% { box-shadow: 0 0 30px rgba(59, 130, 246, 0.6), 0 0 40px rgba(168, 85, 247, 0.4); }
}

.animate-fade-in { animation: fade-in 0.6s ease-out forwards; }
.animate-slide-in-left { animation: slide-in-left 0.6s ease-out forwards; }
.animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
</style>