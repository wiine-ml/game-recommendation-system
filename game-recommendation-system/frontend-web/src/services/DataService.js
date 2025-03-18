import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    APIKEY: '1233211234567',
  },
})

//请求拦截器
apiClient.interceptors.response.use(
  (config) => {
    config.headers.token = localStorage.token || ''
    return config
  },
  (err) => {
    console.log('request错误', err)
    return Promise.reject(err)
  },
)

//响应拦截器
apiClient.interceptors.response.use(
  (res) => {
    const { status, data, headers } = res
    if ((status >= 200 && status < 300) || status === 304) {
      return { data, headers }
    } else {
      console.log('response错误', res)
      throw res
    }
  },
  (err) => {
    console.log('response错误', err)
    throw err
  },
)

//更新拦截器


export default apiClient

export const register = (email, username, password) =>
  apiClient.post('/register', { email, username, password })
