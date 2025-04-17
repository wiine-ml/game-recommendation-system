<template>
  <div class="promoted-games-container">
    <h2>厂商推广图片管理</h2>

    <!-- 推广图片展示区域 -->
    <div class="promoted-images">
      <div v-for="(game, index) in promotedGames" :key="index" class="promoted-image-item">
        <img :src="game.imageUrl" :alt="`推广游戏 ${game.name}`" class="promoted-game-image" />
        <div class="game-info">
          <span class="game-name">{{ game.name }}</span>
          <button class="remove-promotion-btn" @click="removePromotion(game.id)">取消推广</button>
        </div>
      </div>

      <!-- 添加推广区域（当图片数量少于5张时显示） -->
      <div v-if="promotedGames.length < 5" class="add-promotion-area">
        <div class="input-group">
          <input type="text" v-model="newGameId" placeholder="请输入游戏ID" class="game-id-input" />
          <button class="search-game-btn" @click="searchGameById">搜索游戏</button>
        </div>

        <div v-if="foundGame" class="found-game-info">
          <span>找到游戏: {{ foundGame.gameTitle }}</span>
          <button class="add-promotion-btn" @click="addPromotion(foundGame.id)">添加推广</button>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>

    <!-- 错误信息 -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
  </div>

  <!-- 厂商游戏列表 -->
  <ContentMatrix :activeMainContent="activeContent" :interactable="false" class="vendor-games" />
</template>

<script>
import ContentMatrix from './ContentMartix.vue'
import DataService from '../services/DataService.js'
import JSZip from 'jszip'

export default {
  name: 'PromotedGamesManager',
  data() {
    return {
      activeContent: 'vendor',
      promotedGames: [], // 存储推广游戏信息
      newGameId: '', // 新增推广游戏ID输入
      foundGame: null, // 搜索到的游戏信息
      loading: false, // 加载状态
      errorMessage: '', // 错误信息
    }
  },
  components: {
    ContentMatrix,
  },
  methods: {
    // 获取厂商推广图片
    async fetchPromotedImages() {
      this.loading = true
      this.errorMessage = ''
      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        const response = await DataService.get('/vendor/promoted_image/read', {
          params: {
            vendor_id: vendorId,
            vendor_type: vendorType,
          },
          responseType: 'blob', // 指定响应类型为 blob
        })

        const zipBlob = response.data
        const zip = await JSZip.loadAsync(zipBlob)

        // 获取ZIP文件中的所有图片文件
        const imageFiles = []
        for (const fileKey in zip.files) {
          if (!zip.files[fileKey].dir) {
            imageFiles.push(zip.files[fileKey])
          }
        }

        // 按文件名排序（可选）
        imageFiles.sort((a, b) => a.name.localeCompare(b.name))

        // 提取游戏ID
        const gameIds = imageFiles.map((file) => {
          const fileName = file.name.split('_')[0]
          return parseInt(fileName)
        })

        // 获取游戏详情
        const gameDetails = await this.fetchGameDetails(gameIds)

        // 构建推广游戏对象
        const gamePromises = gameDetails.map(async (game) => {
          // 查找对应的游戏图片文件
          const gameImageFile = imageFiles.find((file) => file.name.startsWith(`${game.id}_`))
          if (gameImageFile) {
            // 将图片转换为Blob并生成URL
            const blob = await gameImageFile.async('blob')
            return {
              id: game.id,
              name: game.gameTitle,
              imageUrl: URL.createObjectURL(blob),
            }
          } else {
            // 如果未找到图片文件，使用默认图片
            return {
              id: game.id,
              name: game.gameTitle,
              imageUrl: 'defaultGameImage.jpg',
            }
          }
        })

        this.promotedGames = await Promise.all(gamePromises)
      } catch (error) {
        console.error('获取推广图片失败:', error)
        this.errorMessage = '获取推广图片失败，请稍后再试'
      } finally {
        this.loading = false
      }
    },

    // 获取游戏详情
    async fetchGameDetails(gameIds) {
      const gameDetails = []
      for (const gameId of gameIds) {
        try {
          const response = await DataService.get('/games/read/search', {
            params: {
              game_id: gameId,
            },
          })
          if (response.data.data && response.data.data.gameTitle) {
            gameDetails.push(response.data.data)
          }
        } catch (error) {
          console.error(`获取游戏 ${gameId} 详情失败:`, error)
        }
      }
      return gameDetails
    },

    // 添加推广
    async addPromotion(gameId) {
      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        await DataService.post('/game_vendor/promoted_game/add', {
          game_id: gameId,
          vendor_id: vendorId,
          vendor_type: vendorType,
        })

        this.newGameId = ''
        this.foundGame = null
        await this.fetchPromotedImages()
        alert('添加推广成功')
      } catch (error) {
        console.error('添加推广失败:', error)
        this.errorMessage = '添加推广失败，请稍后再试'
      }
    },

    // 取消推广
    async removePromotion(gameId) {
      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        await DataService.delete('/vendor/promoted_game/delete', {
          data: {
            game_id: gameId,
            vendor_id: vendorId,
            vendor_type: vendorType,
          },
        })

        await this.fetchPromotedImages()
        alert('取消推广成功')
      } catch (error) {
        console.error('取消推广失败:', error)
        this.errorMessage = '取消推广失败，请稍后再试'
      }
    },

    // 根据游戏ID搜索游戏
    async searchGameById() {
      if (!this.newGameId) {
        alert('请输入游戏ID')
        return
      }

      try {
        const response = await DataService.get('/games/read/search', {
          params: {
            game_id: this.newGameId,
          },
        })

        console.log(response.data.data.gameTitle)
        if (response.data.data) {
          this.foundGame = response.data.data
        } else {
          this.foundGame = null
          alert('未找到该游戏')
        }
      } catch (error) {
        console.error('搜索游戏失败:', error)
        this.foundGame = null
        this.errorMessage = '搜索游戏失败，请稍后再试'
      }
    },
  },
  mounted() {
    this.fetchPromotedImages()
  },
}
</script>

<style scoped>
.promoted-games-container {
  padding: 20px;
  background-color: var(--primary-color);
  border-radius: 8px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--contrast-color);
}

.promoted-images {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.promoted-image-item {
  width: 180px;
  background-color: var(--secondary-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.promoted-game-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.game-info {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-name {
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.remove-promotion-btn {
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

.remove-promotion-btn:hover {
  background-color: #ff5252;
}

.add-promotion-area {
  width: 100%;
  background-color: var(--primary-color);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px var(--secondary-color);
}

.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.game-id-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-game-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
}

.search-game-btn:hover {
  background-color: #45a049;
}

.found-game-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.add-promotion-btn {
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

.add-promotion-btn:hover {
  background-color: #0b7dda;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error-message {
  color: var(--contrast-color);
  text-align: center;
  padding: 10px;
  background-color: #f2314e;
  border-radius: 4px;
  margin-top: 10px;
}
</style>
