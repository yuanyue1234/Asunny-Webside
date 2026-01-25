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



.social-icon:hover {
    color:var(--md-sys-color-on-primary-container); 
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
</style>

