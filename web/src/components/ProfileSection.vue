<template>
  <div class="profile">
    <div class="profile-header">
      <div class="carousel">
        <div class="carousel-item active">
          <img :src="profile.avatar" class="clickable">
        </div>
        <div class="carousel-nav"></div>
      </div>
      <img class="avatar" :src="profile.avatar" :alt="profile.name">
    </div>

    <div class="profile-info">
      <div class="name">
        {{ profile.name }}
        <a v-for="social in profile.socialLinks" 
           :key="social.platform"
           :href="social.url" 
           class="social-icon" 
           target="_blank">
          <component :is="social.icon" />
        </a>
      </div>
      <div class="username">{{ profile.email }}</div>
      <div>
        <center class="dibu">
          <div style="line-height: 20px;font-family: 'Microsoft YaHei';font-size:14px;">
            <span>
              <span id="hitokoto">
                <a href="#" id="hitokoto_text">"你只活一次."</a>
              </span>
            </span>
          </div>
        </center>
      </div>
    </div>

    <h2>兴趣</h2>
    <div class="showcase">
      <div v-for="interest in profile.interests" 
           :key="interest.title" 
           class="showcase-item">
        <h3>{{ interest.title }}</h3>
        <div class="showcase-title">{{ interest.subtitle }}</div>
        <div class="showcase-content">
          <img v-for="img in interest.images" 
               :key="img"
               :src="img"
               class="clickable">
        </div>
      </div>
    </div>

    <h2>作品</h2>
    <div class="showcase">
      <div v-for="work in profile.works" 
           :key="work.title" 
           class="showcase-item">
        <div class="showcase-title">{{ work.title }}</div>
        <div class="showcase-content">
          <p v-for="item in work.items" :key="item.url">
            <a :href="item.url">{{ item.text }}</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
defineProps({
  profile: {
    type: Object,
    required: true
  }
})
</script> 