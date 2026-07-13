import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const BUSINESS_TYPES = [
  { value: 'hotel', label: 'فندق' },
  { value: 'restaurant', label: 'مطعم' },
  { value: 'transport', label: 'مواصلات' },
  { value: 'tour_guide', label: 'مرشد سياحي' },
  { value: 'activity', label: 'نشاط سياحي' },
  { value: 'other', label: 'أخرى' },
]

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: '',
    business_name: '',
    business_name_en: '',
    business_type: 'hotel',
    city: '',
  })
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [agree, setAgree] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!form.full_name || !form.email || !form.password || !confirmPassword) {
      setError('من فضلك أكمل جميع الحقول')
      return
    }
    if (form.password !== confirmPassword) {
      setError('كلمة المرور غير متطابقة')
      return
    }
    if (form.password.length < 8) {
      setError('كلمة المرور يجب أن تكون 8 أحرف على الأقل')
      return
    }
    if (!agree) {
      setError('يجب الموافقة على الشروط والأحكام أولاً')
      return
    }

    setLoading(true)
    try {
      await register(form)
    } catch (err) {
      setError(err.response?.data?.detail || 'حدث خطأ أثناء إنشاء الحساب، حاول مرة أخرى')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div dir="rtl" className="min-h-screen relative flex items-center justify-center py-12 px-4">
      {/* Background image */}
      <img
        src="https://i.pinimg.com/1200x/97/c0/77/97c077228459ba50ef898ed05a34f6fd.jpg"
        className="absolute inset-0 w-full h-full object-cover object-center"
        alt=""
      />

      {/* Form card */}
      <div className="relative z-10 bg-white rounded-2xl shadow-2xl w-full max-w-lg px-10 py-10">
        {/* Logo */}
        <button onClick={() => navigate('/')} className="flex items-center gap-2 mb-6">
          <img src="https://img.icons8.com/ios/50/C9A84C/world-map.png" className="w-5 h-5" alt="logo" />
          <span className="text-base font-bold text-nile">فسحني</span>
        </button>

        <h1 className="text-2xl font-heading font-bold text-nile mb-1">سجّل نشاطك كمزوّد خدمة</h1>
        <p className="text-muted text-sm mb-6">انضم إلينا وابدأ استقبال حجوزات العملاء.</p>

        <form onSubmit={handleSubmit}>
          {error && (
            <div className="mb-4 px-4 py-2.5 rounded-lg bg-warning-bg border border-warning/30 text-sm text-coral text-right">
              {error}
            </div>
          )}

          {/* الاسم + الهاتف */}
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-sm font-medium text-ink mb-1">اسمك الكامل</label>
              <input
                required
                value={form.full_name}
                onChange={(e) => update('full_name', e.target.value)}
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1">رقم الهاتف</label>
              <input
                value={form.phone}
                onChange={(e) => update('phone', e.target.value)}
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
            </div>
          </div>

          {/* Email */}
          <div className="mb-3">
            <label className="block text-sm font-medium text-ink mb-1">البريد الإلكتروني</label>
            <div className="relative">
              <input
                type="email"
                required
                value={form.email}
                onChange={(e) => update('email', e.target.value)}
                placeholder="example@domain.com"
                className="w-full border border-line rounded-lg px-4 py-2.5 pl-10 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-300">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              </div>
            </div>
          </div>

          {/* Password */}
          <div className="mb-3">
            <label className="block text-sm font-medium text-ink mb-1">كلمة المرور</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                required
                minLength={8}
                value={form.password}
                onChange={(e) => update('password', e.target.value)}
                placeholder="••••••••"
                className="w-full border border-line rounded-lg px-4 py-2.5 pl-10 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500"
              >
                {!showPassword ? (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                )}
              </button>
            </div>
          </div>

          {/* Confirm Password */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-ink mb-1">تأكيد كلمة المرور</label>
            <div className="relative">
              <input
                type={showConfirm ? 'text' : 'password'}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className={`w-full border rounded-lg px-4 py-2.5 pl-10 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300 ${
                  confirmPassword && confirmPassword !== form.password ? 'border-coral' : 'border-line'
                }`}
              />
              <button
                type="button"
                onClick={() => setShowConfirm(!showConfirm)}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500"
              >
                {!showConfirm ? (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
                )}
              </button>
            </div>
            {confirmPassword && confirmPassword !== form.password && (
              <p className="text-xs text-coral mt-1 text-right">كلمة المرور غير متطابقة</p>
            )}
          </div>

          <hr className="border-line my-2" />

          {/* اسم النشاط عربي/إنجليزي */}
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div>
              <label className="block text-sm font-medium text-ink mb-1">اسم النشاط (عربي)</label>
              <input
                required
                value={form.business_name}
                onChange={(e) => update('business_name', e.target.value)}
                placeholder="فندق النيل أسوان"
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1">اسم النشاط (إنجليزي)</label>
              <input
                value={form.business_name_en}
                onChange={(e) => update('business_name_en', e.target.value)}
                placeholder="Luxor Travels"
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
            </div>
          </div>

          {/* نوع النشاط + المدينة */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            <div>
              <label className="block text-sm font-medium text-ink mb-1">نوع النشاط</label>
              <select
                value={form.business_type}
                onChange={(e) => update('business_type', e.target.value)}
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold bg-white"
              >
                {BUSINESS_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1">المدينة</label>
              <input
                value={form.city}
                onChange={(e) => update('city', e.target.value)}
                placeholder="أسوان"
                className="w-full border border-line rounded-lg px-4 py-2.5 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
            </div>
          </div>

          {/* Terms */}
          <div className="flex items-center justify-end gap-2 mb-5">
            <label htmlFor="agree" className="text-sm text-muted cursor-pointer">
              أوافق على <button type="button" className="text-gold hover:underline">الشروط والأحكام</button>
            </label>
            <input
              id="agree"
              type="checkbox"
              checked={agree}
              onChange={(e) => setAgree(e.target.checked)}
              className="w-4 h-4 accent-gold cursor-pointer"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gold hover:bg-gold-dark disabled:opacity-60 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold transition-colors text-sm flex items-center justify-center gap-2"
          >
            {loading ? 'جاري إنشاء الحساب...' : 'إنشاء الحساب'}
            {!loading && (
              <svg className="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/></svg>
            )}
          </button>
        </form>

        <p className="text-center text-sm text-muted mt-5">
          عندك حساب بالفعل؟{' '}
          <Link to="/login" className="text-gold font-semibold hover:underline">تسجيل الدخول</Link>
        </p>
      </div>
    </div>
  )
}
