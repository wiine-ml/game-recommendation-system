import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import axios from './services/DataService.js'
import store from './services/Store.js'

const app = createApp(App)

app.config.globalProperties.$axios = axios

app.use(store)

app.mount('#app')
