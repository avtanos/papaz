import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import CustomersPage from './pages/CustomersPage'
import DiscountsPage from './pages/DiscountsPage'
import AnalyticsPage from './pages/AnalyticsPage'
import POSPage from './pages/POSPage'
import StoresPage from './pages/StoresPage'
import LoginPage from './pages/LoginPage'
import CashierDashboard from './pages/CashierDashboard'
import './App.css'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { t } = useTranslation()
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>{t('common.loading')}</div>
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <CashierDashboard />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard/customers" replace />} />
        <Route path="customers" element={<CustomersPage />} />
        <Route path="discounts" element={<DiscountsPage />} />
        <Route path="pos" element={<POSPage />} />
        <Route path="analytics" element={<AnalyticsPage />} />
        <Route path="stores" element={<StoresPage />} />
      </Route>
      <Route path="/" element={<Navigate to="/login" replace />} />
    </Routes>
  )
}

function AppContent() {
  return (
    <Router basename="/papaz">
      <AppRoutes />
    </Router>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

