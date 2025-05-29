import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import Landing from '../views/Landing.vue'

const routes = [
  { path: '/', component: Landing, name: 'main' },
  { path: '/login', component: LoginView, name: 'login' },
  { path: '/register', component: RegisterView, name: 'register' },
  { 
    path: '/admin', 
    component: AdminDashboard, 
    name: 'admin',
    beforeEnter: (to, from, next) => {
      const role = localStorage.getItem('userRole')
      if (role === 'admin') {
        next()
      } else {
        next('/login')
      }
    }
  },
  { 
    path: '/user', 
    component: UserDashboard, 
    name: 'user',
    beforeEnter: (to, from, next) => {
      const userId = localStorage.getItem('userId')
      const role = localStorage.getItem('userRole')
      
      if (userId && role === 'user') {
        next()
      } else {
        next('/login')
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router