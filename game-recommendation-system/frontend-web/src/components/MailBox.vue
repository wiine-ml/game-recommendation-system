<template>
  <div class="mail-box" v-if="showMailBox">
    <div class="mail-box-header">
      <h3>邮件收件箱</h3>
      <button id="exit-btn" @click="closeMailBox">X</button>
    </div>
    <div class="mail-box-content">
      <div class="mail-list" v-if="mails.length > 0">
        <div v-for="(mail, index) in mails" :key="index" class="mail-item">
          <p>发送者: {{ mail.sender_type }} - {{ mail.sender_id }}</p>
          <p>内容: {{ mail.message }}</p>
          <button id="delete-btn" @click="deleteMail(mail.id)">删除</button>
        </div>
      </div>

      <div v-else class="empty-mail">
        <p>收件箱空空如也</p>
      </div>

      <div class="mail-pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../services/DataService.js'
import store from '../services/Store.js'

export default {
  props: {
    showMailBox: Boolean,
  },
  data() {
    return {
      mails: [],
      currentPage: 1,
      totalPages: 1,
      receiverType: '',
      receiverId: '',
    }
  },
  methods: {
    async loadMails(page) {
      const loginType = store.getters.currentLoginType
      if (!loginType) {
        console.error('未登录用户无法查看邮件')
        return
      }
      this.receiverType = loginType
      if (loginType === 'user') {
        this.receiverId = store.getters['user/userID']
      } else if (loginType === 'admin') {
        this.receiverId = store.getters['admin/adminID']
      } else if (loginType === 'developer' || loginType === 'publisher') {
        this.receiverId = store.getters['vendor/vendorID']
      } else {
        console.error('未知的登录类型')
        return
      }
      try {
        // 构造查询参数
        const queryParams = new URLSearchParams({
          receiver_type: this.receiverType,
          receiver_id: this.receiverId,
        }).toString()

        // 发送 GET 请求并包含查询参数
        const response = await apiClient.get(`/mail/read/page/${page}?${queryParams}`)

        if (response.data.success) {
          this.mails = response.data.data.mails
          this.currentPage = response.data.data.current_page
          this.totalPages = response.data.data.total_pages
        } else {
          console.error('获取邮件失败')
        }
      } catch (error) {
        console.error('邮件加载错误:', error)
      }
    },
    async deleteMail(mailId) {
      try {
        const response = await apiClient.delete(`/mail/delete/${mailId}`, {
          data: {
            type: this.receiverType,
            id: this.receiverId,
          },
        })
        if (response.data.success) {
          this.loadMails(this.currentPage)
        } else {
          console.error('删除邮件失败')
        }
      } catch (error) {
        console.error('邮件删除错误:', error)
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        this.loadMails(this.currentPage)
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
        this.loadMails(this.currentPage)
      }
    },
    closeMailBox() {
      this.$emit('close')
    },
  },
  watch: {
    showMailBox(newVal) {
      if (newVal) {
        this.loadMails(this.currentPage)
      }
    },
  },
}
</script>

<style scoped>
p {
  margin-top: 5px;
  margin-bottom: 5px;
}

#delete-btn {
  float: right;
  background-color: #ff2222;
  color: var(--contrast-color);
  border-radius: 10px;
  margin-right: 20px;
}

.empty-mail {
  padding: 15px;
  text-align: center;
  color: #999;
}

#exit-btn {
  border-radius: 30%;
}

.mail-box {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mail-box-content {
  background-color: var(--primary-color);
  border-radius: 20px;
  box-shadow: 0 1px 4px var(--contrast-color);
  width: 80%;
  max-width: 1000px;
}

.mail-box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.mail-list {
  padding: 10px;
  max-height: 600px;
  overflow-y: auto;
  margin-bottom: 10px;
  border-radius: 20px;
}

.mail-item {
  border-top: 1px solid var(--contrast-color);
  border-bottom: 1px solid var(--contrast-color);
  padding-bottom: 50px;
  margin: 10px 20px;
}

.mail-item:first-child {
  border-radius: 10px;
}

.mail-item:last-child {
  border-radius: 10px;
}

.mail-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 15px;
}

button {
  padding: 5px 10px;
  cursor: pointer;
}
</style>
