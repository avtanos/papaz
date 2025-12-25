import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useLocation, Outlet } from 'react-router-dom'
import LanguageSwitcher from '../components/LanguageSwitcher'
import MobileMenu from '../components/MobileMenu'
import '../App.css'

function CashierDashboard() {
  const { t } = useTranslation()
  const { cashier, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!cashier) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>{t('common.loading')}</div>
  }

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="nav-title">Plum</h1>

          <button
            className="mobile-menu-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>

          <div className="nav-links">
            <a
              href="#customers"
              onClick={(e) => { e.preventDefault(); navigate('/dashboard/customers') }}
              style={{ backgroundColor: isActive('/dashboard/customers') ? 'rgba(255, 255, 255, 0.2)' : 'transparent' }}
            >
              👥 {t('dashboard.customers')}
            </a>
            <a
              href="#discounts"
              onClick={(e) => { e.preventDefault(); navigate('/dashboard/discounts') }}
              style={{ backgroundColor: isActive('/dashboard/discounts') ? 'rgba(255, 255, 255, 0.2)' : 'transparent' }}
            >
              🎁 {t('dashboard.discounts')}
            </a>
            <a
              href="#pos"
              onClick={(e) => { e.preventDefault(); navigate('/dashboard/pos') }}
              style={{ backgroundColor: isActive('/dashboard/pos') ? 'rgba(255, 255, 255, 0.2)' : 'transparent' }}
            >
              💰 {t('dashboard.pos')}
            </a>
            <a
              href="#analytics"
              onClick={(e) => { e.preventDefault(); navigate('/dashboard/analytics') }}
              style={{ backgroundColor: isActive('/dashboard/analytics') ? 'rgba(255, 255, 255, 0.2)' : 'transparent' }}
            >
              📊 {t('dashboard.analytics')}
            </a>
            {cashier.is_superuser && (
              <a
                href="#stores"
                onClick={(e) => { e.preventDefault(); navigate('/dashboard/stores') }}
                style={{ backgroundColor: isActive('/dashboard/stores') ? 'rgba(255, 255, 255, 0.2)' : 'transparent' }}
              >
                🏪 {t('dashboard.stores')}
              </a>
            )}
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <LanguageSwitcher />
              <button onClick={handleLogout}>
                🚪 {t('common.logout')}
              </button>
            </div>
          </div>

          <MobileMenu isOpen={mobileMenuOpen} onClose={() => setMobileMenuOpen(false)} />
        </div>
      </nav>
      <main className="main-content">
        <div style={{
          marginBottom: '1.5rem',
          padding: '1.25rem',
          background: cashier.is_superuser ? '#C4C4D8' : '#B8B8D4',
          borderRadius: '12px',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
          border: `2px solid ${cashier.is_superuser ? '#7A3E6F' : '#6B6B9A'}`,
        }}>
          {cashier.is_superuser ? (
            <>
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>
                <strong>👑 {t('dashboard.superAdmin')}</strong>
              </p>
              <p style={{ margin: '0 0 0.5rem 0' }}>
                <strong>{t('dashboard.name')}</strong> {cashier.full_name}
              </p>
              <p style={{ margin: 0, color: '#856404', fontSize: '0.9rem' }}>
                {t('dashboard.fullAccess')}
              </p>
            </>
          ) : (
            <>
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>
                <strong>🏪 {t('dashboard.store')}</strong> {cashier.store_name}
              </p>
              <p style={{ margin: 0 }}>
                <strong>👤 {t('dashboard.cashier')}</strong> {cashier.full_name}
              </p>
            </>
          )}
        </div>
        <Outlet />
      </main>
    </div>
  )
}

export default CashierDashboard
