<template>
    <div class="profile-info">
      <div class="">
        {{ profile.name }}
        <a v-for="social in profile.socialLinks" 
           :key="social.platform"
           :href="social.url" 
           class="social-icon" 
           target="_blank">
          <i :class="social.icon"></i>
        </a>
      </div>
      <div class="">{{ profile.email }}</div>
      <!-- 一言 -->
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

    <div class="showcase">
      <div v-for="interest in profile.interests" 
           :key="interest.title" 
           class="showcase-item">
        <div class="showcase-title">{{ interest.subtitle }}</div>
        <div class="showcase-content">
          <img v-for="img in interest.images" 
               :key="img"
               :src="img"
               class="clickable">
        </div>
        <hr>
      </div>
    </div>
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
        <hr>
      </div>
    </div>
</template>

<script setup>
defineProps({
  profile: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>

.clickable {
  max-width: 100px;
  width: 100%;
  height: auto;
  object-fit: contain;
  cursor: pointer;
  margin: 5px;
  transition: transform 0.2s;
}

.clickable:hover {
  transform: scale(1.05);
}
</style> 