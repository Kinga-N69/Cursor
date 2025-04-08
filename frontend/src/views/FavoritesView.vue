<template>
  <main>
    <h1>Moje ulubione pozycje</h1>
    
    <div v-if="favoritesStore.loading" class="loading">
      Ładowanie...
    </div>
    
    <div v-else-if="favoritesStore.error" class="error">
      {{ favoritesStore.error }}
    </div>
    
    <div v-else class="favorites">
      <div v-for="item in favoritesStore.items" :key="item.id" class="item-card">
        <img :src="item.poster_path" :alt="item.title" @error="handleImageError" />
        <div class="item-details">
          <div class="item-header">
            <h3>{{ item.title }}</h3>
            <span class="item-type" :class="item.type">{{ getTypeLabel(item.type) }}</span>
          </div>
          <p>{{ item.description }}</p>
          <div class="item-status">
            <select 
              v-model="item.status"
              @change="handleChange(item)">
              <option value="plan_to_watch">Do obejrzenia</option>
              <option value="watching">W trakcie</option>
              <option value="completed">Ukończone</option>
            </select>
            <div class="rating">
              <span>Ocena:</span>
              <input 
                type="number" 
                v-model.number="item.rating" 
                min="0" 
                max="10" 
                step="0.5"
                @change="handleChange(item)"
              />
            </div>
          </div>
          <textarea 
            v-model="item.notes" 
            placeholder="Twoje notatki..."
            @input="handleInput(item)"
          ></textarea>
          <div class="actions">
            <button 
              class="save-button" 
              :class="{ 'has-changes': hasChanges(item) }"
              @click="saveChanges(item)"
              :disabled="!hasChanges(item) || favoritesStore.loading"
            >
              <span v-if="favoritesStore.loading && isCurrentlySaving === item.id">
                Zapisywanie...
              </span>
              <span v-else-if="hasChanges(item)">
                Zapisz zmiany
              </span>
              <span v-else>
                Zapisano
              </span>
            </button>
            <button 
              class="delete-button" 
              @click="deleteItem(item)"
              :disabled="favoritesStore.loading"
            >
              Usuń
            </button>
          </div>
          <div v-if="saveSuccess === item.id" class="success-message">
            Zmiany zostały zapisane!
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'

const favoritesStore = useFavoritesStore()
const changedItems = ref(new Set())
const isCurrentlySaving = ref(null)
const saveSuccess = ref(null)

onMounted(() => {
  favoritesStore.fetchFavorites()
})

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

function handleChange(item) {
  changedItems.value.add(item.id)
  saveSuccess.value = null
}

function handleInput(item) {
  changedItems.value.add(item.id)
  saveSuccess.value = null
}

function hasChanges(item) {
  return changedItems.value.has(item.id)
}

async function saveChanges(item) {
  try {
    isCurrentlySaving.value = item.id
    await favoritesStore.updateFavorite(item)
    changedItems.value.delete(item.id)
    saveSuccess.value = item.id
    setTimeout(() => {
      if (saveSuccess.value === item.id) {
        saveSuccess.value = null
      }
    }, 3000)
  } finally {
    isCurrentlySaving.value = null
  }
}

async function deleteItem(item) {
  if (confirm('Czy na pewno chcesz usunąć tę pozycję z ulubionych?')) {
    await favoritesStore.deleteFavorite(item.id)
  }
}
</script>

<style scoped>
.favorites {
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
  height: 300px;
  object-fit: cover;
}

.item-details {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
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

.item-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.5rem 0;
}

select, input[type="number"] {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.save-button, .delete-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  flex: 1;
}

.save-button {
  background-color: #e0e0e0;
  color: #666;
  transition: background-color 0.3s;
}

.save-button.has-changes {
  background-color: #42b883;
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

.save-button:not(:disabled):hover {
  background-color: #3aa876;
}

.delete-button {
  background-color: #dc3545;
  color: white;
}

.delete-button:hover:not(:disabled) {
  background-color: #c82333;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: #dc3545;
}

.success-message {
  color: #4caf50;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 0.5rem;
}
</style> 