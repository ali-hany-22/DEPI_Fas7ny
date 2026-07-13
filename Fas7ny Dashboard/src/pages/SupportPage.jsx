import { useEffect, useState, useCallback } from 'react'
import { Plus, X } from 'lucide-react'
import { listTickets, createTicket } from '../api/provider'
import StatusBadge from '../components/StatusBadge'

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' })
}

export default function SupportPage() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [formOpen, setFormOpen] = useState(false)
  const [form, setForm] = useState({ subject: '', message: '' })
  const [saving, setSaving] = useState(false)

  const load = useCallback(() => {
    setLoading(true)
    listTickets()
      .then(setTickets)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    load()
  }, [load])

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    try {
      await createTicket(form)
      setForm({ subject: '', message: '' })
      setFormOpen(false)
      load()
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <button
          onClick={() => setFormOpen((v) => !v)}
          className="flex items-center gap-2 bg-gold-dark hover:bg-gold text-white font-bold px-5 py-2.5 rounded-xl transition-colors"
        >
          {formOpen ? <X size={18} /> : <Plus size={18} />}
          {formOpen ? 'إلغاء' : 'فتح تذكرة جديدة'}
        </button>
        <h1 className="font-heading font-extrabold text-2xl text-ink">الدعم الفني</h1>
      </div>

      {formOpen && (
        <form onSubmit={handleSubmit} className="bg-white border border-line rounded-2xl p-5 flex flex-col gap-4">
          <div>
            <label className="block text-sm font-bold text-ink mb-1.5">الموضوع</label>
            <input
              required
              value={form.subject}
              onChange={(e) => setForm((f) => ({ ...f, subject: e.target.value }))}
              className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right"
              placeholder="مشكلة في رفع الصور"
            />
          </div>
          <div>
            <label className="block text-sm font-bold text-ink mb-1.5">تفاصيل المشكلة</label>
            <textarea
              required
              rows={4}
              value={form.message}
              onChange={(e) => setForm((f) => ({ ...f, message: e.target.value }))}
              className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right resize-none"
            />
          </div>
          <button
            type="submit"
            disabled={saving}
            className="bg-gold-dark hover:bg-gold text-white font-bold py-2.5 rounded-xl transition-colors disabled:opacity-60 self-start px-6"
          >
            {saving ? 'جاري الإرسال...' : 'إرسال التذكرة'}
          </button>
        </form>
      )}

      {loading && <div className="text-center text-muted py-16">جاري التحميل...</div>}

      {!loading && tickets.length === 0 && (
        <div className="text-center text-muted py-16 bg-white border border-line rounded-2xl">
          لا توجد تذاكر دعم فني. لو احتجت مساعدة، افتح تذكرة جديدة.
        </div>
      )}

      <div className="flex flex-col gap-3">
        {tickets.map((t) => (
          <div key={t.id} className="bg-white border border-line rounded-2xl p-5 text-right">
            <div className="flex items-center justify-between mb-2">
              <StatusBadge status={t.status} />
              <div>
                <span className="font-bold text-ink">{t.subject}</span>
                <span className="text-xs text-muted block">{formatDate(t.created_at)}</span>
              </div>
            </div>
            <p className="text-sm text-muted leading-relaxed">{t.message}</p>
            {t.admin_reply && (
              <div className="mt-3 pt-3 border-t border-line">
                <div className="text-xs font-bold text-gold-dark mb-1">رد فريق الدعم</div>
                <p className="text-sm text-ink leading-relaxed">{t.admin_reply}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
