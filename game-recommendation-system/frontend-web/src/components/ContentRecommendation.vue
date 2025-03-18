<template>
  <h2 v-if="msg != ''">{{ msg }}</h2>
  <div class="content-matrix">
    <table>
      <thead>
        <tr>
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
</template>

<script>
import DataService from '../services/DataService.js'
import store from '@/services/Store.js'

export default {
  data() {
    return {
      currentGames: [],
      msg: '',
    }
  },
  created() {
    this.fetchRecommendations()
  },
  methods: {
    async handleGameTitleClick(game) {
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked, true)
      console.log('Game title clicked:', game)
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
        const response = await DataService.post('/interactions/update', {
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
        this.currentGames = response.data.recommendations.map((game) => ({
          ...game,
          isSubscribed: false,
          isDisliked: false,
        }))
        console.log('获取推荐数据成功:', response.data)
      } catch (error) {
        console.error('获取推荐数据失败:', error)
        alert('获取推荐数据失败')
      }
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
