import { useEffect, useState, useCallback } from 'react'
import { getBookings, updateBookingStatus } from '../api/provider'
import StatusBadge from '../components/StatusBadge'

function formatMoney(n) {
  return new Intl.NumberFormat('ar-EG').format(n)
}
function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' })
}

const FILTERS = [
  { value: '', label: 'الكل' },
  { value: 'pending', label: 'قيد الانتظار' },
  { value: 'confirmed', label: 'مؤكد' },
  { value: 'completed', label: 'تم الإكمال' },
  { value: 'cancelled', label: 'ملغي' },
]

const NEXT_STATUS = {
  pending: 'confirmed',
  confirmed: 'completed',
}
const NEXT_LABEL = {
  pending: 'تأكيد الحجز',
  confirmed: 'إنهاء الحجز',
}

export default function BookingsPage() {
  const [bookings, setBookings] = useState([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    getBookings(filter || undefined)
      .then(setBookings)
      .finally(() => setLoading(false))
  }, [filter])

  useEffect(() => {
    load()
  }, [load])

  async function handleAdvance(booking) {
    const next = NEXT_STATUS[booking.status]
    if (!next) return
    await updateBookingStatus(booking.id, next)
    load()
  }

  async function handleCancel(booking) {
    await updateBookingStatus(booking.id, 'cancelled')
    load()
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="font-heading font-extrabold text-2xl text-ink">الحجوزات</h1>
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        {FILTERS.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-4 py-2 rounded-full text-sm font-bold border transition-colors ${
              filter === f.value
                ? 'bg-gold-dark text-white border-gold-dark'
                : 'border-line text-muted hover:bg-sand/40'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="bg-white border border-line rounded-2xl overflow-x-auto">
        <table className="w-full text-sm text-right">
          <thead>
            <tr className="border-b border-line text-muted">
              <th className="font-medium py-3 px-4">إجراء</th>
              <th className="font-medium py-3 px-4">الحالة</th>
              <th className="font-medium py-3 px-4">المبلغ</th>
              <th className="font-medium py-3 px-4">التاريخ</th>
              <th className="font-medium py-3 px-4">الخدمة</th>
              <th className="font-medium py-3 px-4">العميل</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr>
                <td colSpan={6} className="text-center text-muted py-10">
                  جاري التحميل...
                </td>
              </tr>
            )}
            {!loading && bookings.length === 0 && (
              <tr>
                <td colSpan={6} className="text-center text-muted py-10">
                  لا توجد حجوزات
                </td>
              </tr>
            )}
            {bookings.map((b) => (
              <tr key={b.id} className="border-b border-line last:border-0">
                <td className="py-3 px-4">
                  <div className="flex gap-2 justify-end">
                    {NEXT_STATUS[b.status] && (
                      <button
                        onClick={() => handleAdvance(b)}
                        className="text-xs font-bold text-gold-dark border border-gold-dark/30 rounded-lg px-3 py-1.5 hover:bg-sand/40"
                      >
                        {NEXT_LABEL[b.status]}
                      </button>
                    )}
                    {b.status !== 'cancelled' && b.status !== 'completed' && (
                      <button
                        onClick={() => handleCancel(b)}
                        className="text-xs font-bold text-coral border border-red-200 rounded-lg px-3 py-1.5 hover:bg-red-50"
                      >
                        إلغاء
                      </button>
                    )}
                  </div>
                </td>
                <td className="py-3 px-4">
                  <StatusBadge status={b.status} />
                </td>
                <td className="py-3 px-4 font-bold text-ink whitespace-nowrap">{formatMoney(b.amount)} ج.م</td>
                <td className="py-3 px-4 text-muted whitespace-nowrap">{formatDate(b.booking_date)}</td>
                <td className="py-3 px-4 text-ink">{b.service_title}</td>
                <td className="py-3 px-4 text-ink">{b.customer_name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
