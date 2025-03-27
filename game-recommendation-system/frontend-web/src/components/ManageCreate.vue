<template>
  <h2>{{ currentTitle }}</h2>
  <div class="manage-create">
    <form @submit.prevent="handleSubmit">
      <div class="form-group" v-for="(field, index) in currentFields" :key="index">
        <label :for="field.id">{{ field.label }}</label>
        <input
          :type="field.type"
          :id="field.id"
          v-model="formData[field.id]"
          :placeholder="field.placeholder"
          :required="field.required"
        />
      </div>
      <button type="submit" class="submit-btn">创建</button>
    </form>
  </div>
</template>

<script>
import DataService from '../services/DataService.js'
import store from '@/services/Store'

export default {
  name: 'ManageCreate',
  props: {
    activeMainContent: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // 定义不同创建功能的配置
      createConfig: {
        创建公告: {
          title: '创建公告',
          fields: [
            { id: 'title', label: '标题', type: 'text', placeholder: '请输入标题', required: true },
            {
              id: 'content',
              label: '内容',
              type: 'text',
              placeholder: '请输入内容',
              required: true,
            },
          ],
          apiPath: '/notice',
        },
        创建新闻: {
          title: '创建新闻',
          fields: [
            { id: 'title', label: '标题', type: 'text', placeholder: '请输入标题', required: true },
            {
              id: 'description',
              label: '描述',
              type: 'text',
              placeholder: '请输入描述',
              required: true,
            },
            { id: 'type', label: '类型', type: 'text', placeholder: '请输入类型', required: true },
            {
              id: 'image',
              label: '图片URL',
              type: 'text',
              placeholder: '请输入图片URL',
              required: true,
            },
          ],
          apiPath: '/news',
        },
        创建游戏: {
          title: '创建游戏',
          fields: [
            {
              id: 'gameTitle',
              label: '游戏名称',
              type: 'text',
              placeholder: '请输入游戏名称',
              required: true,
            },
            {
              id: 'gameGenre',
              label: '游戏类型',
              type: 'text',
              placeholder: '请输入游戏类型',
              required: true,
            },
            {
              id: 'gamePlatform',
              label: '游戏平台',
              type: 'text',
              placeholder: '请输入游戏平台',
              required: true,
            },
            {
              id: 'releaseYear',
              label: '发行年份',
              type: 'number',
              placeholder: '请输入发行年份',
              required: true,
            },
            {
              id: 'releaseMonth',
              label: '发行月份',
              type: 'number',
              placeholder: '请输入发行月份',
              required: true,
            },
            {
              id: 'releaseDay',
              label: '发行日期',
              type: 'number',
              placeholder: '请输入发行日期',
              required: true,
            },
          ],
          apiPath: '/games',
        },
        创建管理员: {
          title: '创建管理员',
          fields: [
            {
              id: 'admin_name',
              label: '管理员名称',
              type: 'text',
              placeholder: '请输入管理员名称',
              required: true,
            },
            {
              id: 'password',
              label: '密码',
              type: 'password',
              placeholder: '请输入密码',
              required: true,
            },
            {
              id: 'admin_type',
              label: '管理员类型',
              type: 'text',
              placeholder: '请输入管理员类型',
              required: true,
            },
          ],
          apiPath: '/admin',
        },
        //vendor
        上架游戏: {
          title: '创建游戏',
          fields: [
            {
              id: 'gameTitle',
              label: '游戏名称',
              type: 'text',
              placeholder: '请输入游戏名称',
              required: true,
            },
            {
              id: 'gameGenre',
              label: '游戏类型',
              type: 'text',
              placeholder: '请输入游戏类型',
              required: true,
            },
            {
              id: 'gamePlatform',
              label: '游戏平台',
              type: 'text',
              placeholder: '请输入游戏平台',
              required: true,
            },
            {
              id: 'releaseYear',
              label: '发行年份',
              type: 'number',
              placeholder: '请输入发行年份',
              required: true,
            },
            {
              id: 'releaseMonth',
              label: '发行月份',
              type: 'number',
              placeholder: '请输入发行月份',
              required: true,
            },
            {
              id: 'releaseDay',
              label: '发行日期',
              type: 'number',
              placeholder: '请输入发行日期',
              required: true,
            },
          ],
          apiPath: '/games',
        },
        发布新闻: {
          title: '创建新闻',
          fields: [
            { id: 'title', label: '标题', type: 'text', placeholder: '请输入标题', required: true },
            {
              id: 'description',
              label: '描述',
              type: 'text',
              placeholder: '请输入描述',
              required: true,
            },
            { id: 'type', label: '类型', type: 'text', placeholder: '请输入类型', required: true },
            {
              id: 'image',
              label: '图片URL',
              type: 'text',
              placeholder: '请输入图片URL',
              required: true,
            },
          ],
          apiPath: '/news',
        },
      },
      formData: {},
      currentTitle: '',
      currentFields: [],
      apiPath: '',
    }
  },
  watch: {
    activeMainContent() {
      this.loadFormConfig()
    },
  },
  created() {
    this.loadFormConfig()
  },
  methods: {
    loadFormConfig() {
      const config = this.createConfig[this.activeMainContent]
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
        console.error(`未知的创建类型: ${this.activeMainContent}`)
      }
    },
    async handleSubmit() {
      try {
        this.formData.userID = store.getters['user/userID']
        this.formData.username = store.getters['user/username']
        const response = await DataService.post(this.apiPath + '/create', this.formData)
        if (response.data.success) {
          alert('创建成功')
          // 清空表单
          this.currentFields.forEach((field) => {
            this.formData[field.id] = ''
          })
        } else {
          alert(`创建失败: ${response.data.msg || '未知错误'}`)
        }
      } catch (error) {
        console.error('创建失败:', error)
        alert('创建失败: 请检查网络或联系管理员')
      }
    },
  },
}
</script>

<style scoped>
.manage-create {
  max-width: 600px;
  margin: 0 auto;
  border-radius: 10px;
  padding: 20px;
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
