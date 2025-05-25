import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/PageRouter/login.vue'
import Register from '@/components/PageRouter/register.vue'
import lyb from '@/components/PageRouter/lyb.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
  },
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
    path: '/lyb',
    name: 'lyb',
    component: lyb
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 