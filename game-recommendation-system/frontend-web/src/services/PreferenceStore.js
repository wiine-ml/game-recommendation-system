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
        name: '浅色主题',
        variables: {
          '--primary-color': '#777777',
          '--primary-color-alpha1': 'rgba(119, 119, 119, 0.85)',
          '--primary-color-alpha2': 'rgba(119, 119, 119, 0.5)',
          '--secondary-color': '#999999',
          '--secondary-color-alpha1': 'rgba(153, 153, 153, 0.85)',
          '--secondary-color-alpha2': 'rgba(153, 153, 153, 0.5)',
          '--secondary-color-light': '#f5f5f5',
          '--main-color': '#45a045',
          '--main-color-alpha1': 'rgba(69, 160, 69, 0.85)',
          '--main-color-alpha2': 'rgba(69, 160, 69, 0.5)',
          '--contrast-color': '#ffffff',
          '--contrast-color-alpha1': 'rgba(255, 255, 255, 0.85)',
          '--contrast-color-alpha2': 'rgba(255, 255, 255, 0.5)',
        },
      },
      {
        name: '紫色主题',
        variables: {
          '--primary-color': '#3a1c71',
          '--primary-color-alpha1': 'rgba(58, 28, 113, 0.85)',
          '--primary-color-alpha2': 'rgba(58, 28, 113, 0.5)',
          '--secondary-color': '#2a1557',
          '--secondary-color-alpha1': 'rgba(42, 21, 87, 0.85)',
          '--secondary-color-alpha2': 'rgba(42, 21, 87, 0.5)',
          '--secondary-color-light': '#4a2c82',
          '--main-color': '#7e57c2',
          '--main-color-alpha1': 'rgba(126, 87, 194, 0.85)',
          '--main-color-alpha2': 'rgba(126, 87, 194, 0.5)',
          '--contrast-color': '#f3e5f5',
          '--contrast-color-alpha1': 'rgba(243, 229, 245, 0.85)',
          '--contrast-color-alpha2': 'rgba(243, 229, 245, 0.5)',
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
