import { createStore } from 'vuex'
import api from '../services/api'

export default createStore({
  state: {
    supportedFormats: [],
    conversionResult: null,
    isLoading: false,
    error: null
  },
  
  mutations: {
    SET_SUPPORTED_FORMATS(state, formats) {
      state.supportedFormats = formats
    },
    SET_CONVERSION_RESULT(state, result) {
      state.conversionResult = result
    },
    SET_LOADING(state, loading) {
      state.isLoading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    }
  },
  
  actions: {
    async fetchSupportedFormats({ commit }) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
        
        const response = await api.getFormats()
        commit('SET_SUPPORTED_FORMATS', response.data.formats)
      } catch (error) {
        commit('SET_ERROR', error.message || 'Ошибка при получении форматов')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async convertDocument({ commit }, { file, options }) {
      try {
        commit('SET_LOADING', true)
        commit('CLEAR_ERROR')
        commit('SET_CONVERSION_RESULT', null)
        
        const response = await api.convertDocument(file, options)
        commit('SET_CONVERSION_RESULT', response.data)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.detail || error.message || 'Ошибка при конвертации')
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    isSupportedFormat: (state) => (filename) => {
      if (!filename) return false
      const extension = filename.toLowerCase().split('.').pop()
      return state.supportedFormats.includes(`.${extension}`)
    }
  }
})
