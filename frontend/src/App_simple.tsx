import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import CustomersPage from './pages/CustomersPage'
import DiscountsPage from './pages/DiscountsPage'
import AnalyticsPage from './pages/AnalyticsPage'
import POSPage from './pages/POSPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">Kids Store - Discount System</h1>
            <div className="nav-links">
              <Link to="/customers">Customers</Link>
              <Link to="/discounts">Discounts</Link>
              <Link to="/pos">POS</Link>
              <Link to="/analytics">Analytics</Link>
            </div>
          </div>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<CustomersPage />} />
            <Route path="/customers" element={<CustomersPage />} />
            <Route path="/discounts" element={<DiscountsPage />} />
            <Route path="/pos" element={<POSPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

