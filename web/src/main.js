import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 配置 Axios
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.mount('#app')