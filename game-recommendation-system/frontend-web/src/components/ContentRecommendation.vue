<template>
  <h2 v-if="msg != ''">{{ msg }}</h2>
  <div class="content-matrix">
    <table>
      <thead>
        <tr>
          <th>游戏图片</th>
          <th>游戏名称</th>
          <th>游戏类型</th>
          <th>游戏平台</th>
          <th>游戏开发商</th>
          <th>游戏发行商</th>
          <th>游戏关注数</th>
          <th>评分</th>
          <th>评分描述</th>
          <th>发行日期</th>
          <th>关注</th>
          <th>不喜欢</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(game, index) in currentGames" :key="index">
          <td>
            <!-- 游戏图片 -->
            <img
              :src="game.previewImage"
              alt="游戏图片"
              style="max-width: 100px; max-height: 100px"
            />
          </td>
          <td>
            <a href="#" @click.prevent="handleGameTitleClick(game)">
              {{ game.gameTitle || '暂无' }}
            </a>
          </td>
          <td>{{ game.gameGenre || '暂无' }}</td>
          <td>{{ game.gamePlatform || '暂无' }}</td>
          <td>{{ game.gameDeveloper || '暂无' }}</td>
          <td>{{ game.gamePublisher || '暂无' }}</td>
          <td>{{ game.followers || 0 }}</td>
          <td>{{ game.rating || 0 }}</td>
          <td>{{ game.ratingPhrase || '暂无' }}</td>
          <td>
            {{ game.releaseYear + '-' + game.releaseMonth + '-' + game.releaseDay || '暂无' }}
          </td>
          <td>
            <button class="subscribed-btn" @click="toggleSubscribe(game)">
              {{ game.isSubscribed ? '&#128149;' : '&#10084;' }}
            </button>
          </td>
          <td>
            <button class="dislike-btn" @click="toggleDislike(game)">
              {{ game.isDisliked ? '&#128545;' : '&#128533;' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- 游戏详情弹出层 -->
  <GameDetail :showDetail="showDetail" :gameDetail="selectedGame" @close-detail="closeDetail" />
</template>

<script>
import DataService from '../services/DataService.js'
import store from '@/services/Store.js'
import GameDetail from './GameDetail.vue'

export default {
  data() {
    return {
      currentGames: [],
      msg: '',
      showDetail: false,
      selectedGame: null,
    }
  },
  components: {
    GameDetail,
  },
  created() {
    this.fetchRecommendations()
  },
  methods: {
    async handleGameTitleClick(game) {
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked, true)
      this.showGameDetail(game)
    },
    async toggleSubscribe(game) {
      if (game.isDisliked) {
        game.isDisliked = false
      }
      game.isSubscribed = !game.isSubscribed
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked)
      this.fetchRecommendations()
    },
    async toggleDislike(game) {
      if (game.isSubscribed) {
        game.isSubscribed = false
      }
      game.isDisliked = !game.isDisliked
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked)
      this.fetchRecommendations()
    },
    async updateInteraction(game, newSubscribed, newDisliked, newClicked) {
      var oldSubscribed = game.isSubscribed
      var oldDisliked = game.isDisliked
      var oldClicked = game.clicked
      try {
        const response = await DataService.put('/interactions/update', {
          user_id: store.state.user.userID,
          game_id: game.id,
          subscribed: newSubscribed,
          disliked: newDisliked,
          clicked: newClicked,
        })
        console.log('交互更新成功:', response)
      } catch (error) {
        console.error('交互更新失败:', error)
        game.isSubscribed = oldSubscribed
        game.isDisliked = oldDisliked
        game.clicked = oldClicked
      }
    },
    async fetchRecommendations() {
      try {
        console.log('获取推荐数据中...')
        const response = await DataService.get('/recommendations/read', {
          params: {
            user_id: store.state.user.userID,
          },
        })
        this.msg = response.data.msg

        // 获取推荐的游戏数据
        const games = response.data.recommendations.map((game) => ({
          ...game,
          isSubscribed: false,
          isDisliked: false,
          previewImage: '', // 用于存储预览图片的 URL
        }))

        // 为每个游戏获取预览图片
        const gamePromises = games.map(async (game) => {
          try {
            // 调用接口获取预览图片
            const imageResponse = await DataService.get(`/games/preview_image/read/${game.id}`, {
              responseType: 'blob', // 指定响应类型为 blob
            })

            // 创建图片的 URL
            game.previewImage = URL.createObjectURL(imageResponse.data)
          } catch (error) {
            console.error(`获取游戏 ${game.id} 的预览图片失败:`, error)
            game.previewImage = 'defaultGameImage.jpg' // 默认图片
          }
          return game
        })

        // 等待所有游戏的图片加载完成
        this.currentGames = await Promise.all(gamePromises)
        console.log('获取推荐数据成功:', response.data)
      } catch (error) {
        console.error('获取推荐数据失败:', error)
        alert('获取推荐数据失败')
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
.subscribed-btn,
.dislike-btn {
  width: 30px;
  background-color: #00000000;
  border-radius: 25%;
  border-style: dashed;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  margin: 0 5px;
  padding: 5px 10px;
  cursor: pointer;
}

.pagination button.active {
  background-color: var(--main-color);
  color: white;
  border: none;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.content-matrix {
  background-color: var(--background-color);
  color: var(--contrast-color);
  padding: 20px;
  border-radius: 5px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 auto;
}

tbody {
  border-top: 5px solid var(--secondary-color);
  border-bottom: 1px solid var(--secondary-color);
  margin: 10px 0;
}

th,
td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--secondary-color);
  border-radius: 5px;
}

th {
  background-color: var(--main-color);
}

tr {
  background-color: var(--secondary-color);
  box-shadow: 0 0 5px var(--primary-color);
  margin: 10px 0;
}

tr:hover {
  background-color: var(--primary-color);
}

tr:nth-child(odd) {
  background-color: var(--secondary-color-light);
  color: var(--contrasr-color);
}

tr:nth-child(odd):hover {
  background-color: var(--primary-color);
  color: var(--contrasr-color);
}

a {
  color: var(--main-color);
}
</style>
