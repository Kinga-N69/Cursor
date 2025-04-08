<template>
  <main>
    <div class="search-container">
      <div class="search-content">
        <h1>Wyszukaj filmy, książki i gry</h1>
        <div class="search-section">
          <div class="search-controls">
            <input 
              v-model="searchQuery" 
              placeholder="Wpisz tytuł..." 
              @keyup.enter="search"
            />
            <select v-model="searchType">
              <option value="all">Wszystko</option>
              <option value="movie">Filmy</option>
              <option value="book">Książki</option>
              <option value="game">Gry</option>
            </select>
            <button @click="search" :disabled="loading">
              <span v-if="!loading">
                <span class="material-icons">search</span>
                Szukaj
              </span>
              <span v-else>Szukam...</span>
            </button>
          </div>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          Wyszukiwanie...
        </div>
        
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        
        <div v-else-if="searchResults.length > 0" class="results">
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
                <span class="material-icons">favorite_border</span>
                Dodaj do ulubionych
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="searchQuery" class="no-results">
          Nie znaleziono wyników dla "{{ searchQuery }}"
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.search-container {
  width: 100%;
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #1a1a1a;
}

.search-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #ffffff;
  margin-bottom: 2rem;
  font-size: 2rem;
}

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
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #2a2a2a;
  color: #ffffff;
  transition: all 0.2s ease;
}

input::placeholder {
  color: #888;
}

input:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

select {
  padding: 0.75rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #2a2a2a;
  color: #ffffff;
  min-width: 120px;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}

select:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

select:hover {
  background-color: #333;
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
  gap: 0.5rem;
  transition: all 0.2s ease;
  min-width: 120px;
  justify-content: center;
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

.results {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.item-card {
  border: 1px solid #ddd;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.item-card img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.item-details {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.item-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: bold;
  align-self: flex-start;
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
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.add-button {
  margin-top: auto;
  width: 100%;
  justify-content: center;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b883;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>

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
</script> 