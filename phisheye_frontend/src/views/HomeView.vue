<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section
      class="relative overflow-hidden bg-gradient-to-br from-blue-400 via-blue-800 to-teal-600"
      style="
        background: linear-gradient(
          135deg,
          #2caae9 0%,
          #1a5581 50%,
          #1f826b 100%
        );
      "
    >
      <div class="relative container mx-auto px-4 py-24">
        <div class="text-center">
          <!-- Main Hero Content -->
          <div class="mb-8 animate-fade-in-up">
            <!-- <div class="inline-flex items-center mb-6 px-4 py-2 bg-white bg-opacity-10 rounded-full text-sm backdrop-blur-sm" style="color: #e0edfb;">
              <span class="mr-2">🛡️</span>
              <span>Advanced AI Threat Detection</span>
            </div> -->

            <div class="flex items-center justify-center gap-4 md:gap-6 mb-6">
              <img
                src="/src/assets/fisheyeLogoWhite.png"
                alt="PhishEye Logo"
                class="w-16 h-16 md:w-24 md:h-24 lg:w-28 lg:h-28 object-contain"
              />
              <h1
                class="text-6xl md:text-8xl font-bold text-transparent bg-clip-text leading-tight"
                style="
                  background: white;
                  -webkit-background-clip: text;
                "
              >
                PhishEye
              </h1>
            </div>
            <p
              class="text-2xl md:text-3xl mb-4 font-light"
              style="color: #e0edfb"
            >
              <span class="font-semibold" style="color: #6fb4ad"
                >99.58% Accuracy</span
              >
              AI-Powered
            </p>
            <p
              class="text-xl md:text-2xl mb-8"
              style="color: #e0edfb; opacity: 0.9"
            >
              Phishing Detection & Threat Intelligence
            </p>
          </div>

          <!-- CTA Buttons -->
          <div
            class="flex flex-col sm:flex-row gap-4 justify-center mb-12 animate-fade-in-up animation-delay-500"
          >
            <router-link
              to="/analyze"
              class="group inline-flex items-center px-8 py-4 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
              style="
                background: linear-gradient(45deg, #6fb4ad, #1f826b);
                color: #e0edfb;
              "
            >
              <span class="mr-2 group-hover:animate-bounce"></span>
              Analyze Email Now
              <span class="ml-2 group-hover:translate-x-1 transition-transform"
                >→</span
              >
            </router-link>

            <button
              @click="scrollToDemo"
              class="inline-flex items-center px-8 py-4 text-lg font-semibold rounded-xl backdrop-blur-sm transition-all duration-300 border"
              style="
                background-color: rgba(224, 237, 251, 0.1);
                color: #e0edfb;
                border-color: rgba(224, 237, 251, 0.2);
              "
            >
              <span class="mr-2"></span>
              See It In Action
            </button>
          </div>

          <!-- Stats Section -->
          <div
            class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto animate-fade-in-up animation-delay-1000"
          >
            <div class="text-center">
              <div
                class="text-4xl font-bold mb-2 counter"
                data-target="99.58"
                style="color: #e0edfb"
              >
                99.58
              </div>
              <div style="color: #6fb4ad">% Accuracy Rate</div>
            </div>
            <div class="text-center">
              <div
                class="text-4xl font-bold mb-2 counter"
                data-target="142"
                style="color: #e0edfb"
              >
                142
              </div>
              <div style="color: #6fb4ad">Training Samples</div>
            </div>
            <div class="text-center">
              <div
                class="text-4xl font-bold mb-2 counter"
                data-target="6"
                style="color: #e0edfb"
              >
                6
              </div>
              <div style="color: #6fb4ad">Threat Categories</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <!-- <div
        class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce"
      >
        <div
          class="w-6 h-10 border-2 rounded-full flex justify-center"
          style="border-color: rgba(224, 237, 251, 0.5)"
        >
          <div
            class="w-1 h-3 rounded-full mt-2 animate-pulse"
            style="background-color: #e0edfb"
          ></div>
        </div>
      </div> -->
    </section>

    <!-- How It Works Section -->
    <section id="demo" class="py-20" style="background-color: #e0edfb">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold mb-4" style="color: #1a5581">
            How it Works
          </h2>
          <p
            class="text-xl max-w-3xl mx-auto"
            style="color: #1a5581; opacity: 0.8"
          >
            Advanced machine learning meets threat intelligence to provide
            unparalleled phishing detection
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <!-- Step 1 -->
          <div
            class="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
          >
            <div
              class="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl mb-6 group-hover:scale-110 transition-transform"
              style="background: linear-gradient(45deg, #6fb4ad, #2caae9)"
            >
              <PhUploadSimple :size="32" color="#f2f2f2" />
            </div>
            <h3 class="text-2xl font-bold mb-4" style="color: #1a5581">
              1. Input
            </h3>
            <p class="mb-4" style="color: #1a5581; opacity: 0.8">
              Paste email content or upload .eml files. Our system preprocesses
              and cleanses the text for optimal analysis.
            </p>
            <div class="font-semibold" style="color: #1f826b">
              → XLM-RoBERTa Processing
            </div>
          </div>

          <!-- Step 2 -->
          <div
            class="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
          >
            <div
              class="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl mb-6 group-hover:scale-110 transition-transform"
              style="background: linear-gradient(45deg, #2caae9, #1f826b)"
            >
              <PhShareNetwork :size="32" color="#f2f2f2" />
            </div>
            <h3 class="text-2xl font-bold mb-4" style="color: #1a5581">
              2. AI Analysis
            </h3>
            <p class="mb-4" style="color: #1a5581; opacity: 0.8">
              Fine-tuned transformer model analyzes context, semantics, and
              patterns with 99.58% accuracy across 142K+ training samples.
            </p>
            <div class="font-semibold" style="color: #1f826b">
              → Threat Intelligence
            </div>
          </div>

          <!-- Step 3 -->
          <div
            class="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-2"
          >
            <div
              class="w-16 h-16 rounded-full flex items-center justify-center text-white text-2xl mb-6 group-hover:scale-110 transition-transform"
              style="background: linear-gradient(45deg, #1f826b, #6fb4ad)"
            >
              <PhChartDonut :size="32" color="#f2f2f2" />
            </div>
            <h3 class="text-2xl font-bold mb-4" style="color: #1a5581">
              3. Detailed Report
            </h3>
            <p class="mb-4" style="color: #1a5581; opacity: 0.8">
              Comprehensive threat analysis with risk scores, attack
              classification, suspicious URLs, and actionable insights.
            </p>
            <div class="font-semibold" style="color: #2caae9">
              → Protection Achieved!
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Showcase -->
    <section class="py-20 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold mb-4" style="color: #1a5581">
             Advanced Threat Intelligence
          </h2>
          <p class="text-xl" style="color: #1a5581; opacity: 0.8">
            Go beyond simple detection with comprehensive threat analysis
          </p>
        </div>

        <div class="grid lg:grid-cols-2 gap-12 items-center max-w-6xl mx-auto">
          <!-- Features List -->
          <div class="space-y-8">
            <div class="flex items-start space-x-4">
              <div
                class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                style="background-color: rgba(111, 180, 173, 0.1)"
              >
                <span class="text-2xl"><PhTimer :size="32" color="#1a5581" /></span>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2" style="color: #1a5581">
                  Real-time Threat Classification
                </h3>
                <p style="color: #1a5581; opacity: 0.8">
                  Instantly categorizes attacks: Credential Harvesting, Social
                  Engineering, Authority Impersonation, and more.
                </p>
              </div>
            </div>

            <div class="flex items-start space-x-4">
              <div
                class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                style="background-color: rgba(111, 180, 173, 0.1)"
              >
                <span class="text-2xl"><PhBracketsCurly :size="32" color="#1a5581" /></span>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2" style="color: #1a5581">
                  Suspicious URL Detection
                </h3>
                <p style="color: #1a5581; opacity: 0.8">
                  Advanced pattern recognition identifies malicious links,
                  shortened URLs, and suspicious domains automatically.
                </p>
              </div>
            </div>

            <div class="flex items-start space-x-4">
              <div
                class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                style="background-color: rgba(111, 180, 173, 0.1)"
              >
                <span class="text-2xl"><PhChartLine :size="32" color="#1a5581" /></span>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2" style="color: #1a5581">
                  Risk Factor Analysis
                </h3>
                <p style="color: #1a5581; opacity: 0.8">
                  Detailed breakdown of urgency indicators, financial threats,
                  grammar anomalies, and social engineering tactics.
                </p>
              </div>
            </div>

            <div class="flex items-start space-x-4">
              <div
                class="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0"
                style="background-color: rgba(111, 180, 173, 0.1)"
              >
                <span class="text-2xl"><PhArticle :size="32" color="#1a5581" /></span>
              </div>
              <div>
                <h3 class="text-xl font-bold mb-2" style="color: #1a5581">
                  AI-Powered Explanations
                </h3>
                <p style="color: #1a5581; opacity: 0.8">
                  Human-readable threat summaries explain exactly why an email
                  is suspicious with confidence scores.
                </p>
              </div>
            </div>
          </div>

          <!-- Demo Preview -->
          <div
            class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-8 text-white"
          >
            <div class="mb-6">
              <div class="flex items-center mb-4">
                <div class="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                <div class="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span class="ml-4 text-gray-400 text-sm"
                  >Analysis Terminal</span
                >
              </div>

              <div class="font-mono text-sm space-y-2">
                <div class="text-green-400">$ analyzing email content...</div>
                <div class="text-blue-400">⚠️ PHISHING DETECTED</div>
                <div class="text-yellow-400">├─ Confidence: 99.8%</div>
                <div class="text-yellow-400">├─ Risk Level: CRITICAL</div>
                <div class="text-yellow-400">
                  ├─ Attack Type: Credential Harvesting
                </div>
                <div class="text-yellow-400">├─ Suspicious URLs: 2 found</div>
                <div class="text-yellow-400">├─ Urgency Indicators: HIGH</div>
                <div class="text-yellow-400">
                  └─ Financial Threats: DETECTED
                </div>
                <div class="text-green-400 animate-pulse">
                  $ analysis complete ✓
                </div>
              </div>
            </div>

            <router-link
              to="/analyze"
              class="inline-flex items-center px-6 py-3 font-semibold rounded-lg transition-all duration-300"
              style="
                background: linear-gradient(45deg, #6fb4ad, #2caae9);
                color: #e0edfb;
              "
            >
              Try Live Demo
              <span class="ml-2">→</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Technology Section -->
    <section
      class="py-20"
      style="
        background: linear-gradient(
          90deg,
          rgba(224, 237, 251, 0.5),
          rgba(111, 180, 173, 0.1)
        );
      "
    >
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-8" style="color: #1a5581">
          Engineered for performance, designed for experience.
        </h2>

        <div class="grid md:grid-cols-4 gap-8 max-w-5xl mx-auto">
          <div
            class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow"
          >
           <div class="text-center mb-4"><img src="../icons/ai.png" alt="neuraal netwerk" class="inline-block w-12 h-12" /></div>
            <h3 class="font-bold mb-2" style="color: #1a5581">XLM-RoBERTa</h3>
            <p class="text-sm" style="color: #1a5581; opacity: 0.8">
              Fine-tuned transformer model with multilingual capabilities
            </p>
          </div>

          <div
            class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow"
          >
            <div class="text-center mb-4"><img src="../icons/python.png" alt="python logo" class="inline-block w-12 h-12" /></div>
            <h3 class="font-bold mb-2" style="color: #1a5581">FastAPI</h3>
            <p class="text-sm" style="color: #1a5581; opacity: 0.8">
              High-performance Python API with automatic documentation
            </p>
          </div>

          <div
            class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">


           <div class="text-center mb-4"><img src="../icons/php.png" alt="PHP logo" class="inline-block w-12 h-12" /></div>
           <h3 class="font-bold mb-2" style="color: #1a5581">Laravel</h3>
            <p class="text-sm" style="color: #1a5581; opacity: 0.8">
              Robust PHP backend with elegant API architecture
            </p>
          </div>
          <div
            class="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow"
          >
            <div class="text-center mb-4"><img src="../icons/vue.png" alt="vue logo" class="inline-block w-12 h-12" /></div>
            <h3 class="font-bold mb-2" style="color: #1a5581">Vue.js</h3>
            <p class="text-sm" style="color: #1a5581; opacity: 0.8">
              Modern reactive frontend with beautiful UI components
            </p>
          </div>

        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section
      class="py-20"
      style="
        background: linear-gradient(90deg, #1a5581, #1f826b);
        color: #e0edfb;
      "
    >
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-4">Ready to Stop Phishing Attacks?</h2>
        <p
          class="text-xl mb-8 max-w-2xl mx-auto"
          style="color: rgba(224, 237, 251, 0.9)"
        >
          Join the fight against cybercrime with state-of-the-art AI protection.
          Experience 99.58% accurate phishing detection today.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/analyze"
            class="inline-flex items-center px-8 py-4 text-lg font-semibold rounded-xl transform hover:scale-105 transition-all duration-300 shadow-lg"
            style="background-color: #e0edfb; color: #1a5581"
          >
            <span class="mr-2"><PhShieldStar :size="32" color="#1a5581" /></span>
            Start Protecting Now
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { PhUploadSimple, PhShareNetwork, PhChartDonut, PhTimer, PhBracketsCurly, PhArticle, PhChartLine, PhShieldStar } from '@phosphor-icons/vue';

export default {
  components: {
    PhUploadSimple,
    PhShareNetwork,
    PhChartDonut,
    PhTimer,
    PhBracketsCurly,
    PhArticle,
    PhChartLine,
    PhShieldStar 
  },
};
</script>

<style scoped>
.animation-delay-500 {
  animation-delay: 0.5s;
}

.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.6s ease-out forwards;
}
</style>
