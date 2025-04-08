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
    },

    async updateFavorite(item) {
      this.loading = true
      try {
        console.log('Updating item:', item) // Debug log
        const response = await axios.put(`/api/favorites/${item.id}`, {
          title: item.title,
          type: item.type,
          description: item.description,
          external_id: item.external_id,
          poster_path: item.poster_path,
          status: item.status,
          rating: item.rating,
          notes: item.notes
        })
        
        // Aktualizacja elementu w lokalnej tablicy
        const index = this.items.findIndex(i => i.id === item.id)
        if (index !== -1) {
          this.items[index] = response.data
        }
        
        this.error = null
      } catch (error) {
        console.error('Update error:', error) // Debug log
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async deleteFavorite(id) {
      this.loading = true
      try {
        await axios.delete(`/api/favorites/${id}`)
        // Usunięcie elementu z lokalnej tablicy
        this.items = this.items.filter(item => item.id !== id)
        this.error = null
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}) 