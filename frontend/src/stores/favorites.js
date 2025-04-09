import { defineStore } from 'pinia'
import axios from 'axios'

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),

  getters: {
    getItemById: (state) => (id) => {
      return state.items.find(item => item.id === id)
    }
  },

  actions: {
    async fetchFavorites() {
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        
        const response = await axios.get('/api/favorites')
        this.items = response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to fetch favorites'
        throw error
      } finally {
        this.loading = false
      }
    },

    async addFavorite(item) {
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        
        const response = await axios.post('/api/favorites', item)
        this.items.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to add favorite'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateFavorite(id, data) {
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        
        console.log('Updating favorite:', id, data)
        const response = await axios.put(`/api/favorites/${id}`, data)
        const index = this.items.findIndex(item => item.id === id)
        if (index !== -1) {
          this.items[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to update favorite'
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteFavorite(id) {
      this.loading = true
      this.error = null
      try {
        const token = localStorage.getItem('token')
        if (token) {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
        
        await axios.delete(`/api/favorites/${id}`)
        this.items = this.items.filter(item => item.id !== id)
      } catch (error) {
        this.error = error.response?.data?.error || 'Failed to delete favorite'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 