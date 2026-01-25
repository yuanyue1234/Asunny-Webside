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

  // 添加点击一言复制的事件监听
  setupHitokotoClickEvent()
})

// 加载一言API的函数
const loadHitokoto = () => {
  const script = document.createElement('script')
  script.src = 'https://v1.hitokoto.cn/?encode=js&select=%23hitokoto'
  script.defer = true
  document.body.appendChild(script)
}

// 设置点击一言复制的事件
const setupHitokotoClickEvent = () => {
  document.addEventListener('click', async (e) => {
    let target = e.target;
    while (target) {
      if (target.id === 'hitokoto_text') {
        e.preventDefault();

        const text = target.textContent;

        try {
          await navigator.clipboard.writeText(text);

          // 简单的复制反馈
          const originalText = target.textContent;
          target.textContent = '✓ 已复制';
          target.style.color = 'var(--md-sys-color-primary)';

          setTimeout(() => {
            target.textContent = originalText;
            target.style.color = '';
          }, 1500);
        } catch (error) {
          console.error('复制失败:', error);
        }

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
    <div class="hitokoto-container" >
        <div class="hitokoto-text">
          <span>

            <span id="hitokoto">
              <a href="javascript:void(0);" id="hitokoto_text" title="点击复制">"你只活一次"</a>
            </span>

          </span>
        </div>
      </div>
    <div class="manage">
      <div class="nav-items">
        <a :href="isLoggedIn ? `/login` : '/login'">{{ isLoggedIn ? username : '登录' }}</a>
        |
        <a href="/profile">管理</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* PageFooter 组件特定样式 - 磨砂玻璃风格 */
.page-footer{
  color: var(--md-sys-color-on-surface);
  font-weight: bold;

}
/* 一言容器 - 磨砂玻璃卡片 */
#hitokoto {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: var(--spacing-lg) auto;
  padding: var(--spacing-lg);
  max-width: 600px;
  height: 50px;
  transition: all 0.3s ease;
  position: relative;
  padding: 20px;
  /* 0偏移，10px模糊，白色发光 */
  text-shadow: 0 0 2px var(--md-sys-color-surface), 0 0 2px var(--md-sys-color-surface);
}

#hitokoto_text {
  color: var(--md-sys-color-on-surface-variant);
  text-decoration: none;
  font-style: italic;
  transition: all 0.3s ease;
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

.nav-items {
  display: flex;
  gap: 15px;
  align-items: center;
  color: var(--md-sys-color-on-surface);
  border-radius: 32px;
  padding: 8px 12px;
  margin-top: 10px;
  transition: all var(--transition-normal);

  /* 磨砂玻璃效果 */
  background: var(--glass-bg);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.nav-items:hover {
  box-shadow: 0 12px 32px rgba(155, 143, 200, 0.15);
}

body.dark-theme .nav-items:hover {
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
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
  transition: all var(--transition-normal);
  font-weight: 500;
}

.nav-items a:hover {
  width: 40px;
  height: 40px;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.nav-items a.router-link-active {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
}

</style> 