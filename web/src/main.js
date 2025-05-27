import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from '@/utils/axios'
import { useAuthStore } from './stores/auth'

// 配置 Axios
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// 初始化 auth store
const authStore = useAuthStore()
// 从 localStorage 恢复 token
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

app.use(router)
app.use(ElementPlus)
app.mount('#app')