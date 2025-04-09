<template>
  <div class="home">
    <div v-if="!authStore.isAuthenticated" class="auth-message">
      <h2>Witaj w aplikacji Media!</h2>
      <p>Zaloguj się, aby móc wyszukiwać i zarządzać swoimi ulubionymi mediami.</p>
      <div class="auth-buttons">
        <router-link to="/login" class="auth-button login">
          <span class="material-icons">login</span>
          Zaloguj się
        </router-link>
        <router-link to="/register" class="auth-button register">
          <span class="material-icons">person_add</span>
          Zarejestruj się
        </router-link>
      </div>
    </div>

    <div v-else class="search-container">
      <div class="search-section">
        <div class="search-controls">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Wyszukaj filmy, książki, gry..."
            @keyup.enter="search"
          />
          <select v-model="selectedType">
            <option value="all">Wszystkie</option>
            <option value="movie">Filmy</option>
            <option value="book">Książki</option>
            <option value="game">Gry</option>
          </select>
          <button @click="search" :disabled="loading">
            <span class="material-icons">search</span>
            {{ loading ? 'Szukam...' : 'Szukaj' }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <span class="material-icons loading-icon">hourglass_empty</span>
        Wyszukiwanie...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="searchPerformed && !results.length" class="no-results">
        Nie znaleziono wyników dla "{{ searchQuery }}"
      </div>

      <div v-else-if="results.length" class="results">
        <div v-for="item in results" :key="item.id" class="item-card">
          <img :src="item.poster_path" :alt="item.title" @error="handleImageError">
          <div class="item-details">
            <span :class="['item-type', item.type]">{{ getTypeLabel(item.type) }}</span>
            <h3>{{ item.title }}</h3>
            <div class="item-rating" v-if="item.rating">
              <span class="material-icons star">star</span>
              {{ item.rating }}
            </div>
            <p class="description">{{ item.description }}</p>
            <button
              class="add-button"
              :class="{
                'success': item.addedToFavorites,
                'in-favorites': isInFavorites(item)
              }"
              @click="addToFavorites(item)"
              :disabled="isInFavorites(item) || loading"
            >
              <span class="material-icons">
                {{ isInFavorites(item) ? 'favorite' : 'favorite_border' }}
              </span>
              {{ getButtonLabel(item) }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useFavoritesStore } from '@/stores/favorites'

const authStore = useAuthStore()
const favoritesStore = useFavoritesStore()

const searchQuery = ref('')
const selectedType = ref('all')
const loading = ref(false)
const error = ref('')
const results = ref([])
const searchPerformed = ref(false)

const getTypeLabel = (type) => {
  const labels = {
    movie: 'Film',
    book: 'Książka',
    game: 'Gra'
  }
  return labels[type] || type
}

const handleImageError = (event) => {
  event.target.src = '/placeholder.jpg'
}

const isInFavorites = (item) => {
  return favoritesStore.items.some(favorite => 
    favorite.external_id === item.id && favorite.type === item.type
  )
}

const getButtonLabel = (item) => {
  if (isInFavorites(item)) return 'W ulubionych'
  if (item.addedToFavorites) return 'Dodano!'
  return 'Dodaj do ulubionych'
}

async function search() {
  if (!searchQuery.value.trim()) {
    error.value = 'Wprowadź tekst do wyszukiwania'
    return
  }

  loading.value = true
  error.value = ''
  searchPerformed.value = true

  try {
    const response = await fetch(`/api/search?query=${encodeURIComponent(searchQuery.value)}&type=${selectedType.value}`)
    if (!response.ok) throw new Error('Błąd wyszukiwania')
    const data = await response.json()
    results.value = data.results
  } catch (err) {
    error.value = 'Wystąpił błąd podczas wyszukiwania'
    results.value = []
  } finally {
    loading.value = false
  }
}

async function addToFavorites(item) {
  if (isInFavorites(item)) return

  try {
    await favoritesStore.addFavorite({
      title: item.title,
      type: item.type,
      description: item.description,
      external_id: item.id,
      poster_path: item.poster_path
    })
    item.addedToFavorites = true
    setTimeout(() => {
      item.addedToFavorites = false
    }, 2000)
  } catch (error) {
    console.error('Error adding to favorites:', error)
  }
}
</script>

<style scoped>
.home {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.auth-message {
  text-align: center;
  padding: 4rem 1rem;
  color: #ffffff;
}

.auth-message h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #42b883;
}

.auth-message p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.8;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.auth-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  text-decoration: none;
  transition: all 0.2s ease;
}

.auth-button.login {
  background-color: #42b883;
  color: white;
}

.auth-button.register {
  background-color: transparent;
  color: #42b883;
  border: 2px solid #42b883;
}

.auth-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.search-container {
  width: 100%;
}

.loading-icon {
  font-size: 2rem !important;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.error, .no-results {
  text-align: center;
  padding: 2rem;
  color: #ff4757;
}

.no-results {
  color: #ffffff;
  opacity: 0.8;
}

.search-section {
  margin: 1rem 0;
  padding: 0 1rem;
}

.search-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.search-controls input {
  flex: 1;
  min-width: 200px;
  width: 100%;
  box-sizing: border-box;
  padding: 0.75rem;
  font-size: 1rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #2a2a2a;
  color: #ffffff;
  transition: all 0.2s ease;
}

.search-controls input::placeholder {
  color: #888;
}

.search-controls input:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

.search-controls select {
  flex: 0 0 auto;
  width: auto;
  min-width: 120px;
  padding: 0.75rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #2a2a2a;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}

.search-controls select:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

.search-controls select:hover {
  background-color: #333;
}

.search-controls button {
  flex: 0 0 auto;
  width: auto;
  min-width: 100px;
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
  justify-content: center;
}

.search-controls button:hover:not(:disabled) {
  background-color: #3aa876;
  transform: translateY(-1px);
}

.search-controls button:disabled {
  background-color: #2a2a2a;
  border: 2px solid #333;
  color: #666;
  cursor: not-allowed;
}

.results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  padding: 0.5rem;
  width: 100%;
}

.item-card {
  display: flex;
  flex-direction: column;
  border: 2px solid #333;
  border-radius: 12px;
  overflow: hidden;
  background: #2a2a2a;
  height: 100%;
  max-width: 100%;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.item-card img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  object-position: center;
}

.item-details {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-details h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
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
  color: #ffffff;
}

.star {
  color: #ffd700;
}

.description {
  max-height: 100px;
  overflow-y: auto;
  margin: 0.5rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
  color: #ffffff;
  opacity: 0.8;
}

.add-button {
  margin-top: auto;
  width: 100%;
  justify-content: center;
  background-color: #42b883;
  transition: all 0.3s ease;
}

.add-button.success {
  background-color: #4caf50;
}

.add-button:disabled {
  background-color: #2a2a2a;
  border: 2px solid #333;
  color: #666;
}

.add-button.in-favorites {
  background-color: #666;
  cursor: default;
}

.add-button.in-favorites:hover {
  transform: none;
  background-color: #666;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #ff4757;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: #ffffff;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .search-container {
    padding: 0.5rem;
  }

  .search-controls {
    flex-direction: column;
    width: 100%;
  }

  .search-controls input,
  .search-controls select,
  .search-controls button {
    width: 100%;
    min-width: 0;
  }

  .search-controls button {
    padding: 0.75rem;
  }

  .item-card img {
    height: 300px;
  }

  .description {
    max-height: 80px;
  }

  .item-card:hover {
    transform: none;
  }
}

@media (max-width: 480px) {
  .results {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .item-card img {
    height: 250px;
  }
}
</style> 