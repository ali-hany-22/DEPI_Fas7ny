const STYLES = {
  confirmed: { bg: 'bg-success-bg', text: 'text-success', label: 'مؤكد' },
  completed: { bg: 'bg-gray-100', text: 'text-gray-600', label: 'تم الإكمال' },
  pending: { bg: 'bg-warning-bg', text: 'text-warning', label: 'قيد الانتظار' },
  cancelled: { bg: 'bg-red-50', text: 'text-coral', label: 'ملغي' },
  active: { bg: 'bg-success-bg', text: 'text-success', label: 'نشط' },
  disabled: { bg: 'bg-gray-100', text: 'text-gray-500', label: 'معطل' },
  open: { bg: 'bg-warning-bg', text: 'text-warning', label: 'مفتوحة' },
  in_progress: { bg: 'bg-sand', text: 'text-gold-dark', label: 'جاري العمل عليها' },
  resolved: { bg: 'bg-success-bg', text: 'text-success', label: 'تم الحل' },
  closed: { bg: 'bg-gray-100', text: 'text-gray-500', label: 'مغلقة' },
}

export default function StatusBadge({ status }) {
  const style = STYLES[status] || { bg: 'bg-gray-100', text: 'text-gray-600', label: status }
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${style.bg} ${style.text}`}>
      {style.label}
    </span>
  )
}
