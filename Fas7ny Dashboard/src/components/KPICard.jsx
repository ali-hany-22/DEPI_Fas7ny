export default function KPICard({ label, value, changePct, icon: Icon }) {
  const isPositive = changePct > 0
  const isZero = changePct === 0

  return (
    <div className="bg-white border border-line rounded-2xl p-5 flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <span
          className={`text-sm font-bold ${
            isZero ? 'text-muted' : isPositive ? 'text-success' : 'text-coral'
          }`}
        >
          {isZero ? '0.0%' : `${isPositive ? '+' : ''}${changePct}%`}
        </span>
        <div className="w-10 h-10 rounded-xl bg-sand flex items-center justify-center text-gold-dark">
          <Icon size={20} />
        </div>
      </div>
      <div className="text-right">
        <div className="text-sm text-muted mb-1">{label}</div>
        <div className="text-3xl font-heading font-extrabold text-ink">{value}</div>
      </div>
    </div>
  )
}
