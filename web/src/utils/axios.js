import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// 创建 axios 实例
const instance = axios.create({
  baseURL: '/api/is',
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

// 创建一个标记，用于跟踪是否正在刷新令牌
let isRefreshing = false;
// 存储等待令牌刷新的请求
let failedQueue = [];

// 处理等待队列中的请求
const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  
  // 清空队列
  failedQueue = [];
};

// 响应拦截器
instance.interceptors.response.use(
  response => response,
  async error => {
    console.log('响应拦截器捕获错误:', error.response?.status, error.config?.url);
    
    const authStore = useAuthStore()
    const originalRequest = error.config

    // 如果是刷新令牌的请求失败，直接返回错误
    if (originalRequest.url === '/token/refresh/') {
      console.error('刷新令牌请求失败:', error.response?.data);
      authStore.clearAuth();
      return Promise.reject(error);
    }

    // 如果是 401 错误且没有重试过
    if (error.response?.status === 401 && !originalRequest._retry) {
      // 标记该请求已尝试过重试
      originalRequest._retry = true;

      // 如果已经在刷新令牌，将请求加入队列
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return instance(originalRequest);
          })
          .catch(err => {
            return Promise.reject(err);
          });
      }

      // 标记正在刷新令牌
      isRefreshing = true;

      try {
        // 尝试刷新令牌
        const newToken = await authStore.refreshAccessToken();
        
        // 处理队列中的请求
        processQueue(null, newToken);
        
        // 更新请求头并重试
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return instance(originalRequest);
      } catch (refreshError) {
        // 刷新令牌失败，处理队列中的请求
        processQueue(refreshError, null);
        return Promise.reject(refreshError);
      } finally {
        // 重置刷新状态
        isRefreshing = false;
      }
    }

    return Promise.reject(error)
  }
)

export default instance 