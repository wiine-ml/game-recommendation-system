<template>
  <h2>{{ currentTitle }}</h2>
  <div class="manage-update">
    <!-- 添加一个输入框用于输入ID -->
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

    <form @submit.prevent="handleSubmit">
      <div class="form-group" v-for="(field, index) in currentFields" :key="index">
        <label :for="field.id">{{ field.label }}</label>
        <input
          :type="field.type"
          :id="field.id"
          v-model="formData[field.id]"
          :placeholder="field.placeholder"
          :required="field.required"
          :readonly="!field.isEditable"
        />
      </div>
      <button type="submit" class="submit-btn">更新</button>
    </form>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'

export default {
  name: 'ManageUpdate',
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
      // 定义不同更新功能的配置
      updateConfig: {
        更新公告: {
          title: '更新公告',
          fields: [
            {
              id: 'title',
              label: '标题',
              type: 'text',
              placeholder: '请输入标题',
              required: true,
              isEditable: true,
            },
            {
              id: 'content',
              label: '内容',
              type: 'text',
              placeholder: '请输入内容',
              required: true,
              isEditable: true,
            },
            {
              id: 'username',
              label: '发布者',
              type: 'text',
              placeholder: '请输入发布者',
              required: true,
              isEditable: false,
            },
          ],
          apiPath: '/notice',
        },
        更新新闻: {
          title: '更新新闻',
          fields: [
            { id: 'title', label: '标题', type: 'text', placeholder: '请输入标题', required: true },
            {
              id: 'description',
              label: '描述',
              type: 'text',
              placeholder: '请输入描述',
              required: true,
              isEditable: true,
            },
            { id: 'type', label: '类型', type: 'text', placeholder: '请输入类型', required: true },
            {
              id: 'image',
              label: '图片URL',
              type: 'text',
              placeholder: '请输入图片URL',
              required: true,
              isEditable: true,
            },
          ],
          apiPath: '/news',
        },
        更新游戏: {
          title: '更新游戏',
          fields: [
            {
              id: 'gameTitle',
              label: '游戏名称',
              type: 'text',
              placeholder: '请输入游戏名称',
              required: true,
              isEditable: true,
            },
            {
              id: 'gameGenre',
              label: '游戏类型',
              type: 'text',
              placeholder: '请输入游戏类型',
              required: true,
              isEditable: true,
            },
            {
              id: 'gamePlatform',
              label: '游戏平台',
              type: 'text',
              placeholder: '请输入游戏平台',
              required: true,
              isEditable: true,
            },
            {
              id: 'releaseYear',
              label: '发行年份',
              type: 'number',
              placeholder: '请输入发行年份',
              required: true,
              isEditable: true,
            },
            {
              id: 'releaseMonth',
              label: '发行月份',
              type: 'number',
              placeholder: '请输入发行月份',
              required: true,
              isEditable: true,
            },
            {
              id: 'releaseDay',
              label: '发行日期',
              type: 'number',
              placeholder: '请输入发行日期',
              required: true,
              isEditable: true,
            },
          ],
          apiPath: '/games',
        },
        更新管理员: {
          title: '更新管理员',
          fields: [
            {
              id: 'admin_name',
              label: '管理员名称',
              type: 'text',
              placeholder: '请输入管理员名称',
              required: true,
              isEditable: true,
            },
            {
              id: 'password',
              label: '密码',
              type: 'password',
              placeholder: '请输入密码',
              required: true,
              isEditable: true,
            },
            {
              id: 'admin_type',
              label: '管理员类型',
              type: 'text',
              placeholder: '请输入管理员类型',
              required: true,
              isEditable: true,
            },
          ],
          apiPath: '/admin',
        },
        更新用户: {
          title: '更新用户',
          fields: [
            {
              id: 'email',
              label: '邮箱',
              type: 'email',
              placeholder: '请输入邮箱',
              required: true,
              isEditable: true,
            },
            {
              id: 'username',
              label: '用户名',
              type: 'text',
              placeholder: '请输入用户名',
              required: true,
              isEditable: true,
            },
            {
              id: 'password',
              label: '密码',
              type: 'password',
              placeholder: '请输入密码',
              required: true,
              isEditable: true,
            },
          ],
          apiPath: '/users',
        },
      },
      formData: {},
      currentTitle: '',
      currentFields: [],
      apiPath: '',
      inputId: '', // 用于存储用户输入的ID
    }
  },
  watch: {
    activeMainContent() {
      this.loadFormConfig()
      this.fetchData()
    },
    id() {
      this.fetchData()
    },
  },
  created() {
    this.loadFormConfig()
    this.fetchData()
  },
  methods: {
    loadFormConfig() {
      const config = this.updateConfig[this.activeMainContent]
      if (config) {
        this.currentTitle = config.title
        this.currentFields = config.fields
        this.apiPath = config.apiPath
        // 初始化表单数据
        this.formData = {}
        config.fields.forEach((field) => {
          this.formData[field.id] = ''
        })
      } else {
        console.error(`未知的更新类型: ${this.activeMainContent}`)
      }
    },
    async fetchData() {
      try {
        if (!this.id) {
          console.log('缺少数据ID')
          return
        }
        const path = `${this.apiPath}/${this.id}`
        const response = await DataService.get(path)
        if (response.data.success && response.data.data) {
          this.formData = response.data.data
        } else {
          alert(`获取数据失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        alert('获取数据失败: 请检查网络或联系管理员')
      }
    },
    async handleSubmit() {
      try {
        const path = `${this.apiPath}/update/${this.inputId}`
        const response = await DataService.put(path, this.formData)
        if (response.data.success) {
          alert('更新成功')
          // 刷新数据
          this.fetchData()
        } else {
          alert(`更新失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('更新失败:', error)
        alert('更新失败: 请检查网络或联系管理员')
      }
    },
    // 添加一个方法来根据输入的ID获取数据
    async fetchDataById() {
      if (!this.inputId) {
        // 如果没有输入ID，清空表单数据
        this.formData = {}
        return
      }
      try {
        const path = `${this.apiPath}/read/${this.inputId}`
        const response = await DataService.get(path)
        if (response.data.success && response.data.data) {
          this.formData = response.data.data
        } else {
          alert(`获取数据失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('获取数据失败:', error)
        alert('获取数据失败: 请检查网络或联系管理员')
      }
    },
  },
}
</script>

<style scoped>
.manage-update {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  background-color: var(--primary-color);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-btn {
  background-color: var(--main-color);
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.submit-btn:hover {
  background-color: var(--main-color);
}
</style>
