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
    const response = await axios.post('/api/is/register/', {
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
/* register.vue 组件特定样式 - 所有通用样式已移至 styles.css */
</style>
