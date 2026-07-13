import api from './client'

export function registerProvider(payload) {
  return api.post('/provider/auth/register', payload).then((r) => r.data)
}

export function loginProvider(email, password) {
  return api.post('/provider/auth/login', { email, password }).then((r) => r.data)
}
