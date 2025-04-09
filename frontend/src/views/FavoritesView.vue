<template>
  <div class="favorites-container">
    <div v-if="!authStore.isAuthenticated" class="auth-message">
      <h2>Zaloguj się, aby zobaczyć swoje ulubione</h2>
      <router-link to="/login" class="auth-button login">
        <span class="material-icons">login</span>
        Zaloguj się
      </router-link>
    </div>

    <div v-else>
      <div class="favorites-header">
        <h1 class="favorites-title">Moje ulubione</h1>
      </div>

      <div v-if="loading && !items.length" class="loading">
        <span class="material-icons loading-icon">hourglass_empty</span>
        Ładowanie ulubionych...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="!items.length" class="empty-state">
        <p>Nie masz jeszcze żadnych ulubionych. Dodaj coś!</p>
      </div>

      <div v-else class="favorites-grid">
        <div v-for="item in items" :key="item.id" class="favorite-card">
          <img 
            :src="item.poster_path" 
            :alt="item.title"
            @error="handleImageError"
          >
          
          <div class="favorite-details">
            <span :class="['favorite-type', item.type]">{{ getTypeLabel(item.type) }}</span>
            <h3>{{ item.title }}</h3>
            <p class="description">{{ item.description }}</p>

            <div class="favorite-status">
              <select 
                v-model="item.status"
                @change="handleChange(item.id)"
                :disabled="loading"
              >
                <option value="plan_to_watch">Planuję obejrzeć</option>
                <option value="watching">Oglądam</option>
                <option value="completed">Zakończone</option>
                <option value="dropped">Porzucone</option>
              </select>
            </div>

            <div class="favorite-rating">
              <input 
                type="number" 
                v-model.number="item.rating"
                @input="handleChange(item.id)"
                min="0"
                max="10"
                step="0.5"
                :disabled="loading"
                placeholder="Ocena (0-10)"
              >
            </div>

            <div class="favorite-notes">
              <textarea 
                v-model="item.notes"
                @input="handleChange(item.id)"
                :disabled="loading"
                placeholder="Dodaj notatki..."
              ></textarea>
            </div>

            <button 
              @click="deleteItem(item.id)" 
              class="delete-button"
              :disabled="loading"
            >
              <span class="material-icons">delete</span>
              Usuń
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stały pasek z przyciskiem zapisywania na dole ekranu -->
    <div v-if="hasChanges" class="save-bar">
      <div class="unsaved-changes-badge">
        <span class="material-icons">warning</span>
        Masz niezapisane zmiany
      </div>
      <button 
        @click="saveChanges" 
        :disabled="loading"
        class="save-button"
      >
        <span class="material-icons">save</span>
        {{ loading ? 'Zapisywanie...' : 'Zapisz zmiany' }}
      </button>
    </div>

    <!-- Komunikat o sukcesie -->
    <div v-if="saveSuccess" class="success-message">
      Zmiany zostały zapisane!
    </div>
  </div>
</template>

<script>
import { ref, computed, onBeforeUnmount, onMounted } from 'vue'
import { useFavoritesStore } from '@/stores/favorites'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'FavoritesView',
  setup() {
    const favoritesStore = useFavoritesStore()
    const authStore = useAuthStore()
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    const saveSuccess = ref(false)
    const changedItems = ref(new Set())

    const items = computed(() => favoritesStore.items)
    const hasChanges = computed(() => changedItems.value.size > 0)

    const getTypeLabel = (type) => {
      const labels = {
        movie: 'Film',
        book: 'Książka',
        game: 'Gra'
      }
      return labels[type] || type
    }

    const handleChange = (itemId) => {
      changedItems.value.add(itemId)
      saveSuccess.value = false
    }

    const handleImageError = (event) => {
      event.target.src = '/placeholder.jpg'
    }

    const fetchFavorites = async () => {
      if (!authStore.isAuthenticated) return
      
      loading.value = true
      error.value = null
      
      try {
        await favoritesStore.fetchFavorites()
      } catch (err) {
        error.value = err.message || 'Nie udało się pobrać ulubionych'
        console.error('Błąd podczas pobierania ulubionych:', err)
      } finally {
        loading.value = false
      }
    }

    const saveChanges = async () => {
      if (!hasChanges.value) return

      loading.value = true
      error.value = null
      saveSuccess.value = false

      try {
        for (const itemId of changedItems.value) {
          const item = items.value.find(i => i.id === itemId)
          if (item) {
            await favoritesStore.updateFavorite(itemId, {
              title: item.title,
              type: item.type,
              description: item.description,
              external_id: item.external_id,
              poster_path: item.poster_path,
              status: item.status,
              rating: item.rating,
              notes: item.notes
            })
          }
        }
        changedItems.value.clear()
        saveSuccess.value = true
        setTimeout(() => {
          saveSuccess.value = false
        }, 3000)
      } catch (err) {
        error.value = err.message || 'Nie udało się zapisać zmian'
      } finally {
        loading.value = false
      }
    }

    const deleteItem = async (itemId) => {
      if (!confirm('Czy na pewno chcesz usunąć ten element?')) return

      loading.value = true
      error.value = null

      try {
        await favoritesStore.deleteFavorite(itemId)
        changedItems.value.delete(itemId)
      } catch (err) {
        error.value = err.message || 'Nie udało się usunąć elementu'
      } finally {
        loading.value = false
      }
    }

    // Ostrzeżenie przed opuszczeniem strony z niezapisanymi zmianami
    const handleBeforeUnload = (e) => {
      if (hasChanges.value) {
        e.preventDefault()
        e.returnValue = 'Masz niezapisane zmiany. Czy na pewno chcesz opuścić stronę?'
        return e.returnValue
      }
    }

    // Dodaj nasłuchiwanie zdarzenia przed opuszczeniem strony
    window.addEventListener('beforeunload', handleBeforeUnload)

    // Pobierz ulubione przy montowaniu komponentu, jeśli użytkownik jest zalogowany
    onMounted(() => {
      if (authStore.isAuthenticated) {
        fetchFavorites()
      }
    })

    // Usuń nasłuchiwanie przy odmontowaniu komponentu
    onBeforeUnmount(() => {
      window.removeEventListener('beforeunload', handleBeforeUnload)
    })

    return {
      items,
      loading,
      error,
      saveSuccess,
      hasChanges,
      changedItems,
      authStore,
      getTypeLabel,
      handleChange,
      handleImageError,
      saveChanges,
      deleteItem
    }
  }
}
</script>

