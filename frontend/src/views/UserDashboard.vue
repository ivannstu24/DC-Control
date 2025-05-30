<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

const route = useRoute()
const toast = useToast()

const userId = ref(route.query.userId || localStorage.getItem('userId'))
const username = ref('')
const servers = ref([])
const accesses = ref([])
const fetchDataInterval = ref(null)
const serverStatuses = ref({})
const loadingStates = ref({})
const requestedServers = ref(new Set())

const formatDate = (date) => {
  const options = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Date(date).toLocaleDateString('ru-RU', options)
}

const checkAuth = async () => {
  try {
    await axios.get('http://localhost:5000/api/auth/check-auth', {
      withCredentials: true
    })
  } catch (err) {
    router.push('/login')
  }
}

const logout = async () => {
  try {
    await axios.post('http://localhost:5000/api/auth/logout', {}, {
      withCredentials: true
    })
    router.push('/login')
  } catch (err) {
    toast.error('Ошибка при выходе из системы')
  }
}

const fetchData = async () => {
  try {
    const prevAccessCount = accesses.value.length
    const res = await axios.get(`http://localhost:5000/api/user/servers/${userId.value}`)
    servers.value = res.data.servers
    accesses.value = res.data.accesses
    username.value = res.data.username
    serverStatuses.value = res.data.statuses || {}

    if (accesses.value.length > prevAccessCount) {
      const newAccess = accesses.value[accesses.value.length - 1]
      toast.success(`Вам предоставлен доступ к серверу ${newAccess.server} до ${formatDate(newAccess.valid_to)}`)
      await updateServerStatus(newAccess.server_id, 'stopped')
    }
  } catch (err) {
    toast.error('Ошибка при загрузке данных')
    console.error('Ошибка при загрузке данных:', err)
  }
}

const requestAccess = async (serverId) => {
  try {
    requestedServers.value.add(serverId)
    const response = await axios.post('http://localhost:5000/api/user/request-access', {
      employee_id: userId.value,
      server_id: serverId
    })

    toast.success('Запрос отправлен администратору')
    fetchData()
  } catch (err) {
    toast.error(err.response?.data?.error || 'Ошибка при отправке запроса')
    console.error('Ошибка запроса:', err.response?.data)
  }
}

const updateServerStatus = async (serverId, status) => {
  try {
    const response = await axios.post('http://localhost:5000/api/user/update-server-status', {
      user_id: userId.value,
      server_id: serverId,
      status: status
    })
    serverStatuses.value[serverId] = status
    return true
  } catch (error) {
    toast.error('Ошибка при обновлении статуса сервера')
    console.error('Ошибка:', error)
    return false
  }
}

const manageServer = async (serverId, action) => {
  loadingStates.value[`${serverId}_${action}`] = true
  
  try {
    // Проверяем, есть ли активный доступ
    const access = accesses.value.find(a => a.server_id === serverId)
    if (access && access.valid_to && new Date(access.valid_to) < new Date()) {
      toast.error('Срок действия доступа истек')
      return
    }

    let newStatus = 'stopped'
    let message = ''
    
    switch (action) {
      case 'start':
        newStatus = 'running'
        message = `Сервер ${getServerName(serverId)} успешно запущен`
        break
      case 'pause':
        newStatus = 'paused'
        message = `Сервер ${getServerName(serverId)} приостановлен`
        break
      case 'stop':
        newStatus = 'stopped'
        message = `Сервер ${getServerName(serverId)} остановлен`
        break
      case 'restart':
        newStatus = 'restarting'
        message = `Сервер ${getServerName(serverId)} перезагружается...`
        break
    }

    const success = await updateServerStatus(serverId, newStatus)
    
    if (success) {
      if (action === 'restart') {
        await new Promise(resolve => setTimeout(resolve, 1500))
        await updateServerStatus(serverId, 'running')
        toast.success(`Сервер ${getServerName(serverId)} успешно перезагружен`)
      } else {
        toast.success(message)
      }
    }
  } catch (error) {
    toast.error(`Ошибка при выполнении действия: ${action}`)
  } finally {
    loadingStates.value[`${serverId}_${action}`] = false
  }
}

const getServerName = (serverId) => {
  const server = servers.value.find(s => s.id === serverId)
  return server ? `${server.block} - ${server.name}` : 'сервер'
}

