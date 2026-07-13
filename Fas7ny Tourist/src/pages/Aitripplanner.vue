<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { generateTrip, TripGenerationError } from '../services/planner'
import TripGenerationLoader from '../components/TripGenerationLoader.vue'
const router = useRouter()

/* ---------------- Helpers ---------------- */
const arabicDigits = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
const toArabicDigits = (n) => String(n).replace(/[0-9]/g, (d) => arabicDigits[d])
const formatEGP = (n) => `${toArabicDigits(Math.round(n || 0).toLocaleString('en-US'))} ج.م`

/* ---------------- Toast feedback ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2500)
}

/* ---------------- Wizard steps ---------------- */
const steps = [
  { id: 1, label: 'الوجهة والمدة' },
  { id: 2, label: 'التفضيلات' },
  { id: 3, label: 'مراجعة الخطة' },
]
const currentStep = ref(1)
const maxReachedStep = ref(1)

const goToStep = (n) => {
  if (n <= maxReachedStep.value) currentStep.value = n
}
const goToPrevStep = () => {
  if (currentStep.value > 1) currentStep.value -= 1
}
const goToNextStep = () => {
  if (currentStep.value === 1 && selectedCities.value.length === 0) {
    showToast('اختر مدينة واحدة على الأقل للمتابعة')
    return
  }
  if (currentStep.value < steps.length) {
    currentStep.value += 1
    maxReachedStep.value = Math.max(maxReachedStep.value, currentStep.value)
  }
}

/* ---------------- Step 1: destination & duration ---------------- */
const selectedCities = ref(['أسوان', 'الأقصر', 'القاهرة'])
const newCityInput = ref('')
const addCity = () => {
  const value = newCityInput.value.trim()
  if (value && !selectedCities.value.includes(value)) {
    selectedCities.value.push(value)
    showToast(`تمت إضافة ${value}`)
  }
  newCityInput.value = ''
}
const removeCity = (city) => {
  selectedCities.value = selectedCities.value.filter((c) => c !== city)
  showToast(`تم حذف ${city}`)
}

const numDays = ref(7)
const decreaseDays = () => {
  if (numDays.value > 1) numDays.value -= 1
}
const increaseDays = () => {
  if (numDays.value < 21) numDays.value += 1
}

const tripStartDate = ref('١٥ أكتوبر ٢٠٢٤')
const dateInput = ref('2024-10-15')
const onDateChange = () => {
  const d = new Date(dateInput.value)
  if (!isNaN(d)) {
    tripStartDate.value = d.toLocaleDateString('ar-EG', { year: 'numeric', month: 'long', day: 'numeric' })
  }
}

// عدد المسافرين وتفاصيل الأطفال - بتتبعت فعليًا في الـ request للباك اند
// (people / has_children / children_count) عشان الأسعار والاقتراحات
// تتأثر بيها صح
const peopleCount = ref(2)
const decreasePeople = () => {
  if (peopleCount.value > 1) peopleCount.value -= 1
}
const increasePeople = () => {
  if (peopleCount.value < 20) peopleCount.value += 1
}

const hasChildren = ref(false)
const childrenCount = ref(1)
const decreaseChildren = () => {
  if (childrenCount.value > 1) childrenCount.value -= 1
}
const increaseChildren = () => {
  if (childrenCount.value < 10) childrenCount.value += 1
}

/* ---------------- Step 2: preferences ---------------- */
// نوع الرحلة بقى اختيار متعدد (multi-select) بدل اختيار واحد بس
const tripTypes = [
  { id: 'beach', label: 'شواطئ وغوص' },
  { id: 'historic', label: 'تاريخي' },
  { id: 'fun', label: 'ترفيهي' },
  { id: 'family', label: 'عائلي' },
  { id: 'adventure', label: 'مغامرة' },
  { id: 'relax', label: 'استجمام' },
  { id: 'shopping', label: 'تسوق' },
  { id: 'nightlife', label: 'سهر وحياة ليلية' },
]
const selectedTripTypes = ref(['beach'])
const toggleTripType = (id) => {
  if (selectedTripTypes.value.includes(id)) {
    // لازم يفضل نوع واحد مختار على الأقل عشان الطلب يفضل صالح
    if (selectedTripTypes.value.length > 1) {
      selectedTripTypes.value = selectedTripTypes.value.filter((t) => t !== id)
    }
  } else {
    selectedTripTypes.value = [...selectedTripTypes.value, id]
  }
}
const tripTypeLabels = computed(() =>
  tripTypes.filter((t) => selectedTripTypes.value.includes(t.id)).map((t) => t.label)
)
// الباك اند بياخد trip_type كنص واحد - بنجمع كل الأنواع المختارة بفاصلة
const tripTypeValue = computed(() => tripTypeLabels.value.join('، '))

// مكان الإقامة بقى فيه خيارات متنوعة أكتر من فندق 5 نجوم/شقة بس
const accommodationOptions = [
  { id: 'hotel5', label: 'فندق ٥ نجوم' },
  { id: 'hotel4', label: 'فندق ٤ نجوم' },
  { id: 'hotel3', label: 'فندق ٣ نجوم' },
  { id: 'apartment', label: 'شقة مفروشة' },
  { id: 'chalet', label: 'شاليه' },
  { id: 'resort', label: 'منتجع سياحي' },
  { id: 'hostel', label: 'هوستيل اقتصادي' },
]
const selectedAccommodation = ref('apartment')
const accommodationLabel = computed(() => accommodationOptions.find((a) => a.id === selectedAccommodation.value)?.label || '')

// السقف الأقصى للميزانية اليومية اتزود لـ 20,000 ج.م
const MAX_DAILY_BUDGET = 20000
const dailyBudget = ref(1200)

const transportOptions = [
  { id: 'bus', label: 'أوتوبيس سياحي' },
  { id: 'car', label: 'تأجير سيارة' },
  { id: 'train', label: 'قطار' },
]
const selectedTransport = ref('car')
const transportLabel = computed(() => transportOptions.find((t) => t.id === selectedTransport.value)?.label || '')

