import axios from 'axios'

// في الـ dev، vite.config.js بيعمل proxy لـ /provider و /public على الباك اند.
// في الـ production، تقدر تحط الـ base URL الحقيقي هنا عن طريق .env (VITE_API_URL).
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('rehla_provider_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// لو الـ token انتهى أو غير صالح، نرجّع اليوزر لصفحة الدخول تلقائيًا
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('rehla_provider_token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api
