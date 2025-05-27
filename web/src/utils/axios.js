import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// 创建 axios 实例
const instance = axios.create({
  baseURL: 'http://localhost:8000/api/lyb',
  timeout: 5000
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  response => response,
  async error => {
    const authStore = useAuthStore()
    const originalRequest = error.config

    // 如果是 401 错误且没有重试过
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // 尝试刷新 token
        const newToken = await authStore.refreshAccessToken()
        
        // 更新请求头并重试
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return instance(originalRequest)
      } catch (refreshError) {
        // 刷新 token 失败，清除认证状态并跳转到登录页
        authStore.clearAuth()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default instance 