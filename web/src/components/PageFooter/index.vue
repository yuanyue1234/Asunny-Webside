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

</script>

<style scoped>

/* 一言样式 */
#hitokoto {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: var(--spacing-lg) 0;
    padding: var(--spacing-md);
    transition: all var(--transition-normal);
}

#hitokoto_text {
    color: var(--md-sys-color-on-surface-variant);
    text-decoration: none;
    font-style: italic;
    transition: all var(--transition-normal);
    font-weight: 500;
    font-size: var(--font-size-lg);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-md);
}

#hitokoto_text:hover {
    color: var(--md-sys-color-primary);
    background-color: var(--md-sys-color-primary-container);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

</style> 