<template>
  <div class="card-grid">
    <Card
      v-for="(item, index) in filteredCards"
      :key="index"
      :id="item.id"
      :image="newsImage"
      :title="item.title"
      :description="item.description"
      :date="item.date"
    />
  </div>
</template>

<script>
import Card from './CardComponent.vue'
import DataService from '../services/DataService'

export default {
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
  },
  components: { Card },
  created() {
    this.fetchNews()
  },
  data() {
    return {
      cards: [],
      newsImage: '',
    }
  },
  methods: {
    async fetchNews() {
      try {
        const response = await DataService.get('/news/read')
        this.cards = response.data.data
        console.log('获取数据成功:', response.data)
      } catch (error) {
        console.error('获取数据失败:', error)
        alert('获取数据失败')
      } finally {
        this.isLoading = false
      }
    },
  },
  computed: {
    filteredCards() {
      if (!this.activeMainContent) {
        alert('界面出现了点问题？')
        return this.cards
      }
      // 否则，只返回 type 等于 activeMainContent 的卡片
      return this.cards.filter((card) => card.type === this.activeMainContent)
    },
  },
}
</script>

<style scoped>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  padding: 16px;
}
</style>
