<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')

const handleLogin = () => {
  // TODO: 实现登录逻辑
  console.log('登录:', username.value, password.value)
}
</script>

<template>
  <div class="profile">
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
          >
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
  color: var(--md-sys-color-on-surface-variant);
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
  box-shadow: 0 0 0 2px var(--md-sys-color-primary-container);
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
  color: var(--md-sys-color-on-surface-variant);
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
</style>