// تفضيلات الطعام - أنواع أكل حقيقية ومنطقية داخل مصر
const foodTagOptions = [
  'أكل شعبي', 'مأكولات بحرية', 'مشويات', 'حلويات شرقية',
  'مأكولات دولية', 'نباتي', 'مأكولات آسيوية', 'أكل بيتي/أسري',
]
const selectedFoodTags = ref(['أكل شعبي', 'مأكولات بحرية'])
const toggleFoodTag = (tag) => {
  selectedFoodTags.value = selectedFoodTags.value.includes(tag)
    ? selectedFoodTags.value.filter((t) => t !== tag)
    : [...selectedFoodTags.value, tag]
}

/* ---------------- AI generation state ---------------- */
const isGenerating = ref(false)
const isAiLoading = ref(false)
const generatedTrip = ref(null)
const generationError = ref('')
// true لو الخطأ مؤقت (503 - الخدمة مشغولة) ويستاهل زرار "حاول تاني"
// واضح، بدل ما نرجّع المستخدم لخطوة التفضيلات زي أي خطأ تاني
const isRetryableError = ref(false)

const generatePlan = async () => {
  isGenerating.value = true
  isAiLoading.value = true
  generationError.value = ''
  isRetryableError.value = false

  try {
    const requestData = {
      destinations: selectedCities.value,
      trip_type: tripTypeValue.value,
      accommodation: accommodationLabel.value,
      daily_budget: dailyBudget.value,
      transport: transportLabel.value,
      food_preferences: selectedFoodTags.value,
      days: numDays.value,
      people: peopleCount.value,
      start_date: dateInput.value,
      has_children: hasChildren.value,
      children_count: hasChildren.value ? childrenCount.value : 0,
      travel_style: 'Balanced',
      interests: [],
      language: 'Arabic',
      notes: '',
    }

    const response = await generateTrip(requestData)
    generatedTrip.value = response

    isAiLoading.value = false
    goToNextStep()
    showToast('تم إنشاء الرحلة بنجاح')
  } catch (err) {
    console.error(err)
    isAiLoading.value = false

    if (err instanceof TripGenerationError) {
      // الرسالة جاية جاهزة وواضحة من الباك اند (planner_routes.py) -
      // مفيش تفاصيل تقنية، نص عربي مباشر جاهز للعرض زي ما هو
      generationError.value = err.detail
      isRetryableError.value = err.isRetryable
    } else {
      // احتياطي لأي خطأ غير متوقع تمامًا (نادر، لأن generateTrip()
      // بتلف كل حاجة في TripGenerationError فعليًا)
      generationError.value = 'حدث خطأ أثناء إنشاء الرحلة. حاول مرة أخرى.'
      isRetryableError.value = false
    }

    showToast(generationError.value)
  } finally {
    isGenerating.value = false
  }
}

/* ---------------- Step 3: day-by-day itinerary (fully from API) ---------------- */

// فولباك وحيد لو مفيش صورة خالص راجعة من الباك إند (نادر - الباك إند
// نفسه بيحط صورة Wikimedia افتراضية لو معرفش يجيب صورة حقيقية للمكان)
const FALLBACK_IMAGE = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

// خريطة الفئات الثمانية اللي بترجع من الـ API (Activity.category) لأيقونة
// ولون شارة مناسبين. transport مش نشاط بمكان حقيقي (place_details يبقى
// null له من enrich_trip)، فبناخد له معاملة بصرية مختلفة.
const CATEGORY_META = {
  hotel: { label: 'إقامة', color: '#8A5CF6', icon: 'M3 21h18M5 21V7a2 2 0 012-2h10a2 2 0 012 2v14M9 21v-4a2 2 0 012-2h2a2 2 0 012 2v4M9 9h1m4 0h1m-6 4h1m4 0h1' },
  restaurant: { label: 'مطعم', color: '#E07A3F', icon: 'M8 2v6a2 2 0 002 2v10M16 2v20M16 8a4 4 0 000-6' },
  cafe: { label: 'مقهى', color: '#A9713F', icon: 'M3 10h13a4 4 0 010 8H3zM3 10V6h13v4M6 3v2m3-2v2m3-2v2' },
  museum: { label: 'متحف', color: '#1A3C5E', icon: 'M3 21h18M4 21V10l8-6 8 6v11M9 21v-6h6v6' },
  attraction: { label: 'معلم سياحي', color: '#C9A84C', icon: 'M12 2l2.9 6.5L21 9.3l-4.9 4.5 1.2 6.7L12 17.3l-5.3 3.2 1.2-6.7L3 9.3l6.1-.8z' },
  shopping: { label: 'تسوق', color: '#B4529A', icon: 'M6 2l1.5 5h9L18 2M4 8h16l-1.5 12a2 2 0 01-2 2h-9a2 2 0 01-2-2z' },
  park: { label: 'حديقة', color: '#4E9D5C', icon: 'M12 2a5 5 0 015 5c0 3-5 9-5 9s-5-6-5-9a5 5 0 015-5zM12 21v-5' },
  beach: { label: 'شاطئ', color: '#2FA0C9', icon: 'M2 21c2-2 4-2 6 0s4 2 6 0 4-2 6 0M4 15l9-9 7 7M12 6L4 14' },
  activity: { label: 'نشاط', color: '#C9A84C', icon: 'M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z' },
  transport: { label: 'تنقل', color: '#7E7665', icon: 'M5 17h14M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0M5 17V9a2 2 0 012-2h10a2 2 0 012 2v8M5 9l1.5-4h11L19 9' },
}
const DEFAULT_CATEGORY_META = { label: 'نشاط', color: '#7E7665', icon: 'M12 8v4l3 3' }

const getCategoryMeta = (category) => CATEGORY_META[(category || '').toLowerCase()] || DEFAULT_CATEGORY_META

// تحويل activity من شكل الـ API (Activity + place_details enrichment) لشكل
// العرض. كل حقل هنا بييجي من مصدر حقيقي في الـ response - مفيش أي قيمة
// وهمية أو مختلقة.
const mapActivityToItem = (activity) => {
  const details = activity.place_details || null
  return {
    time: activity.time,
    category: activity.category,
    categoryMeta: getCategoryMeta(activity.category),
    title: activity.place,
    desc: activity.description,
    duration: activity.duration,
    priceValue: activity.estimated_cost || 0,
    img: details?.image_url || FALLBACK_IMAGE,
    hasRealPlace: !!details,
    rating: details?.rating ?? null,
    reviews: details?.reviews ?? null,
    popularity: details?.popularity ?? null,
    address: details?.address ?? null,
    googleMaps: details?.google_maps ?? null,
  }
}

