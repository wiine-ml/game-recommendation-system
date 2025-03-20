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
    isLogin: (state, getters, rootState) => {
      // 检查是否登录
      console.log('用户登陆:' + getters['user/isLogin'])
      console.log('管理员登陆:' + getters['admin/isLogin'])
      console.log('厂商登陆:' + getters['vendor/isLogin'])
      return getters['user/isLogin'] || getters['admin/isLogin'] || getters['vendor/isLogin']
    },
    currentLoginType: (state, getters, rootState) => {
      // 判断当前登录类型
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
