import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('esi_access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export function getErrorMessage(error) {
  const data = error?.response?.data
  if (typeof data?.detail === 'string') return data.detail
  if (typeof data?.message === 'string') return data.message
  if (data?.errors && typeof data.errors === 'object') {
    const firstError = Object.values(data.errors).flat()[0]
    if (typeof firstError === 'string') return firstError
  }
  return error?.message || 'Something went wrong. Please try again.'
}

export default api
