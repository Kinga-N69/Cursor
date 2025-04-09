<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Zarejestruj się</h1>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label for="username">Login</label>
          <input 
            id="username" 
            v-model="username" 
            type="text" 
            required 
            placeholder="Wprowadź login"
          />
        </div>
        <div class="form-group">
          <label for="password">Hasło</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            required 
            placeholder="Wprowadź hasło"
          />
        </div>
        <div class="form-group">
          <label for="confirmPassword">Potwierdź hasło</label>
          <input 
            id="confirmPassword" 
            v-model="confirmPassword" 
            type="password" 
            required 
            placeholder="Potwierdź hasło"
          />
        </div>
        <button type="submit" :disabled="loading">
          <span v-if="!loading">
            <span class="material-icons">person_add</span>
            Zarejestruj się
          </span>
          <span v-else>Rejestracja...</span>
        </button>
      </form>
      <div class="login-link">
        Masz już konto? <router-link to="/login">Zaloguj się</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function register() {
  if (!username.value || !password.value || !confirmPassword.value) {
    error.value = 'Wypełnij wszystkie pola'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Hasła nie są identyczne'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await authStore.register(username.value, password.value)
    router.push('/login')
  } catch (err) {
    error.value = err.message || 'Błąd rejestracji'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  width: 100%;
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #1a1a1a;
}

.register-card {
  width: 100%;
  max-width: 400px;
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #ffffff;
  margin-bottom: 2rem;
  font-size: 1.75rem;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #ffffff;
  font-size: 0.9rem;
}

input {
  padding: 0.75rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #1a1a1a;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.2s ease;
}

input:focus {
  border-color: #42b883;
  outline: none;
}

button {
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

button:hover:not(:disabled) {
  background-color: #3aa876;
  transform: translateY(-1px);
}

button:disabled {
  background-color: #2a2a2a;
  border: 2px solid #333;
  color: #666;
  cursor: not-allowed;
}

.error-message {
  background-color: #dc3545;
  color: white;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #ffffff;
}

.login-link a {
  color: #42b883;
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .register-container {
    padding: 1rem;
  }
  
  .register-card {
    padding: 1.5rem;
  }
}
</style> 