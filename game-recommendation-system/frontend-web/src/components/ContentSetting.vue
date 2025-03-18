<template>
  <div class="content-setting">
    <h2>主题设置</h2>
    <div class="current-theme">
      <span>当前主题: </span>
      <span>{{ currentThemeName }}</span>
    </div>
    <div class="theme-selector">
      <div class="theme-option" v-for="(theme, index) in themes" :key="index">
        <button @click="changeTheme(theme)" :style="themePreviewStyle(theme)">
          {{ theme.name }}
        </button>
      </div>
    </div>

    <hr />

    <h2>显示设置</h2>
    <div class="display-settings">
      <div class="setting-item">
        <span for="itemPerpage">每页显示数: </span>
        <input
          type="number"
          id="itemPerpage"
          v-model.number="selectedItemPerpage"
          min="5"
          max="100"
        />
        <span class="hint"> 数值过大会导致卡顿</span>
      </div>
    </div>

    <hr />
  </div>
</template>

<script>
export default {
  computed: {
    // 获取主题列表
    themes() {
      return this.$store.getters['preference/themes']
    },
    // 获取当前主题名称
    currentThemeName() {
      const currentTheme = this.$store.getters['preference/currentTheme']
      if (!currentTheme) {
        return '默认主题'
      }
      return (
        this.themes.find((theme) =>
          Object.entries(theme.variables).every(
            ([key, value]) =>
              getComputedStyle(document.documentElement).getPropertyValue(key).trim() === value,
          ),
        )?.name || '自定义主题'
      )
    },
    selectedItemPerpage: {
      get() {
        return this.$store.getters['preference/itemPerpage']
      },
      set(value) {
        this.$store.dispatch('preference/setItemPerpage', value)
        localStorage.setItem('itemPerpage', value) // 保存到本地存储
      },
    },
  },
  methods: {
    // 切换主题
    changeTheme(theme) {
      this.$store.dispatch('preference/changeTheme', theme)
    },
    // 获取主题预览样式
    themePreviewStyle(theme) {
      return {
        backgroundColor: theme.variables['--main-color'],
        color: this.getReadableColor(theme.variables['--main-color']),
      }
    },
    // 获取可读文字颜色
    getReadableColor(bgColor) {
      const color = bgColor.replace(/#/g, '').substring(0, 6)
      const r = parseInt(color.substring(0, 2), 16)
      const g = parseInt(color.substring(2, 4), 16)
      const b = parseInt(color.substring(4, 6), 16)
      const brightness = (r * 299 + g * 587 + b * 114) / 1000
      return brightness > 128 ? '#000000' : '#ffffff'
    },
  },
}
</script>

<style scoped>
#itemPerpage {
  width: fit-content;
}

.hint {
  color: var(--contrast-color-alpha2);
}

hr {
  margin-top: 20px;
  margin-bottom: 20px;
  border: 0;
  height: 1px;
  background: #333;
  background-image: linear-gradient(
    to right,
    var(--secondary-color),
    var(--main-color),
    var(--secondary-color)
  );
}

.content-setting {
  padding: 20px;
  margin: 20px;
  border: 1px solid var(--secondary-color);
  border-radius: 8px;
  background-color: var(--secondary-color);
}

.theme-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 15px;
}

.theme-option button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s;
}

.theme-option button:hover {
  transform: scale(1.05);
}

.display-settings,
.current-theme {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid var(--secondary-color);
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>
