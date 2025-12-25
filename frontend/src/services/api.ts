import axios from 'axios'

// Используем переменную окружения для API URL, или дефолтный путь
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
})

// Добавляем токен в заголовки при наличии
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Добавляем обработчик ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - backend server may not be running')
    } else if (error.response) {
      console.error('API Error:', error.response.status, error.response.data)
    } else if (error.request) {
      console.error('Network Error - backend server may not be running')
    }
    return Promise.reject(error)
  }
)

export interface Customer {
  id: number
  phone: string
  email?: string
  first_name: string
  last_name?: string
  status: string
  registration_date: string
  total_purchases: number
  total_visits: number
}

export interface DiscountRule {
  id: number
  name: string
  description?: string
  discount_type: string
  value: number
  status: string
  min_purchase_amount?: number
  max_discount_amount?: number
}

export interface Purchase {
  id: number
  customer_id: number
  store_id: number
  store_name?: string
  purchase_date: string
  amount: number
  discount_applied: number
  bonuses_used: number
  bonuses_earned: number
}

export interface BonusBalance {
  id: number
  customer_id: number
  current_balance: number
  total_earned: number
  total_spent: number
}

export interface Store {
  id: number
  name: string
  address?: string
  phone?: string
  email?: string
  is_active: boolean
  created_at: string
}

export const customersApi = {
  getAll: (skip: number = 0, limit: number = 100) => 
    api.get<PaginatedResponse<Customer>>('/customers/', { params: { skip, limit } }),
  getById: (id: number) => api.get<Customer>(`/customers/${id}`),
  getByPhone: (phone: string) => api.get<Customer>(`/customers/phone/${phone}`),
  create: (data: Partial<Customer>) => api.post<Customer>('/customers/', data),
  update: (id: number, data: Partial<Customer>) => api.put<Customer>(`/customers/${id}`, data),
  getPurchases: (customerId: number, skip: number = 0, limit: number = 100) => 
    api.get<PaginatedResponse<Purchase>>(`/customers/${customerId}/purchases`, { params: { skip, limit } }),
  getCustomerHistory: (customerId: number, skip: number = 0, limit: number = 100) => 
    api.get<PaginatedResponse<CustomerHistoryEntry>>(`/customers/${customerId}/history`, { params: { skip, limit } }),
}

export const discountsApi = {
  getAll: (storeId?: number, skip: number = 0, limit: number = 100) => 
    api.get<PaginatedResponse<DiscountRule>>('/discounts/rules', { params: { store_id: storeId, skip, limit } }),
  getById: (id: number) => api.get<DiscountRule>(`/discounts/rules/${id}`),
  create: (data: Partial<DiscountRule>) => api.post<DiscountRule>('/discounts/rules', data),
  update: (id: number, data: Partial<DiscountRule>) => api.put<DiscountRule>(`/discounts/rules/${id}`, data),
  calculate: (data: { customer_id: number; store_id: number; amount: number }) =>
    api.post('/discounts/calculate', data),
}

export const bonusesApi = {
  getBalance: (customerId: number) => api.get<BonusBalance>(`/bonuses/${customerId}/balance`),
  getTransactions: (customerId: number) => api.get(`/bonuses/${customerId}/transactions`),
}

export const posApi = {
  processPurchase: (data: {
    customer_id: number
    store_id: number
    amount: number
    items_count?: number
    bonuses_to_use?: number
    payment_method?: string
    receipt_number?: string
  }) => api.post<Purchase>('/pos/process-purchase', null, { params: data }),
  getAvailableDiscounts: (customerId: number, storeId: number, amount: number) =>
    api.get(`/pos/customer/${customerId}/available-discounts`, { params: { store_id: storeId, amount } }),
}

export const analyticsApi = {
  getSummary: (days: number = 30) => api.get('/analytics/summary', { params: { days } }),
  getAnalytics: (data: { start_date: string; end_date: string; store_ids?: number[] }) =>
    api.post('/analytics/', data),
}

export const storesApi = {
  getAll: (skip: number = 0, limit: number = 100) => 
    api.get<PaginatedResponse<Store>>('/stores/', { params: { skip, limit } }),
  getById: (id: number) => api.get<Store>(`/stores/${id}`),
  create: (data: Partial<Store>) => api.post<Store>('/stores/', data),
  update: (id: number, data: Partial<Store>) => api.put<Store>(`/stores/${id}`, data),
}

export interface CashierProfile {
  id: number
  username: string
  email?: string
  full_name: string
  store_id: number
  store_name: string
  is_active: boolean
  is_superuser?: boolean
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    const response = await api.post<LoginResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    return response.data
  },
  getProfile: async (): Promise<CashierProfile> => {
    const response = await api.get<CashierProfile>('/auth/me')
    return response.data
  },
}

export default api

