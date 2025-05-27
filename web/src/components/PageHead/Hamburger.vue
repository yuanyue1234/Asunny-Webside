<template> 
  <div class="nav-items">
    <div class="theme-toggle" @click="">
      <i class="material-icons">menu</i></div>
    <a v-for="item in navItems" :key="item.id || item.url" :href="item.url">{{ item.text }}</a>
    <ThemeToggle />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ThemeToggle from './ThemeToggle.vue'

// 默认导航项
const defaultNavItems = [
  { text: '首页', url: '/' },
  { text: '登录', url: '/login' },
  { text: '留言', url: '/lyb' }
];

const navItems = ref(defaultNavItems);

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/lyb/navitems/'); 
    if (response.data && response.data.length > 0) {
      navItems.value = response.data;
    }
    console.log('Hamburger.vue - 从 API 获取的导航数据:', navItems.value);
  } catch (error) {
    console.error('Hamburger.vue - 获取导航数据失败:', error);
    // 如果 API 请求失败，使用默认导航项
    navItems.value = defaultNavItems;
  }
});
</script>

<style scoped>

/* 下拉菜单样式 */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: var(--md-sys-color-surface);
    min-width: 100px;
    box-shadow: var(--shadow-md);
    z-index: 1;
    border-radius: var(--border-radius-md);
    overflow: hidden;
    padding: var(--spacing-sm) 0;
    margin-top: var(--spacing-sm);
}

.dropdown-content a {
    color: var(--md-sys-color-on-surface);
    padding: var(--spacing-md);
    text-decoration: none;
    display: block;
    transition: background-color var(--transition-normal);
    border-radius: var(--border-radius-sm);
    margin: 0 var(--spacing-xs);
}

.dropdown-content a:hover {
    background-color: var(--md-sys-color-surface-variant);
}

.dropdown:hover .dropdown-content {
    display: block;
}


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
  background-color: var(--md-sys-color-background);
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