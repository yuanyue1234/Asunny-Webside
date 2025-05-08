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
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0"><i class="fas fa-comments"></i> 留言列表</h5>
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th><i class="fas fa-heading"></i> 标题</th>
                <th><i class="fas fa-user"></i> 作者</th>
                <th><i class="fas fa-file-alt"></i> 内容</th>
                <th><i class="fas fa-cogs"></i> 操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in state.ly_list" :key="index">
                <td>{{ item.title }}</td>
                <td>{{ item.author }}</td>
                <td>{{ item.content }}</td>
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
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0"><i class="fas fa-edit"></i> 留言表单</h5>
        </div>
        <div class="card-body">
          <input type="hidden" v-model="state.lyb.url">
          <div class="form-group">
            <label><i class="fas fa-heading"></i> 标题</label>
            <input type="text" id="title" class="form-control" v-model="state.lyb.title" required>
          </div>
          <div class="form-group">
            <label><i class="fas fa-user"></i> 作者</label>
            <input type="text" id="anthor" class="form-control" v-model="state.lyb.author" required>
          </div>
          <div class="form-group">
            <label><i class="fas fa-file-alt"></i> 内容</label>
            <textarea class="form-control" id="content" v-model="state.lyb.content" rows="4" required></textarea>
          </div>
          <button type="submit" class="btn w-100" @click="savelyb">
            <i class="fas fa-paper-plane"></i> 提交
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
