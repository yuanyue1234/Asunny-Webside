<script setup>
import { ref } from 'vue'
import ProfileSection from '@/components/ProfileSection.vue'
import { profileData } from '@/data/profile'
import { navItems } from '@/data/nav'
import lyb from '@/components/lyb.vue'

// 引入外部CSS和JS
import '@/assets/styles.css'
import '@/assets/scripts.js'
</script>

<style>

</style>
<template>
  <div>
    <header>
      <div class="container header-content">
        <h1><a href="#">ASUNNY</a></h1>
        <button class="theme-toggle" aria-label="Toggle dark mode">
          <i class="material-icons">light_mode</i>
          
        </button>
      </div>
    </header>

    <nav>
      <a v-for="item in navItems" :key="item.url" :href="item.url">{{ item.text }}</a>
    </nav>

    <div class="container">
      <ProfileSection :profile="profileData" />
      <lyb />
    </div>

  </div>
</template>