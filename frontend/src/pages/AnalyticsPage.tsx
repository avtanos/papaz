import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import '../App.css'

function AnalyticsPage() {
  const { t } = useTranslation()
  const { data: summary, isLoading, error } = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: () => analyticsApi.getSummary(30).then(res => res.data),
    retry: 1,
    refetchOnWindowFocus: false,
  })

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
        <h2>{t('analytics.title')} - {t('analytics.summary')}</h2>
        
        {summary && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ padding: '1rem', backgroundColor: '#e3f2fd', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#1976d2' }}>{t('analytics.totalRevenue')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {Number(summary.total_revenue || 0).toFixed(2)} сом
              </p>
            </div>

            <div style={{ padding: '1rem', backgroundColor: '#fff3e0', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#f57c00' }}>{t('analytics.totalDiscounts')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {Number(summary.total_discounts || 0).toFixed(2)} сом
              </p>
            </div>

            <div style={{ padding: '1rem', backgroundColor: '#e8f5e9', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#388e3c' }}>{t('analytics.totalBonusesIssued')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {Number(summary.total_bonuses_issued || 0).toFixed(2)}
              </p>
            </div>

            <div style={{ padding: '1rem', backgroundColor: '#fce4ec', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#c2185b' }}>{t('analytics.totalBonusesSpent')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {Number(summary.total_bonuses_spent || 0).toFixed(2)}
              </p>
            </div>

            <div style={{ padding: '1rem', backgroundColor: '#f3e5f5', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#7b1fa2' }}>{t('customers.title')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {summary.customer_count || 0}
              </p>
            </div>

            <div style={{ padding: '1rem', backgroundColor: '#e0f2f1', borderRadius: '4px' }}>
              <h3 style={{ marginBottom: '0.5rem', color: '#00796b' }}>{t('analytics.averagePurchase')}</h3>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {Number(summary.average_purchase || 0).toFixed(2)} сом
              </p>
            </div>
          </div>
        )}
      </div>

      {summary?.discount_effectiveness && summary.discount_effectiveness.length > 0 && (
        <div className="card">
          <h2>{t('analytics.detailedAnalytics')}</h2>
          <table className="table">
            <thead>
              <tr>
                <th>ID {t('discounts.title')}</th>
                <th>{t('analytics.date')}</th>
                <th>{t('analytics.discount')}</th>
                <th>{t('analytics.revenue')}</th>
              </tr>
            </thead>
            <tbody>
              {summary.discount_effectiveness.map((item: any, index: number) => (
                <tr key={index}>
                  <td data-label={`ID ${t('discounts.title')}`}>{item.rule_id}</td>
                  <td data-label={t('analytics.date')}>{item.applications_count}</td>
                  <td data-label={t('analytics.discount')}>{Number(item.total_discount || 0).toFixed(2)} сом</td>
                  <td data-label={t('analytics.revenue')}>{Number(item.total_revenue || 0).toFixed(2)} сом</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default AnalyticsPage

