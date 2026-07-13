import { NavLink, Outlet } from 'react-router-dom'
import { LayoutGrid, Calendar, Compass, LineChart, CircleHelp, LogOut, Bell, Settings, Plus } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useDashboard } from '../hooks/useDashboard'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutGrid },
  { to: '/bookings', label: 'Bookings', icon: Calendar },
  { to: '/services', label: 'My Services', icon: Compass },
  { to: '/analytics', label: 'Analytics', icon: LineChart },
  { to: '/support', label: 'Support', icon: CircleHelp },
]

export default function DashboardLayout() {
  const { logout } = useAuth()
  const { data } = useDashboard()

  return (
    <div className="min-h-screen bg-page" dir="rtl">
      {/* Topbar */}
      <header className="flex items-center justify-between px-8 py-4 bg-white border-b border-line">
        <div className="flex items-center gap-3">
          <button className="p-2 text-muted hover:text-ink" aria-label="الإعدادات">
            <Settings size={20} />
          </button>
          <button className="p-2 text-muted hover:text-ink relative" aria-label="الإشعارات">
            <Bell size={20} />
          </button>
          <div className="flex items-center gap-2 border-e border-line pe-3 ms-1">
            <div className="w-9 h-9 rounded-full bg-nile text-white flex items-center justify-center text-sm font-bold overflow-hidden">
              {data?.business_name?.[0] || 'ف'}
            </div>
            <div className="text-right">
              <div className="text-sm font-bold text-ink leading-tight">
                {data?.business_name || '...'}
              </div>
              <div className="text-xs text-muted leading-tight">
                {data?.business_name_en || ''}
              </div>
            </div>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted">
          <NavLink to="/services" className={({ isActive }) => (isActive ? 'text-ink' : '')}>
            My Services
          </NavLink>
          <NavLink to="/bookings" className={({ isActive }) => (isActive ? 'text-ink' : '')}>
            Bookings
          </NavLink>
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `pb-1 border-b-2 ${isActive ? 'text-gold border-gold font-bold' : 'border-transparent'}`
            }
          >
            Dashboard
          </NavLink>
          <span className="px-3 py-1.5 rounded-full bg-sand text-gold-dark text-xs font-bold">
            لوحة المزوّدين
          </span>
        </nav>

        <div className="text-xl font-heading font-extrabold text-gold">فسحني</div>
      </header>

      <div className="flex items-start max-w-[1920px] mx-auto">
        {/* Main content */}
        <main className="flex-1 p-6 lg:p-8 min-w-0">
          <Outlet />
        </main>

        {/* Right sidebar */}
        <aside className="hidden lg:flex flex-col w-64 shrink-0 p-6 gap-1 sticky top-0">
          <div className="mb-4">
            <div className="text-lg font-heading font-extrabold text-gold">
              {data?.business_name_en || 'Provider'}
            </div>
            <div className="text-sm text-muted">
              {data?.tier === 'elite' ? 'Elite Provider' : 'Provider'}
            </div>
          </div>

          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-sand text-gold-dark font-bold'
                    : 'text-ink hover:bg-sand/50'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <span>{label}</span>
                  <Icon size={18} className={isActive ? 'text-gold-dark' : 'text-muted'} />
                </>
              )}
            </NavLink>
          ))}

          <button className="mt-6 w-full flex items-center justify-center gap-2 bg-gold-dark hover:bg-gold text-white font-bold py-3 rounded-xl transition-colors">
            <Plus size={18} />
            Add New Service
          </button>

          <div className="mt-auto pt-8 flex flex-col gap-1">
            <a href="#" className="flex items-center justify-between px-4 py-2 text-sm text-muted hover:text-ink">
              Help Center
              <CircleHelp size={16} />
            </a>
            <button
              onClick={logout}
              className="flex items-center justify-between px-4 py-2 text-sm text-coral hover:opacity-80 text-right"
            >
              Sign Out
              <LogOut size={16} />
            </button>
          </div>
        </aside>
      </div>
    </div>
  )
}
