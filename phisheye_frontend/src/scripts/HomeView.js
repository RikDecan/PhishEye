
export default {
  name: 'HomeView',
  mounted() {
    this.animateCounters()
    this.setupScrollAnimations()
  },
  methods: {
    scrollToDemo() {
      document.getElementById('demo').scrollIntoView({ 
        behavior: 'smooth' 
      })
    },
    animateCounters() {
      const counters = document.querySelectorAll('.counter')
      
      counters.forEach(counter => {
        const target = parseFloat(counter.getAttribute('data-target'))
        const increment = target / 100
        let current = 0
        
        const timer = setInterval(() => {
          current += increment
          if (current >= target) {
            current = target
            clearInterval(timer)
          }
          
          if (target === 99.58) {
            counter.textContent = current.toFixed(2)
          } else if (target === 142) {
            counter.textContent = Math.floor(current) + 'K'
          } else {
            counter.textContent = Math.floor(current)
          }
        }, 20)
      })
    },
    setupScrollAnimations() {
      const animatedElements = document.querySelectorAll('.animate-fade-in-up')
      
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