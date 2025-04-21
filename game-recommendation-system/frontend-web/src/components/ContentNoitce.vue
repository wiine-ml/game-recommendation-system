<template>
  <div class="content-list">
    <ul>
      <li v-for="(item, index) in currentNotices" :key="index" class="content-item">
        <div class="header">
          <div class="avatar">
            <img src="/defaultUserImg.jpg" alt="/public/guest.jpg" />
          </div>
          <div class="username">{{ item.username }}</div>
        </div>
        <div class="title">{{ item.title }}</div>
        <div class="content-excerpt">{{ item.content }}</div>
        <div class="date">{{ item.date }}</div>
        <hr />
      </li>
    </ul>

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
</template>

<script>
import DataService from '@/services/DataService'
import store from '@/services/Store.js'

export default {
  props: {
    activeMainContent: {
      type: String,
    },
  },
  data() {
    return {
      notices: [],
      currentNotices: [],
      currentPage: 1,
      totalPages: 1,
      maxPaginationIndex: 5,
    }
  },
  created() {
    this.fetchNotice()
  },
  watch: {
    activeMainContent(newVal) {
      if (newVal) {
        this.currentPage = 1
        this.fetchNotice()
      }
    },
    currentPage() {
      this.fetchNotice()
    },
  },
  methods: {
    async fetchNotice() {
      this.isLoading = true
      try {
        const response = await DataService.get(`/notice/read/page/${this.currentPage}`, {
          params: {
            type: this.activeMainContent,
            itemPerpage: store.state.preference.itemPerpage,
          },
        })
        this.notices = response.data.data.notices
        this.totalPages = response.data.data.totalPages
        this.currentNotices = this.notices
        console.log('获取公告数据成功>>> ', response.data)
      } catch (error) {
        console.error('获取公告数据失败>>> ', error)
      } finally {
        this.isLoading = false
      }
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
hr {
  margin: 0px 20px;
}

#page-btn {
  border-radius: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 15px;
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

.content-list {
  height: 100%;
  overflow: auto;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.content-item {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  position: relative;
  word-break: break-all;
  overflow: hidden;
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
  color: #bbb;
  flex: 1;
  margin-bottom: 2rem;
  overflow-wrap: break-word;
}
.date {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  color: #999;
}
</style>
