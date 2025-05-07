<template>
  <div class="vendor-head-image-manage">
    <!-- 头图预览区域 -->
    <div
      class="preview-container"
      :style="{ backgroundImage: `url(${this.currentHeadImage})` }"
      alt="厂商头图预览"
      v-if="hasHeadImage"
    ></div>
    <div class="placeholder" v-else>
      <p>暂未设置头图</p>
    </div>

    <!-- 文件上传区域 -->
    <div class="upload-container">
      <input
        type="file"
        ref="fileInput"
        accept="image/*"
        @change="handleFileChange"
        style="display: none"
      />
      <button class="upload-btn" @click="triggerFileInput">
        <span v-if="!uploading">上传头图</span>
        <span v-else>正在上传...</span>
      </button>
    </div>

    <!-- 清除头图按钮 -->
    <div class="clear-container" v-if="hasHeadImage">
      <button class="clear-btn" @click="confirmClearHeadImage">清除头图</button>
    </div>

    <!-- 提示信息 -->
    <div class="message" v-if="message">{{ message }}</div>
  </div>
</template>

<script>
import apiClient from '../services/DataService'

export default {
  data() {
    return {
      currentHeadImage: '',
      hasHeadImage: false, // 是否有头图
      uploading: false, // 是否正在上传
      message: '', // 提示信息
    }
  },
  async created() {
    // 页面加载时获取当前头图
    this.fetchCurrentHeadImage()
  },
  methods: {
    // 获取当前头图
    async fetchCurrentHeadImage() {
      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        if (!vendorId || !vendorType) {
          this.message = '无法获取厂商信息'
          return
        }

        const response = await apiClient.get('/vendor/head_image/read', {
          params: {
            vendor_id: vendorId,
            vendor_type: vendorType,
          },
          responseType: 'blob',
        })

        if (response.data) {
          console.log(response)
          this.currentHeadImage = URL.createObjectURL(response.data)
          this.hasHeadImage = true
        } else {
          this.currentHeadImage = ''
          this.hasHeadImage = false
        }
      } catch (error) {
        console.error('获取头图失败:', error)
        this.message = '获取头图失败，请重试'
      }
    },

    // 触发文件选择
    triggerFileInput() {
      this.$refs.fileInput.click()
    },

    // 处理文件选择
    handleFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        this.uploadHeadImage(file)
      }
    },

    // 上传头图
    async uploadHeadImage(file) {
      this.uploading = true
      this.message = ''

      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        if (!vendorId || !vendorType) {
          this.message = '无法获取厂商信息'
          this.uploading = false
          return
        }

        const formData = new FormData()
        formData.append('vendor_id', vendorId)
        formData.append('vendor_type', vendorType)
        formData.append('file', file)

        const response = await apiClient.post('/vendor/head_image/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        if (response.data.success) {
          this.message = '头图上传成功'
          this.fetchCurrentHeadImage() // 刷新头图预览
        } else {
          this.message = '头图上传失败'
        }
      } catch (error) {
        console.error('上传头图失败:', error)
        this.message = '上传头图失败，请重试'
      } finally {
        this.uploading = false
      }
    },

    // 确认清除头图
    confirmClearHeadImage() {
      if (confirm('确定要清除头图吗？')) {
        this.clearHeadImage()
      }
    },

    // 清除头图
    async clearHeadImage() {
      this.message = ''
      try {
        const vendorId = this.$store.getters['vendor/vendorID']
        const vendorType = this.$store.getters['vendor/vendorType']

        if (!vendorId || !vendorType) {
          this.message = '无法获取厂商信息'
          return
        }

        const response = await apiClient.delete('/vendor/head_image/delete', {
          params: {
            vendor_id: vendorId,
            vendor_type: vendorType,
          },
        })

        if (response.data.success) {
          this.message = '头图清除成功'
          this.currentHeadImage = ''
          this.hasHeadImage = false
        } else {
          this.message = '头图清除失败'
        }
      } catch (error) {
        console.error('清除头图失败:', error)
        this.message = '清除头图失败，请重试'
      }
    },
  },
}
</script>

<style scoped>
.vendor-head-image-manage {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.preview-container {
  width: 100%;
  height: 200px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
}

.head-image-preview {
  max-width: 100%;
  max-height: 190px;
}

.placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #999;
  font-size: 14px;
}

.upload-container {
  margin-bottom: 20px;
}

.upload-btn,
.clear-btn {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.upload-btn:hover,
.clear-btn:hover {
  background-color: #45a049;
}

.clear-container {
  margin-bottom: 20px;
}

.clear-btn {
  background-color: #f44336;
}

.clear-btn:hover {
  background-color: #d32f2f;
}

.message {
  color: var(--contrast-color);
  font-size: 14px;
  height: 20px;
}
</style>
