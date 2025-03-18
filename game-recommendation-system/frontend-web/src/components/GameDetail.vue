<template>
  <div v-if="showDetail" class="game-detail-overlay">
    <div class="game-detail-panel">
      <div class="game-detail-header">
        <h2>{{ gameDetail.gameTitle }}</h2>
        <button @click="closeDetail">×</button>
      </div>
      <div class="game-detail-content">
        <div class="game-detail-info">
          <p><strong>游戏类型:</strong> {{ gameDetail.gameGenre }}</p>
          <p><strong>游戏平台:</strong> {{ gameDetail.gamePlatform }}</p>
          <p><strong>游戏开发商:</strong> {{ gameDetail.gameDeveloper }}</p>
          <p><strong>游戏发行商:</strong> {{ gameDetail.gamePublisher }}</p>
          <p><strong>发行日期:</strong> {{ formattedReleaseDate }}</p>
          <p><strong>评分:</strong> {{ gameDetail.rating }}</p>
          <p><strong>评分描述:</strong> {{ gameDetail.ratingPhrase }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    showDetail: {
      type: Boolean,
      default: false,
    },
    gameDetail: {
      type: Object,
      default: null,
    },
  },
  computed: {
    formattedReleaseDate() {
      return this.gameDetail.releaseYear
        ? `${this.gameDetail.releaseYear}-${this.gameDetail.releaseMonth}-${this.gameDetail.releaseDay}`
        : '暂无'
    },
  },
  methods: {
    closeDetail() {
      this.$emit('close-detail')
    },
  },
}
</script>

<style scoped>
.img {
  float: left;
}

.game-detail-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: #00000000;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  z-index: 1;
}

.game-detail-panel {
  background-color: var(--secondary-color-alpha1);
  color: var(--contrast-color);
  width: 80%;
  height: 50%;
  max-width: 700px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  padding: 20px;
  position: relative;
}

.game-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.game-detail-header button {
  border: none;
  border-radius: 10px;
  font-size: 24px;
  cursor: pointer;
  color: var(--main-color);
}

.game-detail-content {
  overflow-y: auto;
  max-height: 80vh;
}
.game-detail-info p {
  margin-bottom: 10px;
  line-height: 1.5;
}
</style>
