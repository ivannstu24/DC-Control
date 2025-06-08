<template>
  <div class="landing-page">
    <nav class="navbar">
      <div class="logo">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
          <line x1="8" y1="21" x2="16" y2="21"></line>
          <line x1="12" y1="17" x2="12" y2="21"></line>
        </svg>
        <span>DataCenter Control</span>
      </div>
      <div class="nav-links">
        <button @click="$router.push('/login')" class="login-btn">Войти</button>
        <button @click="$router.push('/register')" class="register-btn">Регистрация</button>
      </div>
    </nav>

    <section class="hero">
      <div class="hero-content">
        <h1>
          <span class="title-line">Управление дата-центром</span>
          <span class="title-line">на <span class="highlight-text">новом уровне</span></span>
        </h1>
        <p class="subtitle">Мощный инструмент для администрирования серверов, управления доступом и мониторинга инфраструктуры</p>
        <div class="cta-buttons">
          <button @click="$router.push('/login')" class="primary-btn">
            <span>Начать работу</span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
     
        </div>
      </div>
      <div class="hero-image">
        <div class="server-animation">
          <div class="server-rack">
            <div class="server-blade" v-for="n in 8" :key="n" :style="`--delay: ${n * 0.1}s`">
              <div class="led-indicator"></div>
              <div class="blade-content"></div>
            </div>
          </div>
          <div class="network-lines">
            <div class="line" v-for="n in 12" :key="n" :style="`--n: ${n}`"></div>
          </div>
          <div class="floating-elements">
            <div class="circle" v-for="n in 5" :key="'circle'+n" :style="`--size: ${Math.random() * 20 + 10}px; --top: ${Math.random() * 80 + 10}%; --left: ${Math.random() * 80 + 10}%; --delay: ${Math.random() * 5}s`"></div>
          </div>
        </div>
      </div>
      <div class="scrolling-indicator" @click="scrollToFeatures">
        <div class="mouse">
          <div class="wheel"></div>
      
      </div>
      </div>
     </section>

  </div>
  
</template>

<script>
import { ref } from 'vue'

const ServerIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
      <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
      <line x1="6" y1="6" x2="6" y2="6"></line>
      <line x1="6" y1="18" x2="6" y2="18"></line>
    </svg>
  `
}

const ShieldIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    </svg>
  `
}

const UsersIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="9" cy="7" r="4"></circle>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
  `
}

const ActivityIcon = {
  template: `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
    </svg>
  `
}

export default {
  components: {
    ServerIcon,
    ShieldIcon,
    UsersIcon,
    ActivityIcon
  },
  setup() {
    const features = ref([
  
    ])

    const colors = ['#6366f1', '#8b5cf6', '#a855f7', '#d946ef', '#ec4899', '#f43f5e']
    const featuresRef = ref(null)
    
    const companyLogos = ref([
      'https://via.placeholder.com/100x40/6366f1/ffffff?text=Company+1',
      'https://via.placeholder.com/100x40/8b5cf6/ffffff?text=Company+2',
      'https://via.placeholder.com/100x40/a855f7/ffffff?text=Company+3',
      'https://via.placeholder.com/100x40/d946ef/ffffff?text=Company+4'
    ])
    
    const testimonials = ref([
     
    ])
    
    const socialLinks = ref([
      { name: 'Twitter', icon: 'https://via.placeholder.com/24/ffffff/6366f1?text=Tw' },
      { name: 'Facebook', icon: 'https://via.placeholder.com/24/ffffff/6366f1?text=Fb' },
      { name: 'LinkedIn', icon: 'https://via.placeholder.com/24/ffffff/6366f1?text=In' },
      { name: 'Instagram', icon: 'https://via.placeholder.com/24/ffffff/6366f1?text=Ig' }
    ])
    
    const footerLinks = ref([
      
    ])

    const scrollToFeatures = () => {
      featuresRef.value.scrollIntoView({ behavior: 'smooth' })
    }

    return {
      features,
      colors,
      featuresRef,
      companyLogos,
      testimonials,
      socialLinks,
      footerLinks,
      scrollToFeatures
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #6366f1;
  --primary-dark: #4f46e5;
  --secondary: #8b5cf6;
  --accent: #d946ef;
  --text: #1e293b;
  --text-light: #64748b;
  --bg: #f8fafc;
  --bg-dark: #f1f5f9;
  --white: #ffffff;
  --gray: #e2e8f0;
  --gray-dark: #cbd5e1;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.landing-page {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-color: var(--bg);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 5%;
  background-color: var(--white);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.8);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1.25rem;
  color: var(--primary);
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo svg {
  width: 24px;
  height: 24px;
  stroke: var(--primary);
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.login-btn, .register-btn {
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.login-btn {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--gray);
}

.login-btn:hover {
  background: var(--bg);
  border-color: var(--primary);
  box-shadow: 0 2px 10px rgba(99, 102, 241, 0.1);
}

.register-btn {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: var(--white);
  border: none;
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.register-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--secondary));
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8rem 5% 6rem;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 80%;
  height: 200%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, rgba(99, 102, 241, 0) 70%);
  z-index: 0;
}

.hero-content {
  max-width: 550px;
  position: relative;
  z-index: 1;
}

.title-line {
  display: block;
  line-height: 1.2;
}

.hero h1 {
  font-size: 3.25rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.75rem;
  color: var(--text);
}

.highlight-text {
  background: linear-gradient(90deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  background-clip: text;
  color:  #d5a8ff;
  position: relative;
  display: inline-block;
}

.highlight-text::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: 3px;
  transform: scaleX(0);
  transform-origin: right;
  animation: highlightUnderline 1.5s ease-in-out forwards;
  animation-delay: 0.5s;
}

@keyframes highlightUnderline {
  0% {
    transform: scaleX(0);
    transform-origin: right;
  }
  50% {
    transform: scaleX(1);
    transform-origin: right;
  }
  51% {
    transform-origin: left;
  }
  100% {
    transform: scaleX(1);
    transform-origin: left;
  }
}

.subtitle {
  font-size: 1.25rem;
  color: var(--text-light);
  margin-bottom: 2.5rem;
  max-width: 90%;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.primary-btn, .secondary-btn {
  padding: 0.9rem 1.75rem;
  border-radius: 10px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
}

.primary-btn {
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: var(--white);
  border: none;
  box-shadow: 0 4px 15px -3px rgba(99, 102, 241, 0.4);
}

.primary-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--secondary));
  transform: translateY(-3px);
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
}

.primary-btn svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.primary-btn:hover svg {
  transform: translateX(3px);
}

.secondary-btn {
  background: var(--white);
  color: var(--primary);
  border: 1px solid var(--gray);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.secondary-btn:hover {
  background: var(--bg);
  border-color: var(--primary);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.secondary-btn svg {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
}

.secondary-btn:hover svg {
  transform: translateY(3px);
}

.trusted-by {
  margin-top: 3rem;
}

.trusted-text {
  font-size: 0.9rem;
  color: var(--text-light);
  margin-bottom: 1rem;
}

.company-logos {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.logo-item {
  height: 30px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.logo-item:hover {
  opacity: 1;
}

.logo-item img {
  height: 100%;
  object-fit: contain;
  filter: grayscale(100%) brightness(0.5);
  transition: filter 0.3s ease;
}

.logo-item:hover img {
  filter: grayscale(0) brightness(1);
}

.hero-image {
  position: relative;
  width: 50%;
  height: 600px;
  z-index: 1;
}

.server-animation {
  position: relative;
  width: 100%;
  height: 100%;
}

.server-rack {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 220px;
  height: 80%;
  background: var(--white);
  border-radius: 12px;
  box-shadow: 0 20px 50px -10px rgba(0, 0, 0, 0.15);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 2;
}

.server-blade {
  background: var(--bg-dark);
  height: 45px;
  border-radius: 6px;
  position: relative;
  overflow: hidden;
  animation: blink 2s infinite;
  animation-delay: var(--delay);
  display: flex;
  align-items: center;
  padding: 0 1rem;
}

.led-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #10b981;
  margin-right: 0.75rem;
  box-shadow: 0 0 10px #10b981;
  animation: pulse 2s infinite;
  animation-delay: var(--delay);
}

.blade-content {
  flex: 1;
  height: 10px;
  background: linear-gradient(90deg, #e2e8f0, #f1f5f9, #e2e8f0);
  background-size: 200% 100%;
  animation: loading 2s infinite linear;
  animation-delay: var(--delay);
  border-radius: 4px;
}

@keyframes blink {
  0%, 100% { opacity: 0.9; }
  50% { opacity: 1; box-shadow: inset 0 0 15px rgba(99, 102, 241, 0.2); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.network-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100% - 220px);
  height: 100%;
  overflow: hidden;
}

.line {
  position: absolute;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), transparent);
  animation: flow 4s infinite linear;
  opacity: 0;
  filter: drop-shadow(0 0 5px var(--primary));
}

.line:nth-child(odd) {
  background: linear-gradient(90deg, var(--secondary), transparent);
  filter: drop-shadow(0 0 5px var(--secondary));
}

.line:nth-child(3n) {
  background: linear-gradient(90deg, var(--accent), transparent);
  filter: drop-shadow(0 0 5px var(--accent));
}

.line:nth-child(1) {
  top: 15%;
  width: 80%;
  animation-delay: calc(var(--n) * 0.3s);
}

.line:nth-child(2) {
  top: 25%;
  width: 60%;
  animation-delay: calc(var(--n) * 0.5s);
}

.line:nth-child(3) {
  top: 35%;
  width: 90%;
  animation-delay: calc(var(--n) * 0.7s);
}

.line:nth-child(4) {
  top: 45%;
  width: 70%;
  animation-delay: calc(var(--n) * 0.2s);
}

.line:nth-child(5) {
  top: 55%;
  width: 85%;
  animation-delay: calc(var(--n) * 0.4s);
}

.line:nth-child(6) {
  top: 65%;
  width: 75%;
  animation-delay: calc(var(--n) * 0.6s);
}

.line:nth-child(7) {
  top: 75%;
  width: 65%;
  animation-delay: calc(var(--n) * 0.8s);
}

.line:nth-child(8) {
  top: 85%;
  width: 95%;
  animation-delay: calc(var(--n) * 0.1s);
}

@keyframes flow {
  0% { transform: translateX(-100%); opacity: 0; }
  10% { opacity: 0.8; }
  90% { opacity: 0.8; }
  100% { transform: translateX(100%); opacity: 0; }
}

.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
  width: var(--size);
  height: var(--size);
  top: var(--top);
  left: var(--left);
  animation: float 8s infinite ease-in-out;
  animation-delay: var(--delay);
  opacity: 0.7;
}

@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-20px) translateX(10px); }
  50% { transform: translateY(10px) translateX(-10px); }
  75% { transform: translateY(-10px) translateX(20px); }
}

.scrolling-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  z-index: 10;
  opacity: 0.7;
  transition: opacity 0.3s ease;
  animation: bounce 2s infinite;
}

.scrolling-indicator:hover {
  opacity: 1;
}

.mouse {
  width: 24px;
  height: 40px;
  border: 2px solid var(--text-light);
  border-radius: 12px;
  display: flex;
  justify-content: center;
  padding-top: 6px;
  margin-bottom: 0.5rem;
}

.wheel {
  width: 4px;
  height: 8px;
  background-color: var(--text-light);
  border-radius: 2px;
  animation: scroll 2s infinite;
}

.scrolling-indicator span {
  font-size: 0.8rem;
  color: var(--text-light);
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0) translateX(-50%); }
  40% { transform: translateY(-10px) translateX(-50%); }
  60% { transform: translateY(-5px) translateX(-50%); }
}

@keyframes scroll {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(10px); opacity: 0; }
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-header h2 {
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--text);
}

.section-subtitle {
  font-size: 1.125rem;
  color: var(--text-light);
  max-width: 600px;
  margin: 0 auto;
}

.features {
  padding: 8rem 5%;
  background: var(--white);
  position: relative;
  overflow: hidden;
}

.features::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23e2e8f0' fill-opacity='0.2'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.3;
  z-index: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.feature-card {
  background: var(--white);
  border-radius: 16px;
  padding: 2.5rem 2rem;
  transition: all 0.4s ease;
  border: 1px solid var(--gray);
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease forwards;
  animation-delay: var(--delay);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.03);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.75rem;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: rotate(10deg) scale(1.1);
}

.feature-icon svg {
  width: 26px;
  height: 26px;
  stroke: var(--white);
}

.feature-card h3 {
  font-size: 1.375rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text);
}

.feature-card p {
  color: var(--text-light);
  margin-bottom: 1.5rem;
}

.feature-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  border-radius: 0 0 0 100px;
  opacity: 0.1;
  transition: opacity 0.3s ease;
}

.feature-card:hover .feature-decoration {
  opacity: 0.2;
}

.demo {
  display: flex;
  align-items: center;
  padding: 8rem 5%;
  background: linear-gradient(135deg, var(--bg) 0%, var(--bg-dark) 100%);
  position: relative;
}

.demo::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 340px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%236366f1'/%3E%3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='%236366f1'/%3E%3Cpath d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='%236366f1'/%3E%3C/svg%3E");
  background-size: cover;
  background-repeat: no-repeat;
  transform: rotate(180deg);
  opacity: 0.1;
}

.demo-content {
  max-width: 500px;
  position: relative;
  z-index: 1;
}

.demo h2 {
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: var(--text);
}

.demo p {
  font-size: 1.125rem;
  color: var(--text-light);
  margin-bottom: 2.5rem;
}

.demo-preview {
  flex: 1;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.dashboard-preview {
  width: 500px;
  height: 300px;
  background: var(--white);
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  position: relative;
  transform: perspective(1000px) rotateY(-10deg) rotateX(5deg);
  transition: transform 0.5s ease;
}

.dashboard-preview:hover {
  transform: perspective(1000px) rotateY(0) rotateX(0);
}

.preview-header {
  height: 60px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
}

.header-tabs {
  display: flex;
  gap: 1rem;
}

.tab {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab.active {
  background: rgba(255, 255, 255, 0.15);
  color: var(--white);
}

.preview-chart {
  display: flex;
  align-items: flex-end;
  gap: 1.5rem;
  height: 120px;
  padding: 1.5rem;
  border-bottom: 1px solid var(--gray);
}

.chart-line {
  width: 40px;
  background: linear-gradient(to top, var(--primary), var(--secondary));
  border-radius: 6px 6px 0 0;
  height: var(--height);
  animation: pulse 2s infinite ease-in-out;
  animation-delay: calc(var(--n) * 0.1s);
}

.preview-items {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
}

.preview-item {
  background: var(--bg-dark);
  height: 50px;
  border-radius: 6px;
  flex: 1;
  position: relative;
  overflow: hidden;
}

.item-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--width);
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 6px;
  transition: width 1s ease;
}

.notification-bell {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: var(--white);
  border-radius: 50%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  animation: ring 4s infinite ease;
}

.bell-icon {
  font-size: 0.9rem;
}

.notification-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--accent);
  color: var(--white);
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6rem;
  font-weight: 600;
}

@keyframes ring {
  0%, 50%, 100% { transform: rotate(0); }
  5%, 15%, 25% { transform: rotate(15deg); }
  10%, 20%, 30% { transform: rotate(-15deg); }
}

.testimonials {
  padding: 8rem 5%;
  background: var(--white);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.testimonial-card {
  background: var(--bg);
  border-radius: 16px;
  padding: 2.5rem;
  transition: all 0.3s ease;
  border: 1px solid var(--gray);
  position: relative;
  overflow: hidden;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border-color: var(--primary);
}

.testimonial-content {
  position: relative;
  margin-bottom: 2rem;
}

.quote-icon {
  position: absolute;
  top: -1.5rem;
  left: -1rem;
  font-size: 5rem;
  color: var(--primary);
  opacity: 0.1;
  font-family: serif;
  line-height: 1;
}

.testimonial-content p {
  color: var(--text-light);
  font-style: italic;
  position: relative;
  z-index: 1;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary);
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  color: var(--text);
}

.author-position {
  font-size: 0.875rem;
  color: var(--text-light);
}

.cta-section {
  padding: 1rem 5%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: var(--white);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.3;
}

.cta-container {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.cta-section h2 {
  font-size: 2.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.cta-section p {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2.5rem;
}

.primary-btn.large {
  padding: 1.1rem 2.5rem;
  font-size: 1.1rem;
  background: var(--white);
  color: var(--primary);
  margin: 0 auto;
}

.primary-btn.large:hover {
  background: rgba(255, 255, 255, 0.9);
  color: var(--primary-dark);
}

.footer {
  background: var(--text);
  color: var(--white);
  padding: 6rem 5% 3rem;
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%23ffffff'/%3E%3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='%23ffffff'/%3E%3Cpath d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='%23ffffff'/%3E%3C/svg%3E");
  background-size: cover;
  background-repeat: no-repeat;
  transform: rotate(180deg);
  opacity: 0.1;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 3rem;
  position: relative;
  z-index: 1;
  gap: 3rem;
}

.footer-main {
  max-width: 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.footer-logo svg {
  width: 24px;
  height: 24px;
  stroke: var(--white);
}

.footer-description {
  color: #94a3b8;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: var(--primary);
  transform: translateY(-3px);
}

.social-link img {
  width: 18px;
  height: 18px;
}

.footer-links {
  display: flex;
  flex: 1;
  gap: 3rem;
  flex-wrap: wrap;
}

.link-column {
  min-width: 150px;
}

.column-title {
  font-weight: 600;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

.link-item {
  display: block;
  color: #94a3b8;
  text-decoration: none;
  margin-bottom: 0.75rem;
  transition: color 0.3s ease;
}

.link-item:hover {
  color: var(--white);
}

.footer-bottom {
  text-align: center;
  padding-top: 3rem;
  border-top: 1px solid #334155;
  color: #94a3b8;
  font-size: 0.875rem;
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.legal-links {
  display: flex;
  gap: 1.5rem;
}

.legal-links a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.legal-links a:hover {
  color: var(--white);
}

@media (max-width: 1024px) {
  .hero {
    flex-direction: column;
    text-align: center;
    padding-top: 8rem;
    padding-bottom: 4rem;
  }
  
  .hero-content {
    max-width: 100%;
    margin-bottom: 3rem;
  }
  
  .subtitle {
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
  }
  
  .cta-buttons {
    justify-content: center;
  }
  
  .hero-image {
    width: 100%;
    height: 400px;
  }
  
  .server-rack {
    right: 50%;
    transform: translate(50%, -50%);
  }
  
  .demo {
    flex-direction: column;
    text-align: center;
  }
  
  .demo-content {
    max-width: 100%;
    margin-bottom: 3rem;
  }
  
  .dashboard-preview {
    transform: none;
  }
  
  .dashboard-preview:hover {
    transform: none;
  }
  
  .footer-content {
    flex-direction: column;
  }
  
  .footer-main {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .testimonials-grid {
    grid-template-columns: 1fr;
  }
  
  .footer-links {
    flex-direction: column;
    gap: 2rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
  }
  
  .legal-links {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .section-header h2 {
    font-size: 1.8rem;
  }
  
  .section-subtitle {
    font-size: 1rem;
  }
  
  .demo h2 {
    font-size: 1.8rem;
  }
  
  .demo p {
    font-size: 1rem;
  }
  
  .dashboard-preview {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .hero h1 {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .primary-btn, .secondary-btn {
    width: 100%;
  }
  
  .navbar {
    padding: 1rem;
  }
  
  .nav-links {
    gap: 0.5rem;
  }
  
  .login-btn, .register-btn {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
}
</style>