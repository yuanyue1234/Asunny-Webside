<template>
  <div class="page-main">
    <HeaderImg />
    <profile-section v-if="profileDataFromAPI" :profile="profileDataFromAPI" />
    <div v-else-if="loading">正在加载个人信息...</div>
    <div v-else-if="error">加载个人信息失败: {{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ProfileSection from './ProfileSection.vue';

const profileDataFromAPI = ref(null);
const loading = ref(true);
const error = ref('');

const API_URL = 'http://127.0.0.1:8000/api/site/profile/';

const fetchProfileData = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await axios.get(API_URL);
    if (response.data && response.data.profile_data) {
      profileDataFromAPI.value = response.data.profile_data; // 我们需要传递 profile_data 内部的对象
    } else {
      error.value = '未能获取有效的个人配置数据。';
      console.warn('API did not return expected profile_data structure:', response.data);
    }
  } catch (err) {
    console.error('获取个人配置数据失败:', err);
    error.value = '获取个人配置数据失败。';
    if (err.response && err.response.status === 404) {
        error.value = '个人配置端点未找到 (404)。';
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProfileData();
});
</script>

<style scoped>
/* 您可以添加一些样式来处理加载和错误状态 */
</style> 