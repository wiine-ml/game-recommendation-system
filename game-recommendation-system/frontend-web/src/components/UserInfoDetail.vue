<template>
  <div class="user-avatar-container" @mouseenter="showInfo" @mouseleave="hideInfo">
    <!-- 动态绑定头像图片的 src 属性 -->
    <img :src="userAvatar" alt="Avatar" class="user-avatar" v-if="showAvatar" />
    <div class="user-info-panel" v-if="showInfoPanel">
      <div class="user-info-content">
        <div class="info-row" v-if="this.$store.getters.currentLoginType === 'user'">
          <span class="info-label">关注</span>
          <span class="info-value">{{ userInfo.subscribed_count || -1 }}</span>
          <span class="info-label">评论</span>
          <span class="info-value">{{ userInfo.review_count || -1 }}</span>
        </div>
        <div class="info-row">
          <el-button type="danger" plain class="exit-button" @click="logout">退出登陆</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/services/Store.js'
import DataService from '@/services/DataService.js'
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      showInfoPanel: false,
      userInfo: {
        subscribed_count: 0,
        review_count: 0,
      },
      hoverTimeout: null,
      hideTimeout: null,
    }
  },
  computed: {
    ...mapGetters('user', ['avatarUrl']),
    showAvatar() {
      return true
    },
    userAvatar() {
      // 如果用户已登录且有头像 URL，则返回头像 URL
      if (store.getters.currentLoginType === 'user' && store.getters.isLogin && this.avatarUrl) {
        return this.avatarUrl
      } else if (
        store.getters.currentLoginType === 'publisher' ||
        store.getters.currentLoginType === 'developer'
      ) {
        return this.$store.getters['vendor/avatarUrl']
      }
      // 如果用户未登录或没有头像 URL，返回默认头像
      return '/defaultUserImg.jpg'
    },
  },
  methods: {
    async showInfo() {
      if (this.hideTimeout) {
        clearTimeout(this.hideTimeout)
        this.hideTimeout = null
      }

      this.hoverTimeout = setTimeout(async () => {
        try {
          const response = await DataService.get('/interactions/read', {
            params: {
              user_id: store.state.user.userID,
            },
          })
          console.log('获取用户信息成功:', response.data)
          this.userInfo.review_count = response.data.data.review_count
          this.userInfo.subscribed_count = response.data.data.subscribed_count
        } catch (error) {
          console.error('获取用户信息失败:', error)
        } finally {
          this.showInfoPanel = true
        }
      }, 300)
    },
    hideInfo() {
      if (this.hoverTimeout) {
        clearTimeout(this.hoverTimeout)
        this.hoverTimeout = null
      }
      this.hideTimeout = setTimeout(() => {
        this.showInfoPanel = false
      }, 300)
    },
    logout() {
      this.$store.dispatch('user/logout')
      this.$store.dispatch('admin/logout')
      this.$store.dispatch('vendor/logout')
      this.$store.commit('preference/clearPreferences')
      this.showInfoPanel = false
      alert('退出登录成功')
      location.reload()
    },
  },
}
</script>

<style scoped>
.exit-button {
  width: 100%;
  height: 40px;
  border-radius: 15px;
  border: none;
  text-align: center;
  background-color: #333;
  display: inline-block;
}

.user-avatar-container {
  position: relative;
  display: inline-block;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.user-info-panel {
  position: absolute;
  bottom: -80px;
  left: -29px;
  transform: translateX(-50%);
  background-color: var(--secondary-color-alpha1);
  color: var(--contrast-color);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  width: 200px;
  z-index: 10;
}

.user-info-content {
  display: flex;
  flex-direction: column;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.info-label {
  color: var(--contrast-color);
}

.info-value {
  color: var(--main-color-alpha2);
}
</style>
