import { useTranslation } from 'react-i18next'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import LanguageSwitcher from './LanguageSwitcher'
import '../App.css'

interface MobileMenuProps {
  isOpen: boolean
  onClose: () => void
}

function MobileMenu({ isOpen, onClose }: MobileMenuProps) {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()
  const { cashier, logout } = useAuth()

  const isActive = (path: string) => location.pathname === path

  const handleNavigate = (path: string) => {
    navigate(path)
    onClose()
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
    onClose()
  }

  if (!cashier) return null

  return (
    <div className={`mobile-menu ${isOpen ? 'active' : ''}`}>
      <a
        href="#customers"
        onClick={(e) => {
          e.preventDefault()
          handleNavigate('/dashboard/customers')
        }}
        style={{
          backgroundColor: isActive('/dashboard/customers') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
        }}
      >
        👥 {t('dashboard.customers')}
      </a>
      <a
        href="#discounts"
        onClick={(e) => {
          e.preventDefault()
          handleNavigate('/dashboard/discounts')
        }}
        style={{
          backgroundColor: isActive('/dashboard/discounts') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
        }}
      >
        🎁 {t('dashboard.discounts')}
      </a>
      <a
        href="#pos"
        onClick={(e) => {
          e.preventDefault()
          handleNavigate('/dashboard/pos')
        }}
        style={{
          backgroundColor: isActive('/dashboard/pos') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
        }}
      >
        💰 {t('dashboard.pos')}
      </a>
      <a
        href="#analytics"
        onClick={(e) => {
          e.preventDefault()
          handleNavigate('/dashboard/analytics')
        }}
        style={{
          backgroundColor: isActive('/dashboard/analytics') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
        }}
      >
        📊 {t('dashboard.analytics')}
      </a>
      {cashier.is_superuser && (
        <a
          href="#stores"
          onClick={(e) => {
            e.preventDefault()
            handleNavigate('/dashboard/stores')
          }}
          style={{
            backgroundColor: isActive('/dashboard/stores') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
          }}
        >
          🏪 {t('dashboard.stores')}
        </a>
      )}
      <div style={{ padding: '0.875rem 1rem', borderTop: '1px solid rgba(255, 255, 255, 0.2)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <LanguageSwitcher />
        <button onClick={handleLogout} style={{ flex: 1 }}>
          🚪 {t('common.logout')}
        </button>
      </div>
    </div>
  )
}

export default MobileMenu

