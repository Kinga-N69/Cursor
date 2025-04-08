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
        <img :src="item.poster_path" :alt="item.title" />
        <div class="item-details">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
          <div class="item-status">
            <select v-model="item.status">
              <option value="plan_to_watch">Do obejrzenia</option>
              <option value="watching">W trakcie</option>
              <option value="completed">Ukończone</option>
            </select>
            <div class="rating">
              <span>Ocena:</span>
              <input type="number" v-model="item.rating" min="0" max="10" step="0.5" />
            </div>
          </div>
          <textarea v-model="item.notes" placeholder="Twoje notatki..."></textarea>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'

const favoritesStore = useFavoritesStore()

onMounted(() => {
  favoritesStore.fetchFavorites()
})
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
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-card img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 4px;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.item-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
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
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style> 