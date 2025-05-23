<template>
  <div class="control-panel">
    <el-button type="info" @click.prevent="fetchAllReviews" round>刷新</el-button>
    <el-button type="primary" @click.prevent="addReviewBtn" round>{{ addReviewText }}</el-button>
    <el-button type="primary" @click.prevent="deleteReviewBtn" round>{{ delReviewText }}</el-button>
    <el-button type="danger" @click.prevent="deleteConfirmBtn" v-if="isDeleting" round
      >删除</el-button
    >
  </div>

  <div v-if="isAdding">
    <hr />

    <label>游戏ID</label>
    <input
      v-model="newReview.game_id"
      type="number"
      placeholder="游戏ID"
      @input="fetchGameInfo"
      @wheel="fetchGameInfo"
    />

    <input
      class="game-name-tip"
      type="text"
      placeholder="游戏名称"
      readonly
      :value="newReview.game_title"
      @click.prevent
      style="
        background-color: var(--primary-color-alpha2);
        width: fit-content;
        :focus {
          border: 0;
          outline: none;
        }
      "
    />

    <label>评分</label>
    <input
      v-model="newReview.rating"
      type="number"
      placeholder="评分"
      step="0.5"
      min="0.5"
      max="5"
      @wheel.prevent
    />

    <label>评论内容</label>
    <input v-model="newReview.comment" type="text" placeholder="评论内容" style="width: 30%" />

    <el-button type="success" @click="submitReview" round>添加评论</el-button>
  </div>

  <hr />

  <div class="content-list">
    <table>
      <thead>
        <tr>
          <th>游戏id</th>
          <th>游戏名称</th>
          <th>评分</th>
          <th>评论</th>
          <th v-if="isDeleting">删除</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(review, index) in reviews" :key="index">
          <!--<td>{{ review.id }}</td>-->
          <td>{{ review.game_id || '数据错误' }}</td>
          <td>{{ review.game_title || '数据错误' }}</td>
          <td @dblclick="editField(review, 'rating')" contenteditable="false">
            <input
              type="text"
              v-if="review.isEditing && review.editField === 'rating'"
              v-model="review.rating"
              @blur="saveEdit(review)"
            />
            <span v-else>{{ review.review_score || '数据错误' }}</span>
          </td>
          <td @dblclick="editField(review, 'comment')" contenteditable="false">
            <input
              type="text"
              v-if="review.isEditing && review.editField === 'comment'"
              v-model="review.comment"
              @blur="saveEdit(review)"
            />
            <span v-else>{{ review.review_text || '数据错误' }}</span>
          </td>
          <td v-if="isDeleting">
            <input
              type="checkbox"
              @change="handleCheckboxChange(review.game_id, $event.target.checked)"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'
