<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const adminName = ref('Администратор')
const employees = ref([])
const servers = ref([])
const blocks = ref([])
const accesses = ref([])
const accessRequests = ref([])

const showEmployees = ref(true)
const showServers = ref(true)
const showAccesses = ref(true)
const showRequests = ref(true)
const showServerManagement = ref(true)

const form = ref({
  employee_id: '',
  server_id: '',
  valid_from: '',
  valid_to: ''
})

const newBlockForm = ref({
  name: ''
})

const newServerForm = ref({
  name: '',
  block_id: ''
})

const toggleSection = (section) => {
  if (section === 'employees') showEmployees.value = !showEmployees.value
  else if (section === 'servers') showServers.value = !showServers.value
  else if (section === 'accesses') showAccesses.value = !showAccesses.value
  else if (section === 'requests') showRequests.value = !showRequests.value
  else if (section === 'serverManagement') showServerManagement.value = !showServerManagement.value
}

const fetchAccessRequests = async () => {
  const res = await axios.get('http://localhost:5000/api/admin/access-requests', {
    withCredentials: true
  })
  accessRequests.value = res.data
}

const approveRequest = async (requestId) => {
  const validFrom = prompt("Введите дату начала доступа (YYYY-MM-DD HH:MM:SS):")
  const validTo = prompt("Введите дату окончания доступа (YYYY-MM-DD HH:MM:SS):")
  
  if (!validFrom || !validTo) {
    alert("Необходимо указать обе даты")
    return
  }
  
  try {
    await axios.post(`http://localhost:5000/api/admin/approve-request/${requestId}`, {
      valid_from: validFrom,
      valid_to: validTo
    }, {
      withCredentials: true
    })
    await fetchAccessRequests()
    await fetchData()
  } catch (err) {
    console.error("Ошибка при одобрении запроса:", err)
  }
}

const rejectRequest = async (requestId) => {
  await axios.post(`http://localhost:5000/api/admin/reject-request/${requestId}`, {}, {
    withCredentials: true
  })
  await fetchAccessRequests()
}

const fetchData = async () => {
  try {
    const authCheck = await axios.get('http://localhost:5000/api/auth/check-auth', {
      withCredentials: true
    })

    if (!authCheck.data.isAuthenticated || authCheck.data.role !== 'admin') {
      router.push('/login')
      return
    }

    const [emp, srv, acc, blk] = await Promise.all([
      axios.get('http://localhost:5000/api/admin/employees', { withCredentials: true }),
      axios.get('http://localhost:5000/api/admin/servers', { withCredentials: true }),
      axios.get('http://localhost:5000/api/admin/accesses', { withCredentials: true }),
      axios.get('http://localhost:5000/api/admin/blocks', { withCredentials: true })
    ])
    
    employees.value = emp.data
    servers.value = srv.data
    accesses.value = acc.data
    blocks.value = blk.data
  } catch (err) {
    console.error('Ошибка при загрузке данных:', err)
    router.push('/login')
  }
}

const grantAccess = async () => {
  try {
    await axios.post('http://localhost:5000/api/admin/grant-access', form.value, {
      withCredentials: true
    })
    form.value = { 
      employee_id: '', 
      server_id: '', 
      valid_from: '', 
      valid_to: '' 
    }
    await fetchData()
  } catch (err) {
    console.error("Ошибка при выдаче доступа:", err)
  }
}

const revokeAccess = async (id) => {
  await axios.delete(`http://localhost:5000/api/admin/revoke-access/${id}`, {
    withCredentials: true
  })
  await fetchData()
}

const addBlock = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/admin/add-block', {
      name: newBlockForm.value.name
    }, {
      withCredentials: true
    })
    alert(response.data.message)
    newBlockForm.value.name = ''
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка при добавлении блока')
  }
}

const addServer = async () => {
  try {
    const response = await axios.post('http://localhost:5000/api/admin/add-server', {
      name: newServerForm.value.name,
      block_id: newServerForm.value.block_id
    }, {
      withCredentials: true
    })
    alert(response.data.message)
    newServerForm.value = { name: '', block_id: '' }
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка при добавлении сервера')
  }
}

