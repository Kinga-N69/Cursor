<template>
  <main>
    <h1>Dodaj do ulubionych</h1>
    <div class="search-section">
      <div class="search-controls">
        <input 
          v-model="searchQuery" 
          placeholder="Szukaj filmów, książek, gier..." 
          @keyup.enter="search"
        />
        <select v-model="searchType">
          <option value="all">Wszystko</option>
          <option value="movie">Filmy</option>
          <option value="book">Książki</option>
          <option value="game">Gry</option>
        </select>
        <button @click="search" :disabled="loading">
          <span v-if="!loading">Szukaj</span>
          <span v-else>Szukam...</span>
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      Ładowanie...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else class="results">
      <div v-for="item in searchResults" :key="item.id" class="item-card">
        <img 
          :src="item.poster_path" 
          :alt="item.title"
          @error="handleImageError"
        />
        <div class="item-details">
          <h3>{{ item.title }}</h3>
          <span class="item-type" :class="item.type">{{ getTypeLabel(item.type) }}</span>
          <div class="item-rating" v-if="item.rating">
            <span class="star">★</span>
            {{ item.rating.toFixed(1) }}
          </div>
          <p class="description">{{ item.description || 'Brak opisu' }}</p>
          <button 
            @click="addToFavorites(item)"
            :disabled="loading"
            class="add-button"
          >
            Dodaj do ulubionych
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import axios from 'axios'

const searchQuery = ref('')
const searchType = ref('all')
const searchResults = ref([])
const loading = ref(false)
const error = ref(null)
const favoritesStore = useFavoritesStore()

async function search() {
  if (!searchQuery.value) return
  
  loading.value = true
  try {
    const response = await axios.get('/api/search', {
      params: {
        query: searchQuery.value,
        type: searchType.value
      }
    })
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
    type: item.type,
    description: item.description,
    external_id: item.id,
    poster_path: item.poster_path,
    rating: item.rating || 0,
    status: 'plan_to_watch',
    notes: ''
  })
}

function getTypeLabel(type) {
  const labels = {
    movie: 'Film',
    book: 'Książka',
    game: 'Gra'
  }
  return labels[type] || type
}

function handleImageError(e) {
  e.target.src = 'https://via.placeholder.com/300x450?text=Brak+obrazka'
}
</script>

<style scoped>
.search-section {
  margin: 2rem 0;
}

.search-controls {
  display: flex;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

button {
  padding: 0.5rem 1rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  min-width: 100px;
}

button:hover:not(:disabled) {
  background-color: #3aa876;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.item-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.item-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.item-card img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.item-details {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-type {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.item-type.movie {
  background-color: #ff9800;
  color: white;
}

.item-type.book {
  background-color: #2196f3;
  color: white;
}

.item-type.game {
  background-color: #4caf50;
  color: white;
}

.item-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #666;
}

.star {
  color: #ffd700;
}

.description {
  font-size: 0.9rem;
  color: #666;
  margin: 0.5rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.add-button {
  margin-top: auto;
  width: 100%;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: #dc3545;
}
</style> 