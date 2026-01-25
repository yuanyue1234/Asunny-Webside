<script setup>
import { ref, onMounted } from 'vue'
import { isUserLoggedIn, fetchUserInfo } from '@/utils/user.js'

const isLoggedIn = ref(false)
const username = ref('')

onMounted(async () => {
  isLoggedIn.value = isUserLoggedIn()
  if (isLoggedIn.value) {
    try {
      const userInfo = await fetchUserInfo()
      username.value = userInfo?.username || ''
    } catch (error) {
      console.error('Failed to fetch user info:', error)
    }
  }
  
  // 加载一言API
  loadHitokoto()
  
  // 添加点击一言返回顶部的事件监听
  setupHitokotoClickEvent()
})

// 加载一言API的函数
const loadHitokoto = () => {
  const script = document.createElement('script')
  script.src = 'https://v1.hitokoto.cn/?encode=js&select=%23hitokoto'
  script.defer = true
  document.body.appendChild(script)
}

// 设置点击一言返回顶部的事件
const setupHitokotoClickEvent = () => {
  // 使用事件委托，将事件监听器添加到父元素
  document.addEventListener('click', (e) => {
    // 检查点击的元素或其父元素是否是hitokoto_text
    let target = e.target;
    while (target) {
      if (target.id === 'hitokoto_text') {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
        break;
      }
      target = target.parentElement;
    }
  });
}
</script>
<template>
  <div class="page-footer">
    <!-- 一言 -->
    <div class="hitokoto-container">
        <div class="hitokoto-text">
          <span>
            
            <span id="hitokoto">
              <a href="javascript:void(0);" id="hitokoto_text">"你只活一次"</a>
            </span>
            
          </span>
        </div>
      </div>
    <div class="manage">
      <div class="manage-item">
        <a :href="isLoggedIn ? `/login` : '/login'">{{ isLoggedIn ? username : '登录' }}</a>
        |
        <a href="/profile">管理</a>
      </div>
    </div>
  </div>
</template>

<script>
</script>

<style scoped>
/* PageFooter 组件特定样式 - 磨砂玻璃风格 */

/* 一言容器 - 磨砂玻璃卡片 */
#hitokoto {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: var(--spacing-lg) auto;
  padding: var(--spacing-lg);
  max-width: 600px;
  transition: all var(--transition-normal);
  position: relative;
  z-index: 10;

  /* 磨砂玻璃效果 */
  background: var(--glass-bg);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--glass-shadow);
}

#hitokoto:hover {
  box-shadow: 0 12px 40px rgba(155, 143, 200, 0.18);
  transform: translateY(-3px);
}

body.dark-theme #hitokoto:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
}

#hitokoto_text {
  color: var(--md-sys-color-on-surface-variant);
  text-decoration: none;
  font-style: italic;
  transition: all var(--transition-normal);
  font-weight: 500;
  font-size: var(--font-size-lg);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  position: relative;
  z-index: 20;
  line-height: 1.6;
}

#hitokoto_text:hover {
  color: var(--md-sys-color-primary);
  background: var(--md-sys-color-primary-container);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 管理链接区域 */
.manage {
  display: flex;
  justify-content: center;
  padding: var(--spacing-lg) 0 var(--spacing-xl);
}

.manage-item {
  color: var(--md-sys-color-on-surface-variant);
  font-size: var(--font-size-sm);

  /* 磨砂玻璃背景 */
  background: var(--glass-bg);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.manage-item:hover {
  box-shadow: var(--shadow-md);
}

body.dark-theme .manage-item:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.manage-item a {
  color: var(--md-sys-color-on-surface-variant);
  text-decoration: none;
  transition: all var(--transition-normal);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-weight: 500;
}

.manage-item a:hover {
  color: var(--md-sys-color-primary);
  background: var(--md-sys-color-primary-container);
  transform: translateY(-1px);
}
</style> 