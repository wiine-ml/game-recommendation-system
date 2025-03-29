const PreferenceStore = {
  namespaced: true,
  state: {
    themes: [
      {
        name: '默认主题',
        variables: {
          '--primary-color': '#222831',
          '--primary-color-alpha1': 'rgba(34, 40, 49, 0.85)', // 透明度 80%
          '--primary-color-alpha2': 'rgba(34, 40, 49, 0.5)', // 透明度 50%
          '--secondary-color': '#393e46',
          '--secondary-color-alpha1': 'rgba(57, 62, 70, 0.85)',
          '--secondary-color-alpha2': 'rgba(57, 62, 70, 0.5)',
          '--secondary-color-light': '#414e56',
          '--main-color': '#00adb5',
          '--main-color-alpha1': 'rgba(0, 173, 181, 0.85)',
          '--main-color-alpha2': 'rgba(0, 173, 181, 0.5)',
          '--contrast-color': '#eeeeee',
          '--contrast-color-alpha1': 'rgba(238, 238, 238, 0.85)',
          '--contrast-color-alpha2': 'rgba(238, 238, 238, 0.5)',
        },
      },
      {
        name: '深色主题',
        variables: {
          '--primary-color': '#1a1a1a',
          '--primary-color-alpha1': 'rgba(26, 26, 26, 0.85)',
          '--primary-color-alpha2': 'rgba(26, 26, 26, 0.5)',
          '--secondary-color': '#2d2d2d',
          '--secondary-color-alpha1': 'rgba(45, 45, 45, 0.8)',
          '--secondary-color-alpha2': 'rgba(45, 45, 45, 0.5)',
          '--secondary-color-light': '#3a3a3a',
          '--main-color': '#007acc',
          '--main-color-alpha1': 'rgba(0, 122, 204, 0.85)',
          '--main-color-alpha2': 'rgba(0, 122, 204, 0.5)',
          '--contrast-color': '#f5f5f5',
          '--contrast-color-alpha1': 'rgba(245, 245, 245, 0.85)',
          '--contrast-color-alpha2': 'rgba(245, 245, 245, 0.5)',
        },
      },
      {
        name: '紫色主题',
        variables: {
          '--primary-color': '#6a4c93', // 紫色，作为主要颜色
          '--primary-color-alpha1': 'rgba(106, 76, 147, 0.85)',
          '--primary-color-alpha2': 'rgba(106, 76, 147, 0.5)',
          '--secondary-color': '#8a6bb8', // 稍微浅一点的紫色，作为辅助颜色
          '--secondary-color-alpha1': 'rgba(138, 107, 184, 0.85)',
          '--secondary-color-alpha2': 'rgba(138, 107, 184, 0.5)',
          '--secondary-color-light': '#b8a8d2', // 更浅的紫色
          '--main-color': '#9b59b6', // 中等饱和度的紫色，具有较高的辨识度
          '--main-color-alpha1': 'rgba(155, 89, 182, 0.85)',
          '--main-color-alpha2': 'rgba(155, 89, 182, 0.5)',
          '--contrast-color': '#f5f0ff', // 浅紫色，与紫色形成对比
          '--contrast-color-alpha1': 'rgba(245, 240, 255, 0.85)',
          '--contrast-color-alpha2': 'rgba(245, 240, 255, 0.5)',
        },
      },
      {
        name: '橙色主题',
        variables: {
          '--primary-color': '#e67e22', // 橙色，作为主要颜色
          '--primary-color-alpha1': 'rgba(230, 126, 34, 0.85)',
          '--primary-color-alpha2': 'rgba(230, 126, 34, 0.5)',
          '--secondary-color': '#f39c12', // 稍微浅一点的橙色，作为辅助颜色
          '--secondary-color-alpha1': 'rgba(243, 156, 18, 0.85)',
          '--secondary-color-alpha2': 'rgba(243, 156, 18, 0.5)',
          '--secondary-color-light': '#fad6a0', // 更浅的橙色
          '--main-color': '#d35400', // 中等饱和度的橙色，具有较高的辨识度
          '--main-color-alpha1': 'rgba(211, 84, 0, 0.85)',
          '--main-color-alpha2': 'rgba(211, 84, 0, 0.5)',
          '--contrast-color': '#f9f3e9', // 浅米色，与橙色形成对比
          '--contrast-color-alpha1': 'rgba(249, 243, 233, 0.85)',
          '--contrast-color-alpha2': 'rgba(249, 243, 233, 0.5)',
        },
      },
      {
        name: '粉色主题',
        variables: {
          '--primary-color': '#ffc7c7', // 浅粉色，作为主要颜色
          '--primary-color-alpha1': 'rgba(255, 199, 199, 0.85)',
          '--primary-color-alpha2': 'rgba(255, 199, 199, 0.5)',
          '--secondary-color': '#ffe2e2', // 更浅的粉色，作为辅助颜色
          '--secondary-color-alpha1': 'rgba(255, 226, 226, 0.85)',
          '--secondary-color-alpha2': 'rgba(255, 226, 226, 0.5)',
          '--secondary-color-light': '#fff0f0', // 最浅的粉色
          '--main-color': '#ff9a9e', // 中等饱和度的粉色，具有较高的辨识度
          '--main-color-alpha1': 'rgba(255, 154, 158, 0.85)',
          '--main-color-alpha2': 'rgba(255, 154, 158, 0.5)',
          '--contrast-color': '#8785a2', // 深灰色，与粉色形成对比
          '--contrast-color-alpha1': 'rgba(135, 133, 162, 0.85)',
          '--contrast-color-alpha2': 'rgba(135, 133, 162, 0.5)',
        },
      },
      {
        name: '灰色主题',
        variables: {
          '--primary-color': '#757575',
          '--primary-color-alpha1': 'rgba(117, 117, 117, 0.85)',
          '--primary-color-alpha2': 'rgba(117, 117, 117, 0.5)',
          '--secondary-color': '#9e9e9e',
          '--secondary-color-alpha1': 'rgba(158, 158, 158, 0.85)',
          '--secondary-color-alpha2': 'rgba(158, 158, 158, 0.5)',
          '--secondary-color-light': '#e0e0e0',
          '--main-color': '#424242',
          '--main-color-alpha1': 'rgba(66, 66, 66, 0.85)',
          '--main-color-alpha2': 'rgba(66, 66, 66, 0.5)',
          '--contrast-color': '#ffffff',
          '--contrast-color-alpha1': 'rgba(255, 255, 255, 0.85)',
          '--contrast-color-alpha2': 'rgba(255, 255, 255, 0.5)',
        },
      },
    ],
    currentTheme: null,
    itemPerpage: 20,
  },
  mutations: {
    setCurrentTheme(state, theme) {
      state.currentTheme = theme
    },
    setItemPerpage(state, value) {
      state.itemPerpage = value
    },
  },
  actions: {
    changeTheme({ commit, dispatch }, theme) {
      // 切换主题
      Object.entries(theme.variables).forEach(([variable, value]) => {
        document.documentElement.style.setProperty(variable, value)
      })
      commit('setCurrentTheme', theme)
      dispatch('saveThemeToStorage', theme)
    },
    saveThemeToStorage({ state }, theme) {
      // 保存主题到本地存储
      const themeIndex = state.themes.findIndex((t) =>
        Object.entries(t.variables).every(([key, value]) => theme.variables[key] === value),
      )
      if (themeIndex !== -1) {
        localStorage.setItem('selectedThemeIndex', themeIndex)
      } else {
        localStorage.setItem('customTheme', JSON.stringify(theme.variables))
      }
    },
    loadThemeFromStorage({ commit, state, dispatch }) {
      // 从本地存储加载主题
      const savedThemeIndex = localStorage.getItem('selectedThemeIndex')
      if (savedThemeIndex !== null) {
        const index = parseInt(savedThemeIndex)
        if (state.themes[index]) {
          commit('setCurrentTheme', state.themes[index])
          dispatch('changeTheme', state.themes[index])
          return
        }
      }

      const customTheme = localStorage.getItem('customTheme')
      if (customTheme) {
        const variables = JSON.parse(customTheme)
        const customThemeObj = { name: '自定义主题', variables }
        dispatch('changeTheme', customThemeObj)
      }
    },
    setItemPerpage({ commit }, value) {
      commit('setItemPerpage', value)
    },
    loadItemPerpageFromStorage({ commit }) {
      // 从本地存储加载每页显示数
      const savedItemPerpage = localStorage.getItem('itemPerpage')
      if (savedItemPerpage !== null) {
        commit('setItemPerpage', parseInt(savedItemPerpage))
      }
    },
  },
  getters: {
    currentTheme: (state) => state.currentTheme,
    themes: (state) => state.themes,
    itemPerpage: (state) => state.itemPerpage,
  },
}

export default PreferenceStore
