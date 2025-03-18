<template>
  <div class="user-avatar-container" @mouseenter="showInfo" @mouseleave="hideInfo">
    <img :src="avatarSrc" alt="User Avatar" class="user-avatar" />
    <div class="user-info-panel" v-if="showInfoPanel">
      <div class="user-info-content">
        <div class="info-row" v-if="this.$store.getters.currentLoginType === 'user'">
          <span class="info-label">关注</span>
          <span class="info-value">{{ userInfo.subscribed_count }}</span>
          <span class="info-label">评论</span>
          <span class="info-value">{{ userInfo.review_count }}</span>
        </div>
        <div class="info-row">
          <button class="exit-button" @click="logout">退出登陆</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/services/Store.js'
import DataService from '@/services/DataService.js'

export default {
  data() {
    return {
      showInfoPanel: false,
      userInfo: {
        subscribed_count: 0,
        review_count: 0,
      },
      avatarSrc: '/guest.jpg', // 默认头像
      hoverTimeout: null,
      hideTimeout: null,
    }
  },
  methods: {
    async showInfo() {
      // 清除之前的隐藏定时器
      if (this.hideTimeout) {
        clearTimeout(this.hideTimeout)
        this.hideTimeout = null
      }

      // 设置一个短暂的延迟，避免鼠标快速移动时频繁触发
      this.hoverTimeout = setTimeout(async () => {
        try {
          const response = await DataService.get('/interactions/read', {
            params: {
              user_id: store.state.user.userID,
            },
          })
          this.userInfo = response.data
          this.showInfoPanel = true
        } catch (error) {
          console.error('获取用户信息失败:', error)
        }
      }, 300)
    },
    hideInfo() {
      // 清除之前的显示定时器
      if (this.hoverTimeout) {
        clearTimeout(this.hoverTimeout)
        this.hoverTimeout = null
      }

      // 设置一个短暂的延迟，避免鼠标快速移动时频繁触发
      this.hideTimeout = setTimeout(() => {
        this.showInfoPanel = false
      }, 300)
    },
    logout() {
      this.$store.dispatch('user/logout')
      this.$store.dispatch('admin/logout')
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
  border-radius: 13px;
  width: 100%;
  height: 40px;
  border: none;
  text-align: center;
  text-decoration: none;
  background-color: var(--main-color);
  color: var(--contrast-color);
  padding: 10px;
  display: inline-block;
  box-shadow:
    0 1px 3px 0 var(--main-color-alpha2),
    0 1px 3px 0 var(--main-color-alpha2);
}

.exit-button:hover {
  box-shadow:
    0 3px 3px 1 var(--main-color-alpha2),
    0 3px 3px 0 var(--main-color-alpha2);
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
  font-weight: bold;
  color: var(--contrast-color);
}

.info-value {
  color: var(--main-color);
}
</style>
