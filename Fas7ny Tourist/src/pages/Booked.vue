<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

/* ---------------- Booking data (from Payment.vue query params) ---------------- */
const booking = computed(() => ({
  hotel: route.query.hotel || 'سونستا سانت جورج الأقصر',
  city: route.query.city || 'الأقصر',
  room: route.query.room || 'غرفة ملكية مطلة على النيل',
  checkIn: route.query.checkIn || '15 أغسطس',
  checkOut: route.query.checkOut || '20 أغسطس 2025',
  adults: Number(route.query.adults) || 2,
  children: Number(route.query.children) || 0,
  total: Number(route.query.total) || 6783,
  travelerName: route.query.travelerName || 'أحمد',
  image: route.query.image || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80',
}))

const firstName = computed(() => booking.value.travelerName.split(' ')[0] || 'أحمد')

/* ---------------- Booking reference ---------------- */
const bookingRef = ref('FS-' + Math.random().toString(36).slice(2, 8).toUpperCase())

/* ---------------- Toast ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* ---------------- Actions ---------------- */
const addToCalendar = (provider) => showToast(`جاري إضافة الرحلة لتقويم ${provider}...`)
const shareVia = (channel) => showToast(`جاري المشاركة عبر ${channel}...`)
const goToAiPlanner = () => router.push({ path: '/ai-trip-planner', query: { city: booking.value.city } })
const downloadInvoice = () => showToast('جاري تحميل الفاتورة...')
const goHome = () => router.push('/')
const contactSupport = () => router.push('/help')
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">

    <!-- Toast -->
    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <!-- Simplified header -->
    <header class="h-16 bg-[#FAFAF8] border-b border-[#E8E4DC] flex items-center px-8">
      <span class="text-xl font-bold text-[#C9A84C] tracking-widest uppercase">فسحني</span>
    </header>

    <main class="flex flex-col items-center pb-8">

      <!-- Success illustration & headline -->
      <section class="flex flex-col items-center gap-1 max-w-3xl px-4 pt-16 pb-8">
        <div class="relative w-24 h-24">
          <div class="w-24 h-24 rounded-full bg-white border-4 border-[#C9A84C] shadow-sm flex items-center justify-center">
            <svg class="w-10 h-10 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
          </div>
          <svg class="absolute -top-4 -right-4 w-6 h-6 text-[#C9A84C] opacity-40" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z"/></svg>
          <svg class="absolute -bottom-2 -left-6 w-7 h-7 text-[#C9A84C] opacity-40" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z"/></svg>
        </div>

        <h1 class="text-4xl font-bold text-[#1A1C1B] text-center pt-5">تم الحجز بنجاح!</h1>
        <p class="text-lg text-[#7E7665] text-center pb-5">يلا نتمنالك رحلة مميزة يا {{ firstName }}</p>

        <div class="bg-[#C9A84C]/5 border-2 border-dashed border-[#C9A84C] rounded-xl px-6 py-4 flex flex-col items-center gap-1">
          <span class="text-sm font-medium tracking-wide text-[#755B00]">رقم المرجع</span>
          <span class="text-2xl font-semibold tracking-widest text-[#755B00]">{{ bookingRef }}</span>
          <span class="text-sm font-medium text-[#7E7665] pt-1 text-center">تم إرسال تفاصيل التأكيد إلى بريدك الإلكتروني</span>
        </div>
      </section>

      <!-- Booking details card -->
      <section class="w-full max-w-6xl px-4">
        <div class="bg-white border border-[#D0C5B2] shadow-sm rounded-xl overflow-hidden">
          <div class="relative h-58">
            <img :src="booking.image" class="w-full h-full object-cover" :alt="booking.hotel" />
            <span class="absolute top-4 right-4 flex items-center gap-1.5 bg-[#755B00] text-white text-base px-3 py-1.5 rounded-full shadow-md">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
              توصية الذكاء الاصطناعي
            </span>
          </div>

          <div class="p-6 flex flex-col gap-6">
            <h3 class="text-2xl font-semibold text-[#1A1C1B] text-right">{{ booking.hotel }}</h3>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-6 border-t border-[#D0C5B2]/30 pt-6">
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base text-[#7E7665]">التاريخ</p>
                  <p class="text-base font-bold text-[#1A1C1B]">{{ booking.checkIn }} - {{ booking.checkOut }}</p>
                </div>
                <svg class="w-4.5 h-5 text-[#755B00] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base text-[#7E7665]">نوع الغرفة</p>
                  <p class="text-base font-bold text-[#1A1C1B]">{{ booking.room }}</p>
                </div>
                <svg class="w-5 h-3.5 text-[#755B00] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7h18M3 12h18M3 17h18"/></svg>
              </div>
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base text-[#7E7665]">الضيوف</p>
                  <p class="text-base font-bold text-[#1A1C1B]">{{ booking.adults }} بالغين<span v-if="booking.children"> ، {{ booking.children }} طفل</span></p>
                </div>
                <svg class="w-5.5 h-4 text-[#755B00] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m5-3.13a4 4 0 100-8 4 4 0 000 8z"/></svg>
              </div>
              <div class="flex items-center justify-end gap-4">
                <div class="text-right">
                  <p class="text-base text-[#7E7665]">الإجمالي المدفوع</p>
                  <p class="text-2xl font-semibold text-[#755B00]">{{ booking.total.toLocaleString() }} ج.م</p>
                </div>
                <svg class="w-5.5 h-4 text-[#755B00] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V6m0 8v2m9-4a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- What's next -->
      <section class="w-full max-w-6xl px-4 pt-16 flex flex-col gap-8">
        <h2 class="text-3xl font-semibold text-[#1A1C1B] text-center">ماذا بعد؟</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Share -->
          <div class="bg-[#EEEEEC] border border-[#D0C5B2] rounded-xl p-6 flex flex-col items-center gap-2 text-center">
            <div class="w-14 h-14 rounded-full bg-white shadow-sm flex items-center justify-center">
              <svg class="w-6 h-6 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342a4 4 0 100-2.684M8.684 13.342a4 4 0 004.632 4.632m-4.632-4.632l6.632 3.316m0-8.316a4 4 0 10-4.632-4.632m4.632 4.632L8.684 10.658m8.316-4.632a4 4 0 100 2.684"/></svg>
            </div>
            <h4 class="text-xl text-[#1A1C1B] pt-2">شارك رحلتك</h4>
            <p class="text-base text-[#7E7665]">شارك تفاصيل الفندق مع أصدقائك أو عائلتك</p>
            <div class="flex items-center justify-center gap-6 pt-4">
              <button @click="shareVia('واتساب')" class="text-[#755B00] hover:opacity-70">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/></svg>
              </button>
              <button @click="shareVia('البريد الإلكتروني')" class="text-[#755B00] hover:opacity-70">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              </button>
              <button @click="shareVia('نسخ الرابط')" class="text-[#755B00] hover:opacity-70">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 010 5.656l-3 3a4 4 0 01-5.656-5.656l1.5-1.5m5.656-5.656l1.5-1.5a4 4 0 115.656 5.656l-3 3a4 4 0 01-5.656 0"/></svg>
              </button>
            </div>
          </div>

          <!-- AI planning (highlighted) -->
          <div class="relative bg-[#755B00] rounded-xl p-6 flex flex-col items-center gap-2 text-center shadow-[0_10px_15px_-3px_rgba(0,0,0,0.1),0_4px_6px_-4px_rgba(0,0,0,0.1)] overflow-hidden">
            <svg class="absolute top-0 right-0 w-22 h-22 text-white opacity-10 p-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            <div class="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </div>
            <h4 class="text-xl text-white pt-2">خطط رحلتك بذكاء</h4>
            <p class="text-base text-white/80 pb-2">دع مساعدنا الذكي يقترح لك مطاعم وأنشطة في {{ booking.city }}</p>
            <button @click="goToAiPlanner" class="w-full bg-[#C9A84C] hover:bg-[#b8963f] text-[#503D00] font-bold py-3 rounded-lg transition-colors">
              ابدأ التخطيط بالذكاء الاصطناعي
            </button>
          </div>

          <!-- Add to calendar -->
          <div class="bg-[#EEEEEC] border border-[#D0C5B2] rounded-xl p-6 flex flex-col items-center gap-2 text-center">
            <div class="w-14 h-14 rounded-full bg-white shadow-sm flex items-center justify-center">
              <svg class="w-6 h-6 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            </div>
            <h4 class="text-xl text-[#1A1C1B] pt-2">أضف للتقويم</h4>
            <p class="text-base text-[#7E7665]">نظم وقتك وفعل التنبيهات لرحلتك</p>
            <div class="flex items-center justify-center gap-2 pt-4">
              <button @click="addToCalendar('Apple')" class="bg-white border border-[#D0C5B2] rounded-lg px-4 py-2.5 text-base text-[#1A1C1B] hover:bg-[#F4F4F2] transition-colors">Apple</button>
              <button @click="addToCalendar('Google')" class="bg-white border border-[#D0C5B2] rounded-lg px-4 py-2.5 text-base text-[#1A1C1B] hover:bg-[#F4F4F2] transition-colors">Google</button>
            </div>
          </div>
        </div>
      </section>

      <!-- Bottom CTA -->
      <section class="flex flex-col items-center gap-4 pt-16">
        <div class="flex items-center gap-4">
          <button @click="downloadInvoice"
            class="flex items-center gap-4 border-2 border-[#C9A84C] text-[#C9A84C] font-medium px-8 py-4 rounded-xl hover:bg-[#C9A84C]/5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H8a2 2 0 01-2-2V5a2 2 0 012-2h6l6 6v9a2 2 0 01-2 2z"/></svg>
            تحميل الفاتورة
          </button>
          <button @click="goHome"
            class="flex items-center gap-4 border-2 border-[#C9A84C] text-[#C9A84C] font-medium px-8 py-4 rounded-xl hover:bg-[#C9A84C]/5 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            العودة للصفحة الرئيسية
          </button>
        </div>
        <button @click="contactSupport" class="text-base text-[#7E7665] underline">هل تحتاج لمساعدة؟ تواصل مع الدعم</button>
      </section>
    </main>

    <!-- Footer -->
    <footer class="bg-[#F5F5F4] border-t border-[#E8E4DC] py-12 px-8">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <nav class="flex items-center gap-8">
          <a href="#" class="text-base text-[#78716C] hover:text-[#1A1C1B]">Legal</a>
          <a href="#" class="text-base text-[#78716C] hover:text-[#1A1C1B]">Safety</a>
          <a href="#" class="text-base text-[#78716C] hover:text-[#1A1C1B]">Support</a>
        </nav>
        <div class="text-right">
          <p class="text-xl font-bold text-[#C9A84C]">فسحني</p>
          <p class="text-sm text-[#57534E]">© 2024 فسحني للسياحة. البساطة المصرية العصرية.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>