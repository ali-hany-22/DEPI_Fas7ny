import axios from 'axios'

// عنوان الـ backend - غيّره لو الـ FastAPI شغال على بورت مختلف عندك.
// وقت التطوير هو نفس اللي شغال بيه uvicorn (افتراضيًا 8000).
const BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ---------------------------------------------------------------------
// تخزين الـ token: بنستخدم localStorage عشان يفضل موجود بعد ما
// المستخدم يقفل التاب أو يعمل refresh (مش زي sessionStorage اللي
// بيتمسح). لو عايز "تذكرني" اختيارية بمعنى حقيقي (يعني لو مش متفعلة
// الـ session تروح بمجرد قفل المتصفح)، ده محتاج شغل إضافي - نتكلم
// عنه لو احتجته بعدين.
// ---------------------------------------------------------------------
const TOKEN_KEY = 'fas7ny_access_token'
const ROLE_KEY = 'fas7ny_role'

export function saveAuth(accessToken, role) {
  localStorage.setItem(TOKEN_KEY, accessToken)
  localStorage.setItem(ROLE_KEY, role)
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function getRole() {
  return localStorage.getItem(ROLE_KEY)
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(ROLE_KEY)
}

// بيضيف الـ token تلقائيًا لأي request بعد تسجيل الدخول، عشان
// الـ endpoints المحمية (زي provider dashboard) تشتغل من غير ما
// نكتب الهيدر يدويًا في كل مكان.
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ---------------------------------------------------------------------
// دوال الـ Auth الجاهزة للاستخدام المباشر من صفحات login/register
// ---------------------------------------------------------------------

/**
 * تسجيل دخول سائح عادي.
 * بيرمي error فيه response.data.detail (رسالة الخطأ العربي الجاهزة
 * من الـ backend، زي "البريد الإلكتروني أو كلمة المرور غير صحيحة")
 * لو فشل - الصفحة اللي بتستدعيها هي اللي تمسك الـ error وتعرضه.
 */
export async function loginTourist(email, password) {
  const { data } = await api.post('/auth/login', { email, password })
  saveAuth(data.access_token, data.role)
  return data
}

export async function registerTourist({ fullName, email, password, phone = null }) {
  const { data } = await api.post('/auth/register', {
    full_name: fullName,
    email,
    password,
    phone,
  })
  saveAuth(data.access_token, data.role)
  return data
}

export async function loginProvider(email, password) {
  const { data } = await api.post('/provider/auth/login', { email, password })
  saveAuth(data.access_token, data.role)
  return data
}

export async function registerProvider(payload) {
  // payload المتوقع: { fullName, email, password, phone, businessName,
  // businessNameEn, businessType, city } - بنحولها لأسماء snake_case
  // اللي الـ backend مستني (ProviderRegisterRequest schema)
  const { data } = await api.post('/provider/auth/register', {
    full_name: payload.fullName,
    email: payload.email,
    password: payload.password,
    phone: payload.phone ?? null,
    business_name: payload.businessName,
    business_name_en: payload.businessNameEn ?? null,
    business_type: payload.businessType ?? 'hotel',
    city: payload.city ?? null,
  })
  saveAuth(data.access_token, data.role)
  return data
}

export default api