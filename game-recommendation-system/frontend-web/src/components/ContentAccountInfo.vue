<template>
  <div class="avatar-management">
    <h2>头像管理</h2>

    <!-- 显示当前头像 -->
    <div class="current-avatar">
      <img :src="avatarUrl" alt="当前头像" v-if="hasAvatar" />
      <p v-else>您尚未设置头像</p>
    </div>

    <div class="opreate-area">
      <!-- 上传新头像 -->
      <div class="upload-avatar">
        <input
          id="file-input"
          type="file"
          @change="handleFileChange"
          accept="image/*"
          ref="fileInput"
        />
      </div>

      <!-- 操作按钮 -->
      <div class="actions">
        <button @click="uploadUserAvatar" :disabled="!selectedFile">上传头像</button>
        <button @click="deleteUserAvatar" v-if="hasAvatar">删除头像</button>
      </div>
    </div>
  </div>
  <!-- 操作结果提示 -->
  <div class="message" v-if="message">
    {{ message }}
  </div>

  <hr />
  <div class="password-management">
    <h2>修改密码</h2>
    <div class="password-update">
      <form>
        <div class="form-group">
          <label for="oldPassword">旧密码:</label>
          <input type="password" id="oldPassword" v-model="oldPassword" required />
        </div>
        <div class="form-group">
          <label for="newPassword">新密码:</label>
          <input
            type="password"
            id="newPassword"
            v-model="newPassword"
            required
            @blur="validatePassword"
          />
          <span v-if="passwordError" class="error">{{ passwordError }}</span>
        </div>
        <button id="update-btn" type="submit" :disabled="isSubmitting" @click="updatePassword">
          更新密码
        </button>
      </form>
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
      oldPassword: '',
      newPassword: '',
      isSubmitting: false,
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
    validatePassword(pwd) {
      console.log('testing password validation')
      // 密码长度至少8位，包含字母和数字
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

      if (!passwordRegex.test(pwd)) {
        this.passwordError = '密码必须至少8位，包含字母和数字'

        //TODO 为了便于登陆暂时不使用密码强度验证
        return true
      }

      return true
    },
    async updatePassword() {
      console.log('updating password')
      if (!this.oldPassword) {
        console.log('oldpassword:' + this.oldPassword)
        alert('需要输入旧密码')
        return
      }
      if (!this.newPassword) {
        console.log('newpassword:' + this.newPassword)
        alert('需要输入新密码')
        return
      }

      try {
        // 调用后端API更新密码
        const response = await this.$axios.post('/users/password/update', {
          user_id: this.userID,
          old_password: this.oldPassword,
          new_password: this.newPassword,
        })

        if (response.data.success) {
          this.message = response.data.msg
          this.oldPassword = ''
          this.newPassword = ''
          this.passwordError = ''
        } else {
          this.passwordError = response.data.msg || '密码更新失败'
        }
      } catch (error) {
        console.error('密码更新失败:', error)
        this.passwordError = '密码更新失败，请稍后重试'
      } finally {
        this.isSubmitting = false
      }
    },
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
hr {
  margin-top: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin: 10px 40px;
}

.opreate-area {
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  align-items: center;
}

#file-input {
  flex: 1;
  width: 100%;
  height: 100%;
  background-color: var(--primary-color);
  border: 1px solid var(--secondary-color);
  border-radius: 10px;
  padding: 8px;
  margin: 10px;
}

.avatar-management,
.password-management {
  max-width: 800px;
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
  margin: 10px;
}

button {
  margin: 5px;
  padding: 10px 20px;
  background-color: var(--main-color);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

button:hover {
  background-color: var(--primary-color);
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
