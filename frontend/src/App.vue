<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Wyszukaj</RouterLink>
      <RouterLink to="/favorites">Ulubione</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style>
@import '@mdi/font/css/materialdesignicons.css';

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  margin-bottom: 2rem;
}

nav {
  display: flex;
  gap: 1rem;
}

nav a {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

nav a:hover {
  background-color: #eee;
}

nav a.router-link-active {
  background-color: #42b983;
  color: white;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
}
</style>
