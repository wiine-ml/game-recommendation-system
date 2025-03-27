<template>
  <div class="close-btn" v-if="onPriview">
    <button>123</button>
  </div>
  <div class="vendor-home">
    <!-- 顶部厂商信息 -->
    <div class="vendor-header">
      <div class="header-bg" :style="{ backgroundImage: `url(${vendorHeadImage})` }">
        <div class="vendor-profile">
          <img :src="vendorAvatar" alt="厂商头像" class="vendor-avatar" />
          <h1 class="vendor-name">{{ vendorName }}</h1>
        </div>
      </div>
    </div>

    <!-- 厂商游戏列表 -->
    <ContentMatrix :activeMainContent="activeContent" class="vendor-games" />

    <!-- 游戏详情弹窗 -->
    <GameDetail
      v-if="selectedGame"
      :showDetail="showDetail"
      :gameDetail="selectedGame"
      :interactable="false"
      @close-detail="closeDetail"
    />
  </div>
</template>

<script>
import ContentMatrix from './ContentMartix.vue'
import GameDetail from './GameDetail.vue'
import DataService from '../services/DataService'

export default {
  props: {
    onPriview: {
      type: Boolean,
      required: false,
    },
  },
  components: {
    ContentMatrix,
    GameDetail,
  },
  data() {
    return {
      activeContent: 'vendor',
      recommendedGames: [],
      selectedGame: null,
      showDetail: false,
      vendorHeadImage: '', // 用于存储厂商头图
    }
  },
  computed: {
    vendorID() {
      return this.$store.getters['vendor/vendorID']
    },
    vendorType() {
      return this.$store.getters['vendor/vendorType']
    },
    vendorName() {
      return this.$store.getters['vendor/vendorName']
    },
    vendorAvatar() {
      console.log('avatarUrl:' + this.$store.getters['vendor/avatarUrl'])
      return this.$store.getters['vendor/avatarUrl']
    },
    vendorHeadIllustrations() {
      return this.$store.getters['vendor/vendorHeadIllustrations']
    },
  },
  filters: {
    truncate(text, length) {
      return text?.length > length ? text.substr(0, length) + '...' : text
    },
  },
  async created() {
    await this.fetchRecommendedGames()
    await this.fetchVendorHeadImage() // 在页面挂载时加载厂商头图
  },
  methods: {
    async fetchRecommendedGames() {
      try {
        const response = await DataService.get('/vendor/recommended_games', {
          params: {
            vendor_id: this.vendorID,
            vendor_type: this.vendorType,
          },
        })

        this.recommendedGames = await Promise.all(
          response.data.data.map(async (game) => ({
            ...game,
            previewImage: await this.loadGameImage(game.id),
          })),
        )
      } catch (error) {
        console.error('获取推荐游戏失败:', error)
      }
    },

    async loadGameImage(gameId) {
      try {
        const response = await DataService.get(`/games/preview_image/read/${gameId}`, {
          responseType: 'blob',
        })
        return URL.createObjectURL(response.data)
      } catch (error) {
        console.error('加载游戏封面失败:', error)
      }
    },

    async fetchVendorHeadImage() {
      try {
        const response = await DataService.get('/vendor/head_image/read', {
          params: {
            vendor_id: this.vendorID,
            vendor_type: this.vendorType,
          },
          responseType: 'blob',
        })
        this.vendorHeadImage = URL.createObjectURL(response.data)
      } catch (error) {
        console.error('获取厂商头图失败:', error)
        // 如果获取失败，使用默认头图
        this.vendorHeadImage = 'default_head_image.jpg'
      }
    },

    showGameDetail(game) {
      this.selectedGame = game
      this.showDetail = true
    },

    closeDetail() {
      this.showDetail = false
      this.selectedGame = null
    },
  },
}
</script>

<style scoped>
.vendor-home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.vendor-header {
  position: relative;
  margin-bottom: 40px;
}

.header-bg {
  height: 300px;
  background-size: cover;
  background-position: center;
  border-radius: 12px;
  position: relative;
}

.vendor-profile {
  position: absolute;
  bottom: -50px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.vendor-avatar {
  width: 100px;
  height: 100px;
  border-radius: 90%;
  border: 3px solid white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.vendor-name {
  margin-top: 15px;
  color: var(--contrast-color);
  font-size: 24px;
}

.recommended-games {
  margin: 80px 0 40px;
}

.section-title {
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.game-carousel {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding: 10px 0;
}

.game-card {
  flex: 0 0 250px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.game-card:hover {
  transform: translateY(-5px);
}

.game-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.game-info {
  padding: 15px;
}

.game-title {
  font-size: 16px;
  margin: 0 0 8px;
  color: #333;
}

.game-description {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  margin: 0;
}

.vendor-games {
  margin-top: 40px;
}

@media (max-width: 768px) {
  .header-bg {
    height: 200px;
  }

  .vendor-avatar {
    width: 80px;
    height: 80px;
  }

  .vendor-name {
    font-size: 20px;
  }

  .game-card {
    flex: 0 0 200px;
  }
}
</style>
