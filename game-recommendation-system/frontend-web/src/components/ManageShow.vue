<template>
  <div class="content-matrix">
    <table v-if="currentData.length > 0">
      <thead>
        <tr>
          <th v-for="(column, index) in columns" :key="index">
            {{ column.label }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(item, index) in currentData" :key="index">
          <td v-for="(column, colIndex) in columns" :key="colIndex">
            <!-- 处理图片列 -->
            <img
              v-if="column.type === 'image'"
              :src="item[column.field]"
              alt="图片"
              :style="column.style || 'width: 40px; height: 40px; border-radius: 50%'"
            />
            <!-- 处理普通文本列 -->
            <span v-else>
              {{ item[column.field] || '暂无' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>暂无数据</div>

    <div class="pagination" v-if="showPagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <button
        v-for="page in visiblePagesIndex"
        :key="page"
        @click="goToPage(page)"
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'

export default {
  props: {
    // 数据类型配置
    activeMainContent: {
      type: String,
      required: true, // 数据类型，如 'notice', 'news', 'game'
    },
    // 每页显示条数
    itemsPerPage: {
      type: Number,
      default: 20,
    },
    // 是否显示分页
    showPagination: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      currentData: [],
      currentPage: 1,
      totalPages: 1,
      maxPaginationIndex: 5,
      // 定义不同类型的数据配置
      dataTypeConfig: {
        查询公告: {
          columns: [
            { field: 'id', label: '公告编号', type: 'text' },
            {
              field: 'avatar',
              label: '头像',
              type: 'image',
              style: 'width: 40px; height: 40px; border-radius: 50%',
            },
            { field: 'username', label: '发布者', type: 'text' },
            { field: 'title', label: '标题', type: 'text' },
            { field: 'content', label: '内容', type: 'text' },
            { field: 'date', label: '发布日期', type: 'text' },
          ],
          path: 'notice',
        },
        查询新闻: {
          columns: [
            { field: 'id', label: '新闻编号', type: 'text' },
            { field: 'type', label: '新闻类型', type: 'text' },
            {
              field: 'image',
              label: '图片',
              type: 'image',
              style: 'width: 60px; height: 40px',
            },
            { field: 'title', label: '标题', type: 'text' },
            { field: 'description', label: '描述', type: 'text' },
            { field: 'date', label: '发布日期', type: 'text' },
          ],
          path: 'news',
        },
        查询游戏: {
          columns: [
            { field: 'id', label: '游戏编号', type: 'text' },
            { field: 'gameTitle', label: '游戏名称', type: 'text' },
            { field: 'gameGenre', label: '游戏类型', type: 'text' },
            { field: 'gamePlatform', label: '游戏平台', type: 'text' },
            { field: 'releaseYear', label: '发行年份', type: 'text' },
            { field: 'releaseMonth', label: '发行月份', type: 'text' },
            { field: 'releaseDay', label: '发行日期', type: 'text' },
            { field: 'follwers', label: '关注数', type: 'text' },
            { field: 'rating', label: '评分值', type: 'text' },
            { field: 'ratingPhrase', label: '评分描述', type: 'text' },
          ],
          path: 'games',
        },
        查询用户: {
          columns: [
            { field: 'id', label: '用户编号', type: 'text' },
            { field: 'email', label: '邮箱', type: 'text' },
            { field: 'username', label: '用户名', type: 'text' },
            {
              field: 'avatar',
              label: '头像',
              type: 'image',
              style: 'width: 40px; height: 40px; border-radius: 50%',
            },
            { field: 'subscribed_count', label: '关注数', type: 'text' },
            { field: 'review_count', label: '评论数', type: 'text' },
          ],
          path: 'users',
        },
        查询管理员: {
          columns: [
            { field: 'id', label: '管理员编号', type: 'text' },
            { field: 'admin_type', label: '管理员类型', type: 'text' },
            { field: 'admin_name', label: '管理员名称', type: 'text' },
          ],
          path: 'admin',
        },
      },
    }
  },
  created() {
    this.fetchData()
  },
  watch: {
    currentPage() {
      this.fetchData()
    },
    itemsPerPage() {
      this.currentPage = 1
      this.fetchData()
    },
    activeMainContent() {
      this.currentPage = 1
      this.fetchData()
    },
  },
  methods: {
    async fetchData() {
      try {
        // 获取当前数据类型的配置
        const config = this.dataTypeConfig[this.activeMainContent]
        if (!config) {
          console.error(`未知的数据类型: ${this.activeMainContent}`)
          return
        }
        let path = '/' + config.path + '/read/page/' + this.currentPage
        const params = {
          itemPerpage: this.itemsPerPage,
          type: this.activeMainContent,
        }
        const response = await DataService.get(path, { params })
        console.log(`获取${this.activeMainContent}数据成功:`, response)

        // 格式化数据
        if (this.activeMainContent === '查询游戏') {
          this.currentData = response.data.data.games.map((item) => {
            return this.formatData(item)
          })
        } else if (this.activeMainContent === '查询新闻') {
          this.currentData = response.data.data.map((item) => {
            return this.formatData(item)
          })
        }

        this.totalPages = response.data.totalPages
      } catch (error) {
        console.error(`获取${this.activeMainContent}数据失败:`, error)
        alert(`获取${this.activeMainContent}数据失败`)
      }
    },
    // 格式化数据
    formatData(item) {
      // 如果需要对数据进行特殊处理，可以在这里实现
      // 例如日期格式化、图片路径处理等
      return item
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    },
    goToPage(page) {
      if (page !== this.currentPage && page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
  },
  computed: {
    columns() {
      // 获取当前数据类型的列配置
      return this.dataTypeConfig[this.activeMainContent]?.columns || []
    },
    visiblePagesIndex() {
      const maxPagesToShow = 5
      const pages = []

      if (this.totalPages <= maxPagesToShow) {
        return Array.from({ length: this.totalPages }, (_, index) => index + 1)
      }

      const halfMaxPages = Math.floor(maxPagesToShow / 2)
      let startPage = this.currentPage - halfMaxPages
      let endPage = this.currentPage + halfMaxPages

      if (startPage < 1) {
        startPage = 1
        endPage = startPage + maxPagesToShow - 1
      }
      if (endPage > this.totalPages) {
        endPage = this.totalPages
        startPage = endPage - maxPagesToShow + 1
      }

      for (let page = startPage; page <= endPage; page++) {
        pages.push(page)
      }
      return pages
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
