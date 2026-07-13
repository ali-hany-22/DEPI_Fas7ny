<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const API_BASE = 'http://localhost:8000'

/* ---------------- Booking summary (from query params, with fallbacks) ---------------- */
const booking = computed(() => ({
  hotel: route.query.hotel || 'سونستا سانت جورج الأقصر',
  city: route.query.city || 'الأقصر',
  room: route.query.room || 'غرفة ديلوكس مطلة على النيل',
  checkIn: route.query.checkIn || '١٥ أبريل ٢٠٢٤',
  checkOut: route.query.checkOut || '٢٢ أبريل ٢٠٢٤',
  adults: Number(route.query.adults) || 2,
  children: Number(route.query.children) || 0,
  nights: Number(route.query.nights) || 7,
  roomPrice: Number(route.query.total) || 5950,
  image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80',
  stars: 5,
  /* serviceId: لازم يوصلنا من صفحة الفندق عشان نعرف نربط الحجز
     بالخدمة الصح في الباك إند - من غيره مينفعش نبعت حجز حقيقي */
  serviceId: route.query.serviceId || null,
}))

const taxes = computed(() => Math.round(booking.value.roomPrice * 0.14))
const siteFeeOriginal = 120
const total = computed(() => booking.value.roomPrice + taxes.value)

/* ---------------- Steps ---------------- */
const steps = [
  { n: 1, label: 'مراجعة الطلب' },
  { n: 2, label: 'بيانات الدفع' },
  { n: 3, label: 'التأكيد' },
]
const currentStep = ref(2)

/* ---------------- Traveler info ---------------- */
const traveler = ref({
  fullName: '',
  nationality: 'مصر',
  passport: '',
  email: '',
  countryCode: '+20',
  phone: '',
  requests: '',
})

/* ---------------- Payment method ---------------- */
const paymentMethods = [
  { id: 'card', label: 'بطاقة ائتمان', icon: 'card' },
  { id: 'fawry', label: 'فوري', icon: 'fawry' },
  { id: 'wallet', label: 'محفظة إلكترونية', icon: 'wallet' },
  { id: 'transfer', label: 'تحويل بنكي', icon: 'transfer' },
]
const activeMethod = ref('card')

/* ---------------- Card form (live preview) ---------------- */
const card = ref({ number: '', expiry: '', cvv: '', holder: '' })

const formatCardNumber = (val) => {
  const digits = val.replace(/\D/g, '').slice(0, 16)
  return digits.replace(/(.{4})/g, '$1 ').trim()
}
const onCardNumberInput = (e) => { card.value.number = formatCardNumber(e.target.value) }

const formatExpiry = (val) => {
  const digits = val.replace(/\D/g, '').slice(0, 4)
  if (digits.length >= 3) return digits.slice(0, 2) + ' / ' + digits.slice(2)
  return digits
}
const onExpiryInput = (e) => { card.value.expiry = formatExpiry(e.target.value) }

const maskedCardNumber = computed(() => {
  const clean = card.value.number.replace(/\s/g, '')
  const padded = clean.padEnd(16, '•')
  return padded.match(/.{1,4}/g).join(' ')
})

/* ---------------- Terms + submit ---------------- */
const agreed = ref(false)
const submitting = ref(false)
const submitError = ref('')

const canSubmit = computed(() => agreed.value && traveler.value.fullName && traveler.value.email && traveler.value.phone)

/*
  بتبعت الحجز فعليًا للباك إند (POST /bookings) بدل الـ setTimeout
  الوهمي القديم. محتاجة توكن اليوزر (JWT) عشان الـ endpoint محمي
  بـ get_current_user - لو مفيش توكن، بنوجّه المستخدم يسجل دخول
  الأول بدل ما نبعت طلب هيفشل أكيد بـ 401.

  ملحوظة: لو serviceId مش موصلنا في الرابط (يعني صفحة الفندق لسه
  مبعتوش)، منقدرش نربط الحجز بخدمة حقيقية في الباك إند - في الحالة
  دي بنكمل بالسلوك القديم (تنقل بدون حفظ فعلي) عشان الصفحة تفضل
  شغالة، لكن الأفضل تتأكد إن صفحة الفندق بتبعت serviceId في الرابط.
*/

