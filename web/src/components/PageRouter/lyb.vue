<script setup>
import {ref, reactive, onMounted, toRefs} from 'vue'
import axios from '@/utils/axios'
import {useAuthStore} from '@/stores/auth'

const authStore = useAuthStore()

// 用于表单输入
const lyb_blank = {
  url: '',
  author: '',
  content: ''
}

// 展开状态管理
const expandedRows = ref(new Set())

// 切换展开状态
const toggleExpand = (index) => {
  if (expandedRows.value.has(index)) {
    expandedRows.value.delete(index)
  } else {
    expandedRows.value.add(index)
  }
}

// 检查内容是否需要展开按钮
const needsExpand = (content) => {
  return content.length > 100
}

// 获取显示的内容
const getDisplayContent = (content, index) => {
  if (expandedRows.value.has(index)) {
    return content
  }
  return content.length > 100 ? content.slice(0, 100) + '...' : content
}

// 编辑留言
const editLyb = (item) => {
  state.lyb.url = item.url;
  state.lyb.author = item.author;
  state.lyb.content = item.content;
}
// 删除留言
const deletelyb = (item) => {
  let relativeDeleteUrl = item.url;
  if (typeof relativeDeleteUrl === 'string' && relativeDeleteUrl.startsWith('/api/is/')) {
    relativeDeleteUrl = relativeDeleteUrl.substring('/api/is'.length);
  }
  axios.delete(relativeDeleteUrl).then(res => {
    getLyb()
  }).catch(err => {
    console.log(err)
  })
}
const savelyb = () => {
  // 为后端兼容，即使前端不显示 title，也提供一个默认值
  let newdata = {
    title: '留言',  // 默认标题，后端可能需要此字段
    author: state.lyb.author,
    content: state.lyb.content
  }

  if (state.lyb.url == "") {
    //新增
    axios.post("lyb/", newdata).then(res => {
      console.log("留言添加成功:", res.data)
      getLyb()
    }).catch(err => {
      console.error("添加留言失败:", err)
      alert("添加留言失败: " + (err.response?.data?.error || err.message))
    })
  } else {
    //修改
    let relativeEditUrl = state.lyb.url;
    if (typeof relativeEditUrl === 'string' && relativeEditUrl.startsWith('/api/is/')) {
      relativeEditUrl = relativeEditUrl.substring('/api/is'.length);
    }
    axios.put(relativeEditUrl, newdata).then(res => {
      console.log("留言更新成功:", res.data)
      getLyb()
    }).catch(err => {
      console.error("更新留言失败:", err)
      alert("更新留言失败: " + (err.response?.data?.error || err.message))
    })
  }
}

// 用于存储留言列表
const state = reactive({
  ly_list: [],
  lyb: Object.assign({}, lyb_blank) // 单条留言——浮空
});

// 调试状态
const debug = reactive({
  hasData: false,
  dataCount: 0,
  lastResponse: null
})

// 获取留言列表
const getLyb = async () => {
  try {
    const res = await axios.get("lyb/")
    console.log("留言板API响应:", res.data);

    // 保存原始响应用于调试
    debug.lastResponse = JSON.stringify(res.data);

    let dataToUse = [];

    // 处理不同的数据结构情况
    if (res.data && Array.isArray(res.data.results)) {
      // 情况1: API返回 {results: [...]}
      dataToUse = res.data.results;
      console.log("使用res.data.results数组，长度:", dataToUse.length);
    } else if (res.data && Array.isArray(res.data)) {
      // 情况2: API直接返回数组
      dataToUse = res.data;
      console.log("使用res.data数组，长度:", dataToUse.length);
    } else if (res.data && typeof res.data === 'object') {
      // 情况3: API返回单个对象
      dataToUse = [res.data];
      console.log("API返回单个对象，转换为数组");
    } else {
      console.warn("无法识别的数据格式:", res.data);
      dataToUse = [];
    }

    // 更新调试状态
    debug.hasData = dataToUse.length > 0;
    debug.dataCount = dataToUse.length;

    // 使用数组方法确保响应式更新
    state.ly_list = [];
    if (dataToUse.length > 0) {
      // 先清空再添加，确保触发响应式
      dataToUse.forEach(item => {
        state.ly_list.push(item);
      });
    }

    console.log("数据赋值后state.ly_list:", state.ly_list);
    console.log("数据赋值后state.ly_list长度:", state.ly_list.length);

    // 重置表单
    state.lyb = Object.assign({}, lyb_blank);
  } catch (err) {
    console.error("获取留言列表失败:", err);
    state.ly_list = []; // 确保出错时清空
  }
}

// 检查是否有编辑权限
const hasEditPermission = (author) => {
  return authStore.username === 'asunny' || author === authStore.username
}

// 页面加载时获取留言列表
onMounted(async () => {
  await getLyb()
  // 如果用户已登录，自动填充用户名
  if (authStore.username) {
    state.lyb.author = authStore.username
  }
})

const editingItem = ref(null);
const dialogVisible = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
</script>

