<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const email = ref('')
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

const handleRegister = async () => {
  if (!validateForm()) return
  
  try {
    const response = await axios.post('http://localhost:8000/api/lyb/register/', {
      username: username.value,
      password: password.value,
      email: email.value
    })
    
    // 显示注册成功提示
    showMessage('注册成功，即将跳转到登录页面！', 'success')
    
    // 延迟2秒后跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    
  } catch (err) {
    error.value = err.response?.data?.error || '注册失败，请重试'
    // 显示注册失败提示
    showMessage(error.value, 'danger')
  }
}
</script>

<template>
  <div class="register-container">
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
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
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
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required
            placeholder="请输入邮箱"
          >
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
        <button type="submit" class="auth-button">注册</button>
      </form>
      <p class="auth-link">
        已有账号？ <a href="/login">立即登录</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px); /* 减去头部和底部的高度 */
  padding: 20px;
}

.auth-box {
  background: var(--md-sys-color-surface);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
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
  transition: background-color 0.3s;
}

.auth-button:hover {
  background: var(--md-sys-color-primary-container);
}

.auth-link {
  text-align: center;
  margin-top: 1rem;
  color: var(--md-sys-color-on-surface-variant);
}

.auth-link a {
  color: var(--md-sys-color-primary);
  text-decoration: none;
  transition: color 0.3s;
}

.auth-link a:hover {
  color: var(--md-sys-color-primary-container);
  text-decoration: underline;
}

.invalid-feedback {
  color: var(--md-sys-color-error);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.is-invalid {
  border-color: var(--md-sys-color-error) !important;
}

.alert-danger {
  border: none;
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 1rem;
}

/* 优化 Toast 样式以匹配主题 */
.toast-container {
  z-index: 1050;
}

.toast {
  opacity: 0;
  transition: all 0.3s ease-in-out;
  min-width: 280px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: none;
  overflow: hidden;
}

.toast.show {
  opacity: 1;
  transform: translateY(0);
}

.toast-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.toast-body {
  padding: 1rem;
  font-size: 0.95rem;
}

.bg-success {
  background: var(--md-sys-color-primary) !important;
}

.bg-danger {
  background: var(--md-sys-color-error) !important;
}

.btn-close-white {
  opacity: 0.8;
  transition: opacity 0.2s;
}

.btn-close-white:hover {
  opacity: 1;
}
</style>
