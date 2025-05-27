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
      try {
        const response = await axios.post('/token/refresh/', {
          refresh: this.refreshToken
        })
        
        const { access } = response.data
        this.token = access
        localStorage.setItem('token', access)
        
        // 更新 axios 默认头
        axios.defaults.headers.common['Authorization'] = `Bearer ${access}`
        
        return access
      } catch (error) {
        this.clearAuth()
        router.push('/login')
        throw error
      }
    }
  }
}) 