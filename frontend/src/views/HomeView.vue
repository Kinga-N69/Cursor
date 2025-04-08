<template>
  <main>
    <h1>Moje ulubione</h1>
    <div class="search-section">
      <input v-model="searchQuery" placeholder="Szukaj filmów, książek, gier..." />
      <button @click="search">Szukaj</button>
    </div>
    
    <div v-if="loading" class="loading">
      Ładowanie...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="results">
      <div v-for="item in searchResults" :key="item.id" class="item-card">
        <img :src="item.poster_path" :alt="item.title" />
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
        <button @click="addToFavorites(item)">Dodaj do ulubionych</button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import axios from 'axios'

const searchQuery = ref('')
const searchResults = ref([])
const loading = ref(false)
const error = ref(null)
const favoritesStore = useFavoritesStore()

async function search() {
  if (!searchQuery.value) return
  
  loading.value = true
  try {
    const response = await axios.get(`/api/search?query=${encodeURIComponent(searchQuery.value)}`)
    searchResults.value = response.data.results
    error.value = null
  } catch (err) {
    error.value = 'Wystąpił błąd podczas wyszukiwania'
    searchResults.value = []
  } finally {
    loading.value = false
  }
}

async function addToFavorites(item) {
  await favoritesStore.addFavorite({
    title: item.title,
    type: 'movie',
    description: item.overview,
    external_id: item.id.toString(),
    poster_path: `https://image.tmdb.org/t/p/w500${item.poster_path}`,
    status: 'plan_to_watch'
  })
}
</script>

<style scoped>
.search-section {
  margin: 2rem 0;
  display: flex;
  gap: 1rem;
}

input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.item-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-card img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 4px;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}
</style> 