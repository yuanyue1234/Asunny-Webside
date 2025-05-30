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
    },
    {
      path: '/movies',
      name: '豆瓣电影',
      beforeEnter: (to, from, next) => {
        // 跳转到Django后端渲染的电影列表页面
        window.location.href = '/movies/';
      }
    },
    {
      path: '/chart',
      name: '电影图表',
      beforeEnter: (to, from, next) => {
        // 跳转到Django后端渲染的电影图表页面
        window.location.href = '/movies/chart/';
      }
    }
  ]
})

// 添加导航守卫处理外部链接
router.beforeEach((to, from, next) => {
  // 处理电影相关的路由
  if (to.path === '/movies') {
    window.location.href = 'http://127.0.0.1:8000/movies/';
    return;
  }
  if (to.path === '/movies/chart') {
    window.location.href = 'http://127.0.0.1:8000/movies/chart/';
    return;
  }
  
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
      axios.get('/user/info/')
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