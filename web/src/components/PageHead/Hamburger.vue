<template> 
  <div class="nav-container">
    <div class="theme-toggle menu-button" @click="toggleMenu">
      <i class="material-icons">menu</i>
    </div>
    <div class="nav-items" :class="{ 'show-menu': isMenuOpen }">
      <router-link v-for="item in internalNavItems" :key="item.url" :to="item.url">{{ item.text }}</router-link>
      <a v-for="item in externalNavItems" :key="item.url" :href="item.url" target="_blank">{{ item.text }}</a>
    </div>
          <ThemeToggle />

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import ThemeToggle from './ThemeToggle.vue'

const isMenuOpen = ref(false);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

// 默认导航项
const defaultNavItems = [
  { text: '首页', url: '/' },
  { text: '留言', url: '/lyb' },
  { text: '简介', url: '/my' }
];

const navItems = ref(defaultNavItems);

// 分离内部和外部链接
const internalNavItems = computed(() => {
  return navItems.value.filter(item => !item.isExternal);
});

const externalNavItems = computed(() => {
  return navItems.value.filter(item => item.isExternal);
});

const fetchNavItems = async () => {
  try {
    const response = await axios.get('/api/is/navitems/');
    if (response.data && response.data.results) {
      navItems.value = response.data.results.map(item => ({
        text: item.text,
        url: item.url,
        isExternal: item.isExternal
      }));
    }
    console.log('Hamburger.vue - 从 API 获取的导航数据:', navItems.value);
  } catch (error) {
    console.error('Hamburger.vue - 获取导航数据失败:', error);
    // 如果 API 请求失败，使用默认导航项
    navItems.value = defaultNavItems;
  }
};

onMounted(fetchNavItems);
</script>

<style scoped>
.nav-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.menu-button {
  display: none !important;
  position: fixed;
  left: 20px;
  top: 10px;
  z-index: 10000;
  transition: all 0.3s ease;
}

.menu-button:hover {
  transform: scale(1.1);
  background-color: var(--md-sys-color-surface-variant);
}

.nav-items {
  display: flex;
  gap: 15px;
  align-items: center;
  background-color: var(--md-sys-color-background);
  color: var(--md-sys-color-on-surface);
  border-radius: 32px;
  padding: 5px 8px;
  margin-top: 10px;
  transition: all 0.3s ease;
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
  transition: all 0.3s ease;
}

.nav-items a:hover {
  width: 40px;
  height: 40px;
  background-color: var(--md-sys-color-surface-variant);
  transform: scale(1.1);
}

@media screen and (max-width: 650px) {
  .menu-button {
    display: flex !important;
  }

  .nav-items {
    display: none;
    flex-direction: column;
    position: fixed;
    top: 60px;
    left: 20px;
    transform: none;
    background-color: var(--md-sys-color-background);
    border-radius: 12px;
    padding: 8px;
    box-shadow: var(--shadow-md);
    width: 200px;
    animation: slideIn 0.3s ease;
  }

  .nav-items.show-menu {
    display: flex;
  }

  .nav-items a {
    width: 100%;
    text-align: left;
    margin: 0;
    line-height: 25px;
    padding: 8px 16px;
    border-radius: 8px;
  }

  .nav-items a:hover {
    width: 100%;
    transform: translateX(5px);
    background-color: var(--md-sys-color-surface-variant);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 亮暗切换按钮样式 */
:deep(.theme-toggle) {
  position: fixed;
  right: 20px;
  top: 10px;
  z-index: 10000;
  transition: all 0.3s ease;
}

:deep(.theme-toggle:hover) {
  transform: scale(1.1);
  background-color: var(--md-sys-color-surface-variant);
  
  
}

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