<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const usernameError = ref('')
const passwordError = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('')

const showMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    const toast = document.querySelector('.toast')
    if (toast) {
      toast.classList.add('show')
    }
  }, 100)
  
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const validateForm = () => {
  let isValid = true
  
  if (!username.value) {
    usernameError.value = '请输入用户名'
    isValid = false
  } else {
    usernameError.value = ''
  }
  
  if (!password.value) {
    passwordError.value = '请输入密码'
    isValid = false
  } else {
    passwordError.value = ''
  }
  
  return isValid
}

const handleLogin = async () => {
  if (!validateForm()) return
  
  try {
    const response = await axios.post('http://localhost:8000/api/login/', {
      username: username.value,
      password: password.value
    })
    
    // 存储token和用户信息
    localStorage.setItem('token', response.data.token)
    localStorage.setItem('username', response.data.username)
    
    // 显示登录成功提示
    showMessage('登录成功，欢迎回来！', 'success')
    
    // 延迟2秒后跳转，确保用户能看到提示
    setTimeout(() => {
      router.push('/')
    }, 1000)
    
  } catch (err) {
    error.value = err.response?.data?.error || '登录失败，请重试'
    // 显示登录失败提示
    showMessage(error.value, 'danger')
  }
}
</script>

<template>
  <div class="profile">
    <!-- Bootstrap Toast 提示框 -->
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

    <div class="auth-box">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required
            placeholder="请输入用户名"
            :class="{'is-invalid': usernameError}"
            @input="usernameError = ''"
          >
          <div class="invalid-feedback" v-if="usernameError">
            {{ usernameError }}
          </div>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            placeholder="请输入密码"
            :class="{'is-invalid': passwordError}"
            @input="passwordError = ''"
          >
          <div class="invalid-feedback" v-if="passwordError">
            {{ passwordError }}
          </div>
        </div>
        <div class="alert alert-danger" v-if="error" role="alert">
          {{ error }}
        </div>
        <button type="submit" class="auth-button">登录</button>
      </form>
      <p class="auth-link">
         <a href=""><i></i>QQ登录</a>
      </p>
      <p class="auth-link">
        还没有账号？ <a href="/register">立即注册</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-box {
  background: var(--md-sys-color-surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
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

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--md-sys-color-on-surface);
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--md-sys-color-outline);
  border-radius: 8px;
  background: var(--md-sys-color-surface);
  color: var(--md-sys-color-on-surface);
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
  outline: none;
  border-color: var(--md-sys-color-primary);
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.auth-button {
  width: 100%;
  padding: 0.75rem;
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.3s;
}

.auth-button:hover {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  transform: translateY(-2px);
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--md-sys-color-on-surface);
}

.auth-link a {
  color: var(--md-sys-color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.auth-link a:hover {
  color: var(--md-sys-color-primary-container);
  text-decoration: underline;
}

.error-message {
  color: #dc3545;
  margin-bottom: 1rem;
  text-align: center;
}

/* 添加 Bootstrap 相关样式 */
.is-invalid {
  border-color: #dc3545 !important;
}

.invalid-feedback {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  font-size: 0.875em;
  color: #dc3545;
}

.alert {
  position: relative;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border: 1px solid transparent;
  border-radius: 0.25rem;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

/* Toast 样式 */
.toast-container {
  z-index: 1050;
}

.toast {
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  min-width: 250px;
}

.toast.show {
  opacity: 1;
}

.toast-header {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background-color: rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.toast-body {
  padding: 0.75rem;
}

.bg-success {
  background-color: #28a745 !important;
}

.bg-danger {
  background-color: #dc3545 !important;
}
</style>
