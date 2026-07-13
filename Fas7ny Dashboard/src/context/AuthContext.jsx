import { createContext, useContext, useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginProvider, registerProvider } from '../api/auth'

const AuthContext = createContext(null)

const TOKEN_KEY = 'rehla_provider_token'

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const navigate = useNavigate()

  const login = useCallback(
    async (email, password) => {
      const data = await loginProvider(email, password)
      localStorage.setItem(TOKEN_KEY, data.access_token)
      setToken(data.access_token)
      navigate('/dashboard')
    },
    [navigate]
  )

  const register = useCallback(
    async (payload) => {
      const data = await registerProvider(payload)
      localStorage.setItem(TOKEN_KEY, data.access_token)
      setToken(data.access_token)
      navigate('/dashboard')
    },
    [navigate]
  )

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    navigate('/login')
  }, [navigate])

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
