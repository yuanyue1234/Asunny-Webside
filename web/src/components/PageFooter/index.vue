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
            "
            <span id="hitokoto">
              <a href="javascript:void(0);" id="hitokoto_text">"你只活一次"</a>
            </span>
            "
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

/* 一言样式 */
#hitokoto {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: var(--spacing-lg) 0;
    padding: var(--spacing-md);
    transition: all var(--transition-normal);
    position: relative; /* 添加定位 */
    z-index: 10; /* 提高层级 */
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
    cursor: pointer; /* 添加指针样式 */
    position: relative; /* 添加定位 */
    z-index: 20; /* 提高层级 */
}

#hitokoto_text:hover {
    color: var(--md-sys-color-primary);
    background-color: var(--md-sys-color-primary-container);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.manage {
    display: flex;
    justify-content: center;
    padding: var(--spacing-md) 0;
}

.manage-item {
    color: var(--md-sys-color-on-surface-variant);
    font-size: var(--font-size-sm);
}

.manage-item a {
    color: var(--md-sys-color-on-surface-variant);
    text-decoration: none;
    transition: all var(--transition-normal);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius-sm);
}

.manage-item a:hover {
    color: var(--md-sys-color-primary);
    background-color: var(--md-sys-color-primary-container);
}

</style> 