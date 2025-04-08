<template>
  <main class="favorites-container">
    <div class="favorites-content">
      <h1>Moje ulubione</h1>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        Ładowanie...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="items.length === 0" class="no-items">
        Nie masz jeszcze żadnych ulubionych pozycji.
        <router-link to="/" class="add-first">
          <span class="material-icons">add</span>
          Dodaj pierwszą
        </router-link>
      </div>

      <div v-else class="favorites-grid">
        <div v-for="item in items" :key="item.id" class="favorite-card">
          <img 
            :src="item.poster_path" 
            :alt="item.title"
            @error="handleImageError"
          />
          <div class="card-content">
            <h3>{{ item.title }}</h3>
            <span class="item-type" :class="item.type">{{ getTypeLabel(item.type) }}</span>
            
            <div class="card-controls">
              <div class="control-group">
                <label>Status:</label>
                <select v-model="item.status" @change="handleChange(item)">
                  <option value="watching">Oglądane</option>
                  <option value="completed">Ukończone</option>
                  <option value="plan_to_watch">Planuję</option>
                  <option value="dropped">Porzucone</option>
                </select>
              </div>

              <div class="control-group">
                <label>Ocena:</label>
                <input 
                  type="number" 
                  v-model.number="item.rating" 
                  min="0" 
                  max="10" 
                  step="0.5"
                  @input="handleChange(item)"
                />
              </div>

              <div class="control-group full-width">
                <label>Notatki:</label>
                <textarea 
                  v-model="item.notes" 
                  @input="handleChange(item)"
                  rows="3"
                  placeholder="Dodaj swoje przemyślenia..."
                ></textarea>
              </div>
            </div>

            <div class="item-actions">
              <button 
                class="delete-button"
                @click="confirmDelete(item)"
              >
                <span class="material-icons">delete</span>
                Usuń
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="hasChanges" class="save-bar">
        <div class="save-content">
          <span class="material-icons save-icon">warning</span>
          <span>Masz niezapisane zmiany!</span>
          <button 
            class="save-button" 
            :class="{ saving: saving }"
            @click="saveChanges"
            :disabled="saving"
          >
            <span class="material-icons">save</span>
            {{ saving ? 'Zapisywanie...' : 'Zapisz zmiany' }}
          </button>
        </div>
      </div>

      <div v-if="showSuccess" class="success-message">
        <span class="material-icons">check_circle</span>
        Zmiany zostały zapisane!
      </div>
    </div>
  </main>
</template>

<style scoped>
.favorites-container {
  width: 100%;
  min-height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background-color: #1a1a1a;
}

.favorites-content {
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

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 0.5rem;
  width: 100%;
  margin: 0 auto;
}

.favorite-card {
  display: flex;
  flex-direction: column;
  border: 2px solid #333;
  border-radius: 12px;
  overflow: hidden;
  background: #2a2a2a;
  height: 100%;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.favorite-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.favorite-card img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  object-position: center;
}

.card-content {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-content h3 {
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
  margin: 0.5rem 0;
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

.description {
  max-height: 100px;
  overflow-y: auto;
  margin: 0.5rem 0;
  font-size: 0.9rem;
  line-height: 1.4;
  color: #ffffff;
  opacity: 0.8;
}

.card-controls {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.card-controls label {
  color: #ffffff;
  font-size: 0.9rem;
}

.card-controls select,
.card-controls input,
.card-controls textarea {
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

.card-controls select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}

.card-controls select:focus,
.card-controls input:focus,
.card-controls textarea:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

.card-controls textarea {
  min-height: 80px;
  resize: vertical;
}

.save-button {
  margin-top: 1rem;
  width: 100%;
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

.save-button:hover:not(:disabled) {
  background-color: #3aa876;
  transform: translateY(-1px);
}

.save-button:disabled {
  background-color: #2a2a2a;
  border: 2px solid #333;
  color: #666;
  cursor: not-allowed;
}

.save-button.success {
  background-color: #4caf50;
}

.delete-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background-color: #dc3545;
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

.delete-button:hover {
  background-color: #c82333;
  transform: translateY(-1px);
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

.success-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #4caf50;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  z-index: 1000;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 100%);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

.error {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
}

.no-items {
  text-align: center;
  padding: 2rem;
  color: #888;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.add-first {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  transition: all 0.2s ease;
}

.add-first:hover {
  background-color: #3aa876;
  transform: translateY(-1px);
}

@media (max-width: 1200px) {
  .favorites-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .favorites-container {
    padding: 0.5rem;
  }

  .favorites-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  h1 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }

  .favorite-card {
    margin: 0;
  }

  .favorite-card img {
    height: 300px;
  }

  .description {
    max-height: 80px;
  }

  .favorite-card:hover {
    transform: none;
  }

  .save-button:hover,
  .delete-button:hover {
    transform: none;
  }

  .card-controls {
    gap: 0.75rem;
  }

  .card-controls select,
  .card-controls input,
  .card-controls textarea {
    padding: 0.75rem;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .favorites-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .favorite-card img {
    height: 250px;
  }

  .success-message {
    width: 90%;
    text-align: center;
  }
}
</style>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'

const store = useFavoritesStore()
const items = computed(() => store.items)
const loading = computed(() => store.loading)
const error = computed(() => store.error)
const saving = ref(false)
const showSuccess = ref(false)
const changedItems = ref(new Set())

onMounted(() => {
  store.fetchFavorites()
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
  showSuccess.value = false
}

const hasChanges = computed(() => changedItems.value.size > 0)

async function saveChanges() {
  saving.value = true
  try {
    for (const itemId of changedItems.value) {
      const item = items.value.find(i => i.id === itemId)
      if (item) {
        await store.updateFavorite(item)
      }
    }
    changedItems.value.clear()
    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 3000)
  } catch (err) {
    console.error('Error saving changes:', err)
  } finally {
    saving.value = false
  }
}

function confirmDelete(item) {
  if (confirm(`Czy na pewno chcesz usunąć "${item.title}" z ulubionych?`)) {
    store.deleteFavorite(item.id)
  }
}
</script> 