<template>
  <div class="card">
    <div class="card-image">
      <img :src="image" alt="图片" />
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
      <span class="card-date">{{ date }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardComponent',
  props: {
    image: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
    date: {
      type: String,
      required: true,
    },
  },
}
</script>

<style scoped>
.card {
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: var(--secondary-color);
  box-shadow: 0 4px 6px var(--primary-color);
  position: relative;
}

.card-image img {
  width: 100%;
  height: auto;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 18px;
  margin: 0;
  font-weight: bold;
}

.card-description {
  font-size: 14px;
  color: #555;
  margin: 8px 0;
}

.card-date {
  position: absolute;
  right: 16px;
  bottom: 16px;
  font-size: 12px;
  color: #888;
}
</style>
