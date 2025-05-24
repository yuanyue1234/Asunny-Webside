<template>
  <div class="page-footer">
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
</template>

<script>
import Lyb from './lyb.vue'

export default {
  name: 'PageFooter',
  components: {
    Lyb
  }
}
</script>

<style scoped>

/* 一言样式 */
#hitokoto {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: var(--spacing-lg) 0;
}

#hitokoto_text {
    color: var(--md-sys-color-on-primary);
    text-decoration: none;
    font-style: italic;
    transition: color var(--transition-normal);
    font-weight: 900;

}

</style> 