<template>
  <div class="profile-container">
    <!-- Profile Card -->
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

    <!-- Works Showcase -->
    <div class="showcase card" ref="worksCard">
      <div class="card__wrapper">
        <div class="card__3d">
          <div v-for="(work, index) in profile.works"
               :key="work.title"
               class="showcase-item">
            <div class="showcase-title">{{ work.title }}</div>
            <div class="showcase-content">
              <p v-for="item in work.items" :key="item.url">
                <a :href="item.url" target="_blank">{{ item.text }}</a>
              </p>
            </div>
            <!-- 最后一项不显示分割线 -->
            <hr v-if="index !== profile.works.length - 1">
          </div>
        </div>
      </div>
    </div>

    <!-- Interests Showcase -->
    <div class="showcase card" ref="interestsCard">
      <div class="card__wrapper">
        <div class="card__3d">
          <div v-for="(interest, index) in profile.interests"
               :key="interest.title"
               class="showcase-item">
            <div class="showcase-title">{{ interest.subtitle }}</div>
            <div class="showcase-content">
              <img v-for="img in interest.images"
                   :key="img"
                   :src="img"
                   class="clickable">
            </div>
            <hr v-if="index !== profile.interests.length - 1">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';

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
  const isMobile = window.innerWidth <= 650;

  if (isMobile) return;

  cards.forEach(card => {
    if (!card) return;

    // 获取实际进行3D变换的内部容器
    const card3d = card.querySelector('.card__3d');
    let isHovering = false;

    card.addEventListener('mouseenter', () => {
      isHovering = true;
    });

    card.addEventListener('mouseleave', () => {
      isHovering = false;
      // 复位
      card3d.style.transform = 'rotateY(0deg) rotateX(0deg)';
      card3d.style.setProperty('--x', '50%');
      card3d.style.setProperty('--y', '50%');
      card3d.style.setProperty('--bg-x', '40%');
      card3d.style.setProperty('--bg-y', '40%');
    });

    card.addEventListener('mousemove', (e) => {
      if (!isHovering) return;

      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const xPercent = x / rect.width;
      const yPercent = y / rect.height;

      // 更加细腻的倾斜角度
      const rotateY = (xPercent - 0.5) * 8;
      const rotateX = (0.5 - yPercent) * 8;

      card3d.style.transform = `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;

      card3d.style.setProperty('--x', `${xPercent * 100}%`);
      card3d.style.setProperty('--y', `${yPercent * 100}%`);

      const bgX = 40 + 15 * xPercent; // 减缓背景移动速度
      const bgY = 40 + 15 * yPercent;
      card3d.style.setProperty('--bg-x', `${bgX}%`);
      card3d.style.setProperty('--bg-y', `${bgY}%`);
    });
  });

  window.addEventListener('resize', () => {
    const isMobile = window.innerWidth <= 650;
    cards.forEach(card => {
      if (!card) return;
      const card3d = card.querySelector('.card__3d');
      if (isMobile && card3d) {
        card3d.style.transform = 'none';
      }
    });
  });
});
</script>

<style scoped>
@import url("https://chinese-fonts-cdn.deno.dev/packages/LxgwNeoZhiSong/dist/LXGWNeoZhiSong/result.css");

/* ---------------- 基础变量 ---------------- */
:root {
  /* 颜色系统 */
  --md-sys-color-primary: #7D33FF;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EDE0FF;
  --md-sys-color-secondary: #5C4B70;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-background: #F5F3FF;
  --md-sys-color-surface: #FFFFFF;
  --md-sys-color-surface-variant: #ECE6F0;
  --md-sys-color-on-surface: #1B1B1F;
  --md-sys-color-on-surface-variant: #49454F;

  /* 尺寸与间距 */
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 圆角统一 */
  --border-radius-lg: 24px; /* 统一使用 24px 的大圆角 */

  /* 动效 */
  --transition-normal: 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* 深色主题适配变量 */
body.dark-theme {
  --md-sys-color-primary: #D0BCFF;
  --md-sys-color-surface: #1C1B1F;
  --md-sys-color-background: #121212;
  --md-sys-color-surface-variant: #49454F;
  --md-sys-color-on-surface: #E6E1E5;
}

.profile-container {
  max-width: 720px; /* 稍微加宽一点，让卡片更舒展 */
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'LXGW Neo ZhiSong', sans-serif;
}

/* ---------------- 卡片容器系统 (3D核心) ---------------- */

/* 外层 Card 容器：负责占位和透视，不再设置背景色 */
.card {
  position: relative;
  margin-bottom: 32px;
  width: 100%;
  min-height: 200px;
  perspective: 1500px; /* 增加视距，让3D效果更自然 */
  z-index: 1;
  background: transparent; /* 关键：背景透明 */
  border-radius: var(--border-radius-lg);
}

/* 包装器 */
.card__wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

/* 实际的 3D 卡片体：负责背景、阴影和内容承载 */
.card__3d {
  --x: 50%;
  --y: 50%;
  --bg-x: 40%;
  --bg-y: 40%;

  position: relative;
  width: 100%;
  height: 100%;
  padding: 32px; /* 增加内部留白 */
  border-radius: var(--border-radius-lg); /* 统一圆角 */

  /* 背景色与材质 */
  background-color: color-mix(in srgb, var(--md-sys-color-surface), transparent 10%);

  /* 3D 属性 */
  transform: rotateY(0deg) rotateX(0deg);
  transform-style: preserve-3d;
  backface-visibility: hidden;
  transition: transform 0.1s linear, box-shadow 0.3s ease; /* 变换用 linear 避免卡顿 */

  /* 默认阴影 */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05),
  0 2px 4px -1px rgba(0, 0, 0, 0.03),
  0 0 0 1px rgba(0, 0, 0, 0.02); /* 微弱描边增加质感 */
}

/* 光照效果层 */
.card__3d::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--border-radius-lg);
  background: radial-gradient(
      800px circle at var(--x) var(--y),
      rgba(255, 255, 255, 0.4),
      transparent 40%
  );
  opacity: 0; /* 默认隐藏，hover时显示 */
  transition: opacity 0.3s ease;
  pointer-events: none;
  z-index: 10;
  mix-blend-mode: overlay;
}

/* Hover 状态提升 */
.card:hover .card__3d {
  box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.1),
  0 10px 20px -5px rgba(0, 0, 0, 0.05),
  0 0 0 1px rgba(125, 51, 255, 0.1); /* 主色调微光 */
}

.card:hover .card__3d::before {
  opacity: 1;
}

/* ---------------- 内容区域样式 ---------------- */

.profile-header,
.showcase-item {
  position: relative;
  z-index: 20; /* 确保内容在光照层之上 */
  transform: translateZ(30px); /* 内容悬浮感 */
}

/* 头像优化 */
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 16px;
  border: 4px solid var(--md-sys-color-surface); /* 使用背景色做边框，产生切割感 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); /* 弹性动画 */
}

.avatar:hover {
  transform: scale(1.1) rotate(5deg);
}

.profile-name h2 {
  margin: 8px 0;
  color: var(--md-sys-color-on-surface);
  font-size: 1.8rem;
  font-weight: 800;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 16px;
}

.social-icon {
  color: var(--md-sys-color-secondary);
  font-size: 1.5rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--md-sys-color-surface-variant);
}

.social-icon:hover {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  transform: translateY(-3px);
}

/* ---------------- 磨砂玻璃标题 (Glassmorphism) ---------------- */
.showcase-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--md-sys-color-primary);
  margin: 1.5rem 0 1rem;
  padding: 12px 20px;
  border-radius: 12px;

  /* 磨砂玻璃核心代码 */
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);

  /* 玻璃边缘高光 */
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

/* 深色模式下的玻璃效果微调 */
@media (prefers-color-scheme: dark) {
  .showcase-title {
    background: rgba(40, 40, 45, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
  }
}

/* ---------------- 列表内容 ---------------- */
.showcase-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  padding: 8px 0;
}

.showcase-content a {
  color: var(--md-sys-color-on-surface);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 10px;
  background-color: var(--md-sys-color-surface-variant); /* 默认浅灰背景 */
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.95rem;
}

.showcase-content a:hover {
  background-color: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  box-shadow: 0 4px 12px rgba(125, 51, 255, 0.3);
  transform: translateY(-2px);
}

.showcase-content img.clickable {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 16px; /* 图片圆角 */
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 2px solid transparent;
}

.showcase-content img.clickable:hover {
  transform: scale(1.08);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  border-color: var(--md-sys-color-primary-container);
  z-index: 5;
}

/* ---------------- 分割线 ---------------- */
hr {
  border: none;
  height: 1px;
  background: linear-gradient(
      90deg,
      transparent,
      var(--md-sys-color-outline),
      transparent
  ); /* 渐变分割线，看起来更高级 */
  opacity: 0.3;
  margin: 24px 0;
}

/* ---------------- 移动端适配 ---------------- */
@media screen and (max-width: 650px) {
  .card {
    perspective: none;
    margin-bottom: 20px;
  }

  .card__3d {
    transform: none !important;
    padding: 24px;
  }

  .profile-header, .showcase-item {
    transform: none;
  }

  .avatar {
    width: 100px;
    height: 100px;
  }
}
</style>