const submitBooking = async () => {
  console.log("submitBooking called")
  console.log("canSubmit =", canSubmit.value)
  console.log("submitting =", submitting.value)
  if (!canSubmit.value || submitting.value) return

const token =
  localStorage.getItem("fas7ny_access_token") ||
  localStorage.getItem("access_token") ||
  localStorage.getItem("token");
  console.log("access_token =", localStorage.getItem("access_token"))
  console.log("token =", localStorage.getItem("token"))
  console.log("all keys =", Object.keys(localStorage))
  if (!token) {
    submitError.value = 'لازم تسجل دخول الأول عشان تكمل الحجز.'
    return
  }

  if (!booking.value.serviceId) {
    console.warn('serviceId مفقود - الحجز لن يُحفظ فعليًا في الباك إند')
    submitError.value = 'تعذّر تحديد الخدمة المطلوبة. حاول الرجوع واختيار الفندق من جديد.'
    return
  }

  submitting.value = true
  submitError.value = ''

  try {
    const res = await fetch(`${API_BASE}/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        service_id: Number(booking.value.serviceId),
        guest_name: traveler.value.fullName,
        guest_phone: traveler.value.countryCode + traveler.value.phone,
        nights: booking.value.nights,
      }),
    })

    if (!res.ok) {
      if (res.status === 401) {
        submitError.value = 'انتهت صلاحية الجلسة. سجّل دخول تاني وحاول من جديد.'
      } else {
        submitError.value = 'حصل خطأ أثناء تأكيد الحجز. حاول مرة أخرى.'
      }
      submitting.value = false
      return
    }

    const data = await res.json()

    router.push({
      path: '/booked',
      query: {
        bookingReference: data.booking_reference,
        hotel: booking.value.hotel,
        city: booking.value.city,
        room: booking.value.room,
        checkIn: booking.value.checkIn,
        checkOut: booking.value.checkOut,
        adults: booking.value.adults,
        children: booking.value.children,
        total: total.value,
        travelerName: traveler.value.fullName,
        image: booking.value.image,
      },
    })
  } catch (err) {
    console.error('Booking submission failed:', err)
    submitError.value = 'تعذّر الاتصال بالخادم. تأكد من اتصالك بالإنترنت وحاول مرة أخرى.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">

    <!-- Top nav (simplified checkout bar) -->
    <div class="bg-[#F9F9F7] border-b border-[#D0C5B2] px-6 h-16 flex items-center justify-between">
      <span class="text-lg font-bold text-[#C9A84C] tracking-widest uppercase">فسحني</span>

      <div class="flex items-center gap-8">
        <div v-for="(s, i) in steps" :key="s.n" class="flex items-center gap-2" :class="s.n > currentStep ? 'opacity-50' : ''">
          <div v-if="i > 0" class="w-8 h-px bg-[#D0C5B2]"></div>
          <div class="flex items-center gap-2">
            <span :class="[s.label, currentStep === s.n ? 'font-bold text-[#755B00]' : 'text-[#7E7665]']" class="text-base"
              :style="{}">{{ s.label }}</span>
            <div :class="currentStep === s.n ? 'bg-[#C9A84C] text-white border-transparent' : 'border border-[#7E7665] text-[#7E7665]'"
              class="w-8 h-8 rounded-full flex items-center justify-center text-base font-bold">{{ ['١','٢','٣'][s.n-1] }}</div>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-1 text-[#416084] text-base">
        <span>دفع آمن</span>
        <svg class="w-4 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
      </div>
    </div>

    <!-- Header banner -->
    <div class="relative bg-[#F5ECD7] border-b border-[#D0C5B2] px-6 py-8 overflow-hidden">
      <div class="absolute bottom-0 left-0 right-0 h-1 bg-linear-to-r from-transparent via-[#C9A84C] to-transparent"></div>
      <div class="relative max-w-7xl mx-auto flex flex-col gap-2">
        <nav class="flex items-center justify-end gap-2 text-sm text-[#7E7665]">
          <button @click="router.push('/')" class="hover:text-[#1A1C1B]">الرئيسية</button>
          <span>‹</span>
          <button @click="router.back()" class="hover:text-[#1A1C1B]">{{ booking.city }}</button>
          <span>‹</span>
          <span class="text-[#C9A84C] font-medium">إتمام الحجز</span>
        </nav>
        <h1 class="text-2xl font-bold text-[#1A1C1B] text-right">إتمام الحجز</h1>
        <p class="text-base text-[#7E7665] text-right">يرجى مراجعة بيانات المسافرين واختيار وسيلة الدفع المناسبة</p>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-[443px_1fr] gap-8 items-start">

      <!-- Sticky summary -->
      <aside class="w-full lg:sticky lg:top-8 order-1">
        <div class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden flex flex-col">
          <div class="relative h-48">
            <img :src="booking.image" class="w-full h-full object-cover" :alt="booking.hotel" />
            <div class="absolute bottom-0 left-0 right-0 bg-linear-to-t from-black/80 to-transparent p-4 flex flex-col gap-1">
              <h3 class="text-white text-base text-right">{{ booking.hotel }}</h3>
              <div class="flex items-center justify-end gap-0.5">
                <svg v-for="n in booking.stars" :key="n" class="w-3 h-3 text-[#FFE08F]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              </div>
            </div>
          </div>

          <div class="p-8 flex flex-col gap-6">
            <!-- Details -->
            <div class="flex flex-col gap-4">
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base font-bold text-[#1A1C1B]">{{ booking.checkIn }} - {{ booking.checkOut }}</p>
                  <p class="text-sm font-medium text-[#7E7665]">{{ booking.nights }} ليالي • الأسبوع القادم</p>
                </div>
                <svg class="w-4.5 h-5 text-[#416084] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base font-bold text-[#1A1C1B]">{{ booking.adults }} بالغين<span v-if="booking.children"> ، {{ booking.children }} طفل</span></p>
                  <p class="text-sm font-medium text-[#7E7665]">{{ booking.room }}</p>
                </div>
                <svg class="w-5.5 h-4 text-[#416084] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m5-3.13a4 4 0 100-8 4 4 0 000 8z"/></svg>
              </div>
            </div>

            <div class="border-t border-[#D0C5B2]"></div>

            <!-- Pricing -->
            <div class="flex flex-col gap-2">
              <div class="flex items-center justify-between">
                <span class="text-base text-[#1A1C1B]">{{ booking.roomPrice.toLocaleString() }} ج.م</span>
                <span class="text-base text-[#7E7665]">سعر الغرفة</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-base text-[#1A1C1B]">{{ taxes.toLocaleString() }} ج.م</span>
                <span class="text-base text-[#7E7665]">الضرائب والرسوم</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="text-base font-bold text-[#AA3436]">مجاناً</span>
                  <span class="text-base text-[#AA3436]/50 line-through">{{ siteFeeOriginal }} ج.م</span>
                </div>
                <span class="text-base text-[#7E7665]">رسوم الموقع</span>
              </div>
            </div>

            <!-- Total -->
            <div class="border-t border-dashed border-[#D0C5B2] pt-4 flex items-center justify-between">
              <div class="text-right">
                <p class="text-3xl font-bold text-[#755B00]">{{ total.toLocaleString() }}</p>
                <p class="text-xs text-[#7E7665]">جنيه مصري (شامل الضريبة)</p>
              </div>
              <span class="text-base text-[#1A1C1B]">الإجمالي</span>
            </div>

            <!-- Cancellation -->
            <div class="bg-[#ECFDF5] border border-[#D1FAE5] rounded-xl p-4 flex items-start gap-4">
              <div class="flex-1 flex flex-col gap-1">
                <p class="text-sm font-bold text-[#065F46] text-right">إلغاء مجاني</p>
                <p class="text-sm font-medium text-[#065F46] text-right leading-5">يمكنك الإلغاء حتى يوم ١٣ أبريل واسترداد المبلغ بالكامل.</p>
              </div>
              <svg class="w-5 h-5 text-[#059669] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
          </div>
        </div>
      </aside>

      <!-- Forms -->
      <div class="flex flex-col gap-7 order-2">

        <!-- Traveler info -->
        <section class="bg-white border border-[#D0C5B2] rounded-xl p-8 flex flex-col gap-6">
          <div class="flex items-center justify-end gap-2">
            <h2 class="text-base text-[#1A1C1B]">بيانات المسافر الرئيسي</h2>
            <svg class="w-4 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-base text-[#7E7665] text-right">الاسم الكامل (كما في جواز السفر)</label>
              <input v-model="traveler.fullName" type="text" placeholder="مثال: محمد أحمد علي"
                class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-base text-[#7E7665] text-right">الجنسية</label>
              <select v-model="traveler.nationality" class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none">
                <option>مصر</option>
                <option>السعودية</option>
                <option>الإمارات</option>
                <option>أخرى</option>
              </select>
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-base text-[#7E7665] text-right">رقم جواز السفر</label>
              <input v-model="traveler.passport" type="text" placeholder="A12345678"
                class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-base text-[#7E7665] text-right">البريد الإلكتروني</label>
              <input v-model="traveler.email" type="email" placeholder="name@example.com"
                class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
            </div>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-base text-[#7E7665] text-right">رقم الهاتف (واتساب)</label>
            <div class="flex items-center gap-2">
              <div class="bg-[#F4F4F2] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base font-bold text-center">{{ traveler.countryCode }}</div>
              <input v-model="traveler.phone" type="tel" placeholder="10 1234 5678"
                class="flex-1 bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
            </div>
          </div>

          <div class="flex flex-col gap-1">
            <label class="text-base text-[#7E7665] text-right">طلبات خاصة (اختياري)</label>
            <textarea v-model="traveler.requests" rows="2" placeholder="مثل: غرفة في طابق مرتفع، سرير إضافي..."
              class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C] resize-none"></textarea>
          </div>
        </section>

        <!-- Payment method -->
        <section class="bg-white border border-[#D0C5B2] rounded-xl p-8 flex flex-col gap-6">
          <div class="flex items-center justify-end gap-2">
            <h2 class="text-base text-[#1A1C1B]">وسيلة الدفع</h2>
            <svg class="w-5.5 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2 10h20M6 14h4m-4 4h.01M2 6a2 2 0 012-2h16a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
          </div>

          <div class="flex items-center justify-end gap-2 border-b border-[#D0C5B2]">
            <button v-for="m in paymentMethods" :key="m.id" @click="activeMethod = m.id"
              :class="activeMethod === m.id ? 'text-[#755B00] font-bold border-[#C9A84C]' : 'text-[#7E7665] border-transparent'"
              class="px-8 py-4 border-b-2 text-base transition-colors">
              {{ m.label }}
            </button>
          </div>

          <!-- Card form -->
          <div v-if="activeMethod === 'card'" class="flex flex-col md:flex-row gap-6 items-start">
            <!-- 3D card preview -->
            <div class="w-full md:w-110 h-61 rounded-2xl p-8 flex flex-col justify-between shrink-0 relative overflow-hidden shadow-[0_20px_40px_rgba(0,0,0,0.2)]"
              style="background: linear-gradient(122deg, #416084 0%, #1A2A3A 100%);">
              <div class="flex items-center justify-between">
                <svg class="w-8 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01M5 12.859a10 10 0 0114 0M1.394 9.393a15 15 0 0121.212 0"/></svg>
                <span class="text-white text-base tracking-widest uppercase">فسحني</span>
              </div>
              <div class="flex flex-col gap-1 pt-6">
                <span class="text-white/60 text-xs uppercase">Card Number</span>
                <span class="text-white text-xl tracking-widest" dir="ltr">{{ maskedCardNumber }}</span>
              </div>
              <div class="flex items-end justify-between">
                <div class="flex flex-col gap-1">
                  <span class="text-white/60 text-xs uppercase">Expiry</span>
                  <span class="text-white text-base" dir="ltr">{{ card.expiry || 'MM/YY' }}</span>
                </div>
                <div class="flex flex-col gap-1 items-end">
                  <span class="text-white/60 text-xs uppercase">Holder Name</span>
                  <span class="text-white text-lg tracking-wide" dir="ltr">{{ card.holder || 'YOUR NAME' }}</span>
                </div>
              </div>
              <svg class="absolute -bottom-10 -left-10 w-42 h-42 text-white opacity-10" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
            </div>

            <!-- Card fields -->
            <div class="flex-1 w-full flex flex-col gap-6">
              <div class="flex flex-col gap-1">
                <label class="text-base text-[#7E7665] text-right">رقم البطاقة</label>
                <div class="relative">
                  <input :value="card.number" @input="onCardNumberInput" type="text" maxlength="19" placeholder="**** **** **** ****" dir="ltr"
                    class="w-full bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3.5 pl-12 text-base focus:outline-none focus:border-[#C9A84C]" />
                  <svg class="w-5 h-4 text-[#7E7665] absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2 10h20M6 14h4m-4 4h.01M2 6a2 2 0 012-2h16a2 2 0 012 2v12a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/></svg>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="flex flex-col gap-1">
                  <label class="text-base text-[#7E7665] text-right">تاريخ الانتهاء</label>
                  <input :value="card.expiry" @input="onExpiryInput" type="text" maxlength="7" placeholder="MM / YY" dir="ltr"
                    class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-center focus:outline-none focus:border-[#C9A84C]" />
                </div>
                <div class="flex flex-col gap-1">
                  <label class="text-base text-[#7E7665] text-right">رمز CVV</label>
                  <input v-model="card.cvv" type="text" maxlength="3" placeholder="***" dir="ltr"
                    class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-center focus:outline-none focus:border-[#C9A84C]" />
                </div>
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-base text-[#7E7665] text-right">الاسم على البطاقة</label>
                <input v-model="card.holder" type="text" placeholder="اسم حامل البطاقة"
                  class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
              </div>
            </div>
          </div>

          <!-- Other payment methods placeholder -->
          <div v-else class="py-10 text-center text-[#7E7665] text-base">
            سيتم تحويلك لإتمام الدفع عبر {{ paymentMethods.find(m => m.id === activeMethod)?.label }} بعد تأكيد الحجز.
          </div>
        </section>

        <!-- Terms -->
        <div class="bg-[#E8E8E6]/50 rounded-xl p-4 flex items-start gap-4">
          <label class="flex items-start gap-4 cursor-pointer flex-1">
            <p class="flex-1 text-base text-[#1A1C1B] text-right leading-6.5">
              أوافق على <button type="button" class="text-[#C9A84C] underline">شروط وأحكام</button> الرحلة وسياسة الخصوصية. أقر بأن جميع البيانات المدخلة صحيحة وتطابق وثائق السفر.
            </p>
            <input v-model="agreed" type="checkbox" class="w-4 h-4 rounded border-[#6B7280] accent-[#755B00] mt-1 shrink-0" />
          </label>
        </div>

        <!-- Error message -->
        <div v-if="submitError" class="bg-[#FFDAD7] border border-[#AA3436]/30 rounded-xl p-4 text-center text-sm text-[#7F131B]">
          {{ submitError }}
        </div>

        <!-- Submit -->
        <button @click="submitBooking" :disabled="!canSubmit || submitting"
          class="w-full py-6 rounded-xl flex items-center justify-center gap-4 text-white font-bold text-lg shadow-[0_20px_25px_-5px_rgba(0,0,0,0.1),0_8px_10px_-6px_rgba(0,0,0,0.1)] transition-opacity disabled:opacity-50"
          style="background: linear-gradient(94.49deg, #C9A84C 0%, #A68936 100%);">
          <svg v-if="!submitting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          <span>{{ submitting ? 'جاري التأكيد...' : `أكمل الحجز وادفع ${total.toLocaleString()} جنيه` }}</span>
        </button>

        <div class="flex items-center justify-center gap-8 opacity-60 text-xs text-[#7E7665]">
          <div class="flex items-center gap-1">
            <span>دعم ٢٤/٧</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M5.636 5.636l3.536 3.536m0 5.656l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div class="flex items-center gap-1">
            <span>حماية بيانات مشفرة</span>
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>