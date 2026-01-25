

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

    <!-- 用户信息卡片 -->
    <div class="profile-info card">
      <div class="profile-name">
      <div class="card__wrapper">
        <div class="card__3d">
          <h2>用户信息</h2>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading">
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
            <hr>

            <!-- 退出登录按钮 -->
            <div class="logout-section">
              <button class="auth-button" @click="handleLogout">
                <i class="fas fa-sign-out-alt"></i> 退出登录
              </button>
            </div>
          </div>
        </div>
      </div>
      </div>
    </div>

    <!-- 站点配置管理 -->

    <div class="site-config card">
      <div class="profile-name">
      <div class="card__wrapper">
        <div class="card__3d">
          <h2>站点配置管理</h2>

          <!-- 配置加载状态 -->
          <div v-if="configLoading" class="loading">

            <p class="mt-2">{{ isSaving ? '保存中...' : '正在加载配置...' }}</p>
          </div>

          <template v-else>
            <div class="form-group">
              <label class="form-label" for="site-config">
                <i class="fas fa-database"></i> 站点配置 JSON
              </label>
              <textarea
                id="site-config"
                v-model="siteConfig"
                class="form-control"
                rows="15"
                placeholder='{
  "title": "站点标题",
  "avatar": "头像URL",
  ...
}'
                spellcheck="false"
              ></textarea>
            </div>

            <button type="button" class="auth-button" @click="saveSiteConfig" :disabled="!siteConfig">
              <i class="fas fa-save"></i> 保存配置
            </button>
          </template>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

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
})

const loading = ref(true)
const error = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('')
const password = ref('')

// 站点配置相关
const siteConfig = ref('')
const configLoading = ref(false)
const isSaving = ref(false)

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

// 退出登录
const handleLogout = () => {
  authStore.clearAuth()
  showMessage('已成功退出登录', 'success')
  setTimeout(() => {
    router.push('/login')
  }, 1000)
}

// 获取站点配置
const fetchSiteConfig = async () => {
  if (!checkAuth()) return

  try {
    configLoading.value = true
    const response = await axios.get('site/profile/')
    siteConfig.value = JSON.stringify(response.data, null, 2)
    isSaving.value = false
  } catch (err) {
    console.error('获取站点配置失败:', err)
    showMessage(err.response?.data?.error || '获取站点配置失败', 'error')
  } finally {
    configLoading.value = false
  }
}

// 保存站点配置
const saveSiteConfig = async () => {
  if (!checkAuth()) return

  try {
    isSaving.value = true
    configLoading.value = true
    const parsedConfig = JSON.parse(siteConfig.value)
    await axios.put('site/profile/', parsedConfig)
    showMessage('保存站点配置成功', 'success')

    // 保存成功后，延迟1.5秒重新获取配置以确认
    setTimeout(async () => {
      await fetchSiteConfig()
    }, 1500)
  } catch (err) {
    if (err instanceof SyntaxError) {
      showMessage('JSON格式错误，请检查', 'error')
    } else {
      console.error('保存站点配置失败:', err)
      showMessage(err.response?.data?.error || '保存站点配置失败', 'error')
    }
    configLoading.value = false
    isSaving.value = false
  }
}

// 页面加载时
onMounted(async () => {
  // 确保 token 已恢复
  if (!checkAuth()) return

  // 并发获取用户信息和站点配置
  await Promise.all([
    fetchUserInfo(),
    fetchSiteConfig()
  ])
})
</script>

<style scoped>
/* UserProfile.vue 组件特定样式 */
.profile-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl);
  max-width: 800px;
  margin: 0 auto;
}

.info-item {
  padding: 10px;
  border-radius: 8px;
  color: var(--md-sys-color-on-surface);
  transition: all 0.3s ease;
}

.info-item:hover {
  background-color: var(--md-sys-color-surface-variant);
}

/* 加载状态 */
.site-config .loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  min-height: 200px;
}

.site-config .loading p {
  margin-top: var(--spacing-md);
  color: var(--md-sys-color-on-surface-variant);
  font-size: 0.95rem;
}

.site-config textarea {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  color: var(--md-sys-color-on-surface);
  resize: vertical;
}

.site-config textarea:focus {
  background: var(--md-sys-color-surface);
  border-color: var(--md-sys-color-primary);
  box-shadow: 0 0 0 2px var(--md-sys-color-primary-container);
  outline: none;
}

.site-config .form-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
  color: var(--md-sys-color-on-surface);
}

.site-config .form-label i {
  color: var(--md-sys-color-primary);
}
</style> 