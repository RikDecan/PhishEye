<template>
  <div class="mb-6">
    <div class="flex items-center justify-between mb-3">
      <span class="text-sm font-medium flex items-center" style="color: #e0edfb;">
        <span class="mr-2"><PhMicrosoftOutlookLogo :size="24" color="#ffffff" /></span>
        Upload .EML File
      </span>
      <button v-if="selectedFile" @click="clearFile" 
        class="text-xs px-3 py-1 rounded-full transition-all duration-300 hover:scale-105"
        style="background-color: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3);">
        <PhTrash :size="24" color="#f00000" />
      </button>
    </div>
    
    <div class="relative">
      <input 
        ref="fileInput"
        type="file" 
        accept=".eml"
        @change="handleFileUpload"
        class="hidden"
        id="emlFileInput">
      
      <label for="emlFileInput" 
        class="flex items-center justify-center w-full p-4 border-2 border-dashed rounded-xl cursor-pointer transition-all duration-300 hover:scale-[1.02]"
        :class="selectedFile ? 'border-green-500 bg-green-500/10' : 'border-gray-500 hover:border-blue-400'"
        style="border-color: rgba(224, 237, 251, 0.3); background-color: rgba(26, 85, 129, 0.3);">
        
        <div class="text-center">
          <div v-if="isProcessingFile" class="animate-spin text-2xl mb-2"><PhArrowClockwise :size="24" color="#ffffff" /></div>
          <div v-else-if="selectedFile" class="flex justify-center text-2xl mb-2"><PhCheck :size="24" color="#ffffff" /></div>
          <div v-else class="flex justify-center text-2xl mb-2">
            <PhPackage :size="24" color="#ffffff" />
          </div>
          
          <div class="text-sm font-medium" style="color: #e0edfb;">
            <span v-if="isProcessingFile">Processing email file...</span>
            <span v-else-if="selectedFile">{{ selectedFile.name }}</span>
            <span v-else>Click to upload .eml file or drag & drop</span>
          </div>
          
          <div class="text-xs mt-1" style="color: rgba(224, 237, 251, 0.6);">
            <span v-if="!selectedFile">Automatically extracts email content for analysis</span>
          </div>
        </div>
      </label>
    </div>
    
    <!-- File Error Display -->
    <div v-if="fileError" class="mt-3 p-3 rounded-lg border animate-shake"
      style="background-color: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3);">
      <div class="flex items-center text-sm" style="color: #fca5a5;">
        <span class="mr-2">⚠️</span>
        {{ fileError }}
      </div>
    </div>
    
    <!-- Success indicator -->
<div v-if="selectedFile && !fileError && !isProcessingFile" 
  class="mt-3 p-4 rounded-lg shadow-lg animate-fade-in flex items-center space-x-2">
  <div class="text-green-300 font-semibold text-sm">
    Email content extracted successfully
  </div>
</div>
  </div>
</template>

<script>

import { PhPackage, PhMicrosoftOutlookLogo, PhArrowClockwise, PhCheck, PhTrash } from "@phosphor-icons/vue";

export default {
  name: 'FileUpload',
   components: {
    PhPackage, 
    PhMicrosoftOutlookLogo,
    PhArrowClockwise,
    PhCheck,
    PhTrash 
  },
  props: {
    selectedFile: Object,
    isProcessingFile: Boolean,
    fileError: String
  },
  emits: ['file-processed', 'file-cleared'],
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        this.processEmlFile(file)
      }
    },

    async processEmlFile(file) {
      if (!file.name.toLowerCase().endsWith('.eml')) {
        this.$emit('file-processed', { error: 'Please select a valid .eml file' })
        return
      }

      this.$emit('file-processed', { processing: true })

      try {
        const fileContent = await this.readFileAsText(file)
        const extractedText = this.extractEmailBody(fileContent)
        
        if (extractedText.trim()) {
          this.$emit('file-processed', { 
            success: true, 
            file: file, 
            content: extractedText 
          })
        } else {
          this.$emit('file-processed', { 
            error: 'Could not extract readable content from the email file' 
          })
        }
      } catch (error) {
        console.error('File processing error:', error)
        this.$emit('file-processed', { 
          error: 'Failed to process the email file' 
        })
      }
    },

    readFileAsText(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = (e) => resolve(e.target.result)
        reader.onerror = (e) => reject(e)
        reader.readAsText(file)
      })
    },

    extractEmailBody(emlContent) {
      try {
        const headerBodySplit = emlContent.split(/\r?\n\r?\n/)
        if (headerBodySplit.length < 2) return emlContent

        let body = headerBodySplit.slice(1).join('\n\n')

        if (body.includes('Content-Type: text/plain')) {
          const textPlainMatch = body.match(/Content-Type: text\/plain[\s\S]*?\n\n([\s\S]*?)(?=\n--|\nContent-Type:|$)/i)
          if (textPlainMatch && textPlainMatch[1]) {
            body = textPlainMatch[1]
          }
        }

        body = body
          .replace(/^>.*$/gm, '')
          .replace(/Content-Transfer-Encoding:.*$/gm, '')
          .replace(/Content-Type:.*$/gm, '')
          .replace(/--[a-zA-Z0-9_-]+--/g, '')
          .replace(/=\r?\n/g, '')
          .replace(/=[0-9A-F]{2}/g, '')
          .replace(/\n{3,}/g, '\n\n')
          .trim()

        return body
      } catch (error) {
        console.error('Error extracting email body:', error)
        return emlContent
      }
    },

    clearFile() {
      this.$emit('file-cleared')
      const fileInput = this.$refs.fileInput
      if (fileInput) {
        fileInput.value = ''
      }
    }
  }
}
</script>