const getServerStatus = (serverId) => {
  return serverStatuses.value[serverId] || 'stopped'
}

const getStatusText = (status) => {
  const statusMap = {
    running: 'Запущен',
    paused: 'Приостановлен',
    stopped: 'Остановлен',
    restarting: 'Перезагружается'
  }
  return statusMap[status] || 'Неизвестно'
}



onMounted(async () => {
  await checkAuth()
  fetchData()
  fetchDataInterval.value = setInterval(fetchData, 10000)
})

onUnmounted(() => {
  const userId = localStorage.getItem('userId')
  if (!userId) {
    router.push('/login')
  }
  clearInterval(fetchDataInterval.value)
})


</script>

<template>
  <div class="user-dashboard">
    <div class="dashboard-header">
      <div class="user-greeting">
        <h1>Добро пожаловать, <span class="username">{{ username }}</span></h1>
        <p>Ваш персональный кабинет управления доступом к серверам</p>
      </div>
      <div class="user-status">
        <div class="status-item">
          <span class="status-label">Доступно серверов:</span>
          <span class="status-value">{{ servers.length }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">Активных доступов:</span>
          <span class="status-value">{{ accesses.length }}</span>
        </div>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="dashboard-section">
        <div class="section-header">
          <h2>Доступные серверы</h2>
          <p class="section-description">Список всех серверов, к которым вы можете запросить доступ</p>
        </div>
        <ul class="server-list">
          <li v-for="server in servers" :key="server.id" class="server-card">
            <div class="server-info">
              <div class="server-name">{{ server.block }} - {{ server.name }}</div>
              <div class="server-id">ID: {{ server.id }}</div>
            </div>
            <button
              @click="requestAccess(server.id)"
              class="request-btn"
              :disabled="accesses.some(a => a.server_id === server.id)"
              :class="{
                requested: requestedServers.has(server.id),
                granted: accesses.some(a => a.server_id === server.id)
              }"
            >
              <span v-if="accesses.some(a => a.server_id === server.id)">
                <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16.6667 5L7.50001 14.1667L3.33334 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Доступ предоставлен
              </span>
              <span v-else-if="requestedServers.has(server.id)">
                <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 4.16666V10L13.3333 13.3333M18.3333 10C18.3333 14.6024 14.6024 18.3333 10 18.3333C5.39763 18.3333 1.66667 14.6024 1.66667 10C1.66667 5.39763 5.39763 1.66666 10 1.66666C14.6024 1.66666 18.3333 5.39763 18.3333 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Запрос отправлен
              </span>
              <span v-else>
               
                Запросить доступ
              </span>
            </button>
          </li>
        </ul>
      </div>

      <div class="dashboard-section">
        <div class="section-header">
          <h2>Ваши доступы</h2>
          <p class="section-description">Серверы, к которым у вас есть доступ в данный момент</p>
        </div>
        <ul class="access-list">
          <li v-for="access in accesses" :key="access.server_id" class="access-card">
            <div class="access-info">
              <div class="access-server">{{ access.block }} - {{ access.server }}</div>
              <div class="access-date">Доступ с: {{ formatDate(access.granted_at) }}</div>
              <div class="access-date" v-if="access.valid_from && access.valid_to">
                Действителен: {{ formatDate(access.valid_from) }} - {{ formatDate(access.valid_to) }}
              </div>
              <div class="server-status">
                <span>Статус: </span>
                <span class="status-badge" :class="getServerStatus(access.server_id)">
                  {{ getStatusText(getServerStatus(access.server_id)) }}
                </span>
              </div>
            </div>
            <div class="server-controls">
              <button
                @click="manageServer(access.server_id, 'start')"
                :disabled="getServerStatus(access.server_id) === 'running' || loadingStates[`${access.server_id}_start`]"
                class="control-btn start"
              >
                <span v-if="loadingStates[`${access.server_id}_start`]">...</span>
                <span v-else>Запустить</span>
              </button>
              <button
                @click="manageServer(access.server_id, 'pause')"
                :disabled="getServerStatus(access.server_id) !== 'running' || loadingStates[`${access.server_id}_pause`]"
                class="control-btn pause"
              >
                <span v-if="loadingStates[`${access.server_id}_pause`]">...</span>
                <span v-else>Приостановить</span>
              </button>
              <button
                @click="manageServer(access.server_id, 'stop')"
                :disabled="getServerStatus(access.server_id) === 'stopped' || loadingStates[`${access.server_id}_stop`]"
                class="control-btn stop"
              >
                <span v-if="loadingStates[`${access.server_id}_stop`]">...</span>
                <span v-else>Остановить</span>
              </button>
              <button
                @click="manageServer(access.server_id, 'restart')"
                :disabled="getServerStatus(access.server_id) === 'stopped' || loadingStates[`${access.server_id}_restart`]"
                class="control-btn restart"
              >
                <span v-if="loadingStates[`${access.server_id}_restart`]">...</span>
                <span v-else>Перезагрузить</span>
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --primary: #6366F1;
  --primary-light: #818CF8;
  --primary-dark: #4F46E5;
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  --text: #1F2937;
  --text-light: #6B7280;
  --bg: #F9FAFB;
  --white: #FFFFFF;
  --gray: #E5E7EB;
  --gray-light: #F3F4F6;
  --gray-dark: #D1D5DB;
}

