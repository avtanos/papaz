import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { customersApi, posApi, bonusesApi, storesApi } from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import '../App.css'

function POSPage() {
  const { t } = useTranslation()
  const [phone, setPhone] = useState('')
  const [amount, setAmount] = useState('')
  const [bonusesToUse, setBonusesToUse] = useState('')
  const [storeId, setStoreId] = useState<number>(0)
  const queryClient = useQueryClient()
  const { cashier } = useAuth()
  
  // Для супер-админа - загружаем список магазинов и позволяем выбрать
  // Для обычного кассира - используем магазин кассира
  const { data: stores } = useQuery({
    queryKey: ['stores'],
    queryFn: () => storesApi.getAll().then(res => res.data),
    enabled: !!cashier && (cashier.is_superuser || false),
    retry: 1,
    refetchOnWindowFocus: false,
  })
  
  useEffect(() => {
    if (cashier) {
      if (!cashier.is_superuser) {
        // Обычный кассир - используем его магазин
        setStoreId(cashier.store_id)
      } else if (stores && stores.length > 0 && storeId === 0) {
        // Супер-админ - выбираем первый магазин по умолчанию
        setStoreId(stores[0].id)
      }
    }
  }, [cashier, stores, storeId])

  const { data: customer, error: customerError } = useQuery({
    queryKey: ['customer-by-phone', phone],
    queryFn: () => customersApi.getByPhone(phone).then(res => res.data),
    enabled: phone.length > 0,
    retry: false,
    refetchOnWindowFocus: false,
  })

  const { data: balance } = useQuery({
    queryKey: ['bonus-balance', customer?.id],
    queryFn: () => bonusesApi.getBalance(customer!.id).then(res => res.data),
    enabled: !!customer,
    retry: false,
    refetchOnWindowFocus: false,
  })

  const { data: availableDiscounts } = useQuery({
    queryKey: ['available-discounts', customer?.id, storeId, amount],
    queryFn: () => posApi.getAvailableDiscounts(customer!.id, storeId, parseFloat(amount || '0')).then(res => res.data),
    enabled: !!customer && !!amount && !!cashier && storeId > 0 && parseFloat(amount) > 0,
    retry: false,
    refetchOnWindowFocus: false,
  })

  const processPurchaseMutation = useMutation({
    mutationFn: (data: any) => posApi.processPurchase(data).then(res => res.data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['customers'] })
      queryClient.invalidateQueries({ queryKey: ['bonus-balance'] })
      // Инвалидируем историю покупок для этого клиента
      queryClient.invalidateQueries({ queryKey: ['purchases', data.customer_id] })
      // Инвалидируем все запросы истории покупок (на случай если открыта форма деталей)
      queryClient.invalidateQueries({ queryKey: ['purchases'] })
      alert(t('pos.purchaseSuccess'))
      setPhone('')
      setAmount('')
      setBonusesToUse('')
    },
  })

  const handleProcessPurchase = () => {
    if (!customer || !amount) {
      alert(t('pos.fillAllFields'))
      return
    }

    if (!storeId || !cashier) {
      alert(t('pos.storeNotDefined'))
      return
    }

    processPurchaseMutation.mutate({
      customer_id: customer.id,
      store_id: storeId,
      amount: parseFloat(amount),
      bonuses_to_use: bonusesToUse ? parseFloat(bonusesToUse) : 0,
      payment_method: 'cash',
    })
  }

  return (
    <div>
      <div className="card">
        <h2>{t('pos.title')}</h2>
        
        <div className="form-group">
          <label>{t('pos.customerPhone')}</label>
          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+996 555 123 456"
          />
        </div>

        {customerError && phone.length > 0 && (
          <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#ffebee', borderRadius: '4px', color: '#c62828' }}>
            <p><strong>{t('errors.notFound')}:</strong> {t('pos.customerNotFound')}</p>
          </div>
        )}
        
        {customer && (
          <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#e8f5e9', borderRadius: '4px' }}>
            <p><strong>{t('pos.customer')}</strong> {customer.first_name} {customer.last_name}</p>
            <p><strong>{t('customers.phone')}:</strong> {customer.phone}</p>
            {balance && (
              <p><strong>{t('customers.bonusBalance')}:</strong> {Number(balance.current_balance || 0).toFixed(2)} {t('customers.bonuses')}</p>
            )}
          </div>
        )}

        {cashier && (
          <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
            {cashier.is_superuser ? (
              <div className="form-group">
                <label>{t('pos.store')} *</label>
                <select
                  value={storeId}
                  onChange={(e) => setStoreId(parseInt(e.target.value))}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' }}
                >
                  <option value="">{t('pos.selectStore')}</option>
                  {stores?.map((store) => (
                    <option key={store.id} value={store.id}>
                      {store.name} {store.address ? `- ${store.address}` : ''}
                    </option>
                  ))}
                </select>
              </div>
            ) : (
              <p><strong>{t('pos.store')}:</strong> {cashier.store_name}</p>
            )}
          </div>
        )}

        <div className="form-group">
          <label>{t('pos.purchaseAmount')}</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            step="0.01"
            min="0"
          />
        </div>

        {availableDiscounts && (
          <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#fff3cd', borderRadius: '4px' }}>
            <h3>{t('pos.availableDiscounts')}</h3>
            <p><strong>{t('pos.totalDiscount')}</strong> {Number(availableDiscounts.total_discount || 0).toFixed(2)} сом</p>
            <p><strong>{t('pos.finalAmount')}</strong> {Number(availableDiscounts.final_amount || 0).toFixed(2)} сом</p>
            <p><strong>{t('pos.bonusesEarned')}</strong> {Number(availableDiscounts.bonuses_earned || 0).toFixed(2)}</p>
          </div>
        )}

        <div className="form-group">
          <label>{t('pos.useBonuses')}</label>
          <input
            type="number"
            value={bonusesToUse}
            onChange={(e) => setBonusesToUse(e.target.value)}
            step="0.01"
            min="0"
            max={balance?.current_balance || 0}
          />
          {balance && (
            <small style={{ display: 'block', marginTop: '0.25rem', color: '#666' }}>
              {t('pos.available')}: {Number(balance.current_balance || 0).toFixed(2)} {t('customers.bonuses')}
            </small>
          )}
        </div>

        <button
          className="btn btn-success"
          onClick={handleProcessPurchase}
          disabled={!customer || !amount || !cashier || processPurchaseMutation.isPending}
          style={{ width: '100%', marginTop: '1rem' }}
        >
          {processPurchaseMutation.isPending ? t('pos.processing') : t('pos.processPurchase')}
        </button>
      </div>
    </div>
  )
}

export default POSPage

