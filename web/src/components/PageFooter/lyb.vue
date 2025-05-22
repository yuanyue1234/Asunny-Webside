<script setup>
import { ref, reactive, onMounted, toRefs } from 'vue'
import axios from 'axios'

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
const base_url = "http://127.0.0.1:8000/api/lyb/"
const getLyb = () => {
  axios.get(base_url).then(res => {
    state.ly_list = res.data
    state.lyb = Object.assign({}, lyb_blank)
  }).catch(err => {
    console.log(err)
  })
}

// 页面加载时获取留言列表
onMounted(() => {
  getLyb()
})
</script>

<template>

    <div class="row">
      <div class="col-md-8">
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
                  <td>{{ item.title }}</td>
                  <td>{{ item.author }}</td>
                  <td>
                    <div class="content-cell">
                      {{ getDisplayContent(item.content, index) }}
                      <button v-if="needsExpand(item.content)" 
                              class="btn btn-link btn-sm expand-btn" 
                              @click="toggleExpand(index)">
                        {{ expandedRows.has(index) ? '收起' : '展开' }}
                      </button>
                    </div>
                  </td>
                  <td>
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
      <div class="col-md-4">
        <div class="showcase">
          <div class="showcase-item">
            <div class="showcase-title">添加留言</div>
            <div class="showcase-content">
              <input type="hidden" v-model="state.lyb.url">
              <div class="form-group">
                <label><i class="fas fa-heading"></i> 标题</label>
                <input type="text" id="title" class="form-control" v-model="state.lyb.title" placeholder="请输入标题" required>
              </div>
              <div class="form-group">
                <label><i class="fas fa-user"></i> 用户名</label>
                <input type="text" id="anthor" class="form-control" v-model="state.lyb.author" placeholder="请输入您的用户名" required>
              </div>
              <div class="form-group">
                <label><i class="fas fa-file-alt"></i> 内容</label>
                <textarea class="form-control" id="content" v-model="state.lyb.content" rows="6" style="min-height: 100px; resize: vertical;" placeholder="请输入留言内容" required></textarea>
              </div>
              <button type="submit" class="btn w-100" @click="savelyb">
                <i class="fas fa-paper-plane"></i> 提交
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>

.table {
  width: 100%;
  color: var(--md-sys-color-on-surface);
  border-collapse: separate;
  border-spacing: 0;
}

.table thead th {
  background-color: var(--md-sys-color-surface-variant);
  color: var(--md-sys-color-on-surface-variant);
  padding: 12px;
  text-align: left;
  font-weight: 500;
}

.table tbody td {
  padding: 12px;
  vertical-align: top;
}

.table tbody td:nth-child(1) {
  width: 20%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table tbody td:nth-child(2) {
  width: 15%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.table tbody td:nth-child(3) {
  width: 55%;
}

.table tbody td:nth-child(4) {
  width: 10%;
  white-space: nowrap;
}

.content-cell {
  position: relative;
  word-break: break-word;
}

.expand-btn {
  padding: 0;
  margin-left: 8px;
  color: var(--md-sys-color-primary);
  text-decoration: none;
  font-size: 0.9em;
}

.expand-btn:hover {
  color: var(--md-sys-color-primary-container);
  text-decoration: underline;
}

.form-group {
  margin-bottom: 16px;
}

.form-control {
  background-color: var(--md-sys-color-surface);
  border-radius: 8px;
  padding: 8px;
  width: 100%;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  border-color: var(--md-sys-color-primary);
  box-shadow: 0 0 0 2px var(--md-sys-color-primary-container);
}

.btn {
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.btn:hover {
  background-color: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-sm {
  padding: 8px;
  border-radius: 4px;
  background-color: var(--md-sys-color-secondary-container);
  color: var(--md-sys-color-on-secondary-container);
}

.btn-sm:hover {
  background-color: var(--md-sys-color-secondary);
  color: var(--md-sys-color-on-secondary);
}

.row {
  margin: 0;

  display: flex;
  flex-wrap: wrap;
}

.col-md-8 {
  padding:0;
  flex: 0 0 66.666667%;
  max-width: 66.666667%;
}

.col-md-4 {
  padding:0;
  flex: 0 0 33.333333%;
  max-width: 33.333333%;
}

@media (max-width: 768px) {
  .col-md-8, .col-md-4 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
