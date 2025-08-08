import axios from 'axios'

// Создаем экземпляр axios с базовым URL
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000, // 30 секунд
  headers: {
    'Content-Type': 'application/json'
  }
})

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // Получение поддерживаемых форматов
  async getFormats() {
    return api.get('/formats')
  },
  
  // Проверка состояния сервера
  async getHealth() {
    return api.get('/health')
  },
  
  // Конвертация документа
  async convertDocument(file, options = {}) {
    const formData = new FormData()
    formData.append('file', file)
    
    // Добавляем опции конвертации
    formData.append('preserve_formatting', options.preserve_formatting ?? true)
    formData.append('include_images', options.include_images ?? true)
    formData.append('max_image_size', options.max_image_size ?? 1024)
    formData.append('table_format', options.table_format ?? 'grid')
    
    return api.post('/convert', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}
