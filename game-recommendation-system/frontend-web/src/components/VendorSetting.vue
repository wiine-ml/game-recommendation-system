<template>
  <div class="vendor-avatar-manage">
    <h2>厂商头像管理</h2>

    <!-- 显示当前头像 -->
    <div class="current-avatar">
      <img :src="vendorAvatarUrl" alt="当前头像" v-if="hasAvatar" />
      <p v-else>您尚未设置头像</p>
    </div>

    <!-- 上传新头像 -->
    <div class="upload-avatar">
      <input
        type="file"
        @change="handleFileChange"
        accept="image/*"
        ref="fileInput"
        style="display: none"
      />
      <button id="confirm-btn" @click="triggerFileInput" :disabled="uploading">
        <span v-if="!uploading">上传头像</span>
        <span v-else>上传中...</span>
      </button>
    </div>

    <!-- 操作按钮 -->
    <div class="actions">
      <button id="del-btn" @click="deleteVendorAvatar" v-if="hasAvatar">删除头像</button>
    </div>

    <!-- 操作结果提示 -->
    <div class="message" v-if="message">{{ message }}</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      selectedFile: null,
      message: '',
      uploading: false,
    }
  },
  computed: {
    ...mapGetters('vendor', ['isLogin', 'vendorID', 'vendorType', 'vendorAvatar', 'avatarUrl']),
    hasAvatar() {
      return !!this.avatarUrl
    },
    vendorAvatarUrl() {
      return this.avatarUrl || 'defaultAvatar.jpg' // 默认头像路径
    },
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
      }
    },
    async uploadVendorAvatar() {
      if (!this.selectedFile || !this.isLogin) return

      this.uploading = true
      this.message = ''

      try {
        const formData = new FormData()
        formData.append('vendor_id', this.vendorID)
        formData.append('vendor_type', this.vendorType)
        formData.append('file', this.selectedFile)

        const response = await this.$store.dispatch('vendor/uploadAvatar', this.selectedFile)

        if (response.success) {
          this.message = '头像上传成功'
          this.$store.commit('vendor/setAvatarUrl', response.data.avatarUrl)
        } else {
          this.message = '头像上传失败'
        }
      } catch (error) {
        console.error('上传头像失败:', error)
        this.message = '上传头像失败，请重试'
      } finally {
        this.uploading = false
        this.selectedFile = null
        this.$refs.fileInput.value = null // 重置文件输入
      }
    },
    async deleteVendorAvatar() {
      if (!this.isLogin) return

      try {
        const response = await this.$store.dispatch('vendor/deleteAvatar')

        if (response.success) {
          this.message = '头像删除成功'
          this.$store.commit('vendor/setAvatarUrl', '')
        } else {
          this.message = '头像删除失败'
        }
      } catch (error) {
        console.error('删除头像失败:', error)
        this.message = '删除头像失败，请重试'
      }
    },
  },
  mounted() {
    if (this.isLogin) {
      this.$store.dispatch('vendor/fetchAvatar').then((response) => {
        if (response.success) {
          this.$store.commit('vendor/setAvatarUrl', response.data.avatarUrl)
        }
      })
    }
  },
}
</script>

<style scoped>
.vendor-avatar-manage {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: var(--primary-color);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--contrast-color);
}

.current-avatar {
  text-align: center;
  margin-bottom: 20px;
}

.current-avatar img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.upload-avatar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

#del-btn {
  background-color: rgb(212, 35, 35);
}

button:hover {
  background-color: #367e3a;
}

#del-btn:hover {
  background-color: rgb(156, 24, 24);
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.actions {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.message {
  text-align: center;
  color: #666;
  font-size: 14px;
  height: 20px;
}
</style>
