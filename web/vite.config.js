import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      // 代理所有以 /api 开头的请求
      '/api': {
        target: 'http://127.0.0.1:8000', // 后端服务实际地址
        changeOrigin: true, // 需要虚拟主机站点
        // secure: false, // 如果是https接口，需要配置这个
        // 如果后端API路径没有 /api 前缀，可以在这里重写
        // rewrite: (path) => path.replace(/^\/api/, '')
      },
      // 代理 /movies 和 /movies/chart
      // 这些是直接由 Django 渲染的页面，不是 API，但开发时也需要代理
      '/movies': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // 如果还有其他直接由 Django 服务的路径，也需要类似添加
      // 例如 /lyb/ (如果不是通过 /api/is/lyb 访问)
      // 或 /site_config/ (如果不是通过 /api/is/site/profile 访问)
      // 如果这些已经包含在 /api/ 代理规则中，则不需要单独列出
    }
  }
}) 