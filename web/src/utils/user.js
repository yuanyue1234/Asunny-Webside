import axios from 'axios'

// 用户信息存储的key
const USER_INFO_KEY = 'userInfo'

// 获取用户信息
export const getUserInfo = async () => {
  try {
    // 先从本地存储获取
    const localUserInfo = localStorage.getItem(USER_INFO_KEY)
    if (localUserInfo) {
      return JSON.parse(localUserInfo)
    }

    // 如果本地没有，则从后端获取
    const response = await axios.get('/api/user/info')
    if (response.data.code === 0) {
      const userInfo = response.data.data
      // 存储到本地
      localStorage.setItem(USER_INFO_KEY, JSON.stringify(userInfo))
      return userInfo
    }
    return null
  } catch (error) {
    console.error('获取用户信息失败:', error)
    return null
  }
}

// 清除用户信息
export const clearUserInfo = () => {
  localStorage.removeItem(USER_INFO_KEY)
}

// 更新用户信息
export const updateUserInfo = (userInfo) => {
  localStorage.setItem(USER_INFO_KEY, JSON.stringify(userInfo))
}

// 检查是否登录
export const isLoggedIn = async () => {
  const userInfo = await getUserInfo()
  return !!userInfo
}

// 获取用户名
export const getUsername = async () => {
  const userInfo = await getUserInfo()
  return userInfo?.username || ''
} 