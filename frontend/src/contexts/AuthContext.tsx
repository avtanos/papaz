import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authApi, type CashierProfile } from '../services/api'

interface AuthContextType {
  cashier: CashierProfile | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [cashier, setCashier] = useState<CashierProfile | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Проверяем токен при загрузке (только один раз)
    if (token) {
      checkAuth()
    } else {
      setIsLoading(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const checkAuth = async () => {
    try {
      const profile = await authApi.getProfile()
      setCashier(profile)
    } catch (error: any) {
      // Токен невалиден, удаляем его
      localStorage.removeItem('token')
      setToken(null)
      setCashier(null)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (username: string, password: string) => {
    const response = await authApi.login(username, password)
    const newToken = response.access_token
    setToken(newToken)
    localStorage.setItem('token', newToken)
    
    // Получаем профиль
    const profile = await authApi.getProfile()
    setCashier(profile)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setCashier(null)
  }

  return (
    <AuthContext.Provider
      value={{
        cashier,
        token,
        login,
        logout,
        isLoading,
        isAuthenticated: !!cashier && !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

