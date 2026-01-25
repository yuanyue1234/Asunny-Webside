<template>
  <button class="theme-toggle" @click="switchTheme" :title="isDark ? '切换到亮色模式' : '切换到暗色模式'">
    <i class="material-icons">{{ isDark ? 'dark_mode' : 'light_mode' }}</i>
  </button>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const isDark = ref(false)

// 检查系统主题偏好
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')

// 从 localStorage 获取主题设置，如果没有则使用系统偏好
const getInitialTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    return savedTheme === 'dark'
  }
  return prefersDark.matches
}

// 切换主题
async function toggleTheme() {
  isDark.value = !isDark.value
  document.body.classList.toggle('dark-theme', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  await nextTick()
}

// 处理主题切换动画
function switchTheme(event) {
  if (!document.startViewTransition) {
    toggleTheme()
    return
  }

  const { clientX, clientY } = event
  const radius = Math.hypot(
    Math.max(clientX, window.innerWidth - clientX),
    Math.max(clientY, window.innerHeight - clientY)
  )
  const clipPath = [
    `circle(0% at ${clientX}px ${clientY}px)`,
    `circle(${radius}px at ${clientX}px ${clientY}px)`,
  ]

  // 在动画开始前锁定滚动条
  document.documentElement.classList.add('hide-scroll-bar')
  
  const transition = document.startViewTransition(async () => await toggleTheme())
  transition.ready.then(() => {
    document.documentElement.animate({
      clipPath: isDark.value ? clipPath : clipPath.reverse()
    }, {
      duration: 300,
      easing: "ease-in",
      pseudoElement: isDark.value
        ? '::view-transition-new(root)'
        : '::view-transition-old(root)',
    }).onfinish = () => {
      document.documentElement.classList.remove('hide-scroll-bar')
    }
  })
}

// 组件挂载时初始化主题
onMounted(() => {
  isDark.value = getInitialTheme()
  document.body.classList.toggle('dark-theme', isDark.value)
})
</script>

<style scoped>
/* ThemeToggle 组件特定样式 - 主题切换动画相关全局样式 */

/* 隐藏滚动条 */
:global(.hide-scroll-bar) {
  overflow: hidden;
  padding-right: var(--scrollbar-width);
}

/* 确保过渡期间内容可见 */
:global(body) {
  transition: background-color 0s;
  position: relative;
  --scrollbar-width: 0px;
}

:global(body::before) {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--md-sys-color-background);
  z-index: -1;
  transition: background-color 0.3s ease-in;
}

/* 防止动画期间闪烁 */
:global(::view-transition-old(root)),
:global(::view-transition-new(root)) {
  animation: none;
  mix-blend-mode: normal;
}

:global(.dark-theme) {
  --scrollbar-width: 0px;
}

/* 添加平滑滚动条处理 */
:global(html) {
  scrollbar-gutter: stable;
  overflow-y: scroll;
}

:global(::-webkit-scrollbar) {
  width: 8px;
  background-color: transparent;
}

:global(::-webkit-scrollbar-thumb) {
  background-color: var(--md-sys-color-outline);
  border-radius: 4px;
}

:global(::-webkit-scrollbar-thumb:hover) {
  background-color: var(--md-sys-color-outline-variant);
}
</style> 