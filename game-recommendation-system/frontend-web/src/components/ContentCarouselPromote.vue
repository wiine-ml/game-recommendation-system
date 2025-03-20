<template>
  <h1>热门游戏</h1>
  <div class="carousel-container">
    <div class="carousel">
      <button class="carousel-button prev" @click="prevImage">&lt;</button>
      <transition name="fade" mode="out-in">
        <img :key="currentImageIndex" :src="currentImage" alt="轮播图" />
      </transition>
      <button class="carousel-button next" @click="nextImage">&gt;</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import JSZip from 'jszip'

export default {
  data() {
    return {
      images: [], // 存储解压后的图片数据
      currentImageIndex: 0, // 当前显示的图片索引
      carouselInterval: null, // 轮播定时器
    }
  },
  computed: {
    currentImage() {
      // 返回当前显示的图片
      return this.images[this.currentImageIndex] || ''
    },
  },
  created() {
    this.fetchAndUnzipImages()
  },
  mounted() {
    // 组件挂载后启动轮播
    this.startCarousel()
  },
  beforeUnmount() {
    // 组件销毁前清除定时器
    this.stopCarousel()
  },
  methods: {
    async fetchAndUnzipImages() {
      try {
        // 获取后端的ZIP文件
        const response = await axios.get('/api/games/promote_image', {
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
      } catch (error) {
        console.error('获取或解压图片失败:', error)
      }
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

<style>
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
</style>
