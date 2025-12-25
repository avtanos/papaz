import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { customersApi, bonusesApi, type Customer, type Purchase } from '../services/api'
import Pagination from '../components/Pagination'
import '../App.css'

function CustomersPage() {
  const { t } = useTranslation()
  const [showForm, setShowForm] = useState(false)
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(25)
  const queryClient = useQueryClient()

  const { data: customersData, isLoading, error } = useQuery({
    queryKey: ['customers', currentPage, itemsPerPage],
    queryFn: () => customersApi.getAll((currentPage - 1) * itemsPerPage, itemsPerPage).then(res => res.data),
    retry: 1,
    refetchOnWindowFocus: false,
  })

  const customers = customersData?.items || []
  const totalCustomers = customersData?.total || 0
  const totalPages = Math.ceil(totalCustomers / itemsPerPage)

  const createMutation = useMutation({
    mutationFn: (data: Partial<Customer>) => customersApi.create(data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] })
      setShowForm(false)
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data = {
      phone: formData.get('phone') as string,
      email: formData.get('email') as string || undefined,
      first_name: formData.get('first_name') as string,
      last_name: formData.get('last_name') as string || undefined,
    }
    createMutation.mutate(data)
  }

  if (isLoading) return <div className="card"><p>{t('common.loading')}</p></div>
  
  if (error) {
    return (
      <div className="card">
        <h2>{t('errors.serverError')}</h2>
        <p>{t('customers.noCustomers')}</p>
        <p style={{ color: 'red', marginTop: '1rem' }}>{t('errors.unknownError')}: {error instanceof Error ? error.message : 'Unknown error'}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2>{t('customers.title')}</h2>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? t('common.cancel') : t('customers.addCustomer')}
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
            <div className="form-group">
              <label>{t('customers.phone')} *</label>
              <input type="tel" name="phone" required />
            </div>
            <div className="form-group">
              <label>{t('customers.email')}</label>
              <input type="email" name="email" />
            </div>
            <div className="form-group">
              <label>{t('customers.firstName')} *</label>
              <input type="text" name="first_name" required />
            </div>
            <div className="form-group">
              <label>{t('customers.lastName')}</label>
              <input type="text" name="last_name" />
            </div>
            <button type="submit" className="btn btn-primary">
              {t('common.create')}
            </button>
          </form>
        )}
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>{t('customers.phone')}</th>
              <th>{t('customers.firstName')}</th>
              <th>{t('customers.email')}</th>
              <th>{t('customers.status')}</th>
              <th>{t('customers.totalPurchases')}</th>
              <th>{t('customers.visits')}</th>
              <th>{t('customers.actions')}</th>
            </tr>
          </thead>
          <tbody>
            {customers?.map((customer: Customer) => (
              <tr key={customer.id}>
                <td data-label="ID">{customer.id}</td>
                <td data-label={t('customers.phone')}>{customer.phone}</td>
                <td data-label={t('customers.firstName')}>{customer.first_name} {customer.last_name}</td>
                <td data-label={t('customers.email')}>{customer.email || '-'}</td>
                <td data-label={t('customers.status')}>{customer.status}</td>
                <td data-label={t('customers.totalPurchases')}>{Number(customer.total_purchases || 0).toFixed(2)} сом</td>
                <td data-label={t('customers.visits')}>{customer.total_visits}</td>
                <td data-label={t('customers.actions')}>
                  <button
                    className="btn btn-primary"
                    style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                    onClick={() => setSelectedCustomer(customer)}
                  >
                    {t('common.details', 'Детали')}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {totalCustomers > 0 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalCustomers}
            itemsPerPage={itemsPerPage}
            onPageChange={setCurrentPage}
            onItemsPerPageChange={(newItemsPerPage) => {
              setItemsPerPage(newItemsPerPage)
              setCurrentPage(1)
            }}
          />
        )}
      </div>

      {selectedCustomer && (
        <CustomerDetails
          customer={selectedCustomer}
          onClose={() => {
            setSelectedCustomer(null)
            queryClient.invalidateQueries({ queryKey: ['customers'] })
          }}
        />
      )}
    </div>
  )
}

