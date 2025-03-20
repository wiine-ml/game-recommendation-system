<template>
  <div v-if="showDetail" class="game-detail-overlay">
    <div class="game-detail-panel">
      <div class="game-detail-header">
        <h2>{{ gameDetail.gameTitle }}</h2>
        <button @click="closeDetail">x</button>
      </div>
      <div class="game-detail-content">
        <div class="game-detail-image">
          <!-- 游戏图片 -->
          <img :src="originalImage" alt="游戏图片" style="max-width: 100%; max-height: 300px" />
        </div>
        <div class="game-detail-info">
          <p><strong>游戏类型:</strong> {{ gameDetail.gameGenre }}</p>
          <p><strong>游戏平台:</strong> {{ gameDetail.gamePlatform }}</p>
          <p><strong>游戏开发商:</strong> {{ gameDetail.gameDeveloper }}</p>
          <p><strong>游戏发行商:</strong> {{ gameDetail.gamePublisher }}</p>
          <p><strong>发行日期:</strong> {{ formattedReleaseDate }}</p>
          <p><strong>评分:</strong> {{ gameDetail.rating }}</p>
          <p><strong>评分描述:</strong> {{ gameDetail.ratingPhrase }}</p>
        </div>
        <div class="game-detail-rating-chart">
          <div class="chart-container">
            <vue-echarts :option="chartOption" style="width: 80%; height: 300px" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'
import VueEcharts from 'vue-echarts'

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
  components: {
    VueEcharts,
  },
  data() {
    return {
      originalImage: '', // 用于存储游戏图片的 URL
      ratingDistribution: {}, // 评分分布数据
      chartOption: {}, // ECharts 配置选项
    }
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
    async fetchOriginalImage(gameId) {
      try {
        // 调用接口获取游戏图片
        const imageResponse = await DataService.get(`/games/image/read/${gameId}`, {
          responseType: 'blob', // 指定响应类型为 blob
        })

        // 创建图片的 URL
        this.originalImage = URL.createObjectURL(imageResponse.data)
      } catch (error) {
        console.error(`获取游戏 ${gameId} 的图片失败:`, error)
        // 如果获取图片失败，使用默认图片
        this.originalImage = 'defaultGameImage.jpg'
      }
    },
    async fetchRatingDistribution(gameId) {
      try {
        // 调用接口获取评分分布
        const response = await DataService.get(`/games/rating_distribution/${gameId}`)
        this.ratingDistribution = response.data.data

        // 配置 ECharts 选项
        this.chartOption = {
          title: {
            text: '评分分布',
            left: 'center',
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow',
            },
          },
          xAxis: {
            type: 'value',
            name: '数量',
          },
          yAxis: {
            type: 'category',
            data: ['4-5', '3-4', '2-3', '1-2', '0-1'],
            name: '评分区间',
          },
          series: [
            {
              name: '数量',
              type: 'bar',
              data: [
                this.ratingDistribution['4-5'] || 0,
                this.ratingDistribution['3-4'] || 0,
                this.ratingDistribution['2-3'] || 0,
                this.ratingDistribution['1-2'] || 0,
                this.ratingDistribution['0-1'] || 0,
              ],
              label: {
                show: true,
                position: 'right',
              },
            },
          ],
        }
      } catch (error) {
        console.error(`获取游戏 ${gameId} 的评分分布失败:`, error)
      }
    },
  },
  watch: {
    gameDetail(newVal) {
      if (newVal) {
        this.fetchOriginalImage(newVal.id)
        this.fetchRatingDistribution(newVal.id)
      }
    },
  },
  created() {
    if (this.gameDetail) {
      this.fetchOriginalImage(this.gameDetail.id)
      this.fetchRatingDistribution(this.gameDetail.id)
    }
  },
}
</script>

<style scoped>
.chart-container {
  width: 80%;
  height: 200px;
}

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
  height: fit-content;
  max-width: 800px;
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
