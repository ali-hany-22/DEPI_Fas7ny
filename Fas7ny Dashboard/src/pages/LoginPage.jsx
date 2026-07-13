import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [remember, setRemember] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!email || !password) {
      setError('من فضلك أدخل البريد الإلكتروني وكلمة المرور')
      return
    }

    setLoading(true)
    try {
      await login(email, password)
    } catch (err) {
      setError(err.response?.data?.detail || 'حدث خطأ أثناء تسجيل الدخول، حاول مرة أخرى')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex" dir="rtl">
      {/* يمين: الفورم */}
      <div className="w-full md:w-1/2 flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 bg-white order-2">
        {/* Logo */}
        <button onClick={() => navigate('/')} className="flex items-center gap-2 mb-10">
          <img src="https://img.icons8.com/ios/50/C9A84C/world-map.png" className="w-6 h-6" alt="logo" />
          <span className="text-lg font-bold text-nile">فسحني</span>
        </button>

        <h1 className="text-2xl font-heading font-bold text-nile mb-1">أهلاً بيك من جديد</h1>
        <p className="text-muted text-sm mb-8">سعداء بعودتك إلينا، استكمل رحلتك الآن.</p>

        {/* Social buttons */}
        <div className="flex gap-3 mb-5">
          <button className="flex-1 border border-line rounded-lg py-2.5 text-sm text-muted hover:bg-sand/30 transition-colors">iOS</button>
          <button className="flex-1 border border-line rounded-lg py-2.5 flex items-center justify-center hover:bg-sand/30 transition-colors">
            <svg className="w-5 h-5 fill-[#1877F2]" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </button>
          <button className="flex-1 border border-line rounded-lg py-2.5 flex items-center justify-center hover:bg-sand/30 transition-colors">
            <svg className="w-5 h-5" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
          </button>
        </div>

        {/* Divider */}
        <div className="flex items-center gap-3 mb-5">
          <div className="flex-1 h-px bg-line"></div>
          <span className="text-xs text-muted">أو سجل عبر البريد</span>
          <div className="flex-1 h-px bg-line"></div>
        </div>

        <form onSubmit={handleSubmit}>
          {error && (
            <div className="mb-4 px-4 py-2.5 rounded-lg bg-warning-bg border border-warning/30 text-sm text-coral text-right">
              {error}
            </div>
          )}

          {/* Email */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-ink mb-1.5">البريد الإلكتروني</label>
            <div className="relative">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@domain.com"
                className="w-full border border-line rounded-lg px-4 py-2.5 pl-10 text-sm text-right outline-none focus:border-gold placeholder:text-gray-300"
              />
              <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-300">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              </div>
            </div>
          </div>

          {/* Password */}
          <div className="mb-4">
            <div className="flex justify-between mb-1.5">
              <button type="button" className="text-xs text-coral hover:underline">نسيت كلمة المرور؟</button>
              <label className="text-sm font-medium text-ink">كلمة المرور</label>
            </div>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
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

          {/* Remember */}
          <div className="flex items-center justify-end gap-2 mb-6">
            <label htmlFor="remember" className="text-sm text-muted cursor-pointer">تذكرني على هذا الجهاز</label>
            <input
              id="remember"
              type="checkbox"
              checked={remember}
              onChange={(e) => setRemember(e.target.checked)}
              className="w-4 h-4 accent-gold cursor-pointer"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gold hover:bg-gold-dark disabled:opacity-60 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold transition-colors text-sm flex items-center justify-center gap-2"
          >
            {loading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            {!loading && (
              <svg className="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/></svg>
            )}
          </button>
        </form>

        <p className="text-center text-sm text-muted mt-6">
          مالك نشاط جديد؟{' '}
          <Link to="/register" className="text-gold font-semibold hover:underline">سجّل نشاطك</Link>
        </p>
      </div>

      {/* شمال: الصورة */}
      <div className="hidden md:block md:w-1/2 relative order-1">
        <img
          src="https://i.pinimg.com/1200x/df/33/0b/df330b815956e31ee4f8fa3a7f3ba9dd.jpg"
          className="absolute inset-0 w-full h-full object-cover object-center"
          alt=""
        />

        <div className="relative z-10 h-full flex flex-col justify-between py-10 px-10">
          {/* Logo */}
          <div className="flex items-center gap-2 self-start">
            <div className="w-8 h-8 bg-gold rounded-lg flex items-center justify-center">
              <img src="https://img.icons8.com/ios/50/ffffff/world-map.png" className="w-5 h-5" alt="logo" />
            </div>
            <span className="text-xl font-bold text-gold">فسحني</span>
          </div>

          {/* Bottom content */}
          <div>
            <h2 className="text-white text-2xl font-bold mb-2">اكتشف سحر مصر برؤية عصرية ذكية</h2>
            <p className="text-white/70 text-sm mb-6">انضم إلى مجتمع رحلة واستمتع بتجارب سياحية مخصصة بالذكاء الاصطناعي.</p>

            {/* Testimonial */}
            <div className="bg-white/15 backdrop-blur-md rounded-xl p-4 text-right border border-white/20">
              <div className="flex items-center justify-end gap-3 mb-2">
                <div>
                  <p className="font-bold text-white text-sm">سارة محمود</p>
                  <p className="text-xs text-white/60">مسافرة شغوفة</p>
                </div>
                <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&q=80" className="w-9 h-9 rounded-full object-cover" alt="" />
              </div>
              <p className="text-white/85 text-xs leading-relaxed">"الدليل الذكي جعل كل لحظة في الأقصر وأسوان حكاية تاريخية لا تُنسى"</p>
              <div className="flex gap-0.5 mt-2 justify-end">
                {[1, 2, 3, 4].map((i) => (
                  <svg key={i} className="w-3.5 h-3.5 fill-gold" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                ))}
              </div>
            </div>

            <p className="text-white/30 text-xs mt-4 text-center">© 2024 فسحني - جميع الحقوق محفوظة</p>
          </div>
        </div>
      </div>
    </div>
  )
}
