<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  numDays: { type: Number, default: 3 },
})

/*
  المراحل دي مبنية فعليًا على الـ pipeline الحقيقي في enrichment_service.py:
  1) Gemini بيولد الخطة النصية (توزيع أيام + أنشطة)
  2) لكل نشاط: search_place() بينادي OSM (Nominatim/Overpass) + أحيانًا
     Gemini تاني لتفاصيل الـ rating/reviews للأنشطة الرئيسية
  3) إعادة ترتيب الأنشطة جغرافيًا (nearest-neighbor) وحساب أوقات
     التنقل (OSRM أو Haversine fallback)
  4) جلب الطقس لكل يوم (weather_service، مع cache)

  المدة الكلية بتتقدر بناءً على عدد الأيام (كل يوم فيه أنشطة محتاجة
  search_place منفصل)، مش رقم ثابت - رحلة 7 أيام فعليًا بتاخد وقت
  أطول من رحلة يوم واحد.
*/
const stages = [
  { key: 'gemini', label: 'الذكاء الاصطناعي بيصمم خطة رحلتك...', weight: 0.30 },
  { key: 'places', label: 'بنجيب تفاصيل الأماكن والصور...', weight: 0.40 },
  { key: 'routing', label: 'بنرتب الأنشطة جغرافيًا ونحسب أوقات التنقل...', weight: 0.20 },
  { key: 'weather', label: 'بنجيب توقعات الطقس لكل يوم...', weight: 0.10 },
]

// تقدير المدة الكلية: أساس ثابت + وقت إضافي لكل يوم (لأن كل يوم فيه
// أنشطة محتاجة نداءات search_place منفصلة). أرقام تقريبية مبنية على
// مراقبة فعلية للـ backend، مش دقيقة 100% لكنها أصدق من رقم عشوائي.
const estimatedTotalMs = computed(() => {
  const baseMs = 6000
  const perDayMs = 2500
  const days = Math.max(1, props.numDays || 1)
  return Math.min(45000, baseMs + perDayMs * days)
})

const elapsedMs = ref(0)
const currentStageIndex = ref(0)
let intervalId = null

const progressPercent = computed(() => {
  return Math.min(96, Math.round((elapsedMs.value / estimatedTotalMs.value) * 100))
})

const currentStage = computed(() => stages[currentStageIndex.value])

const isTakingLonger = computed(() => elapsedMs.value > estimatedTotalMs.value)

onMounted(() => {
  const tickMs = 200
  intervalId = setInterval(() => {
    elapsedMs.value += tickMs

    // نحدد المرحلة الحالية بناءً على نسبة الوقت المنقضي من الوزن
    // التراكمي لكل مرحلة
    const progressRatio = elapsedMs.value / estimatedTotalMs.value
    let cumulative = 0
    let stageIdx = stages.length - 1
    for (let i = 0; i < stages.length; i++) {
      cumulative += stages[i].weight
      if (progressRatio <= cumulative) {
        stageIdx = i
        break
      }
    }
    currentStageIndex.value = stageIdx
  }, tickMs)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<template>
  <div class="bg-white rounded-2xl border border-[#D0C5B2] p-16 flex flex-col items-center justify-center gap-8">
    <svg class="w-14 h-14 animate-spin text-[#C9A84C]" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
    </svg>

    <div class="text-center space-y-3 w-full max-w-md">
      <h2 class="text-3xl font-bold text-[#1A3C5E]">جاري إنشاء رحلتك...</h2>

      <Transition name="fade-stage" mode="out-in">
        <p :key="currentStage.key" class="text-[#4D4637] font-medium min-h-6">
          {{ currentStage.label }}
        </p>
      </Transition>

      <!-- Progress bar -->
      <div class="w-full bg-[#F4F4F2] rounded-full h-2 overflow-hidden mt-4">
        <div
          class="h-full bg-[#C9A84C] rounded-full transition-all duration-300 ease-out"
          :style="{ width: `${progressPercent}%` }"
        ></div>
      </div>

      <p v-if="!isTakingLonger" class="text-sm text-[#C9A84C]">
        {{ progressPercent }}٪ — قد يستغرق ذلك من ١٠ إلى ٤٥ ثانية حسب عدد الأيام
      </p>
      <p v-else class="text-sm text-[#7E7665]">
        الأمر بياخد وقت أطول من المتوقع، برجاء الانتظار... السيرفر لسه بيشتغل عليها
      </p>

      <!-- Stage checklist -->
      <ul class="flex flex-col gap-2 mt-6 text-right">
        <li v-for="(stage, i) in stages" :key="stage.key"
          class="flex items-center gap-2 justify-end text-sm"
          :class="i < currentStageIndex ? 'text-[#4D4637]' : i === currentStageIndex ? 'text-[#1A3C5E] font-bold' : 'text-[#D0C5B2]'">
          <span>{{ stage.label }}</span>
          <svg v-if="i < currentStageIndex" class="w-4 h-4 text-[#C9A84C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else-if="i === currentStageIndex" class="w-4 h-4 text-[#C9A84C] animate-spin shrink-0" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
          </svg>
          <span v-else class="w-4 h-4 rounded-full border border-[#D0C5B2] shrink-0"></span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.fade-stage-enter-active, .fade-stage-leave-active { transition: opacity 0.3s ease; }
.fade-stage-enter-from, .fade-stage-leave-to { opacity: 0; }
</style>