<script setup>
import { ref, onMounted } from 'vue'

const isDarkTheme = ref(localStorage.getItem('theme') === 'dark')

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value
  document.body.classList.toggle('dark-theme')
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light')
}

onMounted(() => {
  if (isDarkTheme.value) {
    document.body.classList.add('dark-theme')
  }
  
  // 生成目录
  const toc = document.getElementById('toc')
  const headings = document.querySelectorAll('h2, h3')
  const tocLinks = []

  headings.forEach(heading => {
    if (!heading.id) {
      heading.id = heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-')
    }
    
    const link = document.createElement('a')
    link.href = `#${heading.id}`
    link.textContent = heading.textContent
    
    if (heading.tagName === 'H3') {
      link.classList.add('h3-link')
    }
    
    link.addEventListener('click', (e) => {
      e.preventDefault()
      heading.scrollIntoView({ behavior: 'smooth' })
      history.pushState(null, '', link.href)
    })
    
    toc.appendChild(link)
    tocLinks.push({
      link: link,
      heading: heading
    })
  })

  // 添加滚动监听
  let ticking = false
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        highlightCurrentSection(tocLinks)
        ticking = false
      })
      ticking = true
    }
  })

  // 初始检查 URL 中的锚点
  if (window.location.hash) {
    const targetHeading = document.querySelector(window.location.hash)
    if (targetHeading) {
      setTimeout(() => {
        targetHeading.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    }
  }
})

const highlightCurrentSection = (tocLinks) => {
  const scrollPosition = window.scrollY

  tocLinks.forEach(({ link, heading }) => {
    const headingTop = heading.offsetTop
    const headingBottom = headingTop + heading.offsetHeight

    if (scrollPosition >= headingTop - 100 && scrollPosition < headingBottom - 100) {
      link.classList.add('active')
    } else {
      link.classList.remove('active')
    }
  })
}
</script>

<template>
  <div class="container">
    <header>
      <div class="header-content">
        <a href="/">首页</a>
        <button class="theme-toggle" @click="toggleTheme">
          <i class="material-icons">{{ isDarkTheme ? 'dark_mode' : 'light_mode' }}</i>
        </button>
      </div>
    </header>

    <nav>
      <a href="#profile">个人资料</a>
      <a href="#showcase">作品展示</a>
      <a href="#contact">联系方式</a>
    </nav>

    <main>
      <div id="toc" class="sidebar"></div>
      <div class="content">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<style>
:root {
    --md-sys-color-primary: #6750A4;
    --md-sys-color-on-primary: #FFFFFF;
    --md-sys-color-primary-container: #EADDFF;
    --md-sys-color-on-primary-container: #21005D;
    --md-sys-color-secondary: #625B71;
    --md-sys-color-on-secondary: #FFFFFF;
    --md-sys-color-secondary-container: #E8DEF8;
    --md-sys-color-on-secondary-container: #1D192B;
    --md-sys-color-surface: #FFFBFE;
    --md-sys-color-on-surface: #1C1B1F;
    --md-sys-color-surface-variant: #E7E0EC;
    --md-sys-color-on-surface-variant: #49454F;
    --md-sys-color-outline: #79747E;
    --md-sys-color-background: #FFFBFE;
}

body.dark-theme {
    --md-sys-color-primary: #D0BCFF;
    --md-sys-color-on-primary: #381E72;
    --md-sys-color-primary-container: #4F378B;
    --md-sys-color-on-primary-container: #EADDFF;
    --md-sys-color-secondary: #CCC2DC;
    --md-sys-color-on-secondary: #332D41;
    --md-sys-color-secondary-container: #4A4458;
    --md-sys-color-on-secondary-container: #E8DEF8;
    --md-sys-color-surface: #1C1B1F;
    --md-sys-color-on-surface: #E6E1E5;
    --md-sys-color-surface-variant: #49454F;
    --md-sys-color-on-surface-variant: #CAC4D0;
    --md-sys-color-outline: #938F99;
    --md-sys-color-background: #1C1B1F;
}

html, body {
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background-color: var(--md-sys-color-background);
    color: var(--md-sys-color-on-surface);
    transition: background-color 0.3s, color 0.3s;
    min-height: 100vh;
}

.container {
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
}

header {
    background-color: var(--md-sys-color-surface);
    padding: 15px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    transition: background-color 0.3s;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-content a {
    font-size: 28px;
    margin: 0;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-decoration: none;
    color: var(--md-sys-color-primary);
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    background-color: var(--md-sys-color-surface);
    max-width: 800px;
    margin: 0 auto;
    transition: background-color 0.3s;
}

nav a {
    color: var(--md-sys-color-primary);
    text-decoration: none;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 12px;
    border-radius: 20px;
    transition: background-color 0.3s, color 0.3s;
    cursor: pointer;
}

nav a:hover {
    background-color: var(--md-sys-color-secondary-container);
}

.theme-toggle {
    background: none;
    border: none;
    color: var(--md-sys-color-primary);
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.theme-toggle:hover {
    background-color: var(--md-sys-color-surface-variant);
}

.theme-toggle i {
    font-size: 24px;
}

.sidebar {
    position: fixed;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    background-color: var(--md-sys-color-surface);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 200px;
    transition: background-color 0.3s;
}

.sidebar a {
    display: block;
    color: var(--md-sys-color-on-surface);
    text-decoration: none;
    padding: 8px 0;
    font-size: 14px;
    transition: color 0.3s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.sidebar a:hover {
    color: var(--md-sys-color-primary);
}

.sidebar a.active {
    color: var(--md-sys-color-primary);
    font-weight: 500;
}

.sidebar a.h3-link {
    padding-left: 16px;
    font-size: 12px;
}

.sidebar a.h3-link.active {
    color: var(--md-sys-color-primary);
}

.content {
    margin-right: 240px;
    padding: 20px;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.5s ease-out;
}
</style> 