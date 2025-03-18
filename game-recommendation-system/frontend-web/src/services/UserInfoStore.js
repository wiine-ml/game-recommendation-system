import apiClient from './DataService'
import { register } from './DataService'

const UserInfoStore = {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || null,
    isLogin: localStorage.getItem('token') ? true : false,
    userID: localStorage.getItem('userID') || -1,
    userName: localStorage.getItem('userName') || 'Guest',
    avatarFile: null, // 存储头像文件
    avatarUrl: localStorage.getItem('avatarUrl') || '', // 存储头像预览 URL
  },
  mutations: {
    setToken(state, myToken) {
      state.token = myToken
      localStorage.setItem('token', myToken)
    },
    setIsLogin(state, newValue) {
      state.isLogin = newValue
    },
    setUserName(state, name) {
      state.userName = name
      localStorage.setItem('userName', name)
    },
    setUserID(state, id) {
      state.userID = id
      localStorage.setItem('userID', id)
    },
    setAvatarFile(state, file) {
      state.avatarFile = file
      // 如果有文件，生成预览 URL
      if (file) {
        state.avatarUrl = URL.createObjectURL(file)
      } else {
        state.avatarUrl = ''
      }
      localStorage.setItem('avatarUrl', state.avatarUrl)
    },
    removeToken(state) {
      state.token = null
      state.isLogin = false
      state.userID = -1
      state.userName = ''

      state.avatarFile = null
      state.avatarUrl = ''
      localStorage.removeItem('token')
      localStorage.removeItem('userName')
      localStorage.removeItem('userID')
      localStorage.removeItem('avatarUrl')
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        console.log('login credentials', credentials)
        const response = await apiClient.post('/user/login', {
          emailOrName: credentials.emailOrName,
          password: credentials.password,
        })
        const token = response.data.data.token
        const userID = response.data.data.id
        const userName = response.data.data.username
        const avatarFile = response.data.data.avatar

        commit('setToken', token)
        commit('setIsLogin', true)
        commit('setUserID', userID)
        commit('setUserName', userName)
        commit('setAvatarFile', avatarFile)

        return { success: true, msg: 'Login successful' }
      } catch {
        commit('setIsLogin', false)
        return { success: false, msg: 'Login failed' }
      }
    },
    async register(credentials) {
      try {
        const response = await register(
          credentials.email,
          credentials.username,
          credentials.password,
        )
        if (response.data.success) {
          return { success: true, msg: 'Registration successful' }
        } else {
          return { success: false, msg: 'Registration failed' }
        }
      } catch (error) {
        return { success: false, msg: 'Registration failed' + error }
      }
    },
    logout({ commit }) {
      commit('removeToken')
      return { success: true, msg: 'Logout successful' }
    },
    async fetchAvatar({ state }) {
      if (!state.isLogin) {
        return { success: false, msg: 'User not logged in' }
      }
      try {
        const response = await apiClient.get('/users/avatar/read', {
          params: {
            user_id: state.userID,
          },
          responseType: 'blob', // 指定响应类型为二进制数据
        })
        const avatarFile = new File([response.data], 'avatar.jpg', { type: 'image/jpeg' })
        return { success: true, data: { avatarFile } }
      } catch (error) {
        console.error('Fetch avatar failed:', error)
        return { success: false, msg: 'Fetch avatar failed' }
      }
    },
    async uploadAvatar({ state }, file) {
      if (!state.isLogin) {
        return { success: false, msg: 'User not logged in' }
      }
      try {
        const formData = new FormData()
        formData.append('user_id', state.userID)
        formData.append('avatar', file)

        await apiClient.post('/users/avatar/set', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          file: file,
        })

        return { success: true, msg: 'Avatar uploaded successfully' }
      } catch (error) {
        console.error('Upload avatar failed:', error)
        return { success: false, msg: 'Upload avatar failed' }
      }
    },
    async deleteAvatar({ state }) {
      if (!state.isLogin) {
        return { success: false, msg: 'User not logged in' }
      }
      try {
        await apiClient.post('/users/avatar/delete', {
          user_id: state.userID,
        })

        return { success: true, msg: 'Avatar deleted successfully' }
      } catch (error) {
        console.error('Delete avatar failed:', error)
        return { success: false, msg: 'Delete avatar failed' }
      }
    },
  },
  getters: {
    isLogin: (state) => state.isLogin,
    userID: (state) => state.userID,
    userName: (state) => state.userName,
    avatarUrl: (state) => state.avatarUrl, // 获取头像预览 URL
  },
}

export default UserInfoStore
