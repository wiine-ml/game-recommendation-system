import Vuex from 'vuex'
import UserInfoStore from './UserInfoStore'
import AdminInfoStore from './AdminInfoStore'
import VendorInfoStore from './VendorInfoStore'
import PreferenceStore from './PreferenceStore'

const store = new Vuex.Store({
  modules: {
    user: UserInfoStore,
    admin: AdminInfoStore,
    vendor: VendorInfoStore,

    preference: PreferenceStore,
  },
  getters: {
    isLogin: (state, getters) => {
      return getters['user/isLogin'] || getters['admin/isLogin'] || getters['vendor/isLogin']
    },
    currentLoginType: (state, getters) => {
      if (getters['user/isLogin']) {
        return 'user'
      } else if (getters['admin/isLogin']) {
        return getters['admin/adminType']
      } else if (getters['vendor/isLogin']) {
        return getters['vendor/vendorType'] // 返回厂商类型
      }
      return null
    },
  },
})

export default store
