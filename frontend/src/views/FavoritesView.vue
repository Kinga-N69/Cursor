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

      <div v-else class="items-grid">
        <div v-for="item in items" :key="item.id" class="item-card">
          <img 
            :src="item.poster_path" 
            :alt="item.title"
            @error="handleImageError"
          />
          <div class="item-details">
            <h3>{{ item.title }}</h3>
            <span class="item-type" :class="item.type">{{ getTypeLabel(item.type) }}</span>
            
            <div class="item-controls">
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
  min-height: calc(100vh - 64px);
  background-color: #1a1a1a;
  padding: 2rem;
}

.favorites-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

h1 {
  text-align: center;
  color: #ffffff;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.item-card {
  border: 2px solid #333;
  border-radius: 12px;
  overflow: hidden;
  background: #2a2a2a;
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
}

.item-details {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  color: #ffffff;
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

.item-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-group label {
  color: #888;
  font-size: 0.9rem;
}

.control-group.full-width {
  width: 100%;
}

select, input, textarea {
  padding: 0.75rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #222;
  color: #ffffff;
  font-size: 1rem;
  transition: all 0.2s ease;
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white'%3e%3cpath d='M7 10l5 5 5-5z'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}

select:focus, input:focus, textarea:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

textarea {
  resize: vertical;
  min-height: 80px;
}

.item-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}

.delete-button {
  padding: 0.75rem 1.5rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.delete-button:hover {
  background-color: #c82333;
  transform: translateY(-1px);
}

.save-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #2a2a2a;
  border-top: 2px solid #333;
  padding: 1rem;
  z-index: 1000;
}

.save-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #ffffff;
}

.save-icon {
  color: #ffc107;
}

.save-button {
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

.save-button.saving {
  position: relative;
  overflow: hidden;
}

.save-button.saving::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.success-message {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #42b883;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: slideUp 0.3s ease-out;
  z-index: 1000;
}

@keyframes slideUp {
  from { transform: translate(-50%, 100%); opacity: 0; }
  to { transform: translate(-50%, 0); opacity: 1; }
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