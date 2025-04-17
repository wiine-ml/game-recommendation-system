import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import axios from './services/DataService.js'
import store from './services/Store.js'
// 引入 ECharts 核心模块
import * as echarts from 'echarts/core'

// 引入 Canvas 渲染器
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([CanvasRenderer])

// 引入需要的图表类型和组件
import { BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'

//路由跳转

echarts.use([BarChart, TitleComponent, TooltipComponent, GridComponent])

const app = createApp(App)

app.config.globalProperties.$axios = axios
app.config.globalProperties.$echarts = echarts
app.config.devtools = false
app.config.productionTip = false

app.use(store)
app.mount('#app')