.user-dashboard {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  color: var(--text);
  background: var(--bg);
  min-height: 100vh;
}

.dashboard-header {
  margin-bottom: 3rem;
  padding: 2rem;
  background: var(--white);
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, var(--white) 0%, var(--gray-light) 100%);
  border: 1px solid var(--gray);
}

.user-greeting h1 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.username {
  color: var(--primary);
}

.user-greeting p {
  color: var(--text-light);
  font-size: 1rem;
}

.user-status {
  display: flex;
  gap: 2rem;
}

.status-item {
  text-align: center;
}

.status-label {
  display: block;
  font-size: 0.875rem;
  color: var(--text-light);
  margin-bottom: 0.25rem;
}

.status-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
}

.dashboard-content {
  display: grid;
  gap: 2rem;
}

.dashboard-section {
  background: var(--white);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--gray);
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.section-description {
  color: var(--text-light);
  font-size: 0.95rem;
}

.server-list, .access-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 1rem;
}

.server-card, .access-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.server-card {
  background: var(--white);
  border: 1px solid var(--gray);
}

.server-card:hover {
  border-color: var(--primary-light);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
}

.access-card {
  background: var(--gray-light);
  border: 1px solid var(--gray-dark);
  flex-direction: column;
  align-items: stretch;
  gap: 1rem;
}

.access-card:hover {
  background: var(--white);
}

.server-info, .access-info {
  flex: 1;
}

.server-name, .access-server {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.server-id, .access-date {
  font-size: 0.875rem;
  color: var(--text-light);
}

.server-status {
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

.status-badge.running {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.status-badge.paused {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.status-badge.stopped {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.status-badge.restarting {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
}

.server-controls {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.control-btn {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 100px;
}

.control-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.control-btn.start {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.control-btn.start:not(:disabled):hover {
  background: rgba(16, 185, 129, 0.2);
}

.control-btn.pause {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.control-btn.pause:not(:disabled):hover {
  background: rgba(245, 158, 11, 0.2);
}

.control-btn.stop {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.control-btn.stop:not(:disabled):hover {
  background: rgba(239, 68, 68, 0.2);
}

.control-btn.restart {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
}

.control-btn.restart:not(:disabled):hover {
  background: rgba(99, 102, 241, 0.2);
}

.request-btn {
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  border: 1px solid black;
}


.request-btn svg {
  width: 16px;
  height: 16px;
}

.request-btn:not(.granted):not(.requested) {
  background: var(--primary);
  color: var(--white);
}

.request-btn:not(.granted):not(.requested):hover {
  background: var(--primary-dark);
}

.request-btn.requested {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.request-btn.granted {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.request-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.access-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--success);
  font-weight: 500;
}

.access-status svg {
  width: 16px;
  height: 16px;
}

@media (max-width: 1024px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
  
  .user-status {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 768px) {
  .user-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header, .dashboard-section {
    padding: 1.5rem;
  }
  
  .server-card, .access-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .request-btn {
    align-self: stretch;
    justify-content: center;
  }

  .server-controls {
    width: 100%;
    justify-content: space-between;
  }

  .control-btn {
    flex: 1;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .user-greeting h1 {
    font-size: 1.5rem;
  }
  
  .status-value {
    font-size: 1.25rem;
  }

  .control-btn {
    font-size: 0.8rem;
    padding: 0.5rem;
  }
}
</style>