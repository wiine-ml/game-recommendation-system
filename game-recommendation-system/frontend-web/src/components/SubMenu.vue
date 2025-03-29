<template>
  <div class="container">
    <div class="sidebar">
      <h3 id="sub-menu-title">{{ activeSubMenu }}</h3>
      <ul>
        <li v-for="(item, index) in GetSubMenuItem()" :key="index">
          <a
            :href="item.link"
            @click.prevent="SelectMenuItem(item.text)"
            :class="{ active: item.text === activeItem }"
          >
            <span v-if="item.translation" class="translation"> {{ item.translation }} / </span>
            {{ item.text }}
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: ['activeSubMenu', 'activeMainContent'],
  data() {
    return {
      activeItem: null,
      menuItemMap: {
        首页: [
          { text: '热门', link: 'hot' },
          { text: '公告', link: 'noice' },
          { text: '关于', link: 'contact' },
          { text: '设置', link: 'settings' },
        ],
        推荐: [
          { text: '为你推荐', link: '#' },
          { text: '最新上架', link: '#' },
          { text: '最高评分', link: '#' },
          { text: '最受欢迎', link: '#' },
        ],
        类别: [
          { text: '全部', link: '#全部', translation: '' },
          { text: 'Action', link: '#', translation: '动作' },
          { text: 'Adventure', link: '#', translation: '冒险' },
          { text: 'Compilation', link: '#', translation: '合集' },
          { text: 'Educational', link: '#', translation: '教育' },
          { text: 'Fighting', link: '#', translation: '格斗' },
          { text: 'Platformer', link: '#', translation: '平台' },
          { text: 'Puzzle', link: '#', translation: '益智' },
          { text: 'RPG', link: '#', translation: '角色扮演' },
          { text: 'Strategy', link: '#', translation: '策略' },
          { text: 'Simulation', link: '#', translation: '模拟' },
          { text: 'Battle', link: '#', translation: '战斗' },
          { text: 'Card', link: '#', translation: '卡牌' },
        ],
        新闻: [
          { text: '游戏杂谈', link: '#' },
          { text: 'PC游戏', link: '#' },
          { text: '主机游戏', link: '#' },
          { text: '手机游戏', link: '#' },
        ],
        我的: [
          { text: '关注', link: '#' },
          { text: '我的评分', link: '#' },
          { text: '账号信息', link: '#' },
        ],
        //manage
        公告管理: [
          { text: '查询公告', link: '#' },
          { text: '创建公告', link: '#' },
          { text: '更新公告', link: '#' },
          { text: '删除公告', link: '#' },
        ],
        推荐管理: [
          { text: '推荐参数', link: '#' },
          { text: '推荐状态', link: '#' },
        ],
        新闻管理: [
          { text: '查询新闻', link: '#' },
          { text: '创建新闻', link: '#' },
          { text: '更新新闻', link: '#' },
          { text: '删除新闻', link: '#' },
        ],
        游戏管理: [
          { text: '查询游戏', link: '#' },
          { text: '创建游戏', link: '#' },
          { text: '更新游戏', link: '#' },
          { text: '删除游戏', link: '#' },
        ],
        用户管理: [
          { text: '查询用户', link: '#' },
          { text: '更新用户', link: '#' },
          { text: '删除用户', link: '#' },
        ],
        管理员管理: [
          { text: '查询管理员', link: '#' },
          { text: '创建管理员', link: '#' },
          { text: '更新管理员', link: '#' },
          { text: '删除管理员', link: '#' },
        ],
        //vendor
        主页管理: [
          { text: '主页预览', link: '#' },
          { text: '主页插画', link: '#' },
          { text: '主页推广', link: '#' },
          { text: '主页设置', link: '#' },
        ],
        厂商游戏管理: [
          { text: '查询游戏', link: '#' },
          { text: '上架游戏', link: '#' },
          { text: '更新游戏', link: '#' },
          { text: '下架游戏', link: '#' },
        ],
        厂商新闻管理: [
          { text: '查询新闻', link: '#' },
          { text: '发布新闻', link: '#' },
          { text: '下架新闻', link: '#' },
        ],
      },
    }
  },
  emits: ['UpdateMainContent'],
  methods: {
    GetSubMenuItem() {
      return this.menuItemMap[this.activeSubMenu]
    },
    SelectMenuItem(Content) {
      this.$emit('UpdateMainContent', Content)
      this.activeItem = Content
    },
  },
}
</script>

<style scoped>
ul {
  border-radius: 10px;
  border: 5px solid var(--primary-color-alpha2);
  border-top: 0px;
  border-bottom: 0px;
}

h3 {
  background-color: var(--primary-color);
  padding: 5px;
  border-radius: 10px;
  text-align: center;
  color: var(--main-color);
  margin-bottom: 5px;
}

.container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: var(--secondary-color);
  padding: 20px;
  justify-content: flex-start;
  flex-grow: 1;
  align-self: stretch;
  border-radius: 10px;
  box-shadow: 0 0 5px var(--secondary-color);
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
}

.sidebar li {
  border-radius: 10px;
  margin: 10px;
}

.sidebar a {
  border-radius: 13px;
  text-align: center;
  text-decoration: none;
  color: var(--contrast-color);
  display: block;
  padding: 10px;
}

.sidebar a:hover {
  background-color: var(--main-color);
  box-shadow: 0 0 5px var(--main-color);
}

.sidebar a.active {
  background-color: var(--main-color);
  color: #fff;
  box-shadow: 0 0 5px var(--main-color);
}
</style>
