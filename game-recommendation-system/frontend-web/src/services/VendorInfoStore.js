import apiClient from './DataService'

const VendorInfoStore = {
  namespaced: true,
  state: {
    token: localStorage.getItem('vendorToken') || null,
    isLogin: localStorage.getItem('vendorToken') ? true : false,
    vendorID: localStorage.getItem('vendorID') || -1,
    vendorName: localStorage.getItem('vendorName') || null,
    vendorType: localStorage.getItem('vendorType') || null, // 新增字段
    vendorAvatar: localStorage.getItem('vendorAvatar') || null,
    vendorProfile: localStorage.getItem('vendorProfile') || null,
    vendorWebsite: localStorage.getItem('vendorWebsite') || null,
    vendorHeadIllustrations: localStorage.getItem('vendorHeadIllustrations') || null,
    address: localStorage.getItem('address') || null,
    contactEmail: localStorage.getItem('contactEmail') || null,
    foundedYear: localStorage.getItem('foundedYear') || null,
  },
  mutations: {
    setToken(state, myToken) {
      state.token = myToken
      localStorage.setItem('vendorToken', myToken)
    },
    setIsLogin(state, newValue) {
      state.isLogin = newValue
    },
    setVendorID(state, id) {
      state.vendorID = id
      localStorage.setItem('vendorID', id)
    },
    setVendorName(state, name) {
      state.vendorName = name
      localStorage.setItem('vendorName', name)
    },
    setVendorType(state, type) {
      // 新增 mutation
      state.vendorType = type
      localStorage.setItem('vendorType', type)
    },
    setVendorAvatar(state, avatar) {
      state.vendorAvatar = avatar
      localStorage.setItem('vendorAvatar', avatar)
    },
    setVendorProfile(state, profile) {
      state.vendorProfile = profile
      localStorage.setItem('vendorProfile', profile)
    },
    setVendorWebsite(state, website) {
      state.vendorWebsite = website
      localStorage.setItem('vendorWebsite', website)
    },
    setVendorHeadIllustrations(state, headIllustrations) {
      state.vendorHeadIllustrations = headIllustrations
      localStorage.setItem('vendorHeadIllustrations', headIllustrations)
    },
    setAddress(state, address) {
      state.address = address
      localStorage.setItem('address', address)
    },
    setContactEmail(state, email) {
      state.contactEmail = email
      localStorage.setItem('contactEmail', email)
    },
    setFoundedYear(state, year) {
      state.foundedYear = year
      localStorage.setItem('foundedYear', year)
    },
    removeToken(state) {
      state.token = null
      state.isLogin = false
      state.vendorID = -1
      state.vendorName = ''
      state.vendorType = null // 新增字段重置
      state.vendorAvatar = null
      state.vendorProfile = null
      state.vendorWebsite = null
      state.vendorHeadIllustrations = null
      state.address = null
      state.contactEmail = null
      state.foundedYear = null

      localStorage.removeItem('vendorToken')
      localStorage.removeItem('vendorID')
      localStorage.removeItem('vendorName')
      localStorage.removeItem('vendorType') // 新增字段移除
      localStorage.removeItem('vendorAvatar')
      localStorage.removeItem('vendorProfile')
      localStorage.removeItem('vendorWebsite')
      localStorage.removeItem('vendorHeadIllustrations')
      localStorage.removeItem('address')
      localStorage.removeItem('contactEmail')
      localStorage.removeItem('foundedYear')
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await apiClient.post('vendor/login', {
          emailOrName: credentials.emailOrName,
          password: credentials.password,
        })

        console.log(response)

        const token = response?.data?.token
        const vendorID = response?.data?.vendor?.id
        const vendorName = response?.data?.vendor?.vendor_name
        const vendorType = response?.data?.vendor?.vendor_type
        const vendorAvatar = response?.data?.vendor?.vendor_avatar
        const vendorProfile = response?.data?.vendor?.vendor_profile
        const vendorWebsite = response?.data?.vendor?.vendor_website
        const vendorHeadIllustrations = response?.data?.vendor?.vendor_head_illustrations
        const address = response?.data?.vendor?.address
        const contactEmail = response?.data?.vendor?.contact_email
        const foundedYear = response?.data?.vendor?.founded_year

        commit('setToken', token)
        commit('setIsLogin', true)
        commit('setVendorID', vendorID)
        commit('setVendorName', vendorName)
        commit('setVendorType', vendorType) // 新增字段设置
        commit('setVendorAvatar', vendorAvatar)
        commit('setVendorProfile', vendorProfile)
        commit('setVendorWebsite', vendorWebsite)
        commit('setVendorHeadIllustrations', vendorHeadIllustrations)
        commit('setAddress', address)
        commit('setContactEmail', contactEmail)
        commit('setFoundedYear', foundedYear)

        return { success: true, msg: 'Vendor Login successful' }
      } catch (error) {
        commit('setIsLogin', false)
        return { success: false, msg: 'Vendor Login failed' + error }
      }
    },
    logout({ commit }) {
      commit('removeToken')
      return { success: true, msg: 'Vendor Logout successful' }
    },
  },
  getters: {
    isLogin: (state) => state.isLogin,
    vendorID: (state) => state.vendorID,
    vendorName: (state) => state.vendorName,
    vendorType: (state) => state.vendorType, // 新增字段获取
    vendorAvatar: (state) => state.vendorAvatar,
    vendorProfile: (state) => state.vendorProfile,
    vendorWebsite: (state) => state.vendorWebsite,
    vendorHeadIllustrations: (state) => state.vendorHeadIllustrations,
    address: (state) => state.address,
    contactEmail: (state) => state.contactEmail,
    foundedYear: (state) => state.foundedYear,
  },
}

export default VendorInfoStore
