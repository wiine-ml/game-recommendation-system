<template>
  <nav class="navbar">
    <div class="navbar-state">
      <img src="/favicon.ico" alt="Logo" />
    </div>

    <div class="navbar-avatar">
      <p v-if="isLogin">{{ welcomeMessage }}</p>
      <p v-else>暂未登录</p>
      <!-- 邮件按钮，点击后显示 MailBox -->
      <button id="mail-btn" @click="toggleMailBox" class="mail-button">✉️</button>
      <UserInfoDetail v-if="isLogin" />
    </div>
  </nav>
  <nav class="navbar-navigations">
    <!-- 管理员导航栏 -->
    <div class="navbar-bottom-left" v-if="this.$store.getters.currentLoginType === 'admin'">
      <a href="#公告管理" @click="selectMenu('公告管理')">公告管理</a>
      <a href="#推荐管理" @click="selectMenu('推荐管理')">推荐管理</a>
      <a href="#新闻管理" @click="selectMenu('新闻管理')">新闻管理</a>
      <a href="#游戏管理" @click="selectMenu('游戏管理')">游戏管理</a>
      <a href="#用户管理" @click="selectMenu('用户管理')">用户管理</a>
      <a
        href="#"
        @click="selectMenu('管理员管理')"
        v-if="this.$store.getters.currentLoginType === 'superAdmin'"
      >
        管理员管理</a
      >
    </div>

    <!-- 开发商 or 发行商导航栏 -->
    <div
      class="navbar-bottom-left"
      v-else-if="
        this.$store.getters.currentLoginType === 'developer' ||
        this.$store.getters.currentLoginType === 'publisher'
      "
    >
      <a href="#主页管理" @click="selectMenu('主页管理')">主页管理</a>
      <a href="#厂商游戏管理" @click="selectMenu('厂商游戏管理')"
        >{{ this.$store.getters['vendor/vendorName'] }}游戏管理</a
      >
      <a href="#厂商新闻管理" @click="selectMenu('厂商新闻管理')"
        >{{ this.$store.getters['vendor/vendorName'] }}新闻管理</a
      >
    </div>
    <!-- 用户导航栏 -->
    <div class="navbar-bottom-left" v-else>
      <a href="#首页" @click="selectMenu('首页')">首页</a>
      <a href="#推荐" @click="selectMenu('推荐')">推荐</a>
      <a href="#类别" @click="selectMenu('类别')">类别</a>
      <a href="#新闻" @click="selectMenu('新闻')">新闻</a>
      <a href="#我的" @click="selectMenu('我的')">我的</a>
    </div>

    <div class="navbar-search">
      <div class="search-container" v-if="this.$store.getters.currentLoginType === 'user'">
        <input
          type="text"
          placeholder="Search..."
          v-model="searchQuery"
          @input="debounceFetchSuggestions"
          @keydown.enter="performSearch"
        />
        <button id="cleanBtn" @click="cleanSearch">&#10006;</button>
        <button id="searchBtn" @click="performSearch">搜索</button>
        <!-- 搜索提示 -->
        <div class="search-suggestions" v-if="onSearchComplete">
          <ul>
            <li
              v-for="(suggestion, index) in searchSuggestions"
              :key="index"
              @click="selectSuggestion(suggestion)"
            >
              {{ suggestion }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <GameDetail :showDetail="showDetail" :gameDetail="selectedGame" @close-detail="closeDetail" />
  <MailBox :showMailBox="showMailBox" @close="closeMailBox" />
</template>

<script>
import store from '../services/Store.js'
import UserInfoDetail from './UserInfoDetail.vue'
import DataService from '../services/DataService.js'
import GameDetail from './GameDetail.vue'
import MailBox from './MailBox.vue'

export default {
  components: {
    UserInfoDetail,
    GameDetail,
    MailBox,
  },
  emits: ['updataSubMenu'],
  data() {
    return {
      searchQuery: '',
      searchSuggestions: [],
      debounceTimer: null,
      showDetail: false,
      selectedGame: null,
      showMailBox: false, // 控制 MailBox 的显示
    }
  },
  methods: {
    cleanSearch() {
      this.searchQuery = ''
      this.searchSuggestions = []
    },
    selectMenu(menu) {
      this.$emit('updataSubMenu', menu)
    },
    // 获取搜索提示
    debounceFetchSuggestions() {
      // 清除之前的定时器
      if (this.debounceTimer) {
        clearTimeout(this.debounceTimer)
      }
      // 设置新的定时器，延迟0.5秒后发送请求
      this.debounceTimer = setTimeout(this.fetchSearchSuggestions, 500)
    },
    async fetchSearchSuggestions() {
      if (this.searchQuery.length < 1) {
        this.searchSuggestions = []
        return
      }
      try {
        const response = await DataService.post('/autocomplete/' + this.searchQuery, {
          limit: 5,
        })
        this.searchSuggestions = response.data.data.result_games
        console.log('resp:', this.searchSuggestions)
      } catch (error) {
        console.error('搜索提示获取失败:', error)
      }
    },
    // 执行搜索
    async performSearch() {
      if (this.searchQuery.trim().length > 0) {
        try {
          const response = await DataService.get(
            `/games/read/search/${encodeURIComponent(this.searchQuery)}`,
          )
          if (response.data.success) {
            this.selectedGame = response.data.data
            this.showDetail = true
          } else {
            console.log('游戏未找到')
          }
        } catch (error) {
          console.error('搜索失败:', error)
        }
      }
    },
    // 选择搜索提示
    selectSuggestion(suggestion) {
      this.searchQuery = suggestion
      this.searchSuggestions = []
      this.performSearch()
    },
    closeDetail() {
      this.showDetail = false
    },
    toggleMailBox() {
      this.showMailBox = !this.showMailBox
    },
    openMailBox() {
      this.$refs.mailBox.openMailBox()
    },
    closeMailBox() {
      this.showMailBox = false
    },
  },
  computed: {
    isLogin() {
      return store.getters.isLogin
    },
    welcomeMessage() {
      if (this.$store.getters.currentLoginType === 'user') {
        return '欢迎用户 - ' + this.$store.getters['user/userName']
      } else if (this.$store.getters.currentLoginType === 'admin') {
        return '欢迎管理员 - ' + this.$store.getters['admin/adminName']
      } else if (this.$store.getters.currentLoginType === 'superAdmin') {
        return '欢迎 超级管理员'
      } else if (this.$store.getters.currentLoginType === 'developer') {
        return '欢迎登陆' + this.$store.getters['vendor/vendorName']
      } else if (this.$store.getters.currentLoginType === 'publisher') {
        return '欢迎登陆' + this.$store.getters['vendor/vendorName']
      } else {
        console.error('Unknown login type')
      }
      return ''
    },
    onSearchComplete() {
      console.log('searchQuery:', this.searchQuery.length)
      console.log('suggestions:', this.searchSuggestions.length)
      return this.searchSuggestions.length > 0 && this.searchQuery.length > 0
    },
  },
  mounted() {
    console.log(store.getters.currentLoginType)
  },
}
</script>

<style scoped>
#mail-btn {
  margin-top: 0;
  margin-bottom: 0;
  padding-top: 0;
  padding-bottom: 0;
  background-color: var(--background-color);
  border-radius: 10px;
  font-size: 30px;
  width: 60px;
  height: 35px;
  margin-right: 15px;
  margin-left: 15px;
  border: 0px;
  cursor: pointer;
}

