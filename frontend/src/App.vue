<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initialize()
})
</script>

<template>
  <header>
    <nav>
      <div class="nav-content">
        <router-link to="/" class="logo">
          <span class="material-icons logo-icon">play_circle</span>
          <span class="logo-text">Media</span>
        </router-link>
        
        <div class="nav-links">
          <template v-if="authStore.isAuthenticated">
            <router-link to="/" class="nav-link">
              <span class="material-icons">search</span>
              <span class="link-text">Wyszukaj</span>
            </router-link>
            <router-link to="/favorites" class="nav-link">
              <span class="material-icons">favorite</span>
              <span class="link-text">Ulubione</span>
            </router-link>
            <button @click="authStore.logout" class="nav-link logout-button">
              <span class="material-icons">logout</span>
              <span class="link-text">Wyloguj</span>
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">
              <span class="material-icons">login</span>
              <span class="link-text">Zaloguj</span>
            </router-link>
            <router-link to="/register" class="nav-link">
              <span class="material-icons">person_add</span>
              <span class="link-text">Zarejestruj</span>
            </router-link>
          </template>
        </div>
      </div>
    </nav>
  </header>

  <main class="main-content">
    <RouterView />
  </main>
</template>

<style>
@import '@/assets/base.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #1a1a1a;
}

header {
  background-color: #42b883;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

nav {
  height: 64px;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: white;
  text-decoration: none;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.logo:hover {
  background-color: rgba(255,255,255,0.1);
}

.logo-icon {
  font-size: 28px !important;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
  border: none;
  background: none;
  font-size: inherit;
  cursor: pointer;
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255,255,255,0.2);
}

.logout-button {
  color: #ff4757;
}

.material-icons {
  font-size: 20px;
}

.main-content {
  flex: 1;
  margin-top: 64px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (max-width: 480px) {
  .logo-text {
    display: none;
  }

  .link-text {
    display: none;
  }

  .nav-link {
    padding: 0.5rem;
  }

  .nav-content {
    padding: 0 0.5rem;
  }
}
</style>