// تحويل day من شكل الـ API لشكل العرض. day.accommodation مش موجود في
// الـ schema الحالي (DayPlan)، فمبنعملوش اختلاق - بنسيبه null والتصميم
// بيخفي القسم المرتبط بيه بالكامل (v-if) بدل ما يعرض بيانات وهمية.
const mapDay = (day) => ({
  num: day.day,
  title: day.title,
  accommodation: null,
  totalCost: day.total_cost,
  weather: day.weather || null,
  timeline: (day.activities || []).map(mapActivityToItem),
})

// كل أيام الرحلة، محسوبة بالكامل من الـ response الحقيقي
const days = computed(() => {
  if (!generatedTrip.value?.days) return []
  return generatedTrip.value.days.map(mapDay)
})

const initialDayCount = computed(() => Math.min(3, days.value.length))
const extraDaysCount = computed(() => Math.max(0, days.value.length - initialDayCount.value))
const showAllDays = ref(false)
const visibleDays = computed(() =>
  showAllDays.value ? days.value : days.value.slice(0, initialDayCount.value)
)

const revealRemainingDays = () => {
  showAllDays.value = !showAllDays.value
}

const expandedDay = ref(1)
const toggleDay = (day) => {
  expandedDay.value = expandedDay.value === day.num ? 0 : day.num
}

/* ---------------- Editing an activity (local UI state only) ---------------- */
const editingActivity = ref(null) // { dayNum, idx }
const editForm = ref({ title: '', desc: '', time: '', priceValue: 0 })

const startEditActivity = (day, item, idx) => {
  editingActivity.value = { dayNum: day.num, idx }
  editForm.value = { title: item.title, desc: item.desc, time: item.time, priceValue: item.priceValue }
}
const cancelEditActivity = () => {
  editingActivity.value = null
}
const saveEditActivity = (day, idx) => {
  const item = day.timeline[idx]
  item.title = editForm.value.title
  item.desc = editForm.value.desc
  item.time = editForm.value.time
  item.priceValue = Number(editForm.value.priceValue) || 0
  editingActivity.value = null
  // TODO: persist activity edit to backend, e.g. api.patch(`/trip-plans/${planId}/days/${day.num}/items/${idx}`, item)
  showToast('تم تحديث النشاط')
}

/* ---------------- Cost display (100% from API's budget_breakdown) ---------------- */
const budgetBreakdown = computed(() => generatedTrip.value?.budget_breakdown || null)

const budgetStats = computed(() => {
  if (!budgetBreakdown.value) return []
  return [
    { label: 'الإقامة', value: formatEGP(budgetBreakdown.value.accommodation) },
    { label: 'المواصلات', value: formatEGP(budgetBreakdown.value.transportation) },
    { label: 'الطعام', value: formatEGP(budgetBreakdown.value.food) },
    { label: 'الأنشطة', value: formatEGP(budgetBreakdown.value.attractions) },
    { label: 'أخرى', value: formatEGP(budgetBreakdown.value.miscellaneous) },
  ]
})

const estimatedTotalValue = computed(() => generatedTrip.value?.total_estimated_cost || 0)
const estimatedTotal = computed(() => formatEGP(estimatedTotalValue.value))

const plannedBudgetValue = computed(() => dailyBudget.value * numDays.value)
const budgetUsedPercent = computed(() => {
  if (plannedBudgetValue.value === 0) return 0
  return Math.min(100, Math.round((estimatedTotalValue.value / plannedBudgetValue.value) * 100))
})

/* ---------------- Trip-level extras from API (previously unused) ---------------- */
const tripSummary = computed(() => generatedTrip.value?.summary || '')
const transportationTips = computed(() => generatedTrip.value?.transportation_tips || [])
const packingList = computed(() => generatedTrip.value?.packing_list || [])

/* ---------------- Header actions ---------------- */
const isSaved = ref(false)
const savePlan = () => {
  // TODO: persist trip plan to backend / user account
  isSaved.value = !isSaved.value
  showToast(isSaved.value ? 'تم حفظ المسار' : 'تم إلغاء الحفظ')
}

const shareItinerary = async () => {
  const url = window.location.href
  if (navigator.share) {
    try {
      await navigator.share({ title: generatedTrip.value?.trip_title || 'خطة رحلتي في مصر', url })
    } catch (e) {
      /* user cancelled share, ignore */
    }
  } else if (navigator.clipboard) {
    await navigator.clipboard.writeText(url)
    showToast('تم نسخ الرابط')
  }
}

const downloadItinerary = () => {
  // TODO: replace with real PDF export endpoint, e.g. window.open(`/api/trip-plans/${planId}/export`)
  showToast('جاري تجهيز ملف الخطة...')
  window.print()
}

