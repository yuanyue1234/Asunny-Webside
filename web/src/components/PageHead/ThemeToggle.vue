<template>
  <button class="theme-toggle" @click="toggleTheme">
    <i class="material-icons">{{ isDark ? 'dark_mode' : 'light_mode' }}</i>
  </button>
</template>

<script setup>
import { ref } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.body.classList.toggle('dark-theme')
}
</script>

<style scoped>


</style> 