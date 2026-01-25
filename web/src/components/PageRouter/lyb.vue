<script setup>
import {ref, reactive, onMounted, toRefs} from 'vue'
import axios from '@/utils/axios'
import {useAuthStore} from '@/stores/auth'

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
  let newdata = {
    title: state.lyb.title,
    author: state.lyb.author,
    content: state.lyb.content
  }
  if (state.lyb.url == "") {
    //新增
    axios.post("lyb/", newdata).then(res => {
      getLyb()
    }).catch(err => {
      console.log(err)
    })
  } else {
    //修改
    let relativeEditUrl = state.lyb.url;
    if (typeof relativeEditUrl === 'string' && relativeEditUrl.startsWith('/api/is/')) {
      relativeEditUrl = relativeEditUrl.substring('/api/is'.length);
    }
    axios.put(relativeEditUrl, newdata).then(res => {
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
                <input type="text" id="title" class="form-control" v-model="state.lyb.title" placeholder="请输入标题"
                       required>
              </div>

              <div class="form-group">
                <label class="form-label" for="author"><i class="fas fa-user"></i> 用户名</label>
                <input type="text" id="author" class="form-control" v-model="state.lyb.author"
                       placeholder="请输入您的用户名" required>
              </div>

              <div class="form-group">
                <label class="form-label" for="content"><i class="fas fa-file-alt"></i> 内容</label>
                <textarea id="content" class="form-control" v-model="state.lyb.content" rows="6"
                          placeholder="请输入留言内容" required></textarea>
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
/* lyb.vue 组件特定样式 - 留言板布局 */

.lyb-container {
  display: flex;
  gap: 20px;
  padding: 20px;
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

/* 表格样式 */
.table-title {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.table-author {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.table-content {
  max-width: 300px;
}

.content-cell {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.table-actions {
  white-space: nowrap;
}

/* 表单样式 */
.lyb-form {
  width: 100%;
}

.lyb-form input,
.lyb-form textarea {
  width: 100%;
}
</style>
