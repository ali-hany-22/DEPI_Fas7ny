import { Wallet, Star, Smartphone, Eye, Download, Filter, ShieldCheck } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useDashboard } from '../hooks/useDashboard'
import KPICard from '../components/KPICard'
import StatusBadge from '../components/StatusBadge'
import StarRating from '../components/StarRating'
import { toggleServiceStatus } from '../api/provider'

function formatMoney(n) {
  return new Intl.NumberFormat('ar-EG').format(n)
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' })
}

const CHECKLIST_ITEMS = [
  { key: 'phone_verified', title: 'تأكيد رقم الهاتف', doneNote: 'تم التحقق بنجاح', todoNote: 'أكد رقمك لزيادة الثقة', action: null },
  { key: 'commercial_registry_uploaded', title: 'رفع السجل التجاري', doneNote: 'تمت المراجعة والقبول', todoNote: 'ارفع السجل التجاري للتوثيق', action: 'رفع السجل' },
  { key: 'photos_360_uploaded', title: 'إضافة صور 360 درجة', doneNote: 'تم رفع الصور', todoNote: 'ارفع صور بانورامية لمرافق الفندق', action: 'بدء الرفع' },
  { key: 'bank_account_verified', title: 'توثيق الحساب البنكي', doneNote: 'تم التوثيق', todoNote: 'لتلقي المدفوعات بشكل آلي', action: 'إضافة حساب' },
]

