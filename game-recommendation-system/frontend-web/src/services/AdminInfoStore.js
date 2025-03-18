// AdminInfoStore.js
import apiClient from './DataService'

const AdminInfoStore = {
  namespaced: true,
  state: {
    token: localStorage.getItem('adminToken') || null,
    isLogin: localStorage.getItem('adminToken') ? true : false,
    adminID: localStorage.getItem('adminID') || -1,
    adminName: localStorage.getItem('adminName') || 'Guest',
    adminType: localStorage.getItem('adminType') || null,
  },
  mutations: {
    setToken(state, myToken) {
      state.token = myToken
      localStorage.setItem('adminToken', myToken)
    },
    setIsLogin(state, newValue) {
      state.isLogin = newValue
    },
    setAdminName(state, name) {
      state.adminName = name
      localStorage.setItem('adminName', name)
    },
    setAdminID(state, id) {
      state.adminID = id
      localStorage.setItem('adminID', id)
    },
    setAdminType(state, type) {
      state.adminType = type
      localStorage.setItem('adminType', type)
    },
    removeToken(state) {
      state.token = null
      state.isLogin = false
      state.adminID = -1
      state.adminName = ''
      state.adminType = null
      localStorage.removeItem('adminToken')
      localStorage.removeItem('adminName')
      localStorage.removeItem('adminID')
      localStorage.removeItem('adminType')
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await apiClient.post('admin/login', credentials)
        const token = response.data.token
        const adminID = response.data.admin.id
        const adminName = response.data.admin.admin_name
        const adminType = response.data.admin.admin_type

        commit('setToken', token)
        commit('setIsLogin', true)
        commit('setAdminID', adminID)
        commit('setAdminName', adminName)
        commit('setAdminType', adminType)

        return { success: true, msg: 'Admin Login successful' }
      } catch {
        commit('setIsLogin', false)
        return { success: false, msg: 'Admin Login failed' }
      }
    },
    logout({ commit }) {
      commit('removeToken')
      return { success: true, msg: 'Admin Logout successful' }
    },
  },
  getters: {
    isLogin: (state) => state.isLogin,
    adminID: (state) => state.adminID,
    adminName: (state) => state.adminName,
    adminType: (state) => state.adminType,
  },
}

export default AdminInfoStore
