import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'


createApp(App).use(router).mount('#app').use(Toast)