<style scoped>
.favorites-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  padding-bottom: 5rem; /* Dodatkowy padding na dole, aby treść nie była zasłonięta przez pasek zapisywania */
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
  margin: 0 auto;
  width: fit-content;
}

.auth-button.login {
  background-color: #42b883;
  color: white;
}

.auth-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.favorites-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0 1rem;
}

.favorites-title {
  font-size: 1.5rem;
  color: #ffffff;
  margin: 0;
}

/* Stały pasek z przyciskiem zapisywania na dole ekranu */
.save-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: rgba(42, 42, 42, 0.95);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

.unsaved-changes-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #ff9800;
  color: white;
  border-radius: 8px;
  font-weight: bold;
  animation: pulse 2s infinite;
}

.unsaved-changes-badge .material-icons {
  font-size: 1.2rem;
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

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(66, 184, 131, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(66, 184, 131, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(66, 184, 131, 0);
  }
}

.success-message {
  position: fixed;
  top: 1rem;
  right: 1rem;
  padding: 1rem 2rem;
  background-color: #4caf50;
  color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  animation: slideIn 0.3s ease-out;
  z-index: 1000;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 0.5rem;
  justify-items: center;
}

.favorite-card {
  display: flex;
  flex-direction: column;
  border: 2px solid #333;
  border-radius: 12px;
  overflow: hidden;
  background: #2a2a2a;
  width: 100%;
  max-width: 350px;
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

.favorite-details {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.favorite-details h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #ffffff;
}

.favorite-type {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: bold;
  align-self: flex-start;
  margin: 0.5rem 0;
}

.favorite-type.movie {
  background-color: #ff9800;
  color: white;
}

.favorite-type.book {
  background-color: #2196f3;
  color: white;
}

.favorite-type.game {
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

.favorite-status,
.favorite-rating,
.favorite-notes {
  margin: 0.5rem 0;
}

.favorite-status select,
.favorite-rating input,
.favorite-notes textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #333;
  border-radius: 8px;
  background-color: #2a2a2a;
  color: #ffffff;
  transition: all 0.2s ease;
}

.favorite-status select:focus,
.favorite-rating input:focus,
.favorite-notes textarea:focus {
  border-color: #42b883;
  outline: none;
  background-color: #333;
}

.favorite-notes textarea {
  height: 100px;
  resize: vertical;
}

.delete-button {
  margin-top: auto;
  padding: 0.75rem;
  background-color: #ff4757;
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

.delete-button:hover:not(:disabled) {
  background-color: #ff6b81;
  transform: translateY(-1px);
}

.delete-button:disabled {
  background-color: #2a2a2a;
  border: 2px solid #333;
  color: #666;
  cursor: not-allowed;
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

.error {
  text-align: center;
  padding: 2rem;
  color: #ff4757;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #ffffff;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .favorites-container {
    padding: 0.5rem;
    padding-bottom: 5rem;
  }

  .favorites-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }

  .favorite-card {
    max-width: 100%;
  }

  .favorite-card img {
    height: 300px;
  }

  .favorite-card:hover {
    transform: none;
  }

  .save-bar {
    flex-direction: column;
    padding: 0.75rem;
  }
}

@media (min-width: 769px) and (max-width: 1200px) {
  .favorites-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1201px) and (max-width: 1600px) {
  .favorites-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1601px) {
  .favorites-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 480px) {
  .favorite-card img {
    height: 250px;
  }
}
</style> 