import store from '../services/Store.js'
export default {
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      reviews: [],
      newReview: {
        game_id: null,
        game_title: '',
        rating: 0,
        comment: null,
      },
      isAdding: false,
      isDeleting: false,
      selectedGameIds: [],
    }
  },
  created() {
    this.fetchAllReviews()
  },
  methods: {
    // 添加一个方法来查询游戏信息
    async fetchGameInfo() {
      if (!this.newReview.game_id) {
        this.newReview.game_title = ''
        return
      }

      this.isLoading = true
      try {
        const response = await DataService.get('/games/read/search', {
          params: {
            user_id: store.state.user.userID,
            game_id: this.newReview.game_id,
          },
        })
        if (response.data && response.data.data) {
          this.newReview.game_title = response.data.data.gameTitle
        } else {
          this.newReview.game_title = '游戏未找到'
        }
      } catch (error) {
        console.error('查询游戏信息失败:', error)
        this.newReview.game_title = '查询失败'
      } finally {
        this.isLoading = false
      }
    },
    async fetchAllReviews() {
      this.isLoading = true
      console.log(this.isLoading, store.state.user.userID)
      try {
        const response = await DataService.get('/reviews/read', {
          params: {
            type: this.activeMainContent,
            user_id: store.state.user.userID,
          },
        })
        this.reviews = response.data.reviews
        console.log('获取数据成功:', response.data)
      } catch (error) {
        console.error('获取数据失败:', error)
        alert('获取数据失败')
      } finally {
        this.isLoading = false
      }
    },
    async deleteSingleReview(reviewId) {
      try {
        const response = await DataService.post('/reviews/delete', {
          user_id: store.state.user.userID,
          game_id: reviewId,
        })
        console.log('删除评论成功:', response.data)
        this.fetchAllReviews() // 刷新评论列表
      } catch (error) {
        console.error('删除评论失败:', error)
        alert('删除评论失败')
      }
    },
    async saveEdit(review) {
      // 保存编辑内容到后端
      try {
        const response = await DataService.put('/reviews/update', {
          user_id: store.state.user.userID,
          game_id: review.game_id,
          review_score: review.rating,
          review_text: review.comment,
        })
        console.log('更新评论成功:', response.data)
        this.fetchAllReviews() // 刷新评论列表
      } catch (error) {
        console.error('更新评论失败:', error)
        alert('更新评论失败')
      } finally {
        review.isEditing = false
        review.editField = null
      }
    },
    async submitReview() {
      if (!this.newReview.game_id) {
        alert('请填写游戏ID')
        return
      }
      if (!this.newReview.rating) {
        alert('请填写评分')
        return
      }
      if (this.newReview.rating <= 0 || this.newReview.rating > 5) {
        alert('评分范围为0.5-5')
        return
      }
      if (!this.newReview.comment) {
        alert('请填写评论内容')
        return
      }
      console.log(store.getters.userID, this.rating, this.comment)
      DataService.post('/reviews/create', {
        user_id: store.state.user.userID,
        game_id: this.newReview.game_id,
        review_score: this.newReview.rating,
        review_text: this.newReview.comment,
      })
        .then((response) => {
          console.log('添加评论成功:', response.data)
          this.reviews.push(response.data.review)
          this.newReview = {
            game_id: null,
            rating: null,
            comment: null,
          }
          this.isAdding = false
          this.fetchAllReviews() // 刷新评论列表
        })
        .catch((error) => {
          if (error.response.data.message === '用户已经对该游戏进行过评论') {
            alert('你已经评价过这个游戏了！')
            return
          }
          console.error('添加评论失败:', error)
          alert('添加评论失败')
        })
    },
    // 添加一个方法来处理复选框的变化
    handleCheckboxChange(gameId, isChecked) {
      if (isChecked) {
        this.selectedGameIds.push(gameId)
      } else {
        const index = this.selectedGameIds.indexOf(gameId)
        if (index > -1) {
          this.selectedGameIds.splice(index, 1)
        }
      }
    },
    deleteConfirmBtn() {
      if (this.selectedGameIds.length === 0) {
        alert('请选择要删除的评论')
        return
      }
      // 遍历选中的游戏ID，逐个删除评论
      const promises = this.selectedGameIds.map((gameId) => {
        return DataService.delete(`/reviews/delete/${gameId}`, {
          data: {
            user_id: this.$store.getters['user/userID'],
          },
        })
      })

      Promise.all(promises)
        .then((responses) => {
          console.log('删除评论成功:', responses)
          this.fetchAllReviews() // 刷新评论列表
          this.isDeleting = false
          this.selectedGameIds = []
        })
        .catch((error) => {
          console.error('删除评论失败:', error)
          alert('删除评论失败')
        })
    },
    deleteReviewBtn() {
      this.isDeleting = !this.isDeleting
    },
    editField(review, field) {
      this.reviews.forEach((r) => {
        r.isEditing = false
        r.editField = null
      })
      review.isEditing = true
      review.editField = field
      this.$nextTick(() => {
        const input = event.target.querySelector('input')
        if (input) {
          input.focus()
          input.select()
        }
      })
    },
    addReviewBtn() {
      this.isAdding = !this.isAdding
    },
  },
  computed: {
    addReviewText() {
      return this.isAdding ? '取消' : '添加评论'
    },
    delReviewText() {
      return this.isDeleting ? '取消' : '删除评论'
    },
  },
}
</script>

<style scoped>
input[type='checkbox'] {
  width: 15px;
  height: 15px;
}
input {
  width: 120px;
  height: 40px;
  margin: 5px 10px 5px 5px;
  border-radius: 10px;
  background-color: var(--primary-color);
  text-align: center;
}

.content-list {
  overflow: auto;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 0.5rem;
  object-fit: cover;
}

.username {
  font-weight: bold;
}
.title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}
.content-excerpt {
  color: var(--contrasr-color-alpha2);
  flex: 1;
  margin-bottom: 2rem;
  overflow-wrap: break-word;
}
table {
  width: 100%;
  border-collapse: separate;
  text-align: center;
  border-spacing: 0;
  border-radius: 10px;
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
  transition-property: color, background-color;
  transition-duration: 0.5s;
  box-shadow: 3px 3px 3px 3px var(--primary-color);
}

th {
  background-color: var(--primary-color);
}
tr {
  background-color: var(--secondary-color);
}
td:hover {
  background-color: var(--primary-color);
}
td:nth-child(odd) {
  background-color: var(--secondary-color-light);
}
td:nth-child(odd):hover {
  background-color: var(--primary-color);
}
table tr:first-child,
th:first-child {
  border-top-left-radius: 10px;
}
table tr:first-child,
th:last-child {
  border-top-right-radius: 10px;
}
tr:last-child > td:first-child {
  border-bottom-left-radius: 10px;
}
tr:last-child > td:last-child {
  border-bottom-right-radius: 10px;
}
</style>
