<template>
  <div id="app">
    <NavBar />
    <main class="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  }
}
</script>