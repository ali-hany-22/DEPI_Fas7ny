import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import DashboardLayout from './layouts/DashboardLayout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import BookingsPage from './pages/BookingsPage'
import ServicesPage from './pages/ServicesPage'
import AnalyticsPage from './pages/AnalyticsPage'
import SupportPage from './pages/SupportPage'

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        {/*
          كانت هنا بتوجه لـ /dashboard مباشرة وبشكل غير مشروط، حتى لو
          مفيش تسجيل دخول أصلاً - يعني أي حد يفتح الموقع لأول مرة كان
          بيوصل لصفحة "/" فتتحول فورًا لـ "/dashboard" من غير أي تحقق
          هنا. التحقق الحقيقي كان المفروض يحصل جوه ProtectedRoute بعد
          كده، لكن الأصح إن نقطة الدخول الافتراضية تكون /login مش
          /dashboard - عشان أي زائر جديد (مفيش له token خالص) يشوف
          صفحة تسجيل الدخول على طول من غير ما يمر أصلاً على /dashboard
          ويعتمد على redirect تاني جواها.
        */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
          <Route path="/services" element={<ServicesPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/support" element={<SupportPage />} />
        </Route>

        {/*
          نفس المبدأ: أي مسار مش معروف كان بيتحول لـ /dashboard مباشرة
          بدل /login. لو المستخدم مش مسجل دخول أصلاً، الأصح إنه يوصله
          لصفحة الدخول، مش لصفحة محمية هيترفض منها فورًا (حتى لو
          ProtectedRoute في النهاية هيرجعه بره، الأوضح إننا نوجهه صح
          من الأول).
        */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AuthProvider>
  )
}
