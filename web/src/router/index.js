import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/PageRouter/login.vue'
import Register from '@/components/PageRouter/register.vue'
import UserProfile from '@/components/PageRouter/UserProfile.vue'
import lyb from '@/components/PageRouter/lyb.vue'
import profile from '@/components/PageRouter/UserProfile.vue'
import { useAuthStore } from '@/stores/auth'
import my from '@/components/PageRouter/my.vue'
import axios from '@/utils/axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: UserProfile,
      meta: { requiresAuth: true }
    },
    {
      path: '/lyb',
      name: 'Lyb',
      component: lyb
    },
    {
      path: '/profile',
      name: 'Profile',
      component: profile
    },
    {
      path: '/my',
      name: 'My',
      component: my
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 确保 token 存在且有效
    if (!authStore.token) {
      next('/login')
      return
    }
    
    try {
      // 尝试获取用户信息来验证 token
      await axios.get('/user/info/')
      next()
    } catch (error) {
      if (error.response?.status === 401) {
        // token 无效，清除状态并跳转到登录页
        authStore.clearAuth()
        next('/login')
      } else {
        // 其他错误，继续访问
        next()
      }
    }
  } else {
    next()
  }
})

export default router 