import apiClient from './DataService'

const VendorInfoStore = {
  namespaced: true,
  state: {
    token: localStorage.getItem('vendorToken') || null,
    isLogin: localStorage.getItem('vendorToken') ? true : false,
    vendorID: localStorage.getItem('vendorID') || -1,
    vendorName: localStorage.getItem('vendorName') || null,
    vendorType: localStorage.getItem('vendorType') || null,
    vendorAvatar: localStorage.getItem('vendorAvatar') || null,
    vendorProfile: localStorage.getItem('vendorProfile') || null,
    vendorWebsite: localStorage.getItem('vendorWebsite') || null,
    vendorHeadIllustrations: localStorage.getItem('vendorHeadIllustrations') || null,
    address: localStorage.getItem('address') || null,
    contactEmail: localStorage.getItem('contactEmail') || null,
    foundedYear: localStorage.getItem('foundedYear') || null,
    avatarFile: null, // 存储头像文件
    avatarUrl: localStorage.getItem('vendorAvatarUrl') || '', // 存储头像预览 URL
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
    setAvatarFile(state, file) {
      state.avatarFile = file
      // 如果有文件，生成预览 URL
      if (file) {
        state.avatarUrl = URL.createObjectURL(file)
      } else {
        state.avatarUrl = ''
      }
      localStorage.setItem('vendorAvatarUrl', state.avatarUrl)
    },
    setAvatarUrl(state, url) {
      state.avatarUrl = url
      localStorage.setItem('vendorAvatarUrl', url)
    },
    removeToken(state) {
      state.token = null
      state.isLogin = false
      state.vendorID = -1
      state.vendorName = ''
      state.vendorType = null
      state.vendorAvatar = null
      state.vendorProfile = null
      state.vendorWebsite = null
      state.vendorHeadIllustrations = null
      state.address = null
      state.contactEmail = null
      state.foundedYear = null
      state.avatarFile = null
      state.avatarUrl = ''
      localStorage.removeItem('vendorToken')
      localStorage.removeItem('vendorID')
      localStorage.removeItem('vendorName')
      localStorage.removeItem('vendorType')
      localStorage.removeItem('vendorAvatar')
      localStorage.removeItem('vendorProfile')
      localStorage.removeItem('vendorWebsite')
      localStorage.removeItem('vendorHeadIllustrations')
      localStorage.removeItem('address')
      localStorage.removeItem('contactEmail')
      localStorage.removeItem('foundedYear')
      localStorage.removeItem('vendorAvatarUrl')
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

        const token = response.data.data.token
        const vendorID = response.data.data.vendor.id
        const vendorName = response.data.data.vendor.vendor_name
        const vendorType = response.data.data.vendor.vendor_type
        const vendorAvatar = response.data.data.vendor.vendor_avatar
        const vendorProfile = response.data.data.vendor.vendor_profile
        const vendorWebsite = response.data.data.vendor.vendor_website
        const vendorHeadIllustrations = response.data.data.vendor.vendor_head_illustrations
        const address = response.data.data.vendor.address
        const contactEmail = response.data.data.vendor.contact_email
        const foundedYear = response.data.data.vendor.founded_year

        commit('setToken', token)
        commit('setIsLogin', true)
        commit('setVendorID', vendorID)
        commit('setVendorName', vendorName)
        commit('setVendorType', vendorType)
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
    async fetchAvatar({ commit, state }) {
      try {
        const response = await apiClient.get('/vendor/avatar/read', {
          params: { vendor_id: state.vendorID, vendor_type: state.vendorType },
          responseType: 'blob',
        })

        //
        const blob = new Blob([response.data], { type: response.headers['content-type'] })
        const avatarUrl = URL.createObjectURL(blob)
        commit('setAvatarUrl', avatarUrl)

        commit('setAvatarUrl', avatarUrl) // 需要添加对应的 mutation
        console.log('Blob size:' + blob.size)
        return { success: true }
      } catch (error) {
        console.error('Fetch avatar failed:', error)
        return { success: false }
      }
    },
    async uploadAvatar({ state }, file) {
      if (!state.isLogin) {
        return { success: false, msg: 'Vendor not logged in' }
      }
      try {
        const formData = new FormData()
        formData.append('vendor_id', state.vendorID)
        formData.append('vendor_type', state.vendorType)
        formData.append('avatar', file)

        await apiClient.post('/vendor/avatar/set', formData, {
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
        return { success: false, msg: 'Vendor not logged in' }
      }
      try {
        await apiClient.post('/vendor/avatar/delete', {
          vendor_id: state.vendorID,
          vendor_type: state.vendorType,
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
    vendorID: (state) => state.vendorID,
    vendorName: (state) => state.vendorName,
    vendorType: (state) => state.vendorType,
    vendorAvatar: (state) => state.vendorAvatar,
    vendorProfile: (state) => state.vendorProfile,
    vendorWebsite: (state) => state.vendorWebsite,
    vendorHeadIllustrations: (state) => state.vendorHeadIllustrations,
    address: (state) => state.address,
    contactEmail: (state) => state.contactEmail,
    foundedYear: (state) => state.foundedYear,
    avatarUrl: (state) => state.avatarUrl, // 获取头像预览 URL
  },
}

export default VendorInfoStore