/* ---------------- Booking ---------------- */
const confirmBooking = () => {
  showToast('جاري تحويلك لصفحة الدفع...')
  router.push('/payment')
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8] pb-28">
    <Navbar />

    <!-- Toast -->
    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <!-- Page Header -->
    <div class="pt-18">
      <div class="bg-[#F5ECD7] border-b border-[#D0C5B2] py-12 px-6">
        <div class="max-w-348 mx-auto text-right">
          <p class="text-sm font-semibold text-[#C9A84C] mb-2 flex items-center gap-1.5 justify-end">
            <span>خطط رحلتك</span>
            <svg class="w-3 h-3 -scale-x-100" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            <button @click="router.push('/')" class="text-[#7E7665] font-medium hover:text-[#1A3C5E]">الرئيسية</button>
          </p>
          <h1 class="text-[40px] leading-12 font-bold text-[#1A3C5E] mb-2">مساعد رحلة الذكي</h1>
          <p class="text-lg text-[#4D4637] mb-6">يعمل خطتك الكاملة في ثوان — من الطيران للفطار.</p>

          <!-- Planning mode switcher -->
          <div class="flex justify-center">
            <div class="inline-flex items-center bg-white border border-[#D0C5B2] rounded-full p-1.5 shadow-sm">
              <button @click="router.push('/book-trip')"
                class="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold text-[#4D4637] hover:text-[#1A3C5E] transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
                حجز يدوي
              </button>
              <button type="button" disabled
                class="flex items-center gap-2 bg-linear-to-l from-[#C9A84C] to-[#dcbf6d] text-white shadow px-5 py-2.5 rounded-full text-sm font-semibold cursor-default">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
                خطط بالذكاء الاصطناعي
                <span class="text-[9px] bg-white/25 px-1.5 py-0.5 rounded-full font-bold">AI</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Step Indicator -->
      <div class="max-w-348 mx-auto px-6 -mt-8.25 relative z-10">
        <div class="bg-white border border-[#D0C5B2] shadow-sm rounded-xl flex flex-col md:flex-row items-center justify-between gap-4 py-4 px-4">
          <button @click="goToPrevStep" :disabled="currentStep === 1"
            class="flex items-center gap-1.5 text-sm font-semibold px-3 py-2 rounded-lg transition-colors shrink-0"
            :class="currentStep === 1 ? 'text-[#D0C5B2] cursor-not-allowed' : 'text-[#1A3C5E] hover:bg-[#F4F4F2]'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            السابق
          </button>

          <div class="flex items-center justify-center gap-8 md:gap-12 overflow-x-auto">
            <template v-for="(step, i) in steps" :key="step.id">
              <button @click="goToStep(step.id)" :disabled="step.id > maxReachedStep"
                class="flex items-center gap-3 shrink-0" :class="step.id > maxReachedStep ? 'cursor-not-allowed opacity-60' : ''">
                <span :class="step.id === currentStep ? 'text-[#1A3C5E] font-bold' : 'text-[#7E7665]'" class="text-base">
                  {{ step.label }}
                </span>
                <div v-if="step.id < currentStep"
                  class="w-8 h-8 rounded-full bg-[#755B00] border-2 border-[#755B00] flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                </div>
                <div v-else-if="step.id === currentStep"
                  class="w-8 h-8 rounded-full bg-[#C9A84C] border-2 border-[#C9A84C] flex items-center justify-center text-white font-bold text-base">
                  {{ step.id }}
                </div>
                <div v-else
                  class="w-8 h-8 rounded-full border-2 border-[#D0C5B2] flex items-center justify-center text-[#7E7665] font-bold text-base">
                  {{ step.id }}
                </div>
              </button>
              <div v-if="i < steps.length - 1" class="w-12 h-0.5 shrink-0"
                :class="step.id < currentStep ? 'bg-[#755B00]' : 'bg-[#D0C5B2]'"></div>
            </template>
          </div>

          <button @click="goToNextStep" :disabled="currentStep === steps.length"
            class="flex items-center gap-1.5 text-sm font-semibold px-3 py-2 rounded-lg transition-colors shrink-0"
            :class="currentStep === steps.length ? 'text-[#D0C5B2] cursor-not-allowed' : 'text-white bg-[#C9A84C] hover:bg-[#b8963f]'">
            التالي
            <svg class="w-4 h-4 -scale-x-100" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
        </div>
      </div>
    </div>

    <div class="max-w-348 mx-auto px-6 py-10">

      <!-- ============ STEP 1: destination & duration ============ -->
      <div v-if="currentStep === 1" class="max-w-2xl mx-auto bg-white border border-[#D0C5B2] rounded-2xl p-8 flex flex-col gap-8">
        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">المدن اللي هتزورها</h3>
          <div class="flex items-center gap-2 flex-wrap justify-end">
            <span v-for="city in selectedCities" :key="city"
              class="flex items-center gap-2 bg-[#F4F4F2] border border-[#D0C5B2] text-[#1A1C1B] px-4 py-2 rounded-lg text-base">
              <button @click="removeCity(city)" class="text-[#C9A84C]">
                <svg class="w-2.5 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
              {{ city }}
            </span>
            <span v-if="selectedCities.length === 0" class="text-sm text-[#7E7665]">لم تختر أي مدينة بعد</span>
          </div>
          <div class="flex items-center gap-2">
            <button @click="addCity" class="bg-[#C9A84C] text-white text-sm px-5 py-2.5 rounded-lg shrink-0">إضافة</button>
            <input v-model="newCityInput" @keyup.enter="addCity" type="text" placeholder="اكتب اسم مدينة..."
              class="flex-1 border border-[#D0C5B2] rounded-lg px-3 py-2.5 text-sm text-right focus:outline-none focus:border-[#C9A84C]" />
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">مدة الرحلة</h3>
          <div class="flex items-center justify-center gap-6">
            <button @click="increaseDays" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-[#F4F4F2]">+</button>
            <span class="text-2xl font-bold text-[#1A3C5E] w-24 text-center">{{ toArabicDigits(numDays) }} أيام</span>
            <button @click="decreaseDays" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-[#F4F4F2]">-</button>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">تاريخ البدء</h3>
          <input v-model="dateInput" @change="onDateChange" type="date"
            class="w-full border border-[#D0C5B2] rounded-lg px-4 py-3 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">عدد المسافرين</h3>
          <div class="flex items-center justify-center gap-6">
            <button @click="increasePeople" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-[#F4F4F2]">+</button>
            <span class="text-2xl font-bold text-[#1A3C5E] w-24 text-center">{{ toArabicDigits(peopleCount) }} أفراد</span>
            <button @click="decreasePeople" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-[#F4F4F2]">-</button>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <button @click="hasChildren = !hasChildren"
              class="w-12 h-7 rounded-full relative transition-colors shrink-0"
              :class="hasChildren ? 'bg-[#C9A84C]' : 'bg-[#D0C5B2]'">
              <span class="absolute top-1 w-5 h-5 rounded-full bg-white transition-all"
                :class="hasChildren ? 'right-6' : 'right-1'"></span>
            </button>
            <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">هل يوجد أطفال معكم؟</h3>
          </div>
          <div v-if="hasChildren" class="flex items-center justify-center gap-6 bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl py-4">
            <button @click="increaseChildren" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-white">+</button>
            <span class="text-xl font-bold text-[#1A3C5E] w-28 text-center">{{ toArabicDigits(childrenCount) }} أطفال</span>
            <button @click="decreaseChildren" class="w-11 h-11 rounded-full border border-[#D0C5B2] text-[#1A3C5E] text-xl flex items-center justify-center hover:bg-white">-</button>
          </div>
        </div>

        <button @click="goToNextStep"
          class="w-full bg-[#C9A84C] hover:bg-[#b8963f] text-white font-semibold py-3.5 rounded-xl transition-colors">
          التالي: التفضيلات
        </button>
      </div>

      <!-- ============ STEP 2: preferences ============ -->
      <div v-else-if="currentStep === 2" class="max-w-2xl mx-auto bg-white border border-[#D0C5B2] rounded-2xl p-8 flex flex-col gap-8">

        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <span class="text-xs text-[#7E7665]">تقدر تختار أكتر من نوع</span>
            <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">نوع الرحلة</h3>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <button v-for="type in tripTypes" :key="type.id" @click="toggleTripType(type.id)"
              :class="selectedTripTypes.includes(type.id)
                ? 'border-2 border-[#C9A84C] bg-[#C9A84C]/10 text-[#503D00] font-bold'
                : 'border border-[#D0C5B2] text-[#1A1C1B]'"
              class="relative flex flex-col items-center justify-center gap-2 rounded-xl py-4 text-sm transition-colors">
              <span v-if="selectedTripTypes.includes(type.id)"
                class="absolute top-2 left-2 w-4 h-4 rounded-full bg-[#C9A84C] flex items-center justify-center">
                <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
              </span>
              <svg class="w-5 h-5" :class="selectedTripTypes.includes(type.id) ? 'text-[#C9A84C]' : 'text-[#7E7665]'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v18m9-9H3"/></svg>
              {{ type.label }}
            </button>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">مكان الإقامة المفضل</h3>
          <div class="grid grid-cols-2 gap-2">
            <button v-for="opt in accommodationOptions" :key="opt.id" @click="selectedAccommodation = opt.id"
              :class="selectedAccommodation === opt.id
                ? 'border-2 border-[#C9A84C] bg-[#C9A84C]/10'
                : 'border border-[#D0C5B2]'"
              class="flex items-center justify-between px-4 py-3 rounded-lg cursor-pointer transition-colors">
              <span class="w-5 h-5 rounded-full border flex items-center justify-center shrink-0"
                :class="selectedAccommodation === opt.id ? 'border-[#C9A84C] bg-[#C9A84C]' : 'border-[#D0C5B2] bg-white'">
                <span v-if="selectedAccommodation === opt.id" class="w-2 h-2 rounded-full bg-white"></span>
              </span>
              <span class="text-sm" :class="selectedAccommodation === opt.id ? 'font-semibold text-[#1A3C5E]' : 'text-[#1A1C1B]'">{{ opt.label }}</span>
            </button>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <span class="font-bold text-[#C9A84C]">{{ toArabicDigits(Number(dailyBudget).toLocaleString('en-US')) }} ج.م</span>
            <h3 class="text-2xl font-semibold text-[#1A3C5E]">الميزانية اليومية</h3>
          </div>
          <input type="range" min="500" :max="MAX_DAILY_BUDGET" step="100" v-model="dailyBudget"
            class="w-full accent-[#C9A84C]" />
          <div class="flex items-center justify-between text-xs text-[#7E7665]">
            <span>{{ toArabicDigits(MAX_DAILY_BUDGET.toLocaleString('en-US')) }} ج.م+</span>
            <span>٥٠٠ ج.م</span>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">وسيلة المواصلات</h3>
          <div class="flex items-center gap-2 flex-wrap justify-end">
            <button v-for="t in transportOptions" :key="t.id" @click="selectedTransport = t.id"
              :class="selectedTransport === t.id
                ? 'bg-[#C9A84C] border-2 border-[#C9A84C] text-white font-semibold shadow'
                : 'border border-[#D0C5B2] text-[#7E7665]'"
              class="px-4 py-2.5 rounded-full text-base transition-colors">
              {{ t.label }}
            </button>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-2xl font-semibold text-[#1A3C5E] text-right">تفضيلات الطعام</h3>
          <div class="flex items-center gap-2 flex-wrap justify-end">
            <button v-for="tag in foodTagOptions" :key="tag" @click="toggleFoodTag(tag)"
              :class="selectedFoodTags.includes(tag)
                ? 'bg-[#B4D4FE]/40 border-[#B4D4FE] text-[#1A3C5E]'
                : 'bg-transparent border-[#D0C5B2] text-[#7E7665]'"
              class="border text-xs font-semibold px-3 py-1.5 rounded-full transition-colors">
              {{ tag }}
            </button>
          </div>
        </div>

        <button @click="generatePlan" :disabled="isGenerating"
          class="w-full bg-[#C9A84C] hover:bg-[#b8963f] disabled:opacity-70 text-white font-semibold py-3.5 rounded-xl flex items-center justify-center gap-3 transition-colors">
          <svg v-if="isGenerating" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>
          <template v-else>
            بناء الخطة بالذكاء الاصطناعي
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
          </template>
        </button>
      </div>

      <!-- ============ STEP 3: AI loading ============ -->
      <TripGenerationLoader v-else-if="isAiLoading" :num-days="numDays" />

      <!-- ============ STEP 3: generation failed, no data to show ============ -->
      <div v-else-if="!generatedTrip"
        class="bg-white rounded-2xl border border-[#D0C5B2] p-16 flex flex-col items-center justify-center gap-6 text-center">
        <svg class="w-14 h-14 text-[#D0C5B2]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>
        <div>
          <h2 class="text-2xl font-bold text-[#1A3C5E] mb-2">
            {{ isRetryableError ? 'الخدمة مشغولة حاليًا' : 'لسه مفيش خطة جاهزة' }}
          </h2>
          <p class="text-[#7E7665]">{{ generationError || 'ارجع لخطوة التفضيلات واضغط على "بناء الخطة بالذكاء الاصطناعي".' }}</p>
        </div>
        <div class="flex items-center gap-3">
          <!-- الخطأ مؤقت (503) - المنطقي هنا إننا نقترح "حاول تاني" مباشرة
               بنفس البيانات، مش نرجّعه لخطوة التفضيلات من غير داعي -->
          <button v-if="isRetryableError" @click="generatePlan"
            class="bg-[#C9A84C] hover:bg-[#b8963f] text-white font-semibold px-6 py-3 rounded-xl transition-colors">
            حاول تاني
          </button>
          <button @click="goToStep(2)"
            :class="isRetryableError ? 'border border-[#D0C5B2] text-[#1A3C5E]' : 'bg-[#C9A84C] hover:bg-[#b8963f] text-white'"
            class="font-semibold px-6 py-3 rounded-xl transition-colors">
            الرجوع للتفضيلات
          </button>
        </div>
      </div>

      <!-- ============ STEP 3: review (100% from generatedTrip) ============ -->
      <div v-else class="flex flex-col lg:flex-row gap-8 items-start">

        <!-- Plan Content -->
        <div class="flex-1 w-full flex flex-col gap-8 order-2 lg:order-1">

          <!-- Plan Header Actions -->
          <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div class="flex items-center gap-2 flex-wrap">
              <button @click="savePlan"
                :class="isSaved ? 'bg-[#755B00]' : 'bg-[#1A3C5E] hover:bg-[#152f4a]'"
                class="flex items-center gap-2 text-white px-4 py-3 rounded-lg text-base transition-colors">
                {{ isSaved ? 'تم حفظ المسار' : 'حفظ المسار' }}
                <svg v-if="!isSaved" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-6 0V4a1 1 0 011-1h4a1 1 0 011 1v3m-6 0h6"/></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
              </button>
              <button @click="downloadItinerary" title="تحميل الخطة"
                class="border border-[#D0C5B2] text-[#1A3C5E] w-11 h-11 rounded-lg flex items-center justify-center hover:bg-[#F4F4F2] transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H8a2 2 0 01-2-2V5a2 2 0 012-2h4l6 6v9a2 2 0 01-2 2z"/></svg>
              </button>
              <button @click="shareItinerary" title="مشاركة الخطة"
                class="border border-[#D0C5B2] text-[#1A3C5E] w-11 h-11 rounded-lg flex items-center justify-center hover:bg-[#F4F4F2] transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
              </button>
              <button @click="router.push('/community')"
                class="flex items-center gap-2 border border-[#C9A84C] text-[#C9A84C] px-4 py-3 rounded-lg text-base hover:bg-[#C9A84C]/10 transition-colors">
                شوف لحظات من فسحني
                <svg class="w-3.5 h-3.5 -scale-x-100" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
            </div>
            <div class="text-right">
              <h2 class="text-[32px] leading-10.5 font-semibold text-[#1A3C5E]">{{ generatedTrip.trip_title }}</h2>
              <p v-if="tripSummary" class="text-sm text-[#4D4637] max-w-xl mt-1">{{ tripSummary }}</p>
              <p class="text-base text-[#7E7665] mt-1">تاريخ البدء المتوقع: {{ tripStartDate }}</p>
            </div>
          </div>

          <!-- Budget Summary Card -->
          <div class="bg-white border border-[#D0C5B2] rounded-2xl flex flex-col md:flex-row items-center justify-center gap-8 px-8 py-6">
            <div class="flex flex-col items-center gap-1 md:border-l md:border-[#D0C5B2]/30 md:pl-8 shrink-0">
              <div class="relative w-24 h-24">
                <svg class="w-24 h-24 -rotate-90" viewBox="0 0 96 96">
                  <circle cx="48" cy="48" r="40" fill="none" stroke="#E8E4DC" stroke-width="8" />
                  <circle cx="48" cy="48" r="40" fill="none" stroke="#C9A84C" stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="`${2 * Math.PI * 40}`"
                    :stroke-dashoffset="`${2 * Math.PI * 40 * (1 - budgetUsedPercent / 100)}`" />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <span class="text-sm font-bold text-[#1A1C1B]">%{{ toArabicDigits(budgetUsedPercent) }}</span>
                  <span class="text-[10px] text-[#7E7665]">الميزانية</span>
                </div>
              </div>
              <p class="text-xs text-[#7E7665] text-center mt-2 w-40">من إجمالي ميزانيتك المحددة ({{ formatEGP(plannedBudgetValue) }})</p>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-5 gap-4 flex-1 w-full">
              <div v-for="stat in budgetStats" :key="stat.label" class="bg-[#F4F4F2] rounded-xl py-8 px-4 flex flex-col items-end gap-1">
                <span class="text-xs text-[#7E7665]">{{ stat.label }}</span>
                <span class="text-xl text-[#1A3C5E]">{{ stat.value }}</span>
              </div>
            </div>
          </div>

          <!-- Transportation tips + packing list (from API, previously unused) -->
          <div v-if="transportationTips.length || packingList.length" class="grid sm:grid-cols-2 gap-4">
            <div v-if="transportationTips.length" class="bg-white border border-[#D0C5B2] rounded-2xl p-6 flex flex-col gap-3">
              <h3 class="text-lg font-semibold text-[#1A3C5E] text-right flex items-center gap-2 justify-end">
                نصائح المواصلات
                <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 17h14M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0M5 17V9a2 2 0 012-2h10a2 2 0 012 2v8M5 9l1.5-4h11L19 9"/></svg>
              </h3>
              <ul class="flex flex-col gap-2">
                <li v-for="(tip, i) in transportationTips" :key="i" class="text-sm text-[#4D4637] text-right flex items-start gap-2 justify-end">
                  <span>{{ tip }}</span>
                  <span class="w-1.5 h-1.5 rounded-full bg-[#C9A84C] mt-1.5 shrink-0"></span>
                </li>
              </ul>
            </div>
            <div v-if="packingList.length" class="bg-white border border-[#D0C5B2] rounded-2xl p-6 flex flex-col gap-3">
              <h3 class="text-lg font-semibold text-[#1A3C5E] text-right flex items-center gap-2 justify-end">
                قائمة التجهيز
                <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
              </h3>
              <ul class="flex flex-wrap gap-2 justify-end">
                <li v-for="(item, i) in packingList" :key="i"
                  class="text-xs font-semibold text-[#1A3C5E] bg-[#F4F4F2] border border-[#D0C5B2] px-3 py-1.5 rounded-full">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Day-by-Day Accordion -->
          <div class="w-full flex flex-col gap-4">
            <div v-for="day in visibleDays" :key="day.num"
              :class="expandedDay === day.num ? 'bg-white shadow-sm' : 'bg-white/80'"
              class="border border-[#D0C5B2] rounded-2xl overflow-hidden transition-colors">

              <button @click="toggleDay(day)" class="w-full flex items-center justify-between px-6 py-6"
                :class="expandedDay === day.num ? 'bg-[#F4F4F2]' : ''">
                <svg :class="expandedDay === day.num ? '' : 'rotate-180'"
                  class="w-3 h-2 transition-transform" :style="{ color: expandedDay === day.num ? '#1A3C5E' : '#7E7665' }"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"/></svg>
                <div class="flex items-center gap-4">
                  <div class="text-right">
                    <p :class="expandedDay === day.num ? 'text-[#1A3C5E]' : 'text-[#7E7665]'" class="font-normal">{{ day.title }}</p>
                    <div v-if="day.weather" class="flex items-center gap-1.5 justify-end mt-0.5">
                      <img :src="day.weather.icon" class="w-4 h-4" alt="" />
                      <span class="text-xs text-[#7E7665]">{{ day.weather.condition }} • {{ toArabicDigits(Math.round(day.weather.temperature)) }}°</span>
                    </div>
                  </div>
                  <div class="w-12 h-12 rounded-full flex items-center justify-center font-semibold"
                    :class="expandedDay === day.num ? 'bg-[#C9A84C]/20 text-[#C9A84C]' : 'bg-[#EEEEEC] text-[#7E7665]'">
                    {{ toArabicDigits(day.num) }}
                  </div>
                </div>
              </button>

              <div v-if="expandedDay === day.num" class="p-6 flex flex-col gap-6">

                <div v-if="day.timeline.length === 0" class="text-center text-sm text-[#7E7665] py-10">
                  لا توجد تفاصيل لهذا اليوم بعد.
                </div>

                <template v-else>

                  <div v-for="(item, idx) in day.timeline" :key="idx" class="flex items-start gap-6">
                    <!-- Card / edit form -->
                    <div class="flex-1 pb-6">
                      <div v-if="editingActivity && editingActivity.dayNum === day.num && editingActivity.idx === idx"
                        class="bg-[#F9F9F7] border-2 border-[#C9A84C] rounded-xl p-4 flex flex-col gap-3">
                        <input v-model="editForm.title" type="text" placeholder="عنوان النشاط"
                          class="border border-[#D0C5B2] rounded-lg px-3 py-2 text-sm text-right focus:outline-none focus:border-[#C9A84C]" />
                        <textarea v-model="editForm.desc" rows="2" placeholder="الوصف"
                          class="border border-[#D0C5B2] rounded-lg px-3 py-2 text-sm text-right focus:outline-none focus:border-[#C9A84C] resize-none"></textarea>
                        <div class="flex items-center gap-3">
                          <div class="flex-1">
                            <label class="text-xs text-[#7E7665] block mb-1 text-right">الوقت</label>
                            <input v-model="editForm.time" type="text"
                              class="w-full border border-[#D0C5B2] rounded-lg px-3 py-2 text-sm text-right focus:outline-none focus:border-[#C9A84C]" />
                          </div>
                          <div class="flex-1">
                            <label class="text-xs text-[#7E7665] block mb-1 text-right">السعر (ج.م)</label>
                            <input v-model="editForm.priceValue" type="number" min="0"
                              class="w-full border border-[#D0C5B2] rounded-lg px-3 py-2 text-sm text-right focus:outline-none focus:border-[#C9A84C]" />
                          </div>
                        </div>
                        <div class="flex items-center gap-2 justify-end">
                          <button @click="cancelEditActivity" class="text-sm text-[#7E7665] px-4 py-2">إلغاء</button>
                          <button @click="saveEditActivity(day, idx)" class="bg-[#C9A84C] text-white text-sm font-semibold px-5 py-2 rounded-lg">حفظ التعديل</button>
                        </div>
                      </div>

                      <div v-else class="bg-[#F9F9F7] border border-[#D0C5B2] rounded-xl flex items-center gap-4 p-4">
                        <div class="flex-1 flex flex-col gap-1">
                          <div class="flex items-center justify-between">
                            <button @click="startEditActivity(day, item, idx)" class="flex items-center gap-1 text-[10px] text-[#7E7665] hover:text-[#1A3C5E]">
                              عدّل الخطة
                              <svg class="w-2 h-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                            </button>
                            <div class="flex items-center gap-2">
                              <span v-if="item.rating" class="text-xs text-[#C9A84C] font-medium flex items-center gap-1">
                                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.958a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.368 2.447a1 1 0 00-.363 1.118l1.287 3.957c.3.922-.755 1.688-1.538 1.118l-3.367-2.446a1 1 0 00-1.176 0l-3.367 2.446c-.783.57-1.838-.196-1.538-1.118l1.287-3.957a1 1 0 00-.363-1.118L2.813 9.385c-.784-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.958z"/></svg>
                                {{ toArabicDigits(item.rating) }}
                                <span v-if="item.reviews" class="text-[#7E7665]">({{ toArabicDigits(item.reviews) }})</span>
                              </span>
                              <span v-if="item.popularity && item.popularity !== 'Low'"
                                class="text-[10px] font-semibold px-2 py-0.5 rounded-full border"
                                :class="item.popularity === 'High'
                                  ? 'border-[#C9A84C] text-[#755B00] bg-[#C9A84C]/10'
                                  : 'border-[#D0C5B2] text-[#7E7665] bg-[#F4F4F2]'">
                                {{ item.popularity === 'High' ? 'مكان مشهور' : 'شائع نسبيًا' }}
                              </span>
                              <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full text-white"
                                :style="{ backgroundColor: item.categoryMeta.color }">
                                {{ item.categoryMeta.label }}
                              </span>
                            </div>
                          </div>
                          <h4 class="font-bold text-[#1A3C5E]">{{ item.title }}</h4>
                          <p class="text-sm text-[#4D4637]">{{ item.desc }}</p>
                          <p v-if="item.address" class="text-xs text-[#7E7665]">{{ item.address }}</p>
                          <div class="flex items-center gap-4 justify-end mt-1">
                            <span class="text-xs text-[#7E7665]">{{ formatEGP(item.priceValue) }}</span>
                            <span class="text-xs text-[#7E7665]">{{ item.duration }}</span>
                            <a v-if="item.googleMaps" :href="item.googleMaps" target="_blank" rel="noopener"
                              class="text-xs text-[#C9A84C] hover:underline">على الخريطة</a>
                          </div>
                        </div>
                        <img v-if="item.hasRealPlace" :src="item.img" class="w-24 h-24 object-cover rounded-lg shrink-0" alt="" />
                        <div v-else class="w-24 h-24 rounded-lg shrink-0 flex items-center justify-center"
                          :style="{ backgroundColor: item.categoryMeta.color + '1A' }">
                          <svg class="w-8 h-8" :style="{ color: item.categoryMeta.color }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="item.categoryMeta.icon"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <!-- Timeline rail -->
                    <div class="flex flex-col items-center gap-2 pt-1 shrink-0 w-12">
                      <span class="text-sm font-bold text-[#C9A84C] whitespace-nowrap">{{ item.time }}</span>
                      <div class="flex-1 w-px bg-[#D0C5B2]"></div>
                      <div v-if="idx !== day.timeline.length - 1" class="w-2 h-2 rounded-full bg-[#C9A84C]"></div>
                    </div>
                  </div>

                  <!-- Accommodation highlight - only renders once the backend exposes this field -->
                  <div v-if="day.accommodation" class="border-t border-dashed border-[#D0C5B2] pt-4 flex items-center justify-between flex-wrap gap-3">
                    <div class="flex items-center gap-3">
                      <div class="text-right">
                        <p class="text-xs text-[#7E7665]">الإقامة المقترحة لليلة {{ toArabicDigits(day.num) }}</p>
                        <p class="font-bold text-[#1A3C5E]">{{ day.accommodation }}</p>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>

            <!-- Expand remaining days -->
            <button v-if="extraDaysCount > 0 && !showAllDays" @click="revealRemainingDays"
              class="flex items-center justify-center gap-2 py-4 text-[#C9A84C] font-bold text-base border-2 border-dashed border-[#C9A84C]/40 rounded-2xl hover:bg-[#C9A84C]/5 hover:border-[#C9A84C] transition-colors">
              عرض باقي أيام الرحلة ({{ toArabicDigits(extraDaysCount) }} أيام أخرى)
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"/></svg>
            </button>
            <button v-else-if="extraDaysCount > 0 && showAllDays" @click="showAllDays = false"
              class="flex items-center justify-center gap-2 py-4 text-[#C9A84C] font-bold text-base border-2 border-[#C9A84C]/40 rounded-2xl hover:bg-[#C9A84C]/5 hover:border-[#C9A84C] transition-colors">
              إخفاء الأيام الإضافية
              <svg class="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
        </div>

        <!-- Aside: selections summary -->
        <aside class="w-full lg:w-90 bg-white border border-[#D0C5B2] rounded-xl p-6 flex flex-col gap-6 order-1 lg:order-2 lg:sticky lg:top-24">
          <div class="flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <button @click="goToStep(1)" class="text-sm font-semibold text-[#C9A84C] hover:underline">تعديل</button>
              <h3 class="text-lg font-semibold text-[#1A3C5E]">الوجهة والمدة</h3>
            </div>
            <p class="text-sm text-[#4D4637] text-right">{{ selectedCities.join('، ') || 'لا توجد مدن محددة' }}</p>
            <p class="text-sm text-[#7E7665] text-right">{{ toArabicDigits(numDays) }} أيام • يبدأ {{ tripStartDate }}</p>
          </div>

          <div class="border-t border-[#D0C5B2]"></div>

          <div class="flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <button @click="goToStep(2)" class="text-sm font-semibold text-[#C9A84C] hover:underline">تعديل</button>
              <h3 class="text-lg font-semibold text-[#1A3C5E]">التفضيلات</h3>
            </div>
            <div class="text-sm text-[#4D4637] text-right flex flex-col gap-1">
              <p>نوع الرحلة: {{ tripTypeLabels.join('، ') }}</p>
              <p>الإقامة: {{ accommodationLabel }}</p>
              <p>المواصلات: {{ transportLabel }}</p>
              <p>عدد المسافرين: {{ toArabicDigits(peopleCount) }}{{ hasChildren ? ` (منهم ${toArabicDigits(childrenCount)} أطفال)` : '' }}</p>
              <p>الميزانية اليومية: {{ formatEGP(dailyBudget) }}</p>
              <p v-if="selectedFoodTags.length">الطعام: {{ selectedFoodTags.join('، ') }}</p>
            </div>
          </div>

          <button @click="generatePlan" :disabled="isGenerating"
            class="w-full bg-[#C9A84C] hover:bg-[#b8963f] disabled:opacity-70 text-[#1A3C5E] font-semibold py-3 rounded-xl flex items-center justify-center gap-2 transition-colors">
            <svg v-if="isGenerating" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>
            <template v-else>
              تحديث الخطة بالذكاء الاصطناعي
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </template>
          </button>
        </aside>
      </div>
    </div>

    <!-- Bottom Sticky Booking Bar (only visible when reviewing an actual generated trip) -->
    <div v-if="currentStep === 3 && generatedTrip" class="fixed bottom-0 left-0 right-0 bg-white border-t border-[#D0C5B2] shadow-[0_-10px_30px_rgba(0,0,0,0.05)] px-6 py-4 z-40">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <button @click="confirmBooking"
            class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#1A3C5E] font-semibold px-8 py-3 rounded-xl shadow-lg shadow-[#C9A84C]/30 transition-colors">
            احجز الرحلة بالكامل
          </button>
          <button @click="goToStep(1)" class="flex items-center gap-2 border border-[#C9A84C] text-[#C9A84C] font-bold px-6 py-3 rounded-xl hover:bg-[#C9A84C]/10 transition-colors">
            تعديل التواريخ
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          </button>
        </div>
        <div class="flex items-center gap-8">
          <div class="text-right">
            <div class="flex items-center gap-1 justify-end text-xs text-[#4D4637]">
              <span>بناءً على تفضيلاتك</span>
              <svg class="w-2.5 h-2.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </div>
            <p class="text-[10px] text-[#7E7665]">تشمل الإقامة، الأنشطة، والمواصلات المحددة</p>
          </div>
          <span class="w-px h-10 bg-[#D0C5B2]"></span>
          <div class="text-right">
            <p class="text-xs text-[#7E7665]">التكلفة الإجمالية التقديرية</p>
            <p class="text-2xl text-[#1A3C5E]">{{ estimatedTotal }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>