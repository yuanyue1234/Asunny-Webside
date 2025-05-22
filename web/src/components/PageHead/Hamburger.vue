<template> 
  <div class="nav-items">
    <div class="theme-toggle" @click="">
      <i class="material-icons">menu</i></div>
    <a v-for="item in navItems" :key="item.url" :href="item.url">{{ item.text }}</a>
    <ThemeToggle />
  </div>
</template>

<script setup>
import { navItems } from '@/data/nav'
import ThemeToggle from './ThemeToggle.vue'
</script>

<style scoped>

.nav-toggle {
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  opacity: 0.7;
  /* display: none; */
}

.nav-items {
  /* 固定顶层 */
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  /*  */
  display: flex;
  gap: 15px;
  align-items: center;
  background-color: var(--md-sys-color-surface);
  color: var(--md-sys-color-on-surface);
  border-radius: 32px;
  padding:5px 8px;
  margin-top: 10px;
}

.nav-items a {
  text-decoration: none;
  color: inherit;
  font-size: 14px;
  border-radius: 32px;
  padding: auto;
  width: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  transition: background-color 0.2s;

}
.nav-items a:hover{
  width: 40px;
  height: 40px;
  background-color: var(--md-sys-color-surface-variant);
}

.theme-toggle {
    background: none;
    border: none;
    color: var(--md-sys-color-on-surface);
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    transition: background-color 0.3s;
    margin-right: 8px;
}

.theme-toggle:hover {
    background-color: var(--md-sys-color-surface-variant);
}

.theme-toggle i {
    font-size: 24px;
}

</style>