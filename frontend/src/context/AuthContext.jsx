import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import api from '../api/client'

const AuthContext = createContext(null)
const TOKEN_KEY = 'esi_access_token'

function getUserFromResponse(data) {
  return data?.user ?? data?.data?.user ?? data?.data ?? (data?.id ? data : null)
}

function getTokenFromResponse(data) {
  return data?.access_token ?? data?.token ?? data?.data?.access_token ?? data?.data?.token
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = useCallback(async () => {
    const { data } = await api.get('/auth/me')
    const currentUser = getUserFromResponse(data)
    setUser(currentUser)
    return currentUser
  }, [])

  useEffect(() => {
    if (!localStorage.getItem(TOKEN_KEY)) {
      setLoading(false)
      return
    }

    refreshUser()
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY)
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [refreshUser])

  const authenticate = useCallback(async (endpoint, credentials) => {
    const { data } = await api.post(endpoint, credentials)
    const token = getTokenFromResponse(data)
    if (!token && endpoint === '/auth/login') {
      throw new Error('The server did not return an access token.')
    }
    if (token) localStorage.setItem(TOKEN_KEY, token)

    const responseUser = getUserFromResponse(data)
    if (responseUser) {
      setUser(responseUser)
    } else if (token) {
      await refreshUser()
    }
    return responseUser
  }, [refreshUser])

  const login = useCallback((credentials) => authenticate('/auth/login', credentials), [authenticate])
  const register = useCallback(async (details) => {
    await api.post('/auth/register', details)
    return authenticate('/auth/login', { email: details.email, password: details.password })
  }, [authenticate])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setUser(null)
  }, [])

  const value = useMemo(() => ({
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
    refreshUser,
  }), [user, loading, login, register, logout, refreshUser])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
