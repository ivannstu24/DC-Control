import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios' 
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)

axios.defaults.baseURL = 'http://localhost:5000'

axios.interceptors.request.use(config => {
    const token = localStorage.getItem('jwtToken')
    console.log('[AXIOS] Adding token to request:', token) 
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log('[AXIOS] Request headers:', config.headers) 
    }
    return config
}, error => {
    console.error('[AXIOS] Request error:', error)
    return Promise.reject(error)
})

axios.interceptors.response.use(response => {
    console.log('[AXIOS] Response:', response)
    return response
}, error => {
    console.error('[AXIOS] Response error:', error)
    if (error.response?.status === 401) {
        localStorage.clear()
        window.location.href = '/login'
    }
    return Promise.reject(error)
})
app.config.globalProperties.$axios = axios

app.use(router)
app.use(Toast)

app.mount('#app')