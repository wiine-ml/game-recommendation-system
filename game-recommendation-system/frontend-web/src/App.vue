<template>
  <!-- 顶部菜单栏 -->
  <div class="top-menu-container">
    <TopMenu :activeTopMenu="activeTopMenu" @updataSubMenu="UpdateSubMenu" />
  </div>
  <!-- 中间内容区 -->
  <div class="middle-container">
    <!-- 左侧子菜单栏 -->
    <div class="sub-menu-container">
      <SubMenu
        :activeSubMenu="activeSubMenu"
        :activeMainContent="activeMainContent"
        @UpdateMainContent="UpdateMainContent"
      />
    </div>
    <!-- 右侧主要内容区 -->
    <div class="main-content-container">
      <!-- 若未登陆: 显示登录注册框 -->
      <Component v-if="!isLogin" :is="curLoginView" @UpdateLoginView="UpdateLoginView" />

      <!-- 若已登陆: 显示主要内容区 -->
      <MainContentBox v-else :activeMainContent="activeMainContent" />
    </div>
  </div>
</template>

<script>
import store from './services/Store.js'

import TopMenu from './components/TopMenu.vue'
import SubMenu from './components/SubMenu.vue'
import LoginBox from './components/LoginBox.vue'
import RegistrationBox from './components/RegistrationBox.vue'
import MainContentBox from './components/MainContentBox.vue'

import { mapActions } from 'vuex'

export default {
  components: {
    TopMenu,
    SubMenu,
    LoginBox,
    RegistrationBox,
    MainContentBox,
  },
  data() {
    return {
      isLogin: store.getters['isLogin'],
      activeSubMenu: '',
      activeMainContent: '公告',
      curLoginView: LoginBox,
    }
  },
  methods: {
    ...mapActions('user', ['fetchAvatar']),
    UpdateLoginView(newView) {
      this.curLoginView = newView
    },
    UpdateSubMenu(newSubMenu) {
      this.activeSubMenu = newSubMenu
    },
    UpdateMainContent(newMainContent) {
      console.log(newMainContent)
      this.activeMainContent = newMainContent
    },
  },
  mounted() {
    // 在应用挂载时加载上次使用设置
    this.$store.dispatch('preference/loadThemeFromStorage')
    this.$store.dispatch('preference/loadItemPerpageFromStorage')
    if (this.isLogin) {
      this.fetchAvatar().then((response) => {
        if (response.success) {
          this.$store.commit('user/setAvatarFile', response.data.avatarFile)
        }
      })
    }
    if (this.$store.getters.currentLoginType === 'user') {
      this.activeSubMenu = '首页'
    } else {
      this.activeSubMenu = '公告'
    }
  },
}
</script>

<style scoped>
.top-menu-container {
  justify-content: space-around;
}
.middle-container {
  display: flex;
  flex: 1;
}
.sub-menu-container {
  width: 250px;
  padding: 1rem;
}
.main-content-container {
  flex: 1;
  padding: 1rem;
}
</style>
