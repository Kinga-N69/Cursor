<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <div class="nav-content">
        <router-link to="/" class="logo">
          Moje Media
        </router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">
            <span class="material-icons">search</span>
            Wyszukaj
          </router-link>
          <router-link to="/favorites" class="nav-link">
            <span class="material-icons">favorite</span>
            Ulubione
          </router-link>
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
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
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
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
}

.nav-link.router-link-active {
  background-color: rgba(255,255,255,0.2);
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
</style>