export default function DashboardPage() {
  const { data, loading, refresh } = useDashboard()

  if (loading && !data) {
    return <div className="text-muted text-center py-20">جاري تحميل بيانات الداشبورد...</div>
  }
  if (!data) return null

  async function handleToggle(serviceId) {
    await toggleServiceStatus(serviceId)
    refresh()
  }

  return (
    <div className="flex flex-col gap-6">
      {data.verification.is_verified && (
        <div className="flex items-center justify-between bg-success-bg border border-success/20 rounded-2xl p-5">
          <div className="flex items-center gap-4">
            <div className="w-11 h-11 rounded-full bg-success flex items-center justify-center text-white shrink-0">
              <ShieldCheck size={22} />
            </div>
            <div className="text-right">
              <div className="font-bold text-ink">تم توثيق حسابك بنجاح</div>
              <div className="text-sm text-muted">
                أنت الآن مزود خدمة معتمد في منصة رِحلة. يمكنك استقبال الحجوزات بشكل مباشر.
              </div>
            </div>
          </div>
          <button className="text-success font-bold text-sm whitespace-nowrap px-4">عرض الشهادة</button>
        </div>
      )}

      {/* KPIs */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard label="الإيرادات (ج.م)" value={formatMoney(data.kpis.revenue)} changePct={data.kpis.revenue_change_pct} icon={Wallet} />
        <KPICard label="التقييم العام" value={data.kpis.rating.toFixed(1)} changePct={data.kpis.rating_change_pct} icon={Star} />
        <KPICard label="الحجوزات" value={data.kpis.bookings_count} changePct={data.kpis.bookings_change_pct} icon={Smartphone} />
        <KPICard label="المشاهدات" value={formatMoney(data.kpis.views)} changePct={data.kpis.views_change_pct} icon={Eye} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-6">
        {/* Left column */}
        <div className="flex flex-col gap-6 order-2 lg:order-1">
          <div className="bg-white border border-line rounded-2xl p-5">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-bold text-gold-dark">{data.kpis.rating.toFixed(1)}/5.0</span>
              <h3 className="font-heading font-extrabold text-ink">التقييمات الأخيرة</h3>
            </div>
            <div className="flex flex-col divide-y divide-line">
              {data.recent_reviews.length === 0 && (
                <p className="text-muted text-sm py-4 text-center">لا توجد تقييمات بعد</p>
              )}
              {data.recent_reviews.map((r) => (
                <div key={r.id} className="py-4 first:pt-0 text-right">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-muted">{formatDate(r.created_at)}</span>
                    <StarRating rating={r.rating} />
                  </div>
                  {r.title && <div className="font-bold text-ink text-sm mb-1">{r.title}</div>}
                  {r.comment && <p className="text-sm text-muted leading-relaxed">{r.comment}</p>}
                </div>
              ))}
            </div>
            <button className="w-full mt-4 border border-line rounded-xl py-2.5 text-sm font-bold text-ink hover:bg-sand/40">
              قراءة كل التقييمات
            </button>
          </div>

          <div className="bg-white border border-line rounded-2xl p-5">
            <h3 className="font-heading font-extrabold text-ink text-right mb-1">طلبات التحقق</h3>
            <p className="text-sm text-muted text-right mb-4">
              أكمل المهام التالية لزيادة فرصة ظهورك في الصفحة الأولى.
            </p>
            <div className="flex flex-col divide-y divide-line">
              {CHECKLIST_ITEMS.map((item) => {
                const done = data.verification[item.key]
                return (
                  <div key={item.key} className="py-3.5 first:pt-0 flex items-start justify-between gap-3">
                    <div
                      className={`mt-0.5 w-5 h-5 rounded-md border shrink-0 flex items-center justify-center text-xs ${
                        done ? 'bg-success border-success text-white' : 'border-line'
                      }`}
                    >
                      {done ? '✓' : ''}
                    </div>
                    <div className="text-right flex-1">
                      <div className="font-bold text-sm text-ink">{item.title}</div>
                      <div className="text-xs text-muted">{done ? item.doneNote : item.todoNote}</div>
                      {!done && item.action && (
                        <button className="text-xs font-bold text-gold-dark mt-1 hover:underline">
                          {item.action}
                        </button>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>

        {/* Right column */}
        <div className="flex flex-col gap-6 order-1 lg:order-2">
          <div>
            <div className="flex items-center justify-between mb-3">
              <Link to="/services" className="text-sm font-bold text-gold-dark">
                عرض الكل
              </Link>
              <h3 className="font-heading font-extrabold text-ink text-lg">خدماتي المدرجة</h3>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              {data.services.map((s) => (
                <div key={s.id} className="bg-white border border-line rounded-2xl overflow-hidden">
                  <div className="relative h-40 bg-sand">
                    {s.image_url && (
                      <img src={s.image_url} alt={s.title} className="w-full h-full object-cover" />
                    )}
                    <span className="absolute top-3 right-3 bg-white/90 text-xs font-bold px-2.5 py-1 rounded-full">
                      {s.requires_confirmation ? 'يتطلب تأكيد' : 'حجز مباشر'}
                    </span>
                  </div>
                  <div className="p-4 text-right">
                    <div className="font-bold text-ink mb-1">{s.title}</div>
                    <div className="text-xs text-muted mb-4">
                      {s.requires_confirmation ? 'يتطلب تأكيد' : 'حجز مباشر'} · {s.bookings_this_month} حجز هذا الشهر
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleToggle(s.id)}
                        className="flex-1 border border-red-200 text-coral text-sm font-bold rounded-xl py-2 hover:bg-red-50"
                      >
                        {s.status === 'active' ? 'تعطيل' : 'تفعيل'}
                      </button>
                      {/*
                        كانت هنا Link لـ `/services/${s.id}` - مسار مش
                        معرّف خالص في App.jsx (المسار الوحيد المعرّف هو
                        "/services" بدون :id). أي محاولة فتحه كانت بتقع
                        على الـ catch-all route (*) اللي بيحول لـ
                        /login، فكان شكلها "تسجيل الدخول بيرجعني
                        للوجين" بينما هي أصلاً مشكلة route مش موجود.

                        التعديل الفعلي (modal الحقيقي المربوط بالـ
                        backend عبر updateService) موجود بالفعل وشغال
                        في ServicesPage.jsx - فبدل ما نضيف صفحة/route
                        جديد لتكرار نفس المنطق، أبسط وأصح حل إننا
                        نوجّه لنفس الصفحة الشغالة دي.
                      */}
                      <Link
                        to="/services"
                        className="flex-1 border border-line text-sm font-bold rounded-xl py-2 text-center hover:bg-sand/40"
                      >
                        تعديل
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
              {data.services.length === 0 && (
                <p className="text-muted text-sm py-8 text-center sm:col-span-2">لا توجد خدمات مدرجة بعد</p>
              )}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <button className="p-2 border border-line rounded-lg text-muted hover:text-ink">
                  <Filter size={16} />
                </button>
                <button className="p-2 border border-line rounded-lg text-muted hover:text-ink">
                  <Download size={16} />
                </button>
              </div>
              <h3 className="font-heading font-extrabold text-ink text-lg">الحجوزات الأخيرة</h3>
            </div>

            <div className="bg-white border border-line rounded-2xl overflow-x-auto">
              <table className="w-full text-sm text-right">
                <thead>
                  <tr className="border-b border-line text-muted">
                    <th className="font-medium py-3 px-4">الحالة</th>
                    <th className="font-medium py-3 px-4">المبلغ</th>
                    <th className="font-medium py-3 px-4">التاريخ</th>
                    <th className="font-medium py-3 px-4">الخدمة</th>
                    <th className="font-medium py-3 px-4">العميل</th>
                  </tr>
                </thead>
                <tbody>
                  {data.recent_bookings.map((b) => (
                    <tr key={b.id} className="border-b border-line last:border-0">
                      <td className="py-3 px-4">
                        <StatusBadge status={b.status} />
                      </td>
                      <td className="py-3 px-4 font-bold text-ink whitespace-nowrap">
                        {formatMoney(b.amount)} ج.م
                      </td>
                      <td className="py-3 px-4 text-muted whitespace-nowrap">{formatDate(b.booking_date)}</td>
                      <td className="py-3 px-4 text-ink">{b.service_title}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2 justify-end">
                          <span className="text-ink">{b.customer_name}</span>
                          <div className="w-8 h-8 rounded-full bg-sand flex items-center justify-center text-xs font-bold text-gold-dark shrink-0">
                            {b.customer_name?.split(' ').map((w) => w[0]).slice(0, 2).join('')}
                          </div>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {data.recent_bookings.length === 0 && (
                    <tr>
                      <td colSpan={5} className="text-center text-muted py-8">
                        لا توجد حجوزات بعد
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
