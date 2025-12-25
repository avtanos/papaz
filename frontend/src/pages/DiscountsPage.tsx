import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { discountsApi, type DiscountRule } from '../services/api'
import Pagination from '../components/Pagination'
import '../App.css'

function DiscountsPage() {
  const { t } = useTranslation()
  const [showForm, setShowForm] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(25)
  const queryClient = useQueryClient()

  const { data: rulesData, isLoading, error } = useQuery({
    queryKey: ['discount-rules', currentPage, itemsPerPage],
    queryFn: () => discountsApi.getAll(undefined, (currentPage - 1) * itemsPerPage, itemsPerPage).then(res => res.data),
    retry: 1,
    refetchOnWindowFocus: false,
  })

  const rules = rulesData?.items || []
  const totalRules = rulesData?.total || 0
  const totalPages = Math.ceil(totalRules / itemsPerPage)

  const createMutation = useMutation({
    mutationFn: (data: Partial<DiscountRule>) => discountsApi.create(data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['discount-rules'] })
      setShowForm(false)
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data = {
      name: formData.get('name') as string,
      description: formData.get('description') as string || undefined,
      discount_type: formData.get('discount_type') as string,
      value: parseFloat(formData.get('value') as string),
      min_purchase_amount: formData.get('min_purchase_amount') 
        ? parseFloat(formData.get('min_purchase_amount') as string) 
        : undefined,
      max_discount_amount: formData.get('max_discount_amount')
        ? parseFloat(formData.get('max_discount_amount') as string)
        : undefined,
    }
    createMutation.mutate(data)
  }

  if (isLoading) return <div className="card"><p>{t('common.loading')}</p></div>
  
  if (error) {
    return (
      <div className="card">
        <h2>{t('errors.serverError')}</h2>
        <p>{t('errors.serverError')}</p>
      </div>
    )
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h2>{t('discounts.title')}</h2>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? t('common.cancel') : t('discounts.addRule')}
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
            <div className="form-group">
              <label>{t('discounts.name')} *</label>
              <input type="text" name="name" required />
            </div>
            <div className="form-group">
              <label>{t('discounts.description')}</label>
              <textarea name="description" rows={3}></textarea>
            </div>
            <div className="form-group">
              <label>{t('discounts.type')} *</label>
              <select name="discount_type" required>
                <option value="percentage">{t('discounts.percentage')}</option>
                <option value="fixed_amount">{t('discounts.fixed')}</option>
                <option value="bonus_multiplier">Множитель бонусов</option>
              </select>
            </div>
            <div className="form-group">
              <label>{t('discounts.value')} *</label>
              <input type="number" name="value" step="0.01" required />
            </div>
            <div className="form-group">
              <label>{t('discounts.minAmount')}</label>
              <input type="number" name="min_purchase_amount" step="0.01" />
            </div>
            <div className="form-group">
              <label>{t('discounts.maxDiscount')}</label>
              <input type="number" name="max_discount_amount" step="0.01" />
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
              <th>{t('discounts.name')}</th>
              <th>{t('discounts.type')}</th>
              <th>{t('discounts.value')}</th>
              <th>{t('discounts.minAmount')}</th>
              <th>{t('discounts.maxDiscount')}</th>
              <th>{t('discounts.isActive')}</th>
              <th>{t('discounts.actions')}</th>
            </tr>
          </thead>
          <tbody>
            {rules?.map((rule: DiscountRule) => (
              <tr key={rule.id}>
                <td data-label="ID">{rule.id}</td>
                <td data-label={t('discounts.name')}>{rule.name}</td>
                <td data-label={t('discounts.type')}>{rule.discount_type}</td>
                <td data-label={t('discounts.value')}>{rule.value}</td>
                <td data-label={t('discounts.minAmount')}>{rule.min_purchase_amount ? Number(rule.min_purchase_amount).toFixed(2) : '-'}</td>
                <td data-label={t('discounts.maxDiscount')}>{rule.max_discount_amount ? Number(rule.max_discount_amount).toFixed(2) : '-'}</td>
                <td data-label={t('discounts.isActive')}>{rule.status}</td>
                <td data-label={t('discounts.actions')}>-</td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {totalRules > 0 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalRules}
            itemsPerPage={itemsPerPage}
            onPageChange={setCurrentPage}
            onItemsPerPageChange={(newItemsPerPage) => {
              setItemsPerPage(newItemsPerPage)
              setCurrentPage(1)
            }}
          />
        )}
      </div>
    </div>
  )
}

export default DiscountsPage

