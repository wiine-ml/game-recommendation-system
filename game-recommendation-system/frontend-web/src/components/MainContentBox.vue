<template>
  <div class="main-content">
    <component :is="currentComponent" :activeMainContent="activeMainContent" />
  </div>
</template>

<script>
import { markRaw } from 'vue'

export default {
  name: 'MainContentBox',
  inheritAttrs: false,
  props: {
    activeMainContent: String,
  },
  data() {
    return {
      lastComponent: null,
      currentComponent: null,
    }
  },
  methods: {
    async getContentItemMap() {
      try {
        let component = null
        const loginType = this.$store.getters.currentLoginType

        if (loginType === 'user') {
          switch (this.activeMainContent) {
            case '热门':
              component = await import('./ContentCarouselPromote.vue')
              break
            case '公告':
              component = await import('./ContentNoitce.vue')
              break
            case '关于':
              component = await import('./ContentAboutUs.vue')
              break
            case '设置':
              component = await import('./ContentSetting.vue')
              break
            case '为你推荐':
              component = await import('./ContentRecommendation.vue')
              break
            case '最新上架':
            case '最高评分':
            case '最受欢迎':
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
              component = await import('./ContentMartix.vue')
              break
            case '游戏杂谈':
            case 'PC游戏':
            case '主机游戏':
            case '手机游戏':
              component = await import('./ContentNews.vue')
              break
            case '关注':
              component = await import('./ContentMartix.vue')
              break
            case '消息':
            case '我的评分':
              component = await import('./ContentReview.vue')
              break
            case '账号信息':
              component = await import('./ContentAccountInfo.vue')
              break
            default:
              component = await import('./ErrorHandlingPage.vue')
          }
        } else if (loginType === 'admin' || loginType === 'superAdmin') {
          switch (this.activeMainContent) {
            case '查询公告':
            case '查询新闻':
            case '查询游戏':
            case '查询用户':
            case '查询管理员':
              component = await import('./ManageShow.vue')
              break
            case '创建公告':
            case '创建新闻':
            case '创建游戏':
            case '创建管理员':
              component = await import('./ManageCreate.vue')
              break
            case '更新公告':
            case '更新新闻':
            case '更新游戏':
            case '更新用户':
            case '更新管理员':
              component = await import('./ManageUpdate.vue')
              break
            case '删除公告':
            case '删除新闻':
            case '删除游戏':
            case '删除用户':
            case '删除管理员':
              component = await import('./ManageDelete.vue')
              break
            default:
              component = await import('./ErrorHandlingPage.vue')
          }
        } else if (loginType === 'developer' || loginType === 'publisher') {
          switch (this.activeMainContent) {
            case '主页预览':
              component = await import('./VendorHomePage.vue')
              break
            case '主页插画':
              component = await import('./VendorHeadImageManage.vue')
              break
            case '主页推广':
              component = await import('./VendorPromoteImageManage.vue')
              break
            case '主页设置':
              component = await import('./VendorSetting.vue')
              break
            case '查询游戏':
              component = await import('./ManageShow.vue')
              break
            case '上架游戏':
              component = await import('./ManageCreate.vue')
              break
            case '更新游戏':
              component = await import('./ManageUpdate.vue')
              break
            case '下架游戏':
              component = await import('./ManageDelete.vue')
              break
            case '查询新闻':
              component = await import('./ManageShow.vue')
              break
            case '发布新闻':
              component = await import('./ManageCreate.vue')
              break
            case '更新新闻':
              component = await import('./ManageUpdate.vue')
              break
            case '下架新闻':
              component = await import('./ManageDelete.vue')
              break
            default:
              component = await import('./ErrorHandlingPage.vue')
          }
        } else {
          component = await import('./ErrorHandlingPage.vue')
        }

        this.currentComponent = markRaw(component.default || component)
      } catch (error) {
        console.error('Error loading component:', error)
        this.currentComponent = (await import('./ErrorHandlingPage.vue')).default
      }
    },
  },
  watch: {
    activeMainContent: {
      handler() {
        this.getContentItemMap()
      },
      immediate: true,
    },
  },
}
</script>

<style scoped>
.main-content {
  border-radius: 10px;
  background-color: var(--secondary-color);
  box-shadow: 0 0 5px var(--secondary-color);
  padding: 20px;
  height: fit-content;
  overflow: hidden;
}
</style>
