<template>
  <div class="main-content">
    <component :is="getContentItemMap()" :activeMainContent="activeMainContent" />
  </div>
</template>

<script>
import ContentNoitce from './ContentNoitce.vue'
import ContentAboutUs from './ContentAboutUs.vue'
import ContentSetting from './ContentSetting.vue'
import ContentNews from './ContentNews.vue'
import ContentMartix from './ContentMartix.vue'
import ContentReview from './ContentReview.vue'
import ContentRecommendation from './ContentRecommendation.vue'

import ManageShow from './ManageShow.vue'
import ManageCreate from './ManageCreate.vue'
import ManageUpdate from './ManageUpdate.vue'
import ManageDelete from './ManageDelete.vue'
import ContentAccountInfo from './ContentAccountInfo.vue'
import ContentCarouselPromote from './ContentCarouselPromote.vue'
import ErrorHandlingPage from './ErrorHandlingPage.vue'
import VendorHomePage from './VendorHomePage.vue'
import VendorHeadImageManage from './VendorHeadImageManage.vue'
import VendorSetting from './VendorSetting.vue'
import VendorPromoteImageManage from './VendorPromoteImageManage.vue'

export default {
  props: {
    activeMainContent: String,
  },
  name: 'MainContentBox',
  components: {
    ContentAboutUs,
    ContentNoitce,
    ContentNews,
    ContentMartix,
    ContentReview,
    ContentRecommendation,
    ContentSetting,
    ContentAccountInfo,
    ContentCarouselPromote,

    ManageShow,
    ManageCreate,
    ManageUpdate,
    ManageDelete,

    VendorHomePage,
    VendorHeadImageManage,
    VendorPromoteImageManage,
    VendorSetting,

    ErrorHandlingPage,
  },
  methods: {
    getContentItemMap() {
      if (this.$store.getters.currentLoginType === 'user') {
        //用户内容
        switch (this.activeMainContent) {
          // 首页内容
          case '热门':
            return ContentCarouselPromote
          case '公告':
            return ContentNoitce
          case '关于':
            return ContentAboutUs
          case '设置':
            return ContentSetting
          // 推荐内容
          case '最新上架':
          case '最高评分':
          case '最受欢迎':
            return ContentMartix
          case '为你推荐':
            return ContentRecommendation
          // 类别内容
          case '全部':
          case 'Action':
          case 'Adventure':
          case 'Compilation':
          case 'Educational':
          case 'Fighting':
          case 'Platformer':
          case 'Platform':
          case 'Puzzle':
          case 'RPG':
          case 'Strategy':
          case 'Simulation':
          case 'Battle':
          case 'Card':
          case '动作':
          case '冒险':
          case '休闲':
          case '模拟':
          case '策略':
          case '角色扮演':
          case '单人':
          case '二维':
          case '氛围':
            return ContentMartix
          // 新闻内容
          case '游戏杂谈':
          case 'PC游戏':
          case '主机游戏':
          case '手机游戏':
            return ContentNews
          // 我的内容
          case '关注':
            return ContentMartix
          case '消息':
          case '我的评分':
            return ContentReview
          case '账号信息':
            return ContentAccountInfo
        }
      } else if (
        this.$store.getters.currentLoginType === 'admin' ||
        this.$store.getters.currentLoginType === 'superAdmin'
      ) {
        switch (this.activeMainContent) {
          //
          case '查询公告':
          case '查询新闻':
          case '查询游戏':
          case '查询用户':
          case '查询管理员':
            return ManageShow
          //
          case '创建公告':
          case '创建新闻':
          case '创建游戏':
          case '创建管理员':
            return ManageCreate
          //
          case '更新公告':
          case '更新新闻':
          case '更新游戏':
          case '更新用户':
          case '更新管理员':
            return ManageUpdate
          //
          case '删除公告':
          case '删除新闻':
          case '删除游戏':
          case '删除用户':
          case '删除管理员':
            return ManageDelete
        }
      } else if (
        this.$store.getters.currentLoginType === 'developer' ||
        this.$store.getters.currentLoginType === 'publisher'
      ) {
        switch (this.activeMainContent) {
          //
          case '主页预览':
            return VendorHomePage
          case '主页插画':
            return VendorHeadImageManage
          case '主页推广':
            return VendorPromoteImageManage
          case '主页设置':
            return VendorSetting
          //
          case '查询游戏':
            return ManageShow
          case '上架游戏':
            return ManageCreate
          case '更新游戏':
            return ManageUpdate
          case '下架游戏':
            return ManageDelete
          //
          case '查询新闻':
            return ManageShow
          case '发布新闻':
            return ManageCreate
          case '更新新闻':
            return ManageUpdate
          case '下架新闻':
            return ManageDelete
        }
      }
      return ErrorHandlingPage
    },
  },
}
</script>

<style>
.main-content {
  border-radius: 10px;
  background-color: var(--secondary-color);
  box-shadow: 0 0 5px var(--secondary-color);
  padding: 20px;
  height: 100%;
  overflow: auto;
}
</style>