function CustomerDetails({ customer, onClose }: { customer: Customer; onClose: () => void }) {
  const { t } = useTranslation()
  const [activeTab, setActiveTab] = useState<'info' | 'purchases' | 'history'>('info')
  const [isEditing, setIsEditing] = useState(false)
  const [editForm, setEditForm] = useState({
    phone: customer.phone,
    email: customer.email || '',
    first_name: customer.first_name,
    last_name: customer.last_name || '',
  })
  const queryClient = useQueryClient()

  const { data: balance } = useQuery({
    queryKey: ['bonus-balance', customer.id],
    queryFn: () => bonusesApi.getBalance(customer.id).then(res => res.data),
  })

  const [purchasesPage, setPurchasesPage] = useState(1)
  const [purchasesPerPage, setPurchasesPerPage] = useState(10)
  
  const { data: purchasesData } = useQuery({
    queryKey: ['purchases', customer.id, purchasesPage, purchasesPerPage],
    queryFn: () => customersApi.getPurchases(customer.id, (purchasesPage - 1) * purchasesPerPage, purchasesPerPage).then(res => res.data),
    refetchOnWindowFocus: true,
    refetchInterval: activeTab === 'purchases' ? 3000 : false,
  })

  const purchases = purchasesData?.items || []
  const totalPurchases = purchasesData?.total || 0
  const totalPurchasesPages = Math.ceil(totalPurchases / purchasesPerPage)

  const [historyPage, setHistoryPage] = useState(1)
  const [historyPerPage, setHistoryPerPage] = useState(10)
  
  const { data: historyData } = useQuery({
    queryKey: ['customer-history', customer.id, historyPage, historyPerPage],
    queryFn: () => customersApi.getCustomerHistory(customer.id, (historyPage - 1) * historyPerPage, historyPerPage).then(res => res.data),
    enabled: activeTab === 'history',
  })

  const history = historyData?.items || []
  const totalHistory = historyData?.total || 0
  const totalHistoryPages = Math.ceil(totalHistory / historyPerPage)

  const updateMutation = useMutation({
    mutationFn: (data: Partial<Customer>) => customersApi.update(customer.id, data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['customers'] })
      queryClient.invalidateQueries({ queryKey: ['customer-history', customer.id] })
      setIsEditing(false)
      alert(t('common.save', 'Изменения сохранены'))
    },
  })

  const handleSave = () => {
    updateMutation.mutate(editForm)
  }

  const handleCancel = () => {
    setEditForm({
      phone: customer.phone,
      email: customer.email || '',
      first_name: customer.first_name,
      last_name: customer.last_name || '',
    })
    setIsEditing(false)
  }

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1rem',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose()
      }}
    >
      <div
        className="customer-details-modal"
        style={{
          backgroundColor: 'white',
          borderRadius: '12px',
          width: '100%',
          maxWidth: '95vw',
          maxHeight: '95vh',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="customer-details-header" style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          padding: '1rem 1.25rem',
          borderBottom: '2px solid #e0e0e0',
          flexWrap: 'wrap',
          gap: '0.5rem',
        }}>
          <h2 style={{ margin: 0, fontSize: '1.25rem', flex: 1, minWidth: 0 }}>{t('customers.customerDetails')}</h2>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              padding: '0.5rem',
              lineHeight: 1,
              color: '#666',
              borderRadius: '50%',
              width: '36px',
              height: '36px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.3s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#f0f0f0'
              e.currentTarget.style.color = '#333'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'transparent'
              e.currentTarget.style.color = '#666'
            }}
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="customer-details-tabs" style={{ 
          display: 'flex', 
          borderBottom: '2px solid #e0e0e0',
          overflowX: 'auto',
          scrollbarWidth: 'none',
          msOverflowStyle: 'none',
        }}>
          <button
            onClick={() => setActiveTab('info')}
            className={`customer-details-tab ${activeTab === 'info' ? 'active' : ''}`}
            style={{
              padding: '0.875rem 1.25rem',
              border: 'none',
              background: activeTab === 'info' ? '#7A3E6F' : 'transparent',
              color: activeTab === 'info' ? 'white' : '#666',
              cursor: 'pointer',
              fontWeight: activeTab === 'info' ? '600' : '400',
              transition: 'all 0.3s ease',
              whiteSpace: 'nowrap',
              borderBottom: activeTab === 'info' ? '3px solid #7A3E6F' : '3px solid transparent',
              fontSize: '0.9rem',
            }}
          >
            ℹ️ {t('customers.customerDetails', 'Информация')}
          </button>
          <button
            onClick={() => setActiveTab('purchases')}
            className={`customer-details-tab ${activeTab === 'purchases' ? 'active' : ''}`}
            style={{
              padding: '0.875rem 1.25rem',
              border: 'none',
              background: activeTab === 'purchases' ? '#7A3E6F' : 'transparent',
              color: activeTab === 'purchases' ? 'white' : '#666',
              cursor: 'pointer',
              fontWeight: activeTab === 'purchases' ? '600' : '400',
              transition: 'all 0.3s ease',
              whiteSpace: 'nowrap',
              borderBottom: activeTab === 'purchases' ? '3px solid #7A3E6F' : '3px solid transparent',
              fontSize: '0.9rem',
            }}
          >
            🛒 {t('customers.purchaseHistory')}
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`customer-details-tab ${activeTab === 'history' ? 'active' : ''}`}
            style={{
              padding: '0.875rem 1.25rem',
              border: 'none',
              background: activeTab === 'history' ? '#7A3E6F' : 'transparent',
              color: activeTab === 'history' ? 'white' : '#666',
              cursor: 'pointer',
              fontWeight: activeTab === 'history' ? '600' : '400',
              transition: 'all 0.3s ease',
              whiteSpace: 'nowrap',
              borderBottom: activeTab === 'history' ? '3px solid #7A3E6F' : '3px solid transparent',
              fontSize: '0.9rem',
            }}
          >
            📝 {t('customers.changeHistory', 'История изменений')}
          </button>
        </div>

        {/* Content */}
        <div className="customer-details-content" style={{ 
          flex: 1, 
          overflow: 'auto', 
          padding: '1rem 1.25rem',
          minHeight: 0,
        }}>
          {activeTab === 'info' && (
            <div>
              {!isEditing ? (
                <>
                  <div className="customer-details-actions" style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '1rem',
                    flexWrap: 'wrap',
                    gap: '0.75rem',
                  }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{t('customers.customerDetails')}</h3>
                    <button className="btn btn-primary" onClick={() => setIsEditing(true)} style={{ whiteSpace: 'nowrap' }}>
                      {t('common.edit')}
                    </button>
                  </div>
                  
                  <div className="customer-info-list" style={{ 
                    marginBottom: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem',
                  }}>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.phone')}:</strong>
                      <span>{customer.phone}</span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.firstName')}:</strong>
                      <span>{customer.first_name} {customer.last_name}</span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.email')}:</strong>
                      <span>{customer.email || '-'}</span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.status')}:</strong>
                      <span>{customer.status}</span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.totalPurchases')}:</strong>
                      <span>{Number(customer.total_purchases || 0).toFixed(2)} сом</span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <strong style={{ minWidth: '120px' }}>{t('customers.visits')}:</strong>
                      <span>{customer.total_visits}</span>
                    </div>
                  </div>

                  {balance && (
                    <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                      <h3>{t('customers.bonusBalance')}</h3>
                      <p><strong>{t('customers.bonusBalance')}:</strong> {Number(balance.current_balance || 0).toFixed(2)} {t('customers.bonuses')}</p>
                      <p><strong>{t('customers.totalEarned')}:</strong> {Number(balance.total_earned || 0).toFixed(2)} {t('customers.bonuses')}</p>
                      <p><strong>{t('customers.totalSpent')}:</strong> {Number(balance.total_spent || 0).toFixed(2)} {t('customers.bonuses')}</p>
                    </div>
                  )}
                </>
              ) : (
                <div>
                  <div className="customer-details-actions" style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center', 
                    marginBottom: '1rem',
                    flexWrap: 'wrap',
                    gap: '0.75rem',
                  }}>
                    <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{t('customers.editCustomer')}</h3>
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', width: '100%' }}>
                      <button 
                        className="btn btn-primary" 
                        onClick={handleSave} 
                        disabled={updateMutation.isPending}
                        style={{ flex: 1, minWidth: '120px' }}
                      >
                        {updateMutation.isPending ? t('common.loading') : t('common.save')}
                      </button>
                      <button 
                        className="btn" 
                        onClick={handleCancel}
                        style={{ flex: 1, minWidth: '120px' }}
                      >
                        {t('common.cancel')}
                      </button>
                    </div>
                  </div>

                  <div className="form-group">
                    <label>{t('customers.phone')} *</label>
                    <input
                      type="tel"
                      value={editForm.phone}
                      onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('customers.email')}</label>
                    <input
                      type="email"
                      value={editForm.email}
                      onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('customers.firstName')} *</label>
                    <input
                      type="text"
                      value={editForm.first_name}
                      onChange={(e) => setEditForm({ ...editForm, first_name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('customers.lastName')}</label>
                    <input
                      type="text"
                      value={editForm.last_name}
                      onChange={(e) => setEditForm({ ...editForm, last_name: e.target.value })}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'purchases' && (
            <div>
              <h3>{t('customers.purchaseHistory')}</h3>
              {purchases && purchases.length > 0 ? (
                <>
                  <div style={{ overflowX: 'auto' }}>
                    <table className="table">
                      <thead>
                        <tr>
                          <th>{t('customers.purchaseDate')}</th>
                          <th>{t('customers.store')}</th>
                          <th>{t('customers.amount')}</th>
                          <th>{t('customers.discount')}</th>
                          <th>{t('customers.bonusesEarned')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {purchases.map((purchase: Purchase) => (
                          <tr key={purchase.id}>
                            <td data-label={t('customers.purchaseDate')}>{new Date(purchase.purchase_date).toLocaleDateString()}</td>
                            <td data-label={t('customers.store')}>{purchase.store_name || t('customers.store', 'Магазин')} #{purchase.store_id}</td>
                            <td data-label={t('customers.amount')}>{Number(purchase.amount || 0).toFixed(2)} сом</td>
                            <td data-label={t('customers.discount')}>{Number(purchase.discount_applied || 0).toFixed(2)} сом</td>
                            <td data-label={t('customers.bonusesEarned')}>+{Number(purchase.bonuses_earned || 0).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {totalPurchases > 0 && (
                    <Pagination
                      currentPage={purchasesPage}
                      totalPages={totalPurchasesPages}
                      totalItems={totalPurchases}
                      itemsPerPage={purchasesPerPage}
                      onPageChange={setPurchasesPage}
                      onItemsPerPageChange={(newItemsPerPage) => {
                        setPurchasesPerPage(newItemsPerPage)
                        setPurchasesPage(1)
                      }}
                    />
                  )}
                </>
              ) : (
                <p>{t('customers.noPurchases', 'Нет покупок')}</p>
              )}
            </div>
          )}

          {activeTab === 'history' && (
            <div>
              <h3>{t('customers.changeHistory', 'История изменений')}</h3>
              {history && history.length > 0 ? (
                <>
                  <div style={{ overflowX: 'auto' }}>
                    <table className="table">
                      <thead>
                        <tr>
                          <th>{t('customers.purchaseDate', 'Дата')}</th>
                          <th>{t('customers.changeHistory', 'Изменено')}</th>
                          <th>{t('customers.changeHistory', 'Поле')}</th>
                          <th>{t('customers.changeHistory', 'Было')}</th>
                          <th>{t('customers.changeHistory', 'Стало')}</th>
                          <th>{t('customers.changeHistory', 'Кем')}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {history.map((item: any) => (
                          <tr key={item.id}>
                            <td data-label={t('customers.purchaseDate', 'Дата')}>{new Date(item.changed_at).toLocaleString()}</td>
                            <td data-label={t('customers.changeHistory', 'Тип')}>{item.change_type}</td>
                            <td data-label={t('customers.changeHistory', 'Поле')}>{item.field_name}</td>
                            <td data-label={t('customers.changeHistory', 'Было')}>{item.old_value || '-'}</td>
                            <td data-label={t('customers.changeHistory', 'Стало')}>{item.new_value || '-'}</td>
                            <td data-label={t('customers.changeHistory', 'Кем')}>{item.changed_by || '-'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {totalHistory > 0 && (
                    <Pagination
                      currentPage={historyPage}
                      totalPages={totalHistoryPages}
                      totalItems={totalHistory}
                      itemsPerPage={historyPerPage}
                      onPageChange={setHistoryPage}
                      onItemsPerPageChange={(newItemsPerPage) => {
                        setHistoryPerPage(newItemsPerPage)
                        setHistoryPage(1)
                      }}
                    />
                  )}
                </>
              ) : (
                <p>{t('customers.noHistory', 'История изменений пуста')}</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default CustomersPage
