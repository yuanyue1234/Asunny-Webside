<template>
    <div class="profile-header">
      <div class="carousel">
        <div class="carousel-item active">
          <img :src="profile.avatar" class="clickable">
        </div>
        <div class="carousel-nav"></div>
      </div>
      <img class="avatar" :src="profile.avatar" :alt="profile.name">
    </div>
</template>