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

    ManageShow,
    ManageCreate,
    ManageUpdate,
    ManageDelete,
  },
  methods: {
    getContentItemMap() {
      if (this.$store.getters.currentLoginType === 'user') {
        //用户内容
        switch (this.activeMainContent) {
          // 首页内容
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
          case '独立':
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
          // 默认情况
          default:
            return ContentMartix // 或者根据需求处理未知情况
        }
      }
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
        default:
          return ContentMartix // 或者根据需求处理未知情况
      }
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
