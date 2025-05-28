<template>
    <div class="profile-container">
      <div class="profile-info card" ref="profileCard">
        <div class="card__wrapper">
          <div class="card__3d">
            <div class="profile-header">
              <img class="avatar" :src="profile.avatar" :alt="profile.name">
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
          </div>
        </div>
      </div>

      <div class="showcase card" ref="worksCard">
        <div class="card__wrapper">
          <div class="card__3d">
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
      </div>
      
      <div class="showcase card" ref="interestsCard">
        <div class="card__wrapper">
          <div class="card__3d">
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
        </div>
      </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

defineProps({
  profile: {
    type: Object,
    required: true
  }
})

const profileCard = ref(null);
const worksCard = ref(null);
const interestsCard = ref(null);

onMounted(() => {
  const cards = [profileCard.value, worksCard.value, interestsCard.value];
  
  // 检查屏幕宽度
  const isMobile = window.innerWidth <= 650;
  
  if (isMobile) return; // 如果是移动设备，不添加动效
  
  cards.forEach(card => {
    if (!card) return;
    
    const card3d = card.querySelector('.card__3d');
    let isHovering = false;

    card.addEventListener('mouseenter', () => {
      isHovering = true;
    });

    card.addEventListener('mouseleave', () => {
      isHovering = false;
      card3d.style.transform = 'rotateY(0deg) rotateX(0deg)';
    });

    card.addEventListener('mousemove', (e) => {
      if (!isHovering) return;

      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // 计算鼠标在卡片上的相对位置（0-1之间）
      const xPercent = x / rect.width;
      const yPercent = y / rect.height;
      
      // 减小旋转角度（从20度改为10度）
      const rotateY = (xPercent - 0.5) * 10; // 左右旋转
      const rotateX = (0.5 - yPercent) * 10; // 上下旋转
      
      // 应用变换
      card3d.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
    });
  });

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    const isMobile = window.innerWidth <= 650;
    cards.forEach(card => {
      if (!card) return;
      const card3d = card.querySelector('.card__3d');
      if (isMobile) {
        card3d.style.transform = 'rotateY(0deg) rotateX(0deg)';
      }
    });
  });
});
</script>

<style scoped>
.profile-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.card {
    position: relative;
    border-radius: 24px !important;
    background-color: var(--md-sys-color-background) !important;
    padding: 24px !important;
    margin: 16px 0 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    overflow: hidden;
    z-index: 1;
    perspective: 1000px;
    width: 100%;
    min-height: 200px;
}

.card__wrapper {
    perspective: 1000px;
    position: relative;
    width: 100%;
    height: 100%;
}

.card__3d {
    transform: rotateY(0deg) rotateX(0deg);
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 24px;
    background-color: var(--md-sys-color-surface);
    padding: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    transform-style: preserve-3d;
    backface-visibility: hidden;
    box-shadow: 
        0 8px 16px rgba(0, 0, 0, 0.08),
        0 4px 4px rgba(0, 0, 0, 0.08),
        0 0 60px rgba(125, 51, 255, 0.08);
}

.card__3d::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 24px;
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.1) 0%,
        rgba(255, 255, 255, 0) 50%,
        rgba(255, 255, 255, 0.1) 100%
    );
    pointer-events: none;
    z-index: 1;
}

.profile-header {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    transform: translateZ(20px);
}

.profile-name {
    position: relative;
    z-index: 2;
    text-align: center;
    width: 100%;
    transform: translateZ(20px);
}

.showcase-item {
    position: relative;
    z-index: 2;
    margin: 20px 0;
    transform: translateZ(20px);
}

.showcase-content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    padding: 16px 0;
    justify-content: center;
    transform: translateZ(20px);
}

.card:hover {
    transform: translateY(-3px);
}

.card:hover .card__3d {
    box-shadow: 
        0 12px 24px rgba(0, 0, 0, 0.12),
        0 8px 12px rgba(0, 0, 0, 0.08),
        0 0 80px rgba(125, 51, 255, 0.12);
}

/* 移动端样式 */
@media screen and (max-width: 650px) {
    .card {
        perspective: none;
    }
    
    .card__wrapper {
        perspective: none;
    }
    
    .card__3d {
        transform: none !important;
        transform-style: flat;
    }
    
    .profile-header,
    .profile-name,
    .showcase-item,
    .showcase-content {
        transform: none;
    }
    
    .card:hover {
        transform: translateY(-2px);
    }
    
    .card:hover .card__3d {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
    }
}

/* 确保内容在3D效果之上 */
.profile-header, .profile-name, .showcase-item, .showcase-content {
    position: relative;
    z-index: 2;
}

.profile-name{
    text-align: center;
    color: var(--md-sys-color-on-surface);
}

.profile-name h2 {
  margin: 0 0 16px 0;
  color: var(--md-sys-color-primary);
  font-size: 2rem;
}
/* 动画效果 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.fade-in-up {
    animation: fadeInUp var(--transition-normal) ease-out;
}


.social-links {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
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


/* 这里是个人简介部分 */
.social-icon {
    display: inline-flex;
    width: 24px;
    height: 24px;
    align-items: center;
    transition: color 0.3s ease;
}


.social-icon:hover {
    color:var(--md-sys-color-on-primary-container); 
}


/* 头像 */
.avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    display: block;
    margin:5px auto;
    border: 3px solid var(--md-sys-color-primary);
    transition: transform 0.3s ease;
}

.avatar:hover {
    transform: rotate(360deg);
}

/* user card 展示 */


.name {
    font-size: 24px;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
}

.username {
    color: var(--md-sys-color-on-surface-variant);
}


hr {
  border: none;
  height: 1px;
  background: var(--md-sys-color-surface-variant);
  margin: 16px 0;
}
</style> 