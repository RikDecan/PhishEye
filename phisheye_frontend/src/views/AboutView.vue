<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="relative overflow-hidden bg-gradient-to-br from-blue-700 via-green-450 to-green-500">
      <!-- Animated Background -->
      <div class="absolute inset-0">
        <!-- <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div class="absolute top-3/4 right-1/4 w-64 h-64 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-1000"></div>
        <div class="absolute top-1/2 left-3/4 w-64 h-64 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div> -->
      </div>

      <div class="relative container mx-auto px-4 py-24">
        <div class="text-center">
          <div class="inline-flex items-center mb-6 px-4 py-2 bg-white bg-opacity-10 rounded-full text-white text-sm backdrop-blur-sm">
            <span class="mr-2"></span>
            <span>Thesis Project • Advanced AI Research</span>
          </div>
          
          <h1 class="text-[#0f3553]xl md:text-7xl font-bold text-transparent bg-clip-text bg-yellow-50 mb-6">
            The Story Behind
          </h1>
          
          <p class="text-xl md:text-2xl text-white max-w-4xl mx-auto leading-relaxed">
            How cutting-edge AI research meets real-world cybersecurity challenges
            to create the future of phishing detection
          </p>
        </div>
      </div>
    </section>

    <!-- Mission Section -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-[#0f3553] mb-6">
              The Mission
            </h2>
            <p class="text-xl text-[#0f3553] leading-relaxed">
              In an era where <span class="font-bold text-red-600">3.4 billion phishing emails</span> are sent daily, 
              traditional detection methods fail against sophisticated social engineering. 
              PhishEye represents a paradigm shift toward <span class="font-bold text-blue-600">intelligent, 
                threat detection</span> that understands language nuances and malicious intent.
            </p>
          </div>

          <div class="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h3 class="text-2xl font-bold text-[#0f3553] mb-4">The Problem</h3>
              <div class="space-y-4 text-[#0f3553]">
                <p><strong>91% of cyberattacks begin with phishing emails</strong></p>
                <p><strong>$12 billion in losses</strong> annually from phishing attacks</p>
                <p><strong>Sophisticated social engineering</strong> bypasses traditional filters</p>
                <p><strong>Real-time detection</strong> needed for modern threat landscape</p>
              </div>
            </div>

            <div>
              <h3 class="text-2xl font-bold text-[#0f3553] mb-4">Our Solution</h3>
              <div class="space-y-4  text-[#0f3553]">
                <p><strong>Fine-tuned XLM-RoBERTa</strong> understands context and semantics</p>
                <p><strong>99.58% accuracy</strong> across diverse phishing campaigns</p>
                <p><strong>Threat intelligence</strong> explains WHY emails are dangerous</p>
                <p><strong>Real-time analysis</strong> with sub-second response times</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Technical Innovation -->
    <section class="py-20 bg-gradient-to-r from-blue-700  to-emerald-600">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold  text-[#ffffff]">
            Technical Innovation
          </h2>
          <p class="text-xl  text-[#ffffff] max-w-3xl mx-auto">
            PhishEye pushes the boundaries of what's possible with transformer models 
            applied to cybersecurity challenges
          </p>
        </div>

        <div class="max-w-6xl mx-auto">
          <!-- Research Process -->
          <div class="grid md:grid-cols-3 gap-8 mb-16">
            <div class="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-6">
                <PhChartScatter :size="36" color="#ffffff" />
              </div>
              <h3 class="text-xl font-bold text-[#0f3553] mb-4">Data Engineering</h3>
              <p class="text-[#0f3553]">
                Curated and processed <strong>142,000+ email samples</strong> from diverse 
                phishing campaigns and legitimate communications for robust training
              </p>
            </div>

            <div class="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-6">
                <PhBlueprint :size="36" color="#ffffff" />
              </div>
              <h3 class="text-xl font-bold text-[#0f3553] mb-4">Model Architecture</h3>
              <p class="text-[#0f3553]">
                Fine-tuned <strong>XLM-RoBERTa-base</strong> with custom classification heads 
                optimized for multilingual phishing detection and threat classification
              </p>
            </div>

            <div class="bg-white p-8 rounded-2xl shadow-lg text-center">
              <div class="w-16 h-16 bg-gradient-to-r from-pink-500 to-red-500 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-6">
                <PhCircuitry :size="36" color="#ffffff" />
              </div>
              <h3 class="text-xl font-bold text-[#0f3553] mb-4">System Integration</h3>
              <p class="text-[#0f3553]">
                Full-stack architecture with <strong>FastAPI</strong>, <strong>Laravel</strong>, 
                and <strong>Vue.js</strong> for seamless real-time threat analysis
              </p>
            </div>
          </div>

          <!-- Performance Metrics -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            <h3 class="text-2xl font-bold text-[#0f3553] mb-8 text-center">
  <span class="inline-flex items-center gap-2">
    <PhTrophy :size="20" color="#0f3553" />
    Performance Achievements
    <PhTrophy :size="20" color="#0f3553" />
  </span>
</h3>

            
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl">
                <div class="text-3xl font-bold text-blue-600 mb-2">99.58%</div>
                <div class="text-gray-700 font-medium">Accuracy Rate</div>
                <div class="text-sm text-gray-500 mt-1">Industry Leading</div>
              </div>
              
              <div class="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-xl">
                <div class="text-3xl font-bold text-green-600 mb-2">97.84%</div>
                <div class="text-gray-700 font-medium">F1-Score</div>
                <div class="text-sm text-gray-500 mt-1">Balanced Performance</div>
              </div>
              
              <div class="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl">
                <div class="text-3xl font-bold text-purple-600 mb-2">98.83%</div>
                <div class="text-gray-700 font-medium">Precision</div>
                <div class="text-sm text-gray-500 mt-1">Low False Positives</div>
              </div>
              
              <div class="text-center p-6 bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl">
                <div class="text-3xl font-bold text-orange-600 mb-2">96.86%</div>
                <div class="text-gray-700 font-medium">Recall</div>
                <div class="text-sm text-gray-500 mt-1">Catches Real Threats</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- What Makes It Special -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-[#0f3553] mb-6">
              ✨ What Makes PhishEye Special
            </h2>
            <p class="text-xl text-[#0f3553]">
              Beyond traditional keyword matching - true AI understanding
            </p>
          </div>

          <div class="space-y-12">
            <!-- Context Understanding -->
            <div class="flex flex-col lg:flex-row items-center gap-12">
              <div class="lg:w-1/2">
                <h3 class="text-2xl font-bold text-[#0f3553] mb-4">
                  🧠 Contextual Software Analysis
                </h3>
                <p class="text-[#0f3553] text-lg leading-relaxed mb-6">
                  Unlike simple keyword filters, PhishEye understands the semantic meaning of entire messages. 
                  It can distinguish between legitimate urgency and malicious pressure tactics, 
                  recognizing subtle linguistic patterns that indicate social engineering.
                </p>
                <div class="space-y-3">
                  <div class="flex items-center text-green-600">
                    <span class="mr-2">✓</span>
                    <span>Understands context and semantics</span>
                  </div>
                  <div class="flex items-center text-green-600">
                    <span class="mr-2">✓</span>
                    <span>Multilingual threat detection</span>
                  </div>
                  <div class="flex items-center text-green-600">
                    <span class="mr-2">✓</span>
                    <span>Adapts to evolving attack patterns</span>
                  </div>
                </div>
              </div>
              
              <div class="lg:w-1/2">
                <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 text-white">
                  <div class="font-mono text-sm space-y-2">
                    <div class="text-green-400">// Traditional Approach</div>
                    <div class="text-gray-400">if (email.contains("urgent")) {</div>
                    <div class="text-gray-400 ml-4">return "SUSPICIOUS";</div>
                    <div class="text-gray-400">}</div>
                    <div class="text-yellow-400 mt-4">// PhishEye Approach</div>
                    <div class="text-blue-400">analyzeSemanticContext(email)</div>
                    <div class="text-blue-400">evaluateIntentPatterns()</div>
                    <div class="text-blue-400">assessThreatIndicators()</div>
                    <div class="text-green-400">// 99.58% accurate decision</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Threat Intelligence -->
            <div class="flex flex-col lg:flex-row-reverse items-center gap-12">
              <div class="lg:w-1/2">
                <h3 class="text-2xl font-bold text-[#0f3553] mb-4">
                  🛡️ Advanced Threat Intelligence
                </h3>
                <p class="text-[#0f3553] text-lg leading-relaxed mb-6">
                  PhishEye doesn't just say "this is phishing" - it explains exactly WHY. 
                  Our threat intelligence engine provides detailed analysis of attack techniques, 
                  suspicious URLs, impersonation attempts, and risk factors.
                </p>
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-red-50 p-4 rounded-lg border border-red-200">
                    <div class="text-red-600 font-semibold">Attack Classification</div>
                    <div class="text-sm text-[#0f3553]">Credential Harvesting, Social Engineering, etc.</div>
                  </div>
                  <div class="bg-orange-50 p-4 rounded-lg border border-orange-200">
                    <div class="text-orange-600 font-semibold">URL Analysis</div>
                    <div class="text-sm text-[#0f3553]">Suspicious links and domains</div>
                  </div>
                  <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                    <div class="text-yellow-600 font-semibold">Risk Scoring</div>
                    <div class="text-sm text-[#0f3553]">Detailed threat breakdown</div>
                  </div>
                  <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <div class="text-blue-600 font-semibold">Explanations</div>
                    <div class="text-sm text-[#0f3553]">Human-readable analysis</div>
                  </div>
                </div>
              </div>
              
              <div class="lg:w-1/2">
                <div class="bg-gradient-to-br from-red-50 to-red-100 border border-red-200 rounded-2xl p-6">
                  <div class="flex items-center mb-4">
                    <span class="text-2xl mr-3">⚠️</span>
                    <div>
                      <div class="font-bold text-red-800">PHISHING DETECTED</div>
                      <div class="text-red-600 text-sm">Critical Threat Level</div>
                    </div>
                  </div>
                  <div class="space-y-2 text-sm">
                    <div class="text-red-700">• Credential harvesting attempt detected</div>
                    <div class="text-red-700">• 2 suspicious URLs found</div>
                    <div class="text-red-700">• High urgency language patterns</div>
                    <div class="text-red-700">• Authority impersonation indicators</div>
                    <div class="text-green-600 mt-3">→ 99.8% confidence malicious</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Future Vision -->
    <section class="py-20 bg-gradient-to-br  from-blue-400 via-blue-800 to-teal-600">
      <div class="container mx-auto px-4 text-center">
        <div class="max-w-4xl mx-auto">
          <h2 class="text-4xl font-bold mb-6 text-[#ffffff]">
            The Future of Cybersecurity
          </h2>
          <p class="text-xl text-blue-100 leading-relaxed mb-12">
            PhishEye represents more than just a thesis project - it's a glimpse into the future 
            where AI and human intelligence work together to create a safer digital world. 
            As threats evolve, so too must our defenses.
          </p>

          <div class="grid md:grid-cols-3 gap-8">
            <div class="bg-white bg-opacity-10 backdrop-blur-sm rounded-xl p-6 border border-white border-opacity-20">
              <div class="text-3xl mb-4">🌐</div>
              <h3 class="text-xl font-bold mb-2 text-[#ffffff]">Global Impact</h3>
              <p class="text-blue-100 text-sm">
                Protecting millions from sophisticated cyber threats with AI-powered detection
              </p>
            </div>

            <div class="bg-white bg-opacity-10 backdrop-blur-sm rounded-xl p-6 border border-white border-opacity-20">
              <div class="text-3xl mb-4">🔬</div>
              <h3 class="text-xl font-bold mb-2 text-[#ffffff]">Continuous Research</h3>
              <p class="text-blue-100 text-sm">
                Advancing the state-of-the-art in NLP applications for cybersecurity
              </p>
            </div>

            <div class="bg-white bg-opacity-10 backdrop-blur-sm rounded-xl p-6 border border-white border-opacity-20">
              <div class="text-3xl mb-4">🤝</div>
              <h3 class="text-xl font-bold mb-2 text-[#ffffff]">Open Innovation</h3>
              <p class="text-blue-100 text-sm">
                Sharing knowledge to build stronger defenses against evolving threats
              </p>
            </div>
          </div>

          <div class="mt-12">
            <router-link 
              to="/analyze"
              class="inline-flex items-center px-8 py-4 bg-white text-purple-900 text-lg font-semibold rounded-xl hover:bg-gray-100 transform hover:scale-105 transition-all duration-300 shadow-lg"
            >
              <span class="mr-2"></span>
              Try the demo
              <span class="ml-2">→</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Credits -->
    <section class="py-12 bg-gray-900 text-white">
      <div class="container mx-auto px-4 text-center">
        <div class="max-w-2xl mx-auto">
          <h3 class="text-xl font-bold mb-4">🎓 Academic Excellence</h3>
          <p class="text-gray-400 mb-6">
            This research project represents the culmination of advanced studies in 
            artificial intelligence, natural language processing, and cybersecurity.
          </p>
          <div class="flex flex-col sm:flex-row justify-center items-center gap-4 text-sm text-gray-500">
            <div>Advanced AI Research</div>
            <div class="hidden sm:block">•</div>
            <div>Thesis Project 2025</div>
            <div class="hidden sm:block">•</div>
            <div>XLM-RoBERTa Fine-tuning</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { PhTrophy,PhChartScatter, PhBlueprint, PhCircuitry } from '@phosphor-icons/vue';

 

export default {
  name: 'AboutView',
  mounted() {
    this.setupScrollAnimations()
  },
  components: {
    PhTrophy,
    PhChartScatter,
    PhBlueprint,
    PhCircuitry 
  },
  methods: {
    setupScrollAnimations() {
      const animatedElements = document.querySelectorAll('.animate-on-scroll')
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1'
            entry.target.style.transform = 'translateY(0)'
          }
        })
      })
      
      animatedElements.forEach(el => {
        el.style.opacity = '0'
        el.style.transform = 'translateY(20px)'
        el.style.transition = 'all 0.6s ease-out'
        observer.observe(el)
      })
    }
  }
}
</script>

<style scoped>
.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}
</style>