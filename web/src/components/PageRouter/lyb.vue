<script setup>
import { ref, reactive, onMounted, toRefs } from 'vue'
import axios from '@/utils/axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 用于表单输入
const lyb_blank = {
  url: '',
  title: '',
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
  state.lyb.title = item.title;
  state.lyb.author = item.author;
  state.lyb.content = item.content;
}
// 删除留言
const deletelyb = (item) => {
  axios.delete(item.url).then(res => {
    getLyb()
  }).catch(err => {
    console.log(err)
  })
}
const savelyb = () => { 
  let newdata ={
    title: state.lyb.title,
    author: state.lyb.author,
    content: state.lyb.content
  }
  if(state.lyb.url==""){
    //新增
    axios.post(base_url,newdata).then(res => {
      getLyb()
    }).catch(err => {
      console.log(err)
    })
  }else{
    //修改
    axios.put(state.lyb.url,newdata).then(res => {
      getLyb()
    }).catch(err => {
      console.log(err)
    })
  }
}

// 用于存储留言列表
const state = reactive({
  ly_list: [],
  lyb: Object.assign({}, lyb_blank) // 单条留言——浮空
});

// 获取留言列表
const base_url = "http://127.0.0.1:8000/api/is/lyb/"
const getLyb = async () => {
  try {
    const res = await axios.get(base_url)
    state.ly_list = res.data
    state.lyb = Object.assign({}, lyb_blank)
  } catch (err) {
    console.log(err)
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
</script>

<template>
    <div class="lyb-container">
      <div class="lyb-main">
        <div class="showcase">
          <div class="showcase-item">
            <table class="table">
              <thead>
                <tr>
                  <th>标题</th>
                  <th>作者</th>
                  <th>内容</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in state.ly_list" :key="index">
                  <td class="table-title">✍️{{ item.title }}</td>
                  <td class="table-author">😺{{ item.author }}</td>
                  <td class="table-content">
                    <div class="content-cell">
                      📄{{ getDisplayContent(item.content, index) }}
                      <button v-if="needsExpand(item.content)" 
                              class="btn btn-link btn-sm expand-btn" 
                              @click="toggleExpand(index)">
                        {{ expandedRows.has(index) ? '收起' : '展开' }}
                      </button>
                    </div>
                  </td>
                  <td class="table-actions" v-if="hasEditPermission(item.author)">
                    <button class="btn btn-sm me-2" title="编辑" @click="editLyb(item)">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm" title="删除" @click="deletelyb(item)">
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
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
                  <label class="form-label" for="title"><i class="fas fa-heading"></i> 标题</label>
                  <input type="text" id="title" class="form-control" v-model="state.lyb.title" placeholder="请输入标题" required>
                </div>
                
                <div class="form-group">
                  <label class="form-label" for="author"><i class="fas fa-user"></i> 用户名</label>
                  <input type="text" id="author" class="form-control" v-model="state.lyb.author" placeholder="请输入您的用户名" required>
                </div>
                
                <div class="form-group">
                  <label class="form-label" for="content"><i class="fas fa-file-alt"></i> 内容</label>
                  <textarea id="content" class="form-control" v-model="state.lyb.content" rows="6" placeholder="请输入留言内容" required></textarea>
                </div>
                
                <div class="form-group">
                  <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i> 提交
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
/* 重置一些基本样式，防止外部样式干扰 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 主容器布局 */
.lyb-container {
  display: flex;
  width: 100%;
  gap: 20px;
  padding: 20px;
  margin: 0;
}

.lyb-main {
  flex: 2;
}

.lyb-sidebar {
  flex: 1;
}

/* 展示区样式 */
.showcase {
  background-color: var(--md-sys-color-surface);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.showcase-item {
  margin-top: 0px  !important;
  margin-bottom: 0px  !important;
  padding: 20px;
}

.showcase-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 20px;
  color: var(--md-sys-color-on-surface);
  padding-bottom: 10px;
}

.showcase-content {
  padding: 0;
}

/* 表单样式 */
.lyb-form {
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-label {
  display: block;
  width: 100%;
  margin-bottom: 8px;
  color: var(--md-sys-color-on-surface);
  font-size: 14px;
  font-weight: 500;
  text-align: left;
}

.form-label i {
  margin-right: 6px;
  color: var(--md-sys-color-primary);
}

.form-control {
  display: block;
  width: 100%;
  height: auto;
  padding: 12px;
  background-color: var(--md-sys-color-surface-variant);
  border: none;
  border-radius: 8px;
  color: var(--md-sys-color-on-surface-variant);
  font-size: 14px;
  transition: all 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--md-sys-color-primary);
  box-shadow: 0 0 0 2px var(--md-sys-color-primary-container);
  background-color: var(--md-sys-color-surface);
  color: var(--md-sys-color-on-surface);
}

.form-control::placeholder {
  color: var(--md-sys-color-on-surface-variant);
  opacity: 0.7;
}

textarea.form-control {
  min-height: 120px;
  resize: vertical;
}

.submit-btn {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover {
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.submit-btn:active {
  transform: translateY(1px);
}

/* 表格样式 */
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 16px;
  background-color: transparent;
}

.table tbody tr {
  display: block;
  background-color: var(--md-sys-color-surface-variant);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  margin-bottom: 12px;
  transition: box-shadow 0.3s;
}

.table tbody tr:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.table tbody td {
  display: block;
  padding: 8px 0;
  background: transparent;
  border: none;
  color: var(--md-sys-color-on-surface);
}

.table-title {
  font-weight: 500;
}

.table-author {
  font-style: italic;
}

.table-content {
  margin-top: 8px;
}

.table thead {
  display: none;
}

.content-cell {
  position: relative;
  word-break: break-word;
  color: var(--md-sys-color-on-surface);
}

.expand-btn {
  padding: 0;
  margin-left: 8px;
  color: var(--md-sys-color-primary);
  text-decoration: none;
  font-size: 0.9em;
  background: none;
  border: none;
  cursor: pointer;
}

.expand-btn:hover {
  color: var(--md-sys-color-primary-container);
  text-decoration: underline;
}

.btn-sm {
  padding: 8px;
  border-radius: 4px;
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-sm:hover {
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  transform: translateY(-1px);
}

.btn-sm:active {
  transform: translateY(0);
}

.me-2 {
  margin-right: 8px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .lyb-container {
    flex-direction: column;
  }
  
  .lyb-main, .lyb-sidebar {
    width: 100%;
  }
  
  .lyb-sidebar {
    margin-top: 20px;
  }
}
</style>
