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

<template>
    <div class="container">
      <ProfileSection :profile="profileData" />
      <lyb />
    </div>
</template>