/* 添加搜索提示的样式 */
.search-suggestions {
  position: absolute;
  top: 100%;
  background-color: var(--primary-color);
  border: 1px solid var(--secondary-color);
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
}

.search-suggestions ul {
  display: flex;
  flex-direction: column;
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-suggestions li {
  padding: 8px 12px;
  cursor: pointer;
}

.search-suggestions li:hover {
  background-color: var(--secondary-color);
}

.search-container {
  position: relative;
}
/*其他 */
body {
  margin: 0;
  padding: 0;
  color: var(--main-color);
  font-family: Arial, sans-serif;
}
.navbar {
  background-color: var(--primary-color);
  color: var(--contrast-color);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
}
.navbar-state {
  color: var(--main-color);
}
.navbar-logo {
  display: flex;
  align-items: center;
}
.navbar-logo a {
  color: var(--main-color);
  text-decoration: none;
  font-weight: bold;
  font-size: 1.5rem;
}
li {
  list-style: none;
  float: left;
}
.navbar-avatar {
  display: flex;
  align-items: flex-end;
}
.navbar-avatar img {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  box-shadow: 0 0 30px var(--secondary-color);
}
.navbar-navigations {
  background-color: var(--secondary-color);
  color: var(--contrast-color);
  padding: 0.5rem 2rem;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 90% auto;
  border-radius: 5px;
  box-shadow: 0 0 5px var(--secondary-color);
}
.navbar-bottom-left {
  display: flex;
  align-items: center;
}
.navbar-bottom-left a {
  color: var(--main-color);
  text-decoration: none;
  border-radius: 5px;
  padding: 0.5rem;
  margin-left: 1rem;
  cursor: pointer;
}
.navbar-bottom-left a:hover {
  background-color: var(--main-color);
  color: var(--contrast-color);
  font-weight: bold;
  box-shadow: 0 0 5px var(--main-color);
}

#searchBtn {
  padding: 0.5rem;
  width: 80px;
  height: 30px;
  background: var(--main-color-alpha1);
  color: var(--contrast-color);
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  box-shadow: 0 0 10px var(--primary-color);
}

#cleanBtn {
  padding: 0.5rem;
  width: 50px;
  height: 30px;
  background: linear-gradient(to right, var(--primary-color-alpha2) 1%, var(--main-color) 99%);
  color: #000;
  border: none;
  cursor: pointer;
  box-shadow: 0 0 10px var(--primary-color);
}

.search-container {
  display: flex;
  align-items: center;
}
.navbar-search {
  margin-left: 50px;
  display: flex;
  align-items: center;
}
.navbar-search input[type='text'] {
  padding: 0.5rem;
  border: none;
  border-radius: 5px 0 0 5px;
}
</style>
