<template>
  <nav class="navbar">
    <div class="navbar-state">
      <img src="/favicon.ico" alt="Logo" />
    </div>
    <div class="navbar-avatar">
      <p v-if="isLogin">{{ welcomeMessage }}</p>
      <p v-else>暂未登录</p>
      <UserInfoDetail v-if="isLogin" />
      <img v-else src="/guest.jpg" alt="User Avatar" />
    </div>
  </nav>
  <nav class="navbar-navigations">
    <div class="navbar-bottom-left" v-if="this.$store.getters.currentLoginType === 'user'">
      <a href="#" @click="selectMenu('首页')">首页</a>
      <a href="#" @click="selectMenu('推荐')">推荐</a>
      <a href="#" @click="selectMenu('类别')">类别</a>
      <a href="#" @click="selectMenu('新闻')">新闻</a>
      <a href="#" @click="selectMenu('我的')">我的</a>
    </div>
    <div class="navbar-bottom-left" v-else>
      <a href="#" @click="selectMenu('公告管理')">公告管理</a>
      <a href="#" @click="selectMenu('推荐管理')">推荐管理</a>
      <a href="#" @click="selectMenu('新闻管理')">新闻管理</a>
      <a href="#" @click="selectMenu('游戏管理')">游戏管理</a>
      <a href="#" @click="selectMenu('用户管理')">用户管理</a>
      <a
        href="#"
        @click="selectMenu('管理员管理')"
        v-if="this.$store.getters.currentLoginType === 'superAdmin'"
      >
        管理员管理</a
      >
    </div>
    <div class="navbar-search">
      <div class="search-container" v-if="this.$store.getters.currentLoginType === 'user'">
        <input type="text" placeholder="Search..." v-model="searchQuery" />
        <button @click="performSearch">搜索</button>
      </div>
    </div>
  </nav>
</template>

<script>
import store from '../services/Store.js'
import UserInfoDetail from './UserInfoDetail.vue'
export default {
  props: ['activeTopMenu'],
  components: {
    UserInfoDetail,
  },
  emits: ['updataSubMenu'],
  methods: {
    selectMenu(menu) {
      this.$emit('updataSubMenu', menu)
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
      } else {
        console.error('Unknown login type')
      }
      return ''
    },
  },
}
</script>

<style scoped>
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

button {
  padding: 0.5rem;
  width: 50px;
  height: 30px;
  background: linear-gradient(to right, var(--primary-color-alpha2) 1%, var(--main-color) 99%);
  color: var(--contrast-color);
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
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
