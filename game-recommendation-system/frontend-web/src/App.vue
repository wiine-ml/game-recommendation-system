<template>
  <!-- 顶部菜单栏 -->
  <div class="top-menu-container">
    <TopMenu @updataSubMenu="UpdateSubMenu" />
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
    this.$store.dispatch('preference/loadThemeFromStorage')
    this.$store.dispatch('preference/loadItemPerpageFromStorage')
    if (this.isLogin && this.$store.getters.currentLoginType === 'user') {
      this.fetchAvatar().then((response) => {
        if (response.success) {
          this.$store.commit('user/setAvatarFile', response.data.avatarFile)
        }
      })
    } else if (
      this.$store.getters.currentLoginType === 'publisher' ||
      this.$store.getters.currentLoginType === 'developer'
    ) {
      console.log('获取厂商头像')
      this.$store.dispatch('vendor/fetchAvatar')
    }

    if (this.$store.getters.currentLoginType === 'admin') {
      this.activeSubMenu = '公告管理'
      this.activeMainContent = '查询公告'
    } else if (this.$store.getters.currentLoginType === 'developer') {
      this.activeSubMenu = '主页管理'
      this.activeMainContent = '主页预览'
    } else {
      this.activeSubMenu = '首页'
      this.activeMainContent = '热门'
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
