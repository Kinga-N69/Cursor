import { defineStore } from 'pinia'
import axios from 'axios'

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchFavorites() {
      this.loading = true
      try {
        const response = await axios.get('/api/favorites')
        this.items = response.data
        this.error = null
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async addFavorite(item) {
      this.loading = true
      try {
        const response = await axios.post('/api/favorites', item)
        this.items.push(response.data)
        this.error = null
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}) 