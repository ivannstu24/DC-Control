import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import Landing from '../views/Landing.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/user',
      name: 'user',
      component: UserDashboard,
      meta: { requiresAuth: true, role: 'user' }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await axios.get('http://localhost:5000/api/auth/check-auth', {
        withCredentials: true
      })
      
      if (to.meta.role && response.data.role !== to.meta.role) {
        next('/')
      } else {
        next()
      }
    } catch (error) {
      console.error('Ошибка проверки аутентификации:', error)
      next('/')
    }
  } else if ((to.name === 'login' || to.name === 'register') && localStorage.getItem('user')) {
    // Если пользователь уже авторизован, перенаправляем на соответствующую страницу
    try {
      const response = await axios.get('http://localhost:5000/api/auth/check-auth', {
        withCredentials: true
      })
      
      if (response.data.role === 'admin') {
        next({ name: 'admin' })
      } else {
        next({ name: 'user' })
      }
    } catch {
      next()
    }
  } else {
    next()
  }
})

export default router
