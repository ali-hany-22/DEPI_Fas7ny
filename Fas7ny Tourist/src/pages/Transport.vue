<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

/* ---------------- Toast feedback ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* ---------------- Hero stats ---------------- */
const heroStats = [
  { label: '120 مركب نيلية', icon: 'boat', sectionId: 'section-cruises' },
  { label: '800+ وكالة تأجير', icon: 'car', sectionId: 'section-cars' },
  { label: '5000+ كم سكك حديدية', icon: 'train', sectionId: 'section-trains' },
  { label: '22 مطار دولي', icon: 'plane', sectionId: 'section-flights' },
]

/* ---------------- Sticky tabs (scroll-to) ---------------- */
const tabs = [
  { id: 'flights', label: 'الطيران الداخلي', icon: 'plane' },
  { id: 'trains', label: 'القطارات', icon: 'train' },
  { id: 'cars', label: 'سيارات الإيجار', icon: 'car' },
  { id: 'buses', label: 'الباصات', icon: 'bus' },
  { id: 'cruises', label: 'الرحلات النيلية', icon: 'boat' },
]
const activeTab = ref('flights')
const selectTab = (id) => {
  activeTab.value = id
  const el = document.getElementById(`section-${id}`)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

/* ---------------- Flight search ---------------- */
const cityOptions = ['القاهرة (CAI)', 'الأقصر (LXR)', 'أسوان (ASW)', 'الغردقة (HRG)', 'شرم الشيخ (SSH)', 'الإسكندرية (HBE)']
const fromCity = ref('القاهرة (CAI)')
const toCity = ref('الأقصر (LXR)')
const travelDateInput = ref('2024-10-24')
const travelDateLabel = ref('24 أكتوبر 2024')
const travelers = ref(1)
const flightClass = ref('اقتصادي')
const classOptions = ['اقتصادي', 'رجال أعمال', 'الدرجة الأولى']

const onDateChange = () => {
  const d = new Date(travelDateInput.value)
  if (!isNaN(d)) travelDateLabel.value = d.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' })
}

const isSearching = ref(false)
const searchFlights = async () => {
  if (fromCity.value === toCity.value) {
    showToast('اختر مدينتي وصول ومغادرة مختلفتين')
    return
  }
  isSearching.value = true
  // TODO: replace with real API call, e.g. await api.get('/flights', { params: { from: fromCity.value, to: toCity.value, date: travelDateInput.value, travelers: travelers.value, class: flightClass.value } })
  await new Promise((r) => setTimeout(r, 700))
  isSearching.value = false
  showToast('تم تحديث نتائج الرحلات')
}

/* ---------------- Flight results ---------------- */
const flights = ref([
  {
    id: 1, airline: 'مصر للطيران', airlineLogo: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=100&q=80',
    from: 'LXR', to: 'CAI', departTime: '08:00', arriveTime: '09:15', duration: 'ساعة و15 دقيقة', direct: true, price: 2450,
  },
  {
    id: 2, airline: 'العربية للطيران', airlineLogo: 'https://images.unsplash.com/photo-1583468982228-19f19164aee2?w=100&q=80',
    from: 'LXR', to: 'CAI', departTime: '14:30', arriveTime: '15:45', duration: 'ساعة و15 دقيقة', direct: true, price: 1980,
  },
])
const bookFlight = (flight) => {
  showToast(`جاري حجز رحلة ${flight.airline}...`)
  router.push('/payment')
}

/* ---------------- Car rentals ---------------- */
const carTypeFilter = ref('all')
const carSort = ref('price-asc')
const carTypeOptions = [
  { id: 'all', label: 'كل الأنواع' },
  { id: 'economy', label: 'اقتصادية' },
  { id: 'family', label: 'عائلية' },
  { id: 'luxury', label: 'فاخرة' },
]

const cars = ref([
  {
    id: 1, name: 'مرسيدس E-Class', type: 'luxury', badge: 'فاخرة', badgeColor: 'bg-[#FF8985] text-[#7F131B]',
    specs: 'رجال أعمال • سائق خاص', features: ['واي فاي مجاني', 'تأمين شامل'], pricePerDay: 5000,
    image: 'https://images.unsplash.com/photo-1563720223185-11003d516935?w=600&q=80',
  },
  {
    id: 2, name: 'كيا سبورتاج 2024', type: 'family', badge: 'الأكثر طلباً', badgeColor: 'bg-[#B4D4FE] text-[#3C5C7F]',
    specs: 'دفع رباعي • 7 مقاعد', features: ['تكييف ممتاز', 'مساحة واسعة'], pricePerDay: 2500,
    image: 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600&q=80',
  },
  {
    id: 3, name: 'تويوتا كورولا 2024', type: 'economy', badge: 'جديد', badgeColor: 'bg-[#C9A84C] text-[#503D00]',
    specs: 'أتوماتيك • 5 مقاعد', features: ['تكييف ممتاز'], pricePerDay: 1200,
    image: 'https://images.unsplash.com/photo-1494905998402-395d579af36f?w=600&q=80',
  },
])

const filteredCars = computed(() => {
  let list = cars.value.filter((c) => carTypeFilter.value === 'all' || c.type === carTypeFilter.value)
  list = [...list].sort((a, b) => carSort.value === 'price-asc' ? a.pricePerDay - b.pricePerDay : b.pricePerDay - a.pricePerDay)
  return list
})

const chooseCar = (car) => {
  showToast(`جاري حجز ${car.name}...`)
  router.push('/payment')
}

/* ---------------- Nile cruises ---------------- */
const cruises = ref([
  {
    id: 1, title: 'رحلة الأقصر وأسوان', badge: '4 أيام',
    desc: 'اكتشف كنوز النيل في رحلة ساحرة عبر التاريخ على متن مركب تقليدي فاخر.',
    tags: ['عروض فنية', 'مرشد سياحي', 'إفطار شامل'],
    price: 8500, priceUnit: '/ للفرد', buttonLabel: 'تفاصيل الرحلة',
    image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&q=80',
  },
  {
    id: 2, title: 'جولة الفلوكة المسائية', badge: 'ساعتين',
    desc: 'استمتع بغروب الشمس الساحر في قلب القاهرة على متن الفلوكة التقليدية.',
    tags: ['موسيقى هادئة', 'مشروبات باردة'],
    price: 450, priceUnit: '/ للمجموعة', buttonLabel: 'احجز الآن',
    image: 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=600&q=80',
  },
])
const cruiseAction = (cruise) => {
  showToast(`جاري تجهيز حجز "${cruise.title}"...`)
  router.push('/payment')
}

/* ---------------- Live transport map FAB ---------------- */
const openLiveMap = () => {
  showToast('سيتم فتح خريطة المواصلات الحية قريباً')
  // TODO: router.push('/map')
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7] pb-16">
    <Navbar />

    <!-- Toast -->
    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <!-- Hero -->
    <div class="pt-16">
      <div class="bg-[#1A3C5E] pt-12 pb-20 px-10">
        <div class="max-w-360 mx-auto flex flex-col gap-6">
          <div class="flex items-center gap-2 justify-end text-sm">
            <span class="text-white">المواصلات</span>
            <svg class="w-2 h-1.5 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            <button @click="router.push('/')" class="text-white/70 hover:text-white">الرئيسية</button>
          </div>
          <h1 class="text-2xl text-white text-right">تنقّل في مصر بسهولة</h1>
          <div class="flex items-center gap-4 justify-end flex-wrap">
            <button v-for="s in heroStats" :key="s.label" @click="selectTab(s.sectionId.replace('section-',''))"
              class="flex items-center gap-3 bg-white/10 border border-white/20 backdrop-blur-sm px-6 py-3 rounded-full text-white hover:bg-white/20 transition-colors">
              <svg v-if="s.icon === 'boat'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 18l1.5-6h15L21 18M3 18a2 2 0 002 2h14a2 2 0 002-2M8 12V6a1 1 0 011-1h6a1 1 0 011 1v6"/></svg>
              <svg v-else-if="s.icon === 'car'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 17h14M5 17a2 2 0 01-2-2v-2.5a1 1 0 01.257-.67L5.5 9.25A2 2 0 017 8.5h10a2 2 0 011.5.75l2.243 2.58a1 1 0 01.257.67V15a2 2 0 01-2 2M5 17a2 2 0 002 2h1a2 2 0 002-2m8 0a2 2 0 002 2h1a2 2 0 002-2M8 13h8"/></svg>
              <svg v-else-if="s.icon === 'train'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7h8m-8 4h8m-6 8l-2 2m8-2l2 2M6 17h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v9a2 2 0 002 2z"/></svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
              <span class="text-base">{{ s.label }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Sticky tabs -->
      <div class="sticky top-16 z-30 -mt-8 px-10">
        <div class="max-w-360 mx-auto bg-white/90 backdrop-blur-md border border-[#D0C5B2] shadow-sm rounded-2xl p-2 flex items-center justify-end gap-2 overflow-x-auto">
          <button v-for="tab in tabs" :key="tab.id" @click="selectTab(tab.id)"
            :class="activeTab === tab.id ? 'bg-[#C9A84C] text-[#503D00] font-bold shadow-sm' : 'text-[#4D4637] hover:bg-[#F4F4F2]'"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-base whitespace-nowrap transition-colors">
            {{ tab.label }}
            <svg v-if="tab.icon === 'plane'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
            <svg v-else-if="tab.icon === 'train'" class="w-4 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7h8m-8 4h8m-6 8l-2 2m8-2l2 2M6 17h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v9a2 2 0 002 2z"/></svg>
            <svg v-else-if="tab.icon === 'car'" class="w-4.5 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 17h14M5 17a2 2 0 01-2-2v-2.5a1 1 0 01.257-.67L5.5 9.25A2 2 0 017 8.5h10a2 2 0 011.5.75l2.243 2.58a1 1 0 01.257.67V15a2 2 0 01-2 2M5 17a2 2 0 002 2h1a2 2 0 002-2m8 0a2 2 0 002 2h1a2 2 0 002-2M8 13h8"/></svg>
            <svg v-else-if="tab.icon === 'bus'" class="w-4.5 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 17H5a2 2 0 01-2-2V9a2 2 0 012-2h11l4 4v4a2 2 0 01-2 2h-3m-6 0a2 2 0 100 4 2 2 0 000-4zm8 0a2 2 0 100 4 2 2 0 000-4z"/></svg>
            <svg v-else class="w-5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 18l1.5-6h15L21 18M3 18a2 2 0 002 2h14a2 2 0 002-2M8 12V6a1 1 0 011-1h6a1 1 0 011 1v6"/></svg>
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-360 mx-auto px-10 pt-8 flex flex-col gap-12">

      <!-- Flight search card -->
      <div id="section-flights" class="bg-white border border-[#D0C5B2] shadow-sm rounded-3xl p-8 flex flex-col gap-6 scroll-mt-32">
        <div class="grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
          <div class="flex flex-col gap-2">
            <label class="text-base text-[#4D4637] text-right">من</label>
            <select v-model="fromCity" class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3.5 text-base text-right focus:outline-none focus:border-[#C9A84C]">
              <option v-for="c in cityOptions" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-base text-[#4D4637] text-right">إلى</label>
            <select v-model="toCity" class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3.5 text-base text-right focus:outline-none focus:border-[#C9A84C]">
              <option v-for="c in cityOptions" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-base text-[#4D4637] text-right">التاريخ</label>
            <input v-model="travelDateInput" @change="onDateChange" type="date"
              class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
          </div>
          <div class="flex flex-col gap-2">
            <label class="text-base text-[#4D4637] text-right">المسافرون</label>
            <select v-model="travelers" class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl px-4 py-3.5 text-base text-right focus:outline-none focus:border-[#C9A84C]">
              <option v-for="n in 9" :key="n" :value="n">{{ n }} {{ n === 1 ? 'بالغ' : 'بالغين' }}</option>
            </select>
          </div>
          <button @click="searchFlights" :disabled="isSearching"
            class="bg-[#C9A84C] hover:bg-[#b8963f] disabled:opacity-70 text-[#503D00] font-bold py-3.5 rounded-xl flex items-center justify-center gap-2 transition-colors">
            <svg v-if="isSearching" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>
            <span v-else>بحث الرحلات</span>
          </button>
        </div>
        <div class="flex items-center gap-2 justify-end">
          <span class="text-sm text-[#4D4637]">الدرجة:</span>
          <button v-for="c in classOptions" :key="c" @click="flightClass = c"
            :class="flightClass === c ? 'bg-[#C9A84C]/10 border-[#C9A84C] text-[#755B00]' : 'border-[#D0C5B2] text-[#4D4637]'"
            class="border px-4 py-1.5 rounded-full text-sm transition-colors">{{ c }}</button>
        </div>
      </div>

      <!-- Flight results + promo -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 -mt-4">
        <div class="lg:col-span-2 bg-white border border-[#D0C5B2] rounded-3xl p-6 flex flex-col gap-4">
          <div class="text-right">
            <h3 class="text-lg text-[#1A1C1B]">الرحلات المتاحة اليوم</h3>
            <p class="text-sm text-[#7E7665]">اختر من بين أفضل الرحلات الجوية المباشرة</p>
          </div>
          <div class="flex flex-col gap-4">
            <div v-for="f in flights" :key="f.id" class="flex items-center justify-between gap-4 flex-wrap">
              <button @click="bookFlight(f)" class="bg-[#755B00] hover:bg-[#634c00] text-white font-bold px-6 py-2.5 rounded-xl transition-colors shrink-0">حجز</button>
              <div class="flex-1 min-w-50 flex flex-col items-center gap-1">
                <div class="flex items-center gap-4 w-full">
                  <span class="text-xs font-semibold text-[#1A1C1B]">{{ f.from }}</span>
                  <div class="flex-1 h-px bg-[#D0C5B2] relative">
                    <svg class="w-3 h-3 text-[#755B00] absolute right-1/2 translate-x-1/2 -top-1.5 bg-[#F9F9F7]" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
                  </div>
                  <span class="text-xs font-semibold text-[#1A1C1B]">{{ f.to }}</span>
                </div>
              </div>
              <div class="flex items-center gap-6 shrink-0">
                <div class="text-left">
                  <p class="font-bold text-[#1A1C1B]">{{ f.departTime }} - {{ f.arriveTime }}</p>
                  <p class="text-sm text-[#4D4637]">{{ f.direct ? 'مباشر' : 'توقف' }} ({{ f.duration }})</p>
                </div>
                <div class="w-14 h-14 rounded-xl border border-[#D0C5B2] bg-white overflow-hidden shrink-0">
                  <img :src="f.airlineLogo" class="w-full h-full object-cover" :alt="f.airline" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="relative bg-[#E8E8E6] rounded-3xl p-8 flex flex-col justify-between overflow-hidden">
          <div class="absolute -bottom-10 -left-10 w-44 h-44 opacity-5">
            <svg class="w-full h-full" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
          </div>
          <div class="relative w-12 h-12 bg-white rounded-xl shadow-sm flex items-center justify-center">
            <svg class="w-5 h-5 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
          </div>
          <div class="relative text-right mt-4">
            <h4 class="text-lg text-[#1A1C1B]">مصر للطيران</h4>
            <p class="text-base text-[#4D4637] mt-2">الناقل الوطني المصري، تغطية شاملة لجميع محافظات مصر مع أرقى الخدمات.</p>
            <button @click="showToast('سيتم عرض جميع عروض مصر للطيران قريباً')" class="flex items-center gap-2 text-[#755B00] font-bold mt-6">
              عرض العروض
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Trains placeholder -->
      <section id="section-trains" class="scroll-mt-32 bg-white border border-dashed border-[#D0C5B2] rounded-3xl p-10 text-center text-[#7E7665]">
        <p class="text-lg">بحث القطارات قيد التطوير — سيتاح قريباً 🚆</p>
      </section>

      <!-- Car rentals -->
      <section id="section-cars" class="scroll-mt-32 flex flex-col gap-6">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div class="flex items-center gap-2">
            <select v-model="carSort" class="bg-[#E8E8E6] border border-[#D0C5B2] rounded-full px-5 py-2.5 text-base text-[#1A1C1B] focus:outline-none">
              <option value="price-asc">السعر: تصاعدي</option>
              <option value="price-desc">السعر: تنازلي</option>
            </select>
            <select v-model="carTypeFilter" class="bg-[#E8E8E6] border border-[#D0C5B2] rounded-full px-5 py-2.5 text-base text-[#1A1C1B] focus:outline-none">
              <option v-for="t in carTypeOptions" :key="t.id" :value="t.id">النوع: {{ t.label }}</option>
            </select>
          </div>
          <div class="text-right">
            <h2 class="text-lg text-[#1A1C1B]">تأجير السيارات الفاخرة</h2>
            <p class="text-base text-[#4D4637]">انطلق في رحلتك الخاصة بسيارات حديثة ومؤمنة</p>
          </div>
        </div>

        <p v-if="filteredCars.length === 0" class="text-sm text-[#7E7665] text-center py-10">لا توجد سيارات مطابقة لهذا الفلتر.</p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="car in filteredCars" :key="car.id" class="bg-white border border-[#D0C5B2] rounded-3xl overflow-hidden">
            <div class="relative h-56 bg-[#EEEEEC]">
              <img :src="car.image" class="w-full h-full object-cover" :alt="car.name" />
              <span :class="car.badgeColor" class="absolute top-4 right-4 text-xs font-semibold px-3 py-1 rounded-full">{{ car.badge }}</span>
            </div>
            <div class="p-6 flex flex-col gap-4">
              <div class="flex items-start justify-between gap-3">
                <div class="w-9 h-9 rounded-lg bg-[#F4F4F2] flex items-center justify-center shrink-0">
                  <svg class="w-5 h-5 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 17h14M5 17a2 2 0 01-2-2v-2.5a1 1 0 01.257-.67L5.5 9.25A2 2 0 017 8.5h10a2 2 0 011.5.75l2.243 2.58a1 1 0 01.257.67V15a2 2 0 01-2 2M5 17a2 2 0 002 2h1a2 2 0 002-2m8 0a2 2 0 002 2h1a2 2 0 002-2M8 13h8"/></svg>
                </div>
                <div class="text-right flex-1">
                  <h4 class="font-normal text-[#1A1C1B] text-base">{{ car.name }}</h4>
                  <p class="text-sm text-[#4D4637]">{{ car.specs }}</p>
                </div>
              </div>
              <div class="flex items-center gap-4 justify-end flex-wrap text-sm text-[#4D4637]">
                <span v-for="f in car.features" :key="f" class="flex items-center gap-1">
                  {{ f }}
                  <svg class="w-3 h-3 text-[#4D4637]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </span>
              </div>
              <div class="flex items-center justify-between border-t border-[#D0C5B2] pt-4">
                <button @click="chooseCar(car)" class="bg-[#416084] hover:bg-[#374f6c] text-white font-normal px-5 py-2.5 rounded-xl transition-colors">اختر السيارة</button>
                <p class="text-right">
                  <span class="text-2xl font-bold text-[#755B00]">{{ car.pricePerDay.toLocaleString() }}</span>
                  <span class="text-sm text-[#4D4637]"> ج.م / يوم</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Buses placeholder -->
      <section id="section-buses" class="scroll-mt-32 bg-white border border-dashed border-[#D0C5B2] rounded-3xl p-10 text-center text-[#7E7665]">
        <p class="text-lg">حجوزات الباصات قيد التطوير — سيتاح قريباً 🚌</p>
      </section>

      <!-- Nile cruises -->
      <section id="section-cruises" class="scroll-mt-32 flex flex-col gap-6">
        <h2 class="text-lg text-[#1A1C1B] text-right">الرحلات النيلية الملكية</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="cr in cruises" :key="cr.id" class="bg-white border border-[#D0C5B2] rounded-3xl flex overflow-hidden">
            <div class="flex-1 p-8 flex flex-col justify-between gap-4">
              <div class="flex flex-col gap-2">
                <div class="flex items-center justify-between">
                  <span class="bg-[#C9A84C]/20 text-[#755B00] text-xs font-semibold px-3 py-1 rounded-full">{{ cr.badge }}</span>
                  <h4 class="font-normal text-[#1A1C1B] text-base">{{ cr.title }}</h4>
                </div>
                <p class="text-base text-[#4D4637]">{{ cr.desc }}</p>
                <div class="flex items-center gap-2 justify-end flex-wrap">
                  <span v-for="tag in cr.tags" :key="tag" class="bg-[#EEEEEC] text-[#1A1C1B] text-xs px-2 py-1 rounded-md">{{ tag }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between border-t border-[#D0C5B2] pt-4">
                <button @click="cruiseAction(cr)" class="bg-[#755B00] hover:bg-[#634c00] text-white font-bold px-6 py-2.5 rounded-xl transition-colors">{{ cr.buttonLabel }}</button>
                <p class="text-right">
                  <span class="text-xl font-bold text-[#755B00]">{{ cr.price.toLocaleString() }} ج.م</span>
                  <span class="text-xs text-[#4D4637] block">{{ cr.priceUnit }}</span>
                </p>
              </div>
            </div>
            <div class="w-64 shrink-0 hidden sm:block">
              <img :src="cr.image" class="w-full h-full object-cover" :alt="cr.title" />
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Floating live map button -->
    <button @click="openLiveMap"
      class="fixed bottom-12 left-8 flex items-center gap-3 bg-[#1A3C5E] hover:bg-[#152f4a] text-white px-6 py-4 rounded-full shadow-2xl transition-colors z-40">
      <span class="font-bold">خريطة المواصلات الحية</span>
      <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
    </button>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>