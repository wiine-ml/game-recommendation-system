import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import axios from './services/DataService.js'
import store from './services/Store.js'
// 引入ECharts核心模块
import * as echarts from 'echarts/core'

// 引入Canvas渲染器
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([CanvasRenderer])

// 引入图表组件
import { BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'

//引入element-plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

//引入element-icon
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

//路由跳转

echarts.use([BarChart, TitleComponent, TooltipComponent, GridComponent])

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.config.globalProperties.$axios = axios
app.config.globalProperties.$echarts = echarts
app.config.devtools = false
app.config.productionTip = false

app.use(store)
app.use(ElementPlus)

app.mount('#app')
