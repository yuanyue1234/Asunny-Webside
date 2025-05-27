<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from '@/utils/axios'

const router = useRouter()
const authStore = useAuthStore()

const userInfo = ref({
  username: '',
  email: '',
  date_joined: '',
  last_login: ''
})

const loading = ref(true)
const error = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('')

// 显示提示消息
const showMessage = (message, type = 'error') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// 检查认证状态
const checkAuth = () => {
  if (!authStore.token) {
    showMessage('请先登录')
    router.push('/login')
    return false
  }
  return true
}

// 获取用户信息
const fetchUserInfo = async () => {
  if (!checkAuth()) return

  try {
    loading.value = true
    error.value = ''
    
    const response = await axios.get('/user/info/')
    userInfo.value = response.data
    showMessage('获取用户信息成功', 'success')
  } catch (err) {
    console.error('获取用户信息失败:', err)
    
    if (err.response?.status === 401) {
      showMessage('登录已过期，请重新登录')
      authStore.clearAuth()
      router.push('/login')
    } else {
      error.value = err.response?.data?.error || '获取用户信息失败，请稍后重试'
      showMessage(error.value)
    }
  } finally {
    loading.value = false
  }
}

// 页面加载时
onMounted(async () => {
  // 确保 token 已恢复
  if (!checkAuth()) return
  
  // 发起请求
  await fetchUserInfo()
})
</script>

<template>
  <div class="profile-container">
    <!-- Toast 提示 -->
    <div class="toast-container position-fixed top-0 end-0 p-3">
      <div class="toast" :class="`text-white bg-${toastType}`" role="alert" aria-live="assertive" aria-atomic="true" v-show="showToast">
        <div class="toast-header">
          <strong class="me-auto">{{ toastType === 'success' ? '成功' : '错误' }}</strong>
          <button type="button" class="btn-close btn-close-white" @click="showToast = false"></button>
        </div>
        <div class="toast-body">
          {{ toastMessage }}
        </div>
      </div>
    </div>

    <div class="profile-card">
      <h2>用户信息</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
        <p class="mt-2">正在加载用户信息...</p>
      </div>

      <!-- 错误提示 -->
      <div v-else-if="error" class="alert alert-danger">
        {{ error }}
        <button class="btn btn-outline-danger mt-2" @click="fetchUserInfo">
          重试
        </button>
      </div>

      <!-- 用户信息 -->
      <div v-else class="user-info">
        <div class="info-item">
          <label>用户名：</label>
          <span>{{ userInfo.username }}</span>
        </div>
        
        <div class="info-item">
          <label>邮箱：</label>
          <span>{{ userInfo.email }}</span>
        </div>
        
        <div class="info-item">
          <label>注册时间：</label>
          <span>{{ userInfo.date_joined }}</span>
        </div>
        
        <div class="info-item">
          <label>最后登录：</label>
          <span>{{ userInfo.last_login || '从未登录' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.profile-card {
  background: var(--md-sys-color-surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: var(--md-sys-color-primary);
  font-size: 1.8rem;
  font-weight: 500;
  border-bottom: 2px solid var(--md-sys-color-primary-container);
  padding-bottom: 1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: var(--md-sys-color-primary);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  padding: 1rem;
  background: var(--md-sys-color-surface-variant);
  border-radius: 8px;
  transition: background-color 0.3s;
}

.info-item:hover {
  background: var(--md-sys-color-surface-variant-hover);
}

.info-item label {
  font-weight: 500;
  min-width: 100px;
  color: var(--md-sys-color-on-surface-variant);
}

.info-item span {
  color: var(--md-sys-color-on-surface);
}

.alert {
  margin: 0;
  border: none;
  border-radius: 8px;
}

.btn-outline-danger {
  border-color: var(--md-sys-color-error);
  color: var(--md-sys-color-error);
}

.btn-outline-danger:hover {
  background-color: var(--md-sys-color-error);
  color: white;
}
</style> 