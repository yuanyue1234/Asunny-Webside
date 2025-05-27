import axios from '@/utils/axios'
import { useAuthStore } from '@/stores/auth'

// 获取用户信息
export const fetchUserInfo = async () => {
  const authStore = useAuthStore()
  
  if (!authStore.token) {
    return null
  }

  try {
    const response = await axios.get('/user/info/')
    return response.data
  } catch (err) {
    console.error('获取用户信息失败:', err)
    if (err.response?.status === 401) {
      authStore.clearAuth()
    }
    throw err
  }
}

// 检查用户是否已登录
export const isUserLoggedIn = () => {
  const authStore = useAuthStore()
  return !!authStore.token
}
