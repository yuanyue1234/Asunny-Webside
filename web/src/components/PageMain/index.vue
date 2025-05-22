<template>
  <div class="page-main">
    <HeaderImg />
    <profile-section :profile="profileData" />
  </div>
</template>

<script setup>
import ProfileSection from './ProfileSection.vue'
import { profileData } from '@/data/profile'
import "./HeaderImg.vue"
</script>

<style scoped>

</style> 