<template>
  <div class="content-matrix">
    <table>
      <thead>
        <tr>
          <th v-if="!interactable">游戏ID</th>
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
          <th v-if="interactable">关注</th>
          <th v-if="interactable">不喜欢</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(game, index) in currentGames" :key="index">
          <td v-if="!interactable">{{ game.id }}</td>
          <td>
            <!-- 游戏图片 -->
            <img
              id="game-img"
              :src="game.previewImage"
              alt="游戏图片"
              style="max-width: 100px; max-height: 100px"
            />
          </td>
          <td>
            <!-- 游戏名称作为链接 -->
            <a href="#" @click.prevent="handleGameTitleClick(game)">
              {{ game.gameTitle || '暂无' }}
            </a>
          </td>
          <td>{{ game.gameGenre || '暂无' }}</td>
          <td>{{ game.gamePlatform || '暂无' }}</td>
          <td>
            <a
              href="#"
              @click.prevent="
                handleVendorLinkClick('developer', game.gameDeveloperID, game.gameDeveloper)
              "
            >
              {{ game.gameDeveloper || '暂无' }}
            </a>
          </td>
          <td>
            <a
              href="#"
              @click.prevent="
                handleVendorLinkClick('publisher', game.gamePublisherID, game.gamePublisher)
              "
            >
              {{ game.gamePublisher || '暂无' }}
            </a>
          </td>
          <td>{{ game.followers || 0 }}</td>
          <td>{{ game.rating || 0 }}</td>
          <td>{{ game.ratingPhrase || '暂无' }}</td>
          <td>
            {{ game.releaseYear + '-' + game.releaseMonth + '-' + game.releaseDay || '暂无' }}
          </td>
          <td v-if="interactable">
            <!-- 订阅按钮 -->
            <button class="subscribed-btn" @click="toggleSubscribe(game)">
              {{ game.isSubscribed ? '&#128149;' : '&#10084;' }}
            </button>
          </td>
          <td v-if="interactable">
            <!-- 不喜欢按钮 -->
            <button class="dislike-btn" @click="toggleDislike(game)">
              {{ game.isDisliked ? '&#128545;' : '&#128533;' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button id="page-btn" @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <button
        id="page-btn"
        v-for="page in visiblePagesIndex"
        :key="page"
        @click="goToPage(page)"
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
      <button id="page-btn" @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </div>

  <!-- 游戏详情弹出层 -->
  <GameDetail :showDetail="showDetail" :gameDetail="selectedGame" @close-detail="closeDetail" />

  <!-- 厂商信息弹出层 -->
  <VendorHomePage
    v-if="showVendorPage"
    :vendor_id_prop="selectedVendorId"
    :vendor_name_prop="selectedVendorName"
    :vendor_type_prop="selectedVendroType"
    :onPriview="true"
    @close-vendor-page="closeVendorPage"
  />
</template>

<script>
import DataService from '../services/DataService.js'
import store from '@/services/Store.js'
import GameDetail from './GameDetail.vue'
import VendorHomePage from './VendorHomePage.vue'

export default {
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
    interactable: {
      type: Boolean,
      required: false,
      default: true,
    },
    vendorID: {
      required: false,
      default: null,
    },
  },
  components: {
    GameDetail,
    VendorHomePage,
  },
  data() {
    return {
      games: [],
      currentGames: [],
      currentPage: 1,
      totalPages: 1,
      maxPaginationIndex: 5,
      showDetail: false,
      showVendorPage: false,
      //showgameprops
      selectedGame: null,
      //showvendorprops
      selectedVendorId: undefined,
      selectedVendorName: undefined,
      selectedVendroType: undefined,
    }
  },
  created() {
    this.fetchGames()
  },
  watch: {
    activeMainContent(newVal) {
      if (newVal) {
        this.currentPage = 1
        this.fetchGames()
      }
    },
    currentPage() {
      this.fetchGames()
    },
  },
  methods: {
    handleVendorLinkClick(type, id, name) {
      console.log('点击厂商:' + type + ' 名称:' + name + ' id:' + id)
      if (type === undefined || name === undefined) return

      this.selectedVendorId = id
      this.selectedVendorName = name
      this.selectedVendroType = type

      this.showVendorPage = true
    },
    closeVendorPage() {
      console.log('关闭厂商窗口')
      this.selectedVendorId = undefined
      this.selectedVendorName = undefined
      this.selectedVendroType = undefined

      this.showVendorPage = false
    },
    async handleGameTitleClick(game) {
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked, true)
      this.showGameDetail(game)
      console.log('Game title clicked:', game)
    },
    async toggleSubscribe(game) {
      if (game.isDisliked) {
        game.isDisliked = false
      }
      game.isSubscribed = !game.isSubscribed
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked)
      this.fetchGames()
    },
    async toggleDislike(game) {
      if (game.isSubscribed) {
        // 如果之前点了订阅，先取消订阅
        game.isSubscribed = false
      }
      game.isDisliked = !game.isDisliked
      await this.updateInteraction(game, game.isSubscribed, game.isDisliked)
      this.fetchGames()
    },
    // 更新后端交互状态
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
        // 如果更新失败，恢复本地状态
        game.isSubscribed = oldSubscribed
        game.isDisliked = oldDisliked
        game.clicked = oldClicked
      }
    },
    async fetchGames() {
      try {
        let url = ''
        let params = {
          page_id: this.currentPage,
          itemPerpage: store.state.preference.itemPerpage,
          user_id: store.state.user.userID,
          developer_id: this.vendorID,
        }

        console.log('参数params' + params.developer_id)

        switch (this.activeMainContent) {
          case '关注':
            url = '/games/read/subscribed/page/' + this.currentPage
            break
          case '最高评分':
            url = '/games/read/top_rated/page/' + this.currentPage
            break
          case '最受欢迎':
            url = '/games/read/top_subscribed/page/' + this.currentPage
            break
          case '最新上架':
            url = '/games/read/recently/page/' + this.currentPage
            break
          case 'vendor':
            url = 'games/read/by_developer/page/' + this.currentPage
            break
          default:
            url = `/games/read/page/${this.currentPage}`
            params.type = this.activeMainContent
            break
        }

        const response = await DataService.get(url, { params })
        const responseData = response.data

        // 获取每页的游戏数据
        console.log('Response Data:', responseData)
        const games = responseData.data.games.map((game) => ({
          ...game,
          isSubscribed: game.subscribed,
          isDisliked: game.disliked,
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
        this.totalPages = responseData.data.totalPages
      } catch (error) {
        console.error('获取游戏数据失败:', error)
        alert('获取游戏数据失败')
      }
    },
    updateCurrentGames() {
      const start = (this.currentPage - 1) * this.itemPerpage
      const end = start + this.itemsPerPage
      this.currentGames = this.games.slice(start, end)
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.fetchGames()
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.fetchGames()
      }
    },
    goToPage(page) {
      if (page !== this.currentPage && page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.fetchGames()
      }
    },
    showGameDetail(game) {
      this.selectedGame = game
      this.showDetail = true
    },
    closeDetail() {
      console.log('close detail')
      this.showDetail = false
      this.selectedGame = null
    },
  },
  computed: {
    getSubscription(newVal) {
      if (newVal === 'subscription') return '&#10084;'
      else return '&#128149'
    },
    getDislike(newVal) {
      if (newVal === 'subscription') return '&#128533;'
      else return '&#128545'
    },
    visiblePagesIndex() {
      const maxPagesToShow = 5
      const pages = []

      // 如果总页数小于等于最大显示页数，直接返回所有页码
      if (this.totalPages <= maxPagesToShow) {
        return Array.from({ length: this.totalPages }, (_, index) => index + 1)
      }

      // 计算当前页码周围的页码范围
      const halfMaxPages = Math.floor(maxPagesToShow / 2)
      let startPage = this.currentPage - halfMaxPages
      let endPage = this.currentPage + halfMaxPages

      // 调整起始页和结束页，确保不超出范围
      if (startPage < 1) {
        startPage = 1
        endPage = startPage + maxPagesToShow - 1
      }
      if (endPage > this.totalPages) {
        endPage = this.totalPages
        startPage = endPage - maxPagesToShow + 1
      }

      // 生成显示的页码数组
      for (let page = startPage; page <= endPage; page++) {
        pages.push(page)
      }
      return pages
    },
  },
}
</script>

<style scoped>
#page-btn,
#game-img {
  border-radius: 10px;
}

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
  text-align: center;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 10px;
  border: solid 2px var(--contrasr-color);
  margin: 0 auto;
}

tbody {
  border-top: 3px solid var(--secondary-color);
  border-bottom: 3px solid var(--secondary-color);
  margin: 10px 0;
}

table tr th:first-child,
table tr td:first-child {
  border-left: 2px solid var(--primary-color); /* 给table设置左边框 */
}
table tr th:last-child,
table tr td:last-child {
  border-right: 2px solid var(--primary-color); /* 给table设置右边框 */
}
table tr:first-child th:first-child {
  border-top-left-radius: 10px; /* 设置table左上圆角 */
}
table tr:first-child th:last-child {
  border-top-right-radius: 10px; /* 设置table右上圆角 */
}
table tr:last-child td:first-child {
  border-bottom-left-radius: 10px; /* 设置table左下圆角 */
}
table tr:last-child td:last-child {
  border-bottom-right-radius: 10px; /* 设置table右下圆角 */
}
th,
td {
  padding: 12px;
  text-align: left;
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
