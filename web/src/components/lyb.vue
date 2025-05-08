<script setup>
import { ref, reactive, onMounted, toRefs } from 'vue'
import axios from 'axios'

// 用于表单输入
const lyb_blank ={
  url:'',
  title: '',
  author: '',
  content: ''
}
const editLyb =(item)=>{
  state.lyb.url = item.url;
  state.lyb.title = item.title;
  state.lyb.author = item.author;
  state.lyb.content = item.content;
}

// 用于存储留言列表
const state = reactive({
  ly_list: [],
  lyb: Object.assign({},lyb_blank)
})

// 获取留言列表
const base_url = "http://127.0.0.1:8000/api/lyb/"
const getLyb = () => {
  axios.get(base_url).then(res => {
    state.ly_list = res.data
  }).catch(err => {
    console.log(err)
  })
}

// // 添加留言
// const addMessage = () => {
//   axios.post(base_url, state.lyb).then(res => {
//     getLyb()
//     state.lyb = Object.assign({}, lyb_blank)
//   }).catch(err => {
//     console.log(err)
//   })
// }

onMounted(() => {
  getLyb()
})
</script>

<template>
  <div class="row">
    <div class="col-md-8">
      <table class="table table-bordered">
        <thead>
          <tr>
            <td>标题</td>
            <td>作者</td>
            <td>内容</td>
            <td>操作</td>
          </tr>
        </thead> 
        <tbody>
          <tr v-for="(message, index) in state.ly_list" :key="index">
            <td>{{ message.title }}</td>
            <td>{{ message.author }}</td>
            <td>{{ message.content }}</td>
            <td>
              <button class="btn btn-success" title="编辑" @click="editLyb(item)" ">
                <i class="glyphicon glyphicon-pencil"></i> 
              </button>
              <button class="btn btn-danger" title="删除" @click="deleteMessage(item)">
                <i class="glyphicon glyphicon-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="col-md-4">
      <input type="hidden">
      <div class="card">
        <div class="card-header">
          发表留言
        </div>
        <div class="card-body">
          <form @submit.prevent="addMessage">
            <div class="form-group">
              <label>标题</label>
              <input type="text" id="title" class="form-control" v-model="lyb.title" required>
            </div>
            <div class="form-group">
              <label>作者</label>
              <input type="text" id="anthor" class="form-control" v-model="lyb.author" required>
            </div>
            <div class="form-group">
              <label>内容</label>
              <textarea class="form-control" id="content" v-model="lyb.content" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">提交</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}
.card {
  margin-top: 1rem;
}
</style>
