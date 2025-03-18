<template>
  <div class="manage-delete">
    <h2>{{ currentTitle }}</h2>
    <div class="delete-content">
      <!-- 输入框用于输入ID -->
      <div class="form-group">
        <label for="inputId">ID</label>
        <input
          type="text"
          id="inputId"
          v-model="inputId"
          placeholder="请输入ID"
          @input="fetchDataById"
        />
      </div>

      <div v-if="deleteData">
        <p>确定要删除 {{ deleteTarget }} 吗？</p>
        <div class="delete-details">
          <div v-for="(detail, index) in deleteDetails" :key="index" class="detail-item">
            <span class="label">{{ detail.label }}:</span>
            <span class="value">{{ detail.value }}</span>
          </div>
        </div>
        <div class="delete-buttons">
          <button @click="toggleDeleteConfirmation" class="delete-btn">
            {{ isConfirmingDelete ? '确认删除' : '删除' }}
          </button>
          <button @click="handleCancel" class="cancel-btn">取消</button>
        </div>
      </div>
      <div v-else>
        <p>请输入ID以查询要删除的数据</p>
      </div>
    </div>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'

export default {
  name: 'ManageDelete',
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // 定义不同删除功能的配置
      deleteConfig: {
        删除公告: {
          title: '删除公告',
          apiPath: '/notice',
          details: [
            { field: 'title', label: '标题' },
            { field: 'content', label: '内容' },
            { field: 'username', label: '发布者' },
          ],
        },
        删除新闻: {
          title: '删除新闻',
          apiPath: '/news',
          details: [
            { field: 'title', label: '标题' },
            { field: 'description', label: '描述' },
            { field: 'type', label: '类型' },
          ],
        },
        删除游戏: {
          title: '删除游戏',
          apiPath: '/games',
          details: [
            { field: 'gameTitle', label: '游戏名称' },
            { field: 'gameGenre', label: '游戏类型' },
            { field: 'gamePlatform', label: '游戏平台' },
            { field: 'gameDeveloper', label: '游戏开发商' },
            { field: 'gamePublisher', label: '游戏发行商' },
            { field: 'ratingPhrase', label: '游戏评分' },
            { field: 'officalRating', label: '游戏评价' },
            { field: 'releaseYear', label: '发行年份' },
            { field: 'releaseMonth', label: '发行月份' },
            { field: 'releaseDay', label: '发行日期' },
            { field: 'gameUrl', label: '游戏链接' },
          ],
        },
        删除管理员: {
          title: '删除管理员',
          apiPath: '/admin',
          details: [
            { field: 'admin_name', label: '管理员名称' },
            { field: 'admin_type', label: '管理员类型' },
          ],
        },
        删除用户: {
          title: '删除用户',
          apiPath: '/users',
          details: [
            { field: 'email', label: '邮箱' },
            { field: 'username', label: '用户名' },
          ],
        },
      },
      deleteData: null,
      currentTitle: '',
      apiPath: '',
      deleteDetails: [],
      deleteTarget: '',
      inputId: '', // 用于存储用户输入的ID
      isConfirmingDelete: false, // 是否处于删除确认状态
    }
  },
  watch: {
    activeMainContent() {
      this.loadDeleteConfig()
      this.fetchData()
    },
    id() {
      this.fetchData()
    },
  },
  created() {
    this.loadDeleteConfig()
    this.fetchData()
  },
  methods: {
    loadDeleteConfig() {
      const config = this.deleteConfig[this.activeMainContent]
      if (config) {
        this.currentTitle = config.title
        this.apiPath = config.apiPath
        this.deleteDetails = config.details.map((detail) => ({
          label: detail.label,
          value: '',
          field: detail.field,
        }))
        this.deleteTarget = config.title.replace('删除', '')
      } else {
        console.error(`未知的删除类型: ${this.activeMainContent}`)
      }
    },
    async fetchData() {
      try {
        if (!this.id) {
          console.error('缺少数据ID')
          return
        }
        const path = `${this.apiPath}/${this.id}`
        const response = await DataService.get(path)
        if (response.data.success && response.data.data) {
          this.deleteData = response.data.data
          // 填充删除详情
          this.deleteDetails.forEach((detail) => {
            detail.value = this.deleteData[detail.field] || '暂无'
          })
        } else {
          alert(`获取数据失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        alert('获取数据失败: 请检查网络或联系管理员')
      }
    },
    async fetchDataById() {
      if (!this.inputId) {
        // 如果没有输入ID，清空表单数据
        this.deleteData = null
        this.deleteDetails.forEach((detail) => {
          detail.value = ''
        })
        return
      }
      try {
        const path = `${this.apiPath}/${this.inputId}`
        const response = await DataService.get(path)
        if (response.data.success && response.data.data) {
          this.deleteData = response.data.data
          // 填充删除详情
          this.deleteDetails.forEach((detail) => {
            detail.value = this.deleteData[detail.field] || '暂无'
          })
        } else {
          alert(`获取数据失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    },
    async handleDelete() {
      try {
        const path = `${this.apiPath}/${this.inputId}`
        const response = await DataService.delete(path)
        if (response.data.success) {
          alert('删除成功')
          // 清空数据
          this.deleteData = null
          this.deleteDetails.forEach((detail) => {
            detail.value = ''
          })
          this.inputId = ''
          this.isConfirmingDelete = false
          // 触发父组件刷新数据
          this.$emit('data-deleted')
        } else {
          alert(`删除失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('删除失败:', error)
        alert('删除失败: 请检查网络或联系管理员')
      }
    },
    toggleDeleteConfirmation() {
      if (this.isConfirmingDelete) {
        // 如果已经在确认状态，则执行删除
        this.handleDelete()
      } else {
        // 否则切换到确认状态
        this.isConfirmingDelete = true
      }
    },
    handleCancel() {
      // 清空数据
      this.deleteData = null
      this.deleteDetails.forEach((detail) => {
        detail.value = ''
      })
      this.inputId = ''
      this.isConfirmingDelete = false
      // 返回上一页或刷新列表
      this.$router.go(-1)
    },
  },
}
</script>

<style scoped>
input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.form-group {
  margin-bottom: 15px;
}

.manage-delete {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.delete-content {
  background-color: var(--primary-color);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

p {
  margin-bottom: 15px;
  font-size: 16px;
}

.delete-details {
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  width: 100px;
}

.value {
  flex: 1;
  word-break: break-all;
}

.delete-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.delete-btn,
.cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.delete-btn:hover {
  background-color: #d32f2f;
}

.cancel-btn {
  background-color: #cccccc;
  color: white;
}

.cancel-btn:hover {
  background-color: #aaaaaa;
}
</style>
