import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { Star } from 'lucide-react'
import { getAnalytics } from '../api/provider'

function formatMoney(n) {
  return new Intl.NumberFormat('ar-EG').format(n)
}

function monthLabel(ym) {
  const [year, month] = ym.split('-')
  const date = new Date(Number(year), Number(month) - 1, 1)
  return date.toLocaleDateString('ar-EG', { month: 'short' })
}

export default function AnalyticsPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getAnalytics()
      .then(setData)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center text-muted py-20">جاري تحميل التحليلات...</div>
  if (!data) return null

  const chartData = data.monthly_trend.map((p) => ({ ...p, label: monthLabel(p.month) }))

  return (
    <div className="flex flex-col gap-6">
      <h1 className="font-heading font-extrabold text-2xl text-ink text-right">التحليلات</h1>

      <div className="grid sm:grid-cols-2 gap-4">
        <div className="bg-white border border-line rounded-2xl p-5 text-right">
          <div className="text-sm text-muted mb-1">إجمالي التقييمات</div>
          <div className="text-3xl font-heading font-extrabold text-ink">{data.total_reviews}</div>
        </div>
        <div className="bg-white border border-line rounded-2xl p-5 text-right">
          <div className="flex items-center justify-end gap-2 mb-1">
            <span className="text-sm text-muted">متوسط التقييم</span>
            <Star size={16} className="fill-gold text-gold" />
          </div>
          <div className="text-3xl font-heading font-extrabold text-ink">{data.average_rating.toFixed(1)}</div>
        </div>
      </div>

      <div className="bg-white border border-line rounded-2xl p-5">
        <h3 className="font-heading font-extrabold text-ink text-right mb-4">الإيرادات - آخر 6 شهور</h3>
        <div style={{ direction: 'ltr' }} className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#E7E2D6" />
              <XAxis dataKey="label" stroke="#6B7280" fontSize={12} />
              <YAxis stroke="#6B7280" fontSize={12} />
              <Tooltip
                formatter={(value) => [`${formatMoney(value)} ج.م`, 'الإيرادات']}
                contentStyle={{ borderRadius: 12, border: '1px solid #E7E2D6', fontFamily: 'IBM Plex Sans Arabic' }}
              />
              <Line type="monotone" dataKey="revenue" stroke="#A8872F" strokeWidth={2.5} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white border border-line rounded-2xl p-5">
        <h3 className="font-heading font-extrabold text-ink text-right mb-4">أفضل الخدمات</h3>
        {data.top_services.length === 0 ? (
          <p className="text-muted text-sm text-center py-6">لا توجد بيانات كافية بعد</p>
        ) : (
          <div className="flex flex-col divide-y divide-line">
            {data.top_services.map((s, i) => (
              <div key={i} className="py-3 flex items-center justify-between">
                <div className="text-right">
                  <span className="font-bold text-gold-dark">{formatMoney(s.revenue)} ج.م</span>
                </div>
                <div className="text-right">
                  <div className="font-bold text-ink text-sm">{s.service_title}</div>
                  <div className="text-xs text-muted">{s.bookings_count} حجز</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
