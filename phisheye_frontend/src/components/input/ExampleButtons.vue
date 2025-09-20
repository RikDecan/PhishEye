<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
    
    <!-- phishing Example -->
    <button @click="$emit('load-example', 'phishing')"
      class="group relative px-4 py-3 text-white border-2 white rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg animate-slide-in-up animation-delay-100 flex flex-col items-center"
      style="
        background: linear-gradient(
          45deg,
          rgba(220, 38, 38, 0.6),
          rgba(185, 28, 2, 0.7)
        );
      " :disabled="disabled">
      <div class="text-lg mb-1 group-hover:animate-pulse">
        <PhWarning :size="32" color="#f2f2f2" />
      </div>
      <div class="text-xs font-semibold">Phishing</div>
      <div class="absolute inset-0 bg-red-400 opacity-0 group-hover:opacity-20 rounded-xl transition-opacity"></div>
    </button>

    <!-- Legitimate Example -->
    <button @click="$emit('load-example', 'legitimate')"
      class="group relative px-4 py-3 text-white border-2 white rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg animate-slide-in-up animation-delay-200 flex flex-col items-center"
      style="
        background: linear-gradient(
          45deg,
          rgba(31, 130, 107, 0.6),
          rgba(5, 150, 105, 0.7)
        );
      " :disabled="disabled">
      <div class="text-lg mb-1 group-hover:animate-pulse">
        <PhCheckCircle :size="32" color="#f2f2f2" />
      </div>
      <div class="text-xs font-semibold">Legitimate</div>
      <div class="absolute inset-0 opacity-0 group-hover:opacity-20 rounded-xl transition-opacity"
        style="background-color: #6fb4ad"></div>
    </button>

    <!-- sophisticated Example -->
    <button @click="$emit('load-example', 'sophisticated')"
      class="group relative px-4 py-3 text-white border-2 white rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg animate-slide-in-up animation-delay-300 flex flex-col items-center"
      style="
        background: linear-gradient(
          45deg,
          rgba(234, 88, 12, 0.6),
          rgba(194, 65, 12, 0.7)
        );
      " :disabled="disabled">
      <div class="text-lg mb-1 group-hover:animate-pulse">
        <PhDetective :size="32" color="#f2f2f2" />
      </div>
      <div class="text-xs font-semibold">Advanced</div>
      <div class="absolute inset-0 bg-orange-400 opacity-0 group-hover:opacity-20 rounded-xl transition-opacity"></div>
    </button>

    <!-- Clear button -->
    <button @click="$emit('clear-text')"
      class="group relative px-4 py-3 border-2 white rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg animate-slide-in-up animation-delay-400 flex flex-col items-center"
      style="
        background: linear-gradient(
          45deg,
          rgba(31, 31, 31, 0.5),
          rgba(31, 31, 31, 0.5)
        );
        color: #e0edfb;
      " :disabled="disabled">
      <div class="text-lg mb-1 group-hover:animate-pulse">
        <PhTrash :size="32" color="#f2f2f2" />
      </div>
      <div class="text-xs font-semibold">Clear</div>
      <div class="absolute inset-0 opacity-0 group-hover:opacity-20 rounded-xl transition-opacity"
        style="background-color: rgba(224, 237, 251, 0.2)"></div>
    </button>
  </div>
</template>

<script>
import {
  PhTray,
  PhDetective,
  PhTrash,
  PhCheckCircle,
  PhWarning,
} from "@phosphor-icons/vue";

export default {
  name: "ExampleButtons",
  emits: ["load-example", "clear-text"],
  components: {
    PhTray,
    PhDetective,
    PhTrash,
    PhCheckCircle,
    PhWarning,
  },
};
</script>
