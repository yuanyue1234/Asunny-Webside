<script setup>
import PageHead from '@/components/PageHead/index.vue'
import PageMain from '@/components/PageMain/index.vue'
import PageFooter from '@/components/PageFooter/index.vue'

// 引入外部CSS和JS
import '@/assets/styles.css'
import '@/assets/js/scripts.js'
import '@/assets/css/normalize.css'
import '@/assets/js/maodian.js'
</script>

<template>
  <div class="app-container">
    <div class="profile">
      <PageHead />
      <router-view></router-view>
      <PageMain />
      <PageFooter />
    </div>
  </div>
</template>

<style>
.app-container {
  min-height: 100vh;
}

.profile {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>