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
})
</script>
<template>
  <div class="page-footer">
    <!-- 一言 -->
    <div class="hitokoto-container">
        <div class="hitokoto-text">
          <span>
            <span id="hitokoto">
              <a href="#" id="hitokoto_text">"你只活一次."</a>
            </span>
          </span>
        </div>
      </div>
    <div class="manage">
      <div class="manage-item">
        <a :href="isLoggedIn ? `/profile/${username}` : '/login'">{{ isLoggedIn ? username : '登录' }}</a>
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