const deleteServer = async (serverId) => {
  if (!confirm('Вы уверены, что хотите удалить этот сервер?')) return
  
  try {
    const response = await axios.delete(`http://localhost:5000/api/admin/delete-server/${serverId}`, {
      withCredentials: true
    })
    alert(response.data.message)
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка при удалении сервера')
  }
}

const deleteBlock = async (blockId) => {
  if (!confirm('Вы уверены, что хотите удалить этот блок?')) return
  
  try {
    const response = await axios.delete(`http://localhost:5000/api/admin/delete-block/${blockId}`, {
      withCredentials: true
    })
    alert(response.data.message)
    await fetchData()
  } catch (err) {
    alert(err.response?.data?.error || 'Ошибка при удалении блока')
  }
}

const logout = async () => {
  try {
    await axios.post('http://localhost:5000/api/auth/logout', {}, {
      withCredentials: true
    })
    router.push('/login')
  } catch (err) {
    console.error('Ошибка при выходе:', err)
  }
}

onMounted(() => {
  
  fetchData()
  fetchAccessRequests()
})
</script>


<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <div class="header-content">
        <h1>DataCenter Control</h1>
      </div>
      <button class="logout-btn" @click="logout">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Выйти
      </button>
    </div>

    <div class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.3503 17.623 3.8507 18.1676 4.55231C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89317 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ employees.length }}</div>
            <div class="stat-label">Пользователей</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ servers.length }}</div>
            <div class="stat-label">Серверов</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path data-v-996bf7cb="" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ accesses.length }}</div>
            <div class="stat-label">Активных доступов</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ accessRequests.length }}</div>
            <div class="stat-label">Запросов</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H21M3 12H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ blocks.length }}</div>
            <div class="stat-label">Блоков</div>
          </div>
        </div>
      </div>

      <div class="dashboard-section">
        <div class="section-header" @click="toggleSection('serverManagement')">
          <h2>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Управление серверами и блоками
          </h2>
          <span :class="['arrow-icon', { open: showServerManagement }]">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </div>
        <transition name="slide-fade">
          <div v-show="showServerManagement" class="section-content">
            <div class="management-form">
              <h3>Добавить новый блок</h3>
              <form @submit.prevent="addBlock" class="form-grid">
                <div class="form-group">
                  <label>Название блока</label>
                  <input v-model="newBlockForm.name" type="text" class="form-input" required>
                </div>
                <button type="submit" class="add-btn">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4v16m8-8H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Добавить блок
                </button>
              </form>
            </div>

            <div class="management-form">
              <h3>Добавить новый сервер</h3>
              <form @submit.prevent="addServer" class="form-grid">
                <div class="form-group">
                  <label>Название сервера</label>
                  <input v-model="newServerForm.name" type="text" class="form-input" required>
                </div>
                <div class="form-group">
                  <label>Блок</label>
                  <select v-model="newServerForm.block_id" class="form-select" required>
                    <option value="" disabled selected>Выберите блок</option>
                    <option v-for="block in blocks" :key="block.id" :value="block.id">{{ block.name }}</option>
                  </select>
                </div>
                <button type="submit" class="add-btn">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 4v16m8-8H4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Добавить сервер
                </button>
              </form>
            </div>

            <div class="management-list">
              <h3>Список блоков</h3>
              <ul>
                <li v-for="block in blocks" :key="block.id" class="list-item">
                  <div class="item-content">
                    <div class="item-info">
                      <div class="item-title">{{ block.name }}</div>
                      <div class="item-subtitle">ID: {{ block.id }}</div>
                    </div>
                    <button class="delete-btn" @click="deleteBlock(block.id)">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19 7L5 21M5 7L19 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      Удалить
                    </button>
                  </div>
                </li>
              </ul>
            </div>

            <div class="management-list">
              <h3>Список серверов</h3>
              <ul>
                <li v-for="server in servers" :key="server.id" class="list-item">
                  <div class="item-content">
                    <div class="item-info">
                      <div class="item-title">{{ server.block }} - {{ server.name }}</div>
                      <div class="item-subtitle">ID: {{ server.id }}</div>
                    </div>
                    <button class="delete-btn" @click="deleteServer(server.id)">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M19 7L5 21M5 7L19 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      Удалить
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </transition>
      </div>

      <div class="dashboard-section">
        <div class="section-header" @click="toggleSection('employees')">
          <h2>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.3503 17.623 3.8507 18.1676 4.55231C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89317 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Пользователи
          </h2>
          <span :class="['arrow-icon', { open: showEmployees }]">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </div>
        <transition name="slide-fade">
          <div v-show="showEmployees" class="section-content">
            <div v-for="e in employees" :key="e.id" class="list-item">
              <div class="item-content">
                <div class="avatar">
                  {{ e.username.charAt(0).toUpperCase() }}
                </div>
                <div class="item-info">
                  <div class="item-title">{{ e.username }}</div>
                  <div class="item-subtitle">ID: {{ e.id }}</div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div class="dashboard-section">
        <div class="section-header" @click="toggleSection('servers')">
          <h2>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Серверы
          </h2>
          <span :class="['arrow-icon', { open: showServers }]">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </div>
        <transition name="slide-fade">
          <div v-show="showServers" class="section-content">
            <div v-for="s in servers" :key="s.id" class="list-item">
              <div class="item-content">
                <div class="server-icon">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="item-info">
                  <div class="item-title">{{ s.block }} - {{ s.name }}</div>
                  <div class="item-subtitle">ID: {{ s.id }}</div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div class="dashboard-section">
        <div class="section-header" @click="toggleSection('accesses')">
          <h2>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Доступы
          </h2>
          <span :class="['arrow-icon', { open: showAccesses }]">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </div>
        <transition name="slide-fade">
          <div v-show="showAccesses" class="section-content">
            <div v-for="a in accesses" :key="a.id" class="list-item">
              <div class="item-content">
                <div class="avatar">
                  {{ a.username.charAt(0).toUpperCase() }}
                </div>
                <div class="item-info">
                  <div class="item-title">{{ a.username }}</div>
                  <div class="item-subtitle">{{ a.server }}</div>
                  <div class="item-subtitle" v-if="a.valid_from && a.valid_to">
                    Действителен: {{ new Date(a.valid_from).toLocaleString() }} - {{ new Date(a.valid_to).toLocaleString() }}
                  </div>
                </div>
                <div class="item-meta">
                  <div class="meta-text">Выдан: {{ new Date(a.granted_at).toLocaleDateString() }}</div>
                  <button class="revoke-btn" @click="revokeAccess(a.id)">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M19 7L5 21M5 7L19 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Отозвать
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div class="dashboard-section">
        <div class="section-header" @click="toggleSection('requests')">
          <h2>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Запросы на доступ
          </h2>
          <span :class="['arrow-icon', { open: showRequests }]">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </div>
        <transition name="slide-fade">
          <div v-show="showRequests" class="section-content">
            <div v-for="req in accessRequests" :key="req.id" class="list-item">
              <div class="item-content">
                <div class="avatar">
                  {{ req.username.charAt(0).toUpperCase() }}
                </div>
                <div class="item-info">
                  <div class="item-title">{{ req.username }}</div>
                  <div class="item-subtitle">{{ req.server }}</div>
                </div>
                <div class="item-meta">
                  <div class="meta-text">Запрошен: {{ new Date(req.created_at).toLocaleDateString() }}</div>
                  <div class="request-actions">
                    <button class="approve-btn" @click="approveRequest(req.id)">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      Одобрить
                    </button>
                    <button class="reject-btn" @click="rejectRequest(req.id)">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      Отклонить
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <div class="dashboard-section grant-form">
        <h2>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-top: 10px; width: 20px; margin-left: 15px; margin-right: 10px;">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          Выдать доступ
        </h2>
        <form @submit.prevent="grantAccess" class="access-form">
          <div class="form-group">
            <label>Пользователь</label>
            <select v-model="form.employee_id" class="form-select" required>
              <option value="" disabled selected>Выберите пользователя</option>
              <option v-for="e in employees" :key="e.id" :value="e.id">{{ e.username }}</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Сервер</label>
            <select v-model="form.server_id" class="form-select" required>
              <option value="" disabled selected>Выберите сервер</option>
              <option v-for="s in servers" :key="s.id" :value="s.id">{{ s.block }} - {{ s.name }}</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Действителен с</label>
            <input v-model="form.valid_from" type="datetime-local" class="form-select" required>
          </div>
          
          <div class="form-group">
            <label>Действителен до</label>
            <input v-model="form.valid_to" type="datetime-local" class="form-select" required>
          </div>
          
          <button type="submit" class="grant-btn">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Выдать доступ
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.management-form {
  background: var(--gray-light);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.management-form h3 {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: var(--text);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: flex-end;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid black;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background-color: var(--white);
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-light);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.add-btn {
  background: var(--success);
  color: var(--white);
  padding: 0.75rem 1.5rem;
  border: 1px solid #0da271;
  border-radius: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-btn:hover {
  background: #0da271;
}

.add-btn svg {
  width: 16px;
  height: 16px;
}

.management-list {
  margin-top: 2rem;
}

.management-list h3 {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: var(--text);
  margin-left: 20px;
}

.delete-btn {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.delete-btn svg {
  width: 14px;
  height: 14px;
}

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
  --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.admin-dashboard {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
}

.dashboard-header {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: var(--white);
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 10;
}

.header-content h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.admin-name {
  font-size: 0.95rem;
  opacity: 0.9;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: var(--white);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: var(--card-shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-light);
}

.sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.dashboard-section {
  background: var(--white);
  border-radius: 12px;
  margin-bottom: 50px;
  box-shadow: var(--card-shadow);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid black;
  padding-top: 50px;
    padding-left: 20px;
    padding-right: 20px;
}

.dashboard-section:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.section-header {
  padding: 1.25rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  background: var(--white);
  border-bottom: 1px solid var(--gray);
}

.section-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 0;
}

.section-header svg {
  width: 20px;
  height: 20px;
  color: var(--primary);
}

.arrow-icon {
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow-icon svg {
  width: 16px;
  height: 16px;
}

.arrow-icon.open {
  transform: rotate(180deg);
}

.section-content {
  padding: 0.5rem 0;
  max-height: 400px;
  overflow-y: auto;
  padding-bottom: 40px;
}

.list-item {
  padding: 0.75rem 1.5rem;
  transition: background-color 0.2s ease;
}

.list-item:hover {
  background: var(--gray-light);
}

.list-item:not(:last-child) {
  border-bottom: 1px solid var(--gray);
}

.item-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar, .server-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary);
  color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.server-icon {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
}

.server-icon svg {
  width: 20px;
  height: 20px;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-weight: 500;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-subtitle {
  font-size: 0.875rem;
  color: var(--text-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  margin-left: auto;
  text-align: right;
}

.meta-text {
  font-size: 0.75rem;
  color: var(--text-light);
  white-space: nowrap;
}

.grant-form {
  grid-column: 1 / -1;
}

.access-form {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  align-items: flex-end;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text);
}

.form-select, input[type="datetime-local"] {
  padding: 0.75rem;
  border: 1px solid black;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background-color: var(--white);
}

input[type="datetime-local"] {
  width: 100%;
}

.form-select:focus, input[type="datetime-local"]:focus {
  outline: none;
  border-color: var(--primary-light);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

/* Кнопки */
button {
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  border-radius: 8px;
  font-size: 0.95rem;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

button svg {
  width: 16px;
  height: 16px;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.1);
  color: var(--white);
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.grant-btn {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: var(--white);
  padding: 0.75rem 1.5rem;
  height: 44px;
  border: 1px solid;
}

.grant-btn:hover {
  background: #e34747;
}

.revoke-btn {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.revoke-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.approve-btn {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.approve-btn:hover {
  background: rgba(16, 185, 129, 0.2);
}

.reject-btn {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  margin-left: 0.5rem;
}

.reject-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.request-actions {
  display: flex;
  gap: 0.5rem;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 1024px) {
  .dashboard-content {
    padding: 1.5rem;
  }
  
  .sections-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .access-form {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .item-content {
    flex-wrap: wrap;
  }
  
  .item-meta {
    flex-direction: row;
    width: 100%;
    justify-content: space-between;
    margin-top: 0.5rem;
  }
  
  .request-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .access-form {
    grid-template-columns: 1fr 1fr;
  }
  
  .section-content {
    max-height: none;
    overflow-y: visible;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .access-form {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .item-meta {
    flex-direction: column;
    align-items: flex-start;
    margin-top: 1rem;
  }
  
  .request-actions {
    margin-top: 0.5rem;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-content {
    padding: 1rem;
  }
  
  .list-item {
    padding: 0.75rem;
  }
  
  .item-content {
    flex-wrap: wrap;
  }
  
  .section-header {
    padding: 1rem;
  }
}
</style>
