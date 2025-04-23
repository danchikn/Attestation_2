import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

// Добавляем access токен в каждый запрос
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Обновляем access токен при 401 Unauthorized
instance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refresh = localStorage.getItem('refresh')
        const response = await axios.post('http://127.0.0.1:8000/api/refresh/', {
          refresh: refresh,
        })
        localStorage.setItem('token', response.data.access)
        originalRequest.headers.Authorization = `Bearer ${response.data.access}`
        return instance(originalRequest)
      } catch (refreshError) {
        console.error('Refresh token expired')
        localStorage.removeItem('token')
        localStorage.removeItem('refresh')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default instance
