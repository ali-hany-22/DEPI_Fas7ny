import { useState, useEffect } from 'react'
import { X } from 'lucide-react'

export default function ServiceFormModal({ initial, onClose, onSubmit }) {
  const [form, setForm] = useState({
    title: '',
    description: '',
    price: '',
    image_url: '',
    requires_confirmation: false,
  })
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (initial) {
      setForm({
        title: initial.title || '',
        description: initial.description || '',
        price: initial.price ?? '',
        image_url: initial.image_url || '',
        requires_confirmation: !!initial.requires_confirmation,
      })
    }
  }, [initial])

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    try {
      await onSubmit({ ...form, price: parseFloat(form.price) })
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50" dir="rtl">
      <div className="bg-white rounded-2xl w-full max-w-md p-6 relative">
        <button onClick={onClose} className="absolute left-4 top-4 text-muted hover:text-ink">
          <X size={20} />
        </button>
        <h2 className="font-heading font-extrabold text-xl text-ink mb-5">
          {initial ? 'تعديل الخدمة' : 'إضافة خدمة جديدة'}
        </h2>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div>
            <label className="block text-sm font-bold text-ink mb-1.5">اسم الخدمة</label>
            <input
              required
              value={form.title}
              onChange={(e) => update('title', e.target.value)}
              className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right"
              placeholder="غرفة مزدوجة - كلاسيكية"
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-ink mb-1.5">الوصف</label>
            <textarea
              value={form.description}
              onChange={(e) => update('description', e.target.value)}
              rows={3}
              className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-ink mb-1.5">السعر (ج.م)</label>
              <input
                required
                type="number"
                min="0"
                step="0.01"
                value={form.price}
                onChange={(e) => update('price', e.target.value)}
                className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right"
              />
            </div>
            <div className="flex items-center gap-2 pt-7">
              <input
                type="checkbox"
                id="requires_confirmation"
                checked={form.requires_confirmation}
                onChange={(e) => update('requires_confirmation', e.target.checked)}
                className="w-4 h-4 accent-gold-dark"
              />
              <label htmlFor="requires_confirmation" className="text-sm text-ink">
                يتطلب تأكيد
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-bold text-ink mb-1.5">رابط الصورة (اختياري)</label>
            <input
              value={form.image_url}
              onChange={(e) => update('image_url', e.target.value)}
              className="w-full border border-line rounded-xl px-4 py-2.5 outline-none focus:border-gold text-right"
              placeholder="https://..."
            />
          </div>

          <button
            type="submit"
            disabled={saving}
            className="mt-2 bg-gold-dark hover:bg-gold text-white font-bold py-3 rounded-xl transition-colors disabled:opacity-60"
          >
            {saving ? 'جاري الحفظ...' : initial ? 'حفظ التعديلات' : 'إضافة الخدمة'}
          </button>
        </form>
      </div>
    </div>
  )
}
