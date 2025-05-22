import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/PageHead/login.vue'
import Register from '@/components/PageHead/register.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 