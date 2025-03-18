import Vuex from 'vuex'
import UserInfoStore from './UserInfoStore'
import AdminInfoStore from './AdminInfoStore'
import PreferenceStore from './PreferenceStore'

const store = new Vuex.Store({
  modules: {
    user: UserInfoStore,
    admin: AdminInfoStore,
    preference: PreferenceStore,
  },
  getters: {
    isLogin: (state, getters, rootState) => {
      // 检查用户或管理员是否登录
      return getters['user/isLogin'] || getters['admin/isLogin']
    },
    currentLoginType: (state, getters, rootState) => {
      // 判断当前登录类型
      if (getters['user/isLogin']) {
        return 'user'
      } else if (getters['admin/isLogin']) {
        return getters['admin/adminType']
      }
      return null
    },
  },
})

export default store
