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
                :disabled="isAddingToFavorites[item.id] || isInFavorites(item)"
                :class="{ 
                  'success': addedToFavorites[item.id],
                  'in-favorites': isInFavorites(item)
                }"
                class="add-button"
              >
                <span class="material-icons">
                  {{ isInFavorites(item) ? 'favorite' : (addedToFavorites[item.id] ? 'check_circle' : 'favorite_border') }}
                </span>
                {{ getAddButtonLabel(item) }}
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
  padding: 1rem;
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
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  padding: 0 1rem;
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

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #333;
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
  color: #ffffff;
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

  h1 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
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

<script setup>
import { ref, onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import axios from 'axios'

const searchQuery = ref('')
const searchType = ref('all')
const searchResults = ref([])
const loading = ref(false)
const error = ref(null)
const favoritesStore = useFavoritesStore()
const isAddingToFavorites = ref({})
const addedToFavorites = ref({})

// Pobierz ulubione przy montowaniu komponentu
onMounted(() => {
  favoritesStore.fetchFavorites()
})

function isInFavorites(item) {
  console.log('Checking item:', item.id, typeof item.id);
  console.log('Current favorites:', favoritesStore.items.map(f => ({ id: f.external_id, type: typeof f.external_id })));
  
  return favoritesStore.items.some(favorite => {
    // Konwertuj oba ID do stringów dla pewności
    const favoriteId = String(favorite.external_id);
    const itemId = String(item.id);
    console.log('Comparing:', favoriteId, itemId, favoriteId === itemId);
    return favoriteId === itemId && favorite.type === item.type;
  });
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

function getAddButtonLabel(item) {
  if (isInFavorites(item)) {
    return 'Już w ulubionych'
  }
  if (isAddingToFavorites.value[item.id]) {
    return 'Dodawanie...'
  }
  if (addedToFavorites.value[item.id]) {
    return 'Dodano do ulubionych'
  }
  return 'Dodaj do ulubionych'
}

async function search() {
  if (!searchQuery.value) return
  
  loading.value = true
  error.value = null
  try {
    const response = await axios.get('/api/search', {
      params: {
        query: searchQuery.value,
        type: searchType.value
      }
    })
    searchResults.value = response.data.results
    // Reset status dla nowych wyników
    isAddingToFavorites.value = {}
    addedToFavorites.value = {}
  } catch (err) {
    error.value = 'Wystąpił błąd podczas wyszukiwania'
    searchResults.value = []
  } finally {
    loading.value = false
  }
}

async function addToFavorites(item) {
  // Sprawdź czy element już jest w ulubionych lub jest w trakcie dodawania
  if (isInFavorites(item) || isAddingToFavorites.value[item.id]) {
    return;
  }

  isAddingToFavorites.value[item.id] = true;
  try {
    const result = await favoritesStore.addFavorite({
      title: item.title,
      type: item.type,
      description: item.description,
      external_id: item.id,
      poster_path: item.poster_path,
      rating: item.rating || 0,
      status: 'plan_to_watch',
      notes: ''
    });

    if (result.error) {
      console.log('Error adding to favorites:', result.error);
      // Jeśli element już istnieje, oznacz go jako dodany
      if (result.error === 'Item already exists') {
        addedToFavorites.value[item.id] = true;
      }
    } else {
      addedToFavorites.value[item.id] = true;
      setTimeout(() => {
        addedToFavorites.value[item.id] = false;
      }, 3000);
    }
  } catch (err) {
    console.error('Error adding to favorites:', err);
  } finally {
    isAddingToFavorites.value[item.id] = false;
  }
}
</script> 