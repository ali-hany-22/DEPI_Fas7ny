import { useEffect, useState, useCallback } from 'react'
import { Plus, Pencil, Trash2 } from 'lucide-react'
import { listServices, createService, updateService, deleteService } from '../api/provider'
import StatusBadge from '../components/StatusBadge'
import ServiceFormModal from '../components/ServiceFormModal'

function formatMoney(n) {
  return new Intl.NumberFormat('ar-EG').format(n)
}

export default function ServicesPage() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)

  const load = useCallback(() => {
    setLoading(true)
    listServices()
      .then(setServices)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load()
  }, [load])

  function openCreate() {
    setEditing(null)
    setModalOpen(true)
  }

  function openEdit(service) {
    setEditing(service)
    setModalOpen(true)
  }

  async function handleSubmit(payload) {
    if (editing) {
      await updateService(editing.id, payload)
    } else {
      await createService(payload)
    }
    setModalOpen(false)
    load()
  }

  async function handleDelete(service) {
    if (!confirm(`هل تريد حذف "${service.title}"؟`)) return
    try {
      await deleteService(service.id)
      load()
    } catch (err) {
      if (err.response?.status === 409) {
        alert(err.response.data.detail)
      } else {
        alert('حدث خطأ أثناء الحذف')
      }
    }
  }

  async function handleToggle(service) {
    await updateService(service.id, {
      status: service.status === 'active' ? 'disabled' : 'active',
    })
    load()
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <button
          onClick={openCreate}
          className="flex items-center gap-2 bg-gold-dark hover:bg-gold text-white font-bold px-5 py-2.5 rounded-xl transition-colors"
        >
          <Plus size={18} />
          إضافة خدمة
        </button>
        <h1 className="font-heading font-extrabold text-2xl text-ink">خدماتي</h1>
      </div>

      {loading && <div className="text-center text-muted py-16">جاري التحميل...</div>}

      {!loading && services.length === 0 && (
        <div className="text-center text-muted py-16 bg-white border border-line rounded-2xl">
          لا توجد خدمات مضافة بعد. ابدأ بإضافة أول خدمة.
        </div>
      )}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((s) => (
          <div key={s.id} className="bg-white border border-line rounded-2xl overflow-hidden flex flex-col">
            <div className="relative h-36 bg-sand">
              {s.image_url && <img src={s.image_url} alt={s.title} className="w-full h-full object-cover" />}
              <div className="absolute top-3 right-3">
                <StatusBadge status={s.status} />
              </div>
            </div>
            <div className="p-4 flex flex-col flex-1 text-right">
              <div className="font-bold text-ink mb-1">{s.title}</div>
              {s.description && <p className="text-xs text-muted mb-2 line-clamp-2">{s.description}</p>}
              <div className="text-sm font-bold text-gold-dark mb-1">{formatMoney(s.price)} ج.م</div>
              <div className="text-xs text-muted mb-4">{s.bookings_this_month} حجز هذا الشهر</div>

              <div className="flex gap-2 mt-auto">
                <button
                  onClick={() => handleToggle(s)}
                  className="flex-1 border border-red-200 text-coral text-sm font-bold rounded-xl py-2 hover:bg-red-50"
                >
                  {s.status === 'active' ? 'تعطيل' : 'تفعيل'}
                </button>
                <button
                  onClick={() => openEdit(s)}
                  className="flex-1 border border-line text-sm font-bold rounded-xl py-2 hover:bg-sand/40 flex items-center justify-center gap-1.5"
                >
                  <Pencil size={14} />
                  تعديل
                </button>
                <button
                  onClick={() => handleDelete(s)}
                  className="border border-line text-coral rounded-xl px-3 hover:bg-red-50"
                  aria-label="حذف"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {modalOpen && (
        <ServiceFormModal initial={editing} onClose={() => setModalOpen(false)} onSubmit={handleSubmit} />
      )}
    </div>
  )
}