<template>
  <!-- 调试信息区域
  <div v-if="debug.lastResponse" style="border: 2px solid red; padding: 10px; margin: 10px; background: #fee;">
    <h3>调试信息</h3>
    <p>数据状态: {{ debug.hasData ? '有数据' : '无数据' }}, 数量: {{ debug.dataCount }}</p>
    <p>state.ly_list长度: {{ state.ly_list.length }}</p>
    <details>
      <summary>查看原始数据</summary>
      <pre style="max-height: 200px; overflow: auto;">{{ debug.lastResponse }}</pre>
    </details>
    <details>
      <summary>查看当前state.ly_list</summary>
      <pre style="max-height: 200px; overflow: auto;">{{ JSON.stringify(state.ly_list, null, 2) }}</pre>
    </details>
  </div> -->

  <div class="lyb-container">
    <div class="lyb-main">
      <div class="lyb-list">
        <div v-for="(item, index) in state.ly_list" :key="index" class="lyb-card">
          <div class="lyb-card-header">
            <span class="lyb-author">😺 {{ item.author }}</span>
            <div class="lyb-actions" v-if="hasEditPermission(item.author)">
              <button class="btn-icon" title="编辑" @click="editLyb(item)">
                <i class="fas fa-edit"></i>
              </button>
              <button class="btn-icon" title="删除" @click="deletelyb(item)">
                <i class="fas fa-trash-alt"></i>
              </button>
            </div>
          </div>
          <div class="lyb-content">
            <p>{{ expandedRows.has(index) ? item.content : getDisplayContent(item.content, index) }}</p>
            <button v-if="needsExpand(item.content)"
                    class="btn-expand"
                    @click="toggleExpand(index)">
              {{ expandedRows.has(index) ? '收起' : '展开全文' }}
            </button>
          </div>
        </div>
        <div v-if="state.ly_list.length === 0" class="lyb-empty">
          <i class="fas fa-comments"></i>
          <p>暂无留言，快来添加第一条吧！</p>
        </div>
      </div>
    </div>
    <div class="lyb-sidebar">
      <div class="showcase">
        <div class="showcase-item">
          <div class="showcase-title">添加留言</div>
          <div class="showcase-content">
            <form class="lyb-form" @submit.prevent="savelyb">
              <input type="hidden" v-model="state.lyb.url">

              <div class="form-group">
                <label class="form-label" for="author"><i class="fas fa-user"></i> 用户名</label>
                <input type="text" id="author" class="form-control" v-model="state.lyb.author"
                       placeholder="请输入您的用户名" required>
              </div>

              <div class="form-group">
                <label class="form-label" for="content"><i class="fas fa-comment"></i> 留言内容</label>
                <textarea id="content" class="form-control" v-model="state.lyb.content" rows="6"
                          placeholder="写下你的想法..." required></textarea>
              </div>

              <div class="form-group">
                <button type="submit" class="submit-btn">
                  <i class="fas fa-paper-plane"></i> 提交留言
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* lyb.vue 组件特定样式 - 卡片式留言板 */

.lyb-container {
  display: flex;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl);
  max-width: 1400px;
  margin: 0 auto;
}

.lyb-main {
  flex: 1;
  min-width: 0;
}

.lyb-sidebar {
  width: 350px;
  flex-shrink: 0;
}

@media screen and (max-width: 900px) {
  .lyb-container {
    flex-direction: column;
  }

  .lyb-sidebar {
    width: 100%;
  }
}

/* 留言列表容器 */
.lyb-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

/* 留言卡片 - 磨砂玻璃风格 */
.lyb-card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--glass-shadow);
  padding: var(--spacing-lg);
  transition: all var(--transition-normal);
}

.lyb-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-hover-md);
  border-color: rgba(255, 255, 255, 0.5);
}

/* 留言卡片头部 */
.lyb-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--glass-border);
}

.lyb-author {
  font-weight: 600;
  color: var(--md-sys-color-primary);
  font-size: 1rem;
}

.lyb-actions {
  display: flex;
  gap: var(--spacing-sm);
}

/* 图标按钮 */
.btn-icon {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  color: var(--md-sys-color-primary);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
}

.btn-icon:hover {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  transform: scale(1.1);
}

.btn-icon i {
  font-size: 0.9rem;
}

/* 留言内容 */
.lyb-content {
  color: var(--md-sys-color-on-surface);
  line-height: 1.8;
  font-size: 0.95rem;
}

.lyb-content p {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 展开按钮 */
.btn-expand {
  background: none;
  border: none;
  color: var(--md-sys-color-primary);
  cursor: pointer;
  padding: var(--spacing-xs) 0;
  font-size: 0.875rem;
  margin-top: var(--spacing-sm);
  transition: all var(--transition-normal);
  font-weight: 500;
}

.btn-expand:hover {
  color: var(--md-sys-color-primary-container);
  text-decoration: underline;
}

/* 空状态 */
.lyb-empty {
  text-align: center;
  padding: var(--spacing-xl);
  color: var(--md-sys-color-on-surface-variant);
}

.lyb-empty i {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.lyb-empty p {
  margin: 0;
  font-size: 1rem;
}

/* 表单样式 */
.lyb-form {
  width: 100%;
}

.lyb-form input,
.lyb-form textarea {
  width: 100%;
}

/* 确保 showcase 容器也有样式 */
.showcase {
  margin-bottom: var(--spacing-lg);
}
</style>
