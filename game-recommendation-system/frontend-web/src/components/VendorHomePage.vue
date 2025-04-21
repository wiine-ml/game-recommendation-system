<template>
  <div class="close-btn" v-if="onPriview">
    <button @click="closeVendorPage"><p>返回</p></button>
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

    <hr />

    <div class="carousel-container">
      <div class="carousel">
        <button class="carousel-button prev" @click="prevImage">&lt;</button>
        <transition name="fade" mode="out-in">
          <img :key="currentImageIndex" :src="currentImage" alt="轮播图" />
        </transition>
        <button class="carousel-button next" @click="nextImage">&gt;</button>
      </div>
    </div>

    <hr />

    <!-- 厂商游戏列表 -->
    <ContentMatrix
      :activeMainContent="activeContent"
      :vendorID="this.vendorID"
      class="vendor-games"
    />

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
import DataService from '../services/DataService'
import JSZip from 'jszip'
import { defineAsyncComponent } from 'vue'

export default {
  emits: ['closeVendorPage'],
  props: {
    avtiveMainContent: String,
    onPriview: Boolean,
    vendor_id_prop: Number,
    vendor_type_prop: String,
    vendor_name_prop: String,
  },
  components: {
    ContentMatrix: defineAsyncComponent(() => import('./ContentMartix.vue')),
    GameDetail: defineAsyncComponent(() => import('./GameDetail.vue')),
  },
  data() {
    return {
      activeContent: 'vendor',
      recommendedGames: [],
      selectedGame: null,
      showDetail: false,
      vendorHeadImage: '',

      recommendationType: 'user_based_CF',
      images: [], // 存储解压后的图片数据
      currentImageIndex: 0, // 当前显示的图片索引
      carouselInterval: null, // 轮播定时器
    }
  },
  computed: {
    vendorID() {
      if (this.vendor_id_prop !== undefined) {
        return this.vendor_id_prop
      }
      return this.$store.getters['vendor/vendorID']
    },
    vendorType() {
      if (this.vendor_type_prop !== undefined) {
        return this.vendor_type_prop
      }
      return this.$store.getters['vendor/vendorType']
    },
    vendorName() {
      if (this.vendor_name_prop !== undefined) {
        return this.vendor_name_prop
      }
      return this.$store.getters['vendor/vendorName']
    },
    vendorAvatar() {
      console.log('avatarUrl:' + this.$store.getters['vendor/avatarUrl'])
      return this.$store.getters['vendor/avatarUrl']
    },
    vendorHeadIllustrations() {
      return this.$store.getters['vendor/vendorHeadIllustrations']
    },
    currentImage() {
      return this.images[this.currentImageIndex] || ''
    },
  },
  mounted() {
    // 组件挂载后启动轮播
    this.startCarousel()
  },
  beforeUnmount() {
    // 组件销毁前清除定时器
    this.stopCarousel()
  },
  filters: {
    truncate(text, length) {
      return text?.length > length ? text.substr(0, length) + '...' : text
    },
  },
  async created() {
    await this.fetchAndUnzipImages()
    await this.fetchVendorHeadImage() // 在页面挂载时加载厂商头图
  },
  methods: {
    closeVendorPage() {
      console.log('closeVendorPage called')
      this.$emit('close-vendor-page')
    },
    getVendorParams() {
      // 判断是否使用props中的参数
      if (this.vendor_id_prop !== undefined && this.vendor_type_prop !== undefined) {
        console.log('使用参数:' + this.vendor_id_prop + this.vendor_type_prop)
        return {
          vendor_id: this.vendor_id_prop,
          vendor_type: this.vendor_type_prop,
        }
      } else {
        // 否则使用store中的参数
        console.log('使用vuex数据:' + this.vendorID + this.vendorType)
        return {
          vendor_id: this.vendorID,
          vendor_type: this.vendorType,
        }
      }
    },
    async fetchAndUnzipImages() {
      try {
        console.log('fetchAndUnzipImages')
        const params = this.getVendorParams()

        // 获取后端的ZIP文件
        const response = await DataService.get('/vendor/promoted_image/read', {
          params,
          responseType: 'blob',
        })

        // 使用JSZip解压ZIP文件
        const zipBlob = response.data
        const zip = new JSZip()
        const zipContent = await zip.loadAsync(zipBlob)

        // 提取ZIP中的图片文件
        const imageFiles = []
        for (const fileKey in zipContent.files) {
          if (!zipContent.files[fileKey].dir) {
            imageFiles.push(zipContent.files[fileKey])
          }
        }

        // 按文件名排序（可选）
        imageFiles.sort((a, b) => a.name.localeCompare(b.name))

        // 限制最多5张图片
        const maxImages = 5
        const selectedFiles = imageFiles.slice(0, maxImages)
        console.log('selectedFiles:', selectedFiles)

        // 将图片转换为Base64格式
        this.images = await Promise.all(
          selectedFiles.map(async (file) => {
            const fileContent = await file.async('blob')
            return URL.createObjectURL(fileContent)
          }),
        )

        // 如果没有图片，显示错误信息
        if (this.images.length === 0) {
          console.error('没有找到图片文件')
        }

        console.log('fetchAndUnzipImages success')
      } catch (error) {
        console.error('获取或解压图片失败:', error)
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
    startCarousel() {
      // 清除之前的定时器
      this.stopCarousel()
      // 设置新的定时器，每3秒切换一次图片
      this.carouselInterval = setInterval(() => {
        this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length
      }, 3000)
    },
    stopCarousel() {
      if (this.carouselInterval) {
        clearInterval(this.carouselInterval)
        this.carouselInterval = null
      }
    },
    prevImage() {
      // 手动切换到上一张图片
      console.log('prev')
      this.currentImageIndex =
        (this.currentImageIndex - 1 + this.images.length) % this.images.length
    },
    nextImage() {
      // 手动切换到下一张图片
      console.log('next')
      this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length
    },
  },
}
</script>

<style scoped>
hr {
  margin-top: 20px;
  margin-bottom: 20px;
  border: 0;
  height: 3px;
  background: #333;
  background-image: linear-gradient(
    to right,
    var(--secondary-color),
    var(--main-color),
    var(--secondary-color)
  );
}

.carousel-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  position: relative;
}

.carousel {
  width: 100%;
  height: 400px;
  overflow: hidden;
  position: relative;
}

.carousel img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 添加按钮样式 */
.carousel-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
}

.carousel-button.prev {
  left: 10px;
}

.carousel-button.next {
  right: 10px;
}

/* 轮播过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

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
  margin-bottom: 10px;
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
