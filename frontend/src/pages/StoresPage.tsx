import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { storesApi, type Store } from '../services/api'
import Pagination from '../components/Pagination'
import '../App.css'

function StoresPage() {
  const { t } = useTranslation()
  const [showForm, setShowForm] = useState(false)
  const [editingStore, setEditingStore] = useState<Store | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [itemsPerPage, setItemsPerPage] = useState(25)
  const queryClient = useQueryClient()

  const { data: storesData, isLoading, error } = useQuery({
    queryKey: ['stores', currentPage, itemsPerPage],
    queryFn: () => storesApi.getAll((currentPage - 1) * itemsPerPage, itemsPerPage).then(res => res.data),
    retry: 1,
    refetchOnWindowFocus: false,
  })

  const stores = storesData?.items || []
  const totalStores = storesData?.total || 0
  const totalPages = Math.ceil(totalStores / itemsPerPage)

  const createMutation = useMutation({
    mutationFn: (data: Partial<Store>) => storesApi.create(data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['stores'] })
      setShowForm(false)
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Store> }) => 
      storesApi.update(id, data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['stores'] })
      setEditingStore(null)
    },
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data = {
      name: formData.get('name') as string,
      address: formData.get('address') as string || undefined,
      phone: formData.get('phone') as string || undefined,
      email: formData.get('email') as string || undefined,
    }
    
    if (editingStore) {
      updateMutation.mutate({ id: editingStore.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const handleEdit = (store: Store) => {
    setEditingStore(store)
    setShowForm(true)
  }

  const handleCancel = () => {
    setShowForm(false)
    setEditingStore(null)
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
          <h2>{t('stores.title')}</h2>
          <button className="btn btn-primary" onClick={() => { setShowForm(!showForm); setEditingStore(null) }}>
            {showForm ? t('common.cancel') : t('stores.addStore')}
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
            <div className="form-group">
              <label>{t('stores.name')} *</label>
              <input type="text" name="name" required defaultValue={editingStore?.name || ''} />
            </div>
            <div className="form-group">
              <label>{t('stores.address')}</label>
              <input type="text" name="address" defaultValue={editingStore?.address || ''} />
            </div>
            <div className="form-group">
              <label>{t('stores.phone')}</label>
              <input type="tel" name="phone" defaultValue={editingStore?.phone || ''} />
            </div>
            <div className="form-group">
              <label>{t('customers.email')}</label>
              <input type="email" name="email" defaultValue={editingStore?.email || ''} />
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="submit" className="btn btn-primary">
                {editingStore ? t('common.save') : t('common.create')}
              </button>
              <button type="button" className="btn" onClick={handleCancel}>
                {t('common.cancel')}
              </button>
            </div>
          </form>
        )}
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>{t('stores.name')}</th>
              <th>{t('stores.address')}</th>
              <th>{t('stores.phone')}</th>
              <th>{t('customers.email')}</th>
              <th>{t('stores.status')}</th>
              <th>{t('customers.actions')}</th>
            </tr>
          </thead>
          <tbody>
            {stores?.map((store) => (
              <tr key={store.id}>
                <td data-label="ID">{store.id}</td>
                <td data-label={t('stores.name')}>{store.name}</td>
                <td data-label={t('stores.address')}>{store.address || '-'}</td>
                <td data-label={t('stores.phone')}>{store.phone || '-'}</td>
                <td data-label={t('customers.email')}>{store.email || '-'}</td>
                <td data-label={t('stores.status')}>{store.is_active ? t('stores.active') : t('stores.inactive')}</td>
                <td data-label={t('customers.actions')}>
                  <button
                    className="btn btn-primary"
                    style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                    onClick={() => handleEdit(store)}
                  >
                    {t('common.edit')}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {totalStores > 0 && (
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            totalItems={totalStores}
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

export default StoresPage

