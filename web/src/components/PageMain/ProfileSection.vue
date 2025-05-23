<template>
    <div class="profile-container">
      <div class="profile-info card">
        <div class="profile-header">
          <div class="profile-name">
            <h2>{{ profile.name }}</h2>
            <div class="social-links">
              <a v-for="social in profile.socialLinks" 
                :key="social.platform"
                :href="social.url" 
                class="social-icon" 
                target="_blank">
                <i :class="social.icon"></i>
              </a>
            </div>
          </div>
        </div>
        <!-- 一言 -->
        <div class="hitokoto-container">
          <div class="hitokoto-text">
            <span>
              <span id="hitokoto">
                <a href="#" id="hitokoto_text">"你只活一次."</a>
              </span>
            </span>
          </div>
        </div>
      </div>

      <div class="showcase card">
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

      <div class="showcase card">
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
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: var(--md-sys-color-surface);
  border-radius: 16px;
  padding: 24px;
  margin: 16px 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.profile-info {
  position: relative;
  overflow: hidden;
}

.profile-header {
  margin-bottom: 20px;
}

.profile-name {
  text-align: center;
}

.profile-name h2 {
  margin: 0 0 16px 0;
  color: var(--md-sys-color-primary);
  font-size: 2rem;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}

.social-icon {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  color: var(--md-sys-color-on-surface);
  background: var(--md-sys-color-surface-variant);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.social-icon:hover {
  color: var(--md-sys-color-on-primary);
  background: var(--md-sys-color-primary);
  transform: translateY(-2px);
}


.clickable {
  max-width: 100px;
  width: 100%;
  height: auto;
  object-fit: contain;
  cursor: pointer;
  margin: 5px;
  transition: transform 0.2s;
  border-radius: 8px;
}

.clickable:hover {
  transform: scale(1.05);
}

.showcase-title {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--md-sys-color-primary);
  margin: 1rem 0;
  padding: 0.8rem 1.2rem;
  background-color: var(--md-sys-color-surface-variant);
  border-radius: 8px;
}

.showcase-content {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px 0;
  justify-content: center;
}

.showcase-content a {
  color: var(--md-sys-color-primary);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 6px;
  background: var(--md-sys-color-surface-variant);
  transition: all 0.3s ease;
}

.showcase-content a:hover {
  background: var(--md-sys-color-primary-container);
  color: var(--md-sys-color-on-primary-container);
  transform: translateY(-2px);
}

hr {
  border: none;
  height: 1px;
  background: var(--md-sys-color-surface-variant);
  margin: 16px 0;
}
</style> 