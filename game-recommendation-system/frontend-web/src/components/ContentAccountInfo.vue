<template>
  <div class="avatar-management">
    <h2>头像管理</h2>

    <!-- 显示当前头像 -->
    <div class="current-avatar">
      <img :src="avatarUrl" alt="当前头像" v-if="hasAvatar" />
      <p v-else>您尚未设置头像</p>
    </div>

    <!-- 上传新头像 -->
    <div class="upload-avatar">
      <input type="file" @change="handleFileChange" accept="image/*" ref="fileInput" />
      <button @click="uploadUserAvatar" :disabled="!selectedFile">上传头像</button>
    </div>

    <!-- 操作按钮 -->
    <div class="actions">
      <button @click="deleteUserAvatar" v-if="hasAvatar">删除头像</button>
    </div>

    <!-- 操作结果提示 -->
    <div class="message" v-if="message">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      selectedFile: null,
      message: '',
    }
  },
  computed: {
    ...mapGetters('user', ['isLogin', 'userID', 'userName', 'avatarUrl']),
    hasAvatar() {
      return !!this.avatarUrl
    },
  },
  methods: {
    ...mapActions('user', ['fetchAvatar', 'uploadAvatar', 'deleteAvatar']),
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    async uploadUserAvatar() {
      console.log('上传头像:', this.selectedFile)
      if (!this.selectedFile || !this.isLogin) return

      try {
        const response = await this.uploadAvatar(this.selectedFile)
        if (response.success) {
          this.message = response.msg
          this.$store.commit('user/setAvatarFile', this.selectedFile)
          this.selectedFile = null
          this.$refs.fileInput.value = null // 重置文件输入
        } else {
          this.message = response.msg
        }
      } catch (error) {
        console.error('上传头像失败:', error)
        this.message = '上传头像失败，请重试'
      }
    },
    async deleteUserAvatar() {
      if (!this.isLogin) return

      try {
        const response = await this.deleteAvatar()
        if (response.success) {
          this.message = response.msg
          this.$store.commit('user/setAvatarFile', null)
        } else {
          this.message = response.msg
        }
      } catch (error) {
        console.error('删除头像失败:', error)
        this.message = '删除头像失败，请重试'
      }
    },
  },
  mounted() {
    if (this.isLogin) {
      this.fetchAvatar().then((response) => {
        if (response.success) {
          this.$store.commit('user/setAvatarFile', response.data.avatarFile)
        }
      })
    }
  },
}
</script>

<style scoped>
.avatar-management {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.current-avatar {
  margin: 20px 0;
  text-align: center;
}

.current-avatar img {
  max-width: 150px;
  border-radius: 50%;
}

.upload-avatar {
  margin: 20px 0;
}

.actions {
  margin: 20px 0;
}

button {
  margin: 0 10px;
  padding: 8px 16px;
  background-color: var(--main-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: var(--primary-color);
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.message {
  margin-top: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 4px;
}
</style>
