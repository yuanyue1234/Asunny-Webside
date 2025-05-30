import { defineStore } from 'pinia'
import axios from '@/utils/axios'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    username: localStorage.getItem('username') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  actions: {
    setAuth(token, refreshToken, username) {
      this.token = token
      this.refreshToken = refreshToken
      this.username = username
      this.isAuthenticated = true

      // 保存到 localStorage
      localStorage.setItem('token', token)
      localStorage.setItem('refreshToken', refreshToken)
      localStorage.setItem('username', username)

      // 设置 axios 默认头
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    },

    clearAuth() {
      this.token = null
      this.refreshToken = null
      this.username = null
      this.isAuthenticated = false

      // 清除 localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('username')

      // 清除 axios 默认头
      delete axios.defaults.headers.common['Authorization']
    },

    async refreshAccessToken() {
      // 检查是否有刷新令牌
      if (!this.refreshToken) {
        console.error('没有刷新令牌可用');
        this.clearAuth();
        router.push('/login');
        throw new Error('没有刷新令牌可用');
      }

      try {
        console.log('尝试刷新令牌，当前刷新令牌:', this.refreshToken);
        
        // 使用原始axios实例而不是拦截器处理的实例，避免循环
        const response = await axios.post('/token/refresh/', {
          refresh: this.refreshToken
        });
        
        console.log('令牌刷新成功:', response.data);
        
        // 处理可能的不同键名 (access 或 token)
        const newToken = response.data.access || response.data.token;
        if (!newToken) {
          throw new Error('刷新令牌响应中没有找到新的访问令牌');
        }
        
        this.token = newToken;
        localStorage.setItem('token', newToken);
        
        // 更新 axios 默认头
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
        
        return newToken;
      } catch (error) {
        console.error('刷新令牌失败:', error.response?.data || error.message);
        this.clearAuth();
        router.push('/login');
        throw error;
      }
    }
  }
}) 