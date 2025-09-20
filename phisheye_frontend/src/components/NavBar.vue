<template>
  <nav class="relative z-50 shadow-lg border-b backdrop-blur-lg" style="background: linear-gradient(90deg, rgba(224, 237, 251, 0.95), rgba(224, 237, 251, 0.98)); border-color: rgba(111, 180, 173, 0.2);">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-3 group hover:scale-105 transition-all duration-300">
            <img 
              src="/src/assets/fisheyeLogo.png" 
              alt="PhishEye Logo" 
              class="w-8 h-8 object-contain group-hover:animate-pulse transition-all duration-300"
            />
            <span class="text-2xl font-bold text-transparent bg-clip-text" style="background: linear-gradient(45deg, #1a5581, #6fb4ad, #2caae9); -webkit-background-clip: text;">
              PhishEye
            </span>
          </router-link>
        </div>
        
        <div class="flex items-center space-x-2">
          <router-link 
            to="/" 
            class="relative px-4 py-2 font-medium rounded-lg transition-all duration-300 group hover:scale-105"
            :class="{ 'font-bold': $route.name === 'home' }"
            :style="{ 
              color: $route.name === 'home' ? '#1a5581' : '#1a5581', 
              opacity: $route.name === 'home' ? '1' : '0.7' 
            }"
          >
            <span class="relative z-10">Home</span>
            <div v-if="$route.name === 'home'" 
                 class="absolute bottom-0 left-0 w-full h-0.5 transform origin-center transition-all duration-300 rounded-full"
                 style="background: linear-gradient(45deg, #6fb4ad, #2caae9);"></div>
            <div class="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" 
                 style="background: rgba(111, 180, 173, 0.1);"></div>
          </router-link>
          
          <router-link 
            to="/analyze" 
            class="relative px-4 py-2 font-medium rounded-lg transition-all duration-300 group hover:scale-105"
            :class="{ 'font-bold': $route.name === 'analyze' }"
            :style="{ 
              color: $route.name === 'analyze' ? '#1a5581' : '#1a5581', 
              opacity: $route.name === 'analyze' ? '1' : '0.7' 
            }"
          >
            <span class="relative z-10 flex items-center">
              <span class="mr-2"></span>
              Analyze 
            </span>
            <div v-if="$route.name === 'analyze'" 
                 class="absolute bottom-0 left-0 w-full h-0.5 transform origin-center transition-all duration-300 rounded-full"
                 style="background: linear-gradient(45deg, #6fb4ad, #2caae9);"></div>
            <div class="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" 
                 style="background: rgba(111, 180, 173, 0.1);"></div>
          </router-link>
          
          <router-link 
            to="/about" 
            class="relative px-4 py-2 font-medium rounded-lg transition-all duration-300 group hover:scale-105"
            :class="{ 'font-bold': $route.name === 'about' }"
            :style="{ 
              color: $route.name === 'about' ? '#1a5581' : '#1a5581', 
              opacity: $route.name === 'about' ? '1' : '0.7' 
            }"
          >
            <span class="relative z-10 flex items-center">
              <span class="mr-2"></span>
              About
            </span>
            <div v-if="$route.name === 'about'" 
                 class="absolute bottom-0 left-0 w-full h-0.5 transform origin-center transition-all duration-300 rounded-full"
                 style="background: linear-gradient(45deg, #6fb4ad, #2caae9);"></div>
            <div class="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" 
                 style="background: rgba(111, 180, 173, 0.1);"></div>
          </router-link>

          <!-- CTA Button -->
          <router-link 
            to="/analyze" 
            class="ml-4 inline-flex items-center px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-300 transform hover:scale-105 shadow-md hover:shadow-lg"
            style="background: linear-gradient(45deg, #6fb4ad, #1f826b); color: #e0edfb;"
          >
            <span class="mr-1"></span>
            Get Started
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
/* Additional hover effects and animations */
@keyframes subtle-glow {
  0%, 100% { 
    box-shadow: 0 0 5px rgba(111, 180, 173, 0.2); 
  }
  50% { 
    box-shadow: 0 0 15px rgba(111, 180, 173, 0.4); 
  }
}

.group:hover img {
  filter: drop-shadow(0 0 8px rgba(111, 180, 173, 0.3));
}

/* Smooth transitions for active states */
.router-link-active {
  position: relative;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .space-x-2 > * + * {
    margin-left: 0.25rem;
  }
  
  .px-4 {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
  }
}
</style>