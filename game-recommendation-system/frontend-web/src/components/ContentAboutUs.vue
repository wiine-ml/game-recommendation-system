<template>
  <hr />
  <h2 class="title" id="intro">欢迎使用 GRS 游戏推荐系统</h2>
  <hr />

  <div class="content-flat">
    <div class="content-item" v-for="(item, index) in contents" :key="index">
      <h2 class="title" v-if="item.mainTitle">{{ item.mainTitle }}</h2>
      <div class="content">
        <h3 class="sub-title">{{ item.para.subTitle }}</h3>
        <div v-if="item.para.content">
          <p class="para-content">{{ item.para.content }}</p>
        </div>

        <div v-else-if="item.para.multiLine && item.para.multiLine.length > 0">
          <p class="para-content" v-for="(line, lineIndex) in item.para.multiLine" :key="lineIndex">
            {{ line }}
          </p>
        </div>

        <div v-else></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['activeMainContent'],
  data() {
    return {
      contents: [
        {
          mainTitle: '',
          para: {
            subTitle: '团队及其使命介绍',
            content:
              '各位玩家朋友们，欢迎使用GRS游戏推荐系统！我们是一支充满活力与创意的团队，致力于打造个性化、贴心的游戏推荐服务。从游戏的开发背景、玩法特色到玩家评分、热门推荐，我们应有尽有，只为帮助你找到最适合自己的游戏。',
          },
        },
        {
          mainTitle: '',
          para: {
            subTitle: '我们的核心价值观',
            content:
              '在GRS游戏推荐系统，我们始终坚持以下核心价值观：我们的一切努力都以玩家的需求为中心，致力于为玩家提供最优质的游戏推荐服务。创新驱动。我们不断探索和尝试新的技术和方法，以提升我们的推荐算法和服务质量。合作共赢。我们与玩家社区紧密合作，共同推动游戏行业的发展。我们相信，只有坚持这些，我们才能真正为玩家创造价值，实现我们的使命。',
          },
        },
        {
          mainTitle: '',
          para: {
            subTitle: '我们的未来展望',
            content:
              '展望未来，GRS游戏推荐系统将继续秉承玩家至上的理念，不断提升我们的服务质量和用户体验。我们将进一步优化推荐算法，引入更多创新技术，如人工智能和大数据分析，以提供更精准、更个性化的游戏推荐。我们还将拓展我们的服务范围，覆盖更多的游戏类型和平台，满足不同玩家的需求。此外，我们将加强与游戏开发商和发行商的合作，为玩家带来更多独家内容和优惠活动。我们相信，通过我们的不懈努力，GRS游戏推荐系统将成为全球最懂玩家的游戏推荐平台。',
          },
        },
        {
          mainTitle: '联系我们',
          para: {
            subTitle: '',
            content: '',
            multiLine: ['电话: 111-1111-1111', '邮箱: 111-1111@111.com', '地址: 11市11区11路11号'],
          },
        },
      ],
    }
  },
}
</script>

<style scoped>
#intro {
  display: flex;
  margin: 0px 50px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
  color: var(--contrast-color);
  background-image: linear-gradient(
    to right,
    var(--secondary-color-alpha2) 5%,
    var(--primary-color) 50%,
    var(--secondary-color-alpha2) 95%
  );
}

.content-flat {
  width: 80%;
  background-color: var(--secondary-color);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  min-height: 100vh;
  margin: 0 auto;
}

.content-item {
  background-color: var(--primary-color);
  padding: 1.5rem;
  border-radius: 20px;
  width: 60%;
}

@media (max-width: 2000px) {
  .content-item {
    width: 100%;
  }
}

.title {
  color: var(--main-color-alpha1);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.sub-title {
  color: var(--main-color-alpha1);
  font-size: 1.3rem;
  font-style: bold;
}

.para-content {
  color: var(--contrast-color);
  font-size: 1rem;
  line-height: 1.5;
}
</style>
