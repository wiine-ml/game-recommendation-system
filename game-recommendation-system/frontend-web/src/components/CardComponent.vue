<template>
  <div class="card">
    <div class="card-image">
      <img id="news-image" :src="this.newsImage" alt="图片" />
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
      <span class="card-date">{{ date }}</span>
    </div>
  </div>
</template>

<script>
import DataService from '@/services/DataService'

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
    id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      newsImage: '',
      isImageLoading: true, // 跟踪图片加载状态
    }
  },
  methods: {
    async fetchNewsImage(newsId) {
      try {
        // 调用接口获取新闻图片
        const imageResponse = await DataService.get(`/news/img/read/${newsId}`, {
          responseType: 'blob', // 指定响应类型为 blob
        })

        // 创建图片的 URL
        this.newsImage = URL.createObjectURL(imageResponse.data)
        console.log(`获取新闻 ${newsId} 的图片成功>>> `, this.newsImage)
      } catch (error) {
        console.error(`获取新闻 ${newsId} 的图片失败:`, error)
        // 如果获取图片失败，使用默认图片
        this.newsImage = 'defaultNewsImage.jpg'
      }
    },
  },
  created() {
    this.fetchNewsImage(this.id)
  },
  mounted() {
    this.fetchNewsImage(this.id)
  },
  watch: {
    id: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchNewsImage(newVal)
      }
    },
  },
}
</script>

<style scoped>
#news-image {
  width: 100%;
  height: auto;
  aspect-ratio: 16/9;
  object-fit: cover;
  max-width: 100%;
  max-height: 200px;
}

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
  color: var(--contrast-color-alpha1);
  margin: 8px 0;
}

.card-date {
  position: absolute;
  right: 16px;
  bottom: 16px;
  color: var(--contrast-color-alpha2);
}
</style>
