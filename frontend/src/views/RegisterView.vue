<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="logo-container">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="logo-icon">
          <path fill-rule="evenodd" d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z" clip-rule="evenodd" />
        </svg>
      </div>
      <h2 class="auth-title">Регистрация</h2>
      <form @submit.prevent="register" class="auth-form">
        <div class="form-group">
          <input 
            v-model="username" 
            @input="validateUsername"
            placeholder="Логин" 
            required 
            class="form-input" 
            :class="{ 'input-error': usernameError }"
          />
          <span v-if="usernameError" class="error-text">{{ usernameError }}</span>
        </div>
        <div class="form-group">
          <input 
            v-model="password" 
            @input="validatePassword"
            type="password" 
            placeholder="Пароль" 
            required 
            class="form-input" 
            :class="{ 'input-error': passwordError }"
          />
          <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
        </div>
        <div class="form-group">
          <div class="select-wrapper">
            <select 
              v-model="role" 
              @change="validateRole"
              required 
              class="form-select"
              :class="{ 'input-error': roleError }"
            >
              <option disabled value="">Выберите роль</option>
              <option value="admin">Администратор</option>
              <option value="user">Пользователь</option>
            </select>
            <span v-if="roleError" class="error-text">{{ roleError }}</span>
          </div>
        </div>
        <button type="submit" class="auth-btn" :disabled="isFormInvalid">
          <span>Зарегистрироваться</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="btn-icon">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
          </svg>
        </button>
      </form>
      <p v-if="error" class="error-message">{{ error }}</p>
      <p v-if="success" class="success-message">{{ success }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      role: '',
      usernameError: '',
      passwordError: '',
      roleError: '',
      error: '',
      success: ''
    }
  },
  methods: {
    async register() {
      this.validateUsername()
      this.validatePassword()
      this.validateRole()
      
      if (this.isFormInvalid) {
        return
      }
      
      this.error = ''
      try {
        await axios.post('http://localhost:5000/api/auth/register', {
          username: this.username,
          password: this.password,
          role: this.role
        }, {
          withCredentials: true
        })
        this.success = 'Регистрация успешна! Войдите в систему.'
        this.$router.push('/')
      } catch (err) {
        this.error = err.response?.data?.msg || 'Ошибка регистрации'
      }
    }
  }
}
</script>

<style scoped>

.auth-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.auth-btn:disabled:hover {
  background: #cbd5e0;
  transform: none;
  box-shadow: none;
}

.auth-btn:disabled .btn-icon {
  transform: none;
}

.input-error {
  border-color: #e53e3e !important;
  background-color: #fff5f5 !important;
}

.error-text {
  color: #e53e3e;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.form-group {
  margin-bottom: 0.5rem;
}
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 1rem;
}

.auth-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
  padding: 3rem 2.5rem;
  width: 100%;
  max-width: 420px;
  position: relative;
  overflow: hidden;
}

.auth-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  color: #667eea;
}

.auth-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 2rem;
  text-align: center;
  position: relative;
}

.auth-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  margin: 0.75rem auto 0;
  border-radius: 3px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-input {
  padding: 0.875rem 1.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #a3bffa;
  box-shadow: 0 0 0 3px rgba(164, 202, 254, 0.3);
  background-color: white;
}

.form-input::placeholder {
  color: #a0aec0;
  opacity: 1;
}

.select-wrapper {
  position: relative;
}

.form-select {
  width: 100%;
  padding: 0.875rem 1.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: #f8fafc;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23667eea' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
}

.form-select:focus {
  outline: none;
  border-color: #a3bffa;
  box-shadow: 0 0 0 3px rgba(164, 202, 254, 0.3);
  background-color: white;
}

.auth-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.auth-btn:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.auth-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.auth-btn:hover .btn-icon {
  transform: scale(1.1);
}

.error-message {
  color: #e53e3e;
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  padding: 0.75rem;
  background-color: #fff5f5;
  border-radius: 8px;
  border-left: 4px solid #e53e3e;
}

.success-message {
  color: #38a169;
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  padding: 0.75rem;
  background-color: #f0fff4;
  border-radius: 8px;
  border-left: 4px solid #38a169;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 2rem 1.5rem;
  }
  
  .auth-title {
    font-size: 1.5rem;
  }
  
  .logo-icon {
    width: 40px;
    height: 40px;
  }
}
</style>