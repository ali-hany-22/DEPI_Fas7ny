<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

const planningMode = ref('manual') // 'manual' | 'ai'
const goToAiPlanner = () => {
  planningMode.value = 'ai'
  router.push('/ai-trip-planner')
}

const departureDate = ref('02/24/2024')
const adults = ref(2)
const children = ref(0)

const hotel = ref(true)
const transport = ref(true)
const activity1 = ref(false)
const activity2 = ref(false)

const hotelPrice = 4200
const transportPrice = 1100
const activity1Price = 350
const activity2Price = 850
const discount = 350

const total = computed(() => {
  let sum = 0
  if (hotel.value) sum += hotelPrice
  if (transport.value) sum += transportPrice
  if (activity1.value) sum += activity1Price
  if (activity2.value) sum += activity2Price
  sum -= discount
  return sum
})
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8]">
    <Navbar />

    <div class="max-w-6xl mx-auto px-4 md:px-8 pt-24 pb-16">

      <!-- Breadcrumb -->
      <div class="flex items-center gap-2 text-sm text-gray-400 mb-4 justify-end">
        <span class="text-[#C9A84C] font-medium">حجز رحلة مشابهة</span>
        <span>›</span>
        <span>ألبوم سيوة</span>
        <span>›</span>
        <span>مجتمع فسحني</span>
        <span>›</span>
        <span>الرئيسية</span>
      </div>

      <h1 class="text-3xl font-bold text-[#1A3C5E] mb-4 text-center">احجز رحلة مشابهة لرحلة سيوة</h1>

      <!-- Planning mode switcher -->
      <div class="flex justify-center mb-8">
        <div class="inline-flex items-center bg-white border border-[#D0C5B2] rounded-full p-1.5 shadow-sm">
          <button @click="planningMode = 'manual'"
            :class="planningMode === 'manual'
              ? 'bg-[#1A3C5E] text-white shadow'
              : 'text-[#4D4637] hover:text-[#1A3C5E]'"
            class="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
            حجز يدوي
          </button>
          <button @click="goToAiPlanner"
            :class="planningMode === 'ai'
              ? 'bg-linear-to-l from-[#C9A84C] to-[#dcbf6d] text-white shadow'
              : 'text-[#C9A84C] hover:bg-[#C9A84C]/10'"
            class="flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold transition-colors">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            خطط بالذكاء الاصطناعي
            <span class="text-[9px] bg-white/25 px-1.5 py-0.5 rounded-full font-bold">AI</span>
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

        <!-- Left: Booking Summary -->
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 order-2 lg:order-1">
          <h2 class="text-lg font-bold text-[#1A3C5E] mb-5 text-center">ملخص الحجز</h2>

          <!-- Date -->
          <div class="mb-4">
            <label class="text-xs text-gray-400 block mb-1 text-right">تاريخ المغادرة</label>
            <input v-model="departureDate" type="text"
              class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm text-right focus:outline-none focus:border-[#C9A84C]" />
          </div>

          <!-- Travelers -->
          <div class="grid grid-cols-2 gap-3 mb-5">
            <div>
              <label class="text-xs text-gray-400 block mb-1 text-right">أطفال</label>
              <select v-model="children" class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-[#C9A84C] text-right">
                <option v-for="n in 5" :key="n-1" :value="n-1">{{ n-1 }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-gray-400 block mb-1 text-right">بالغين</label>
              <select v-model="adults" class="w-full border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-[#C9A84C] text-right">
                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
              </select>
            </div>
          </div>

          <!-- Price breakdown -->
          <div class="space-y-2 mb-4 text-sm border-t border-gray-100 pt-4">
            <div v-if="hotel" class="flex justify-between">
              <span class="text-gray-600">4,200 ج.م</span>
              <span class="text-gray-400">الإقامة (6 ليالي)</span>
            </div>
            <div v-if="transport" class="flex justify-between">
              <span class="text-gray-600">1,100 ج.م</span>
              <span class="text-gray-400">الانتقالات</span>
            </div>
            <div v-if="activity1 || activity2" class="flex justify-between">
              <span class="text-gray-600">{{ (activity1 ? 350 : 0) + (activity2 ? 850 : 0) }} ج.م</span>
              <span class="text-gray-400">الأنشطة</span>
            </div>
            <div class="flex justify-between text-[#AA3436]">
              <span>350- ج.م</span>
              <span>خصم مجتمع Rehla</span>
            </div>
          </div>

          <!-- Total -->
          <div class="flex justify-between items-center border-t border-gray-100 pt-4 mb-5">
            <span class="text-2xl font-bold text-[#C9A84C]">{{ total.toLocaleString() }} ج.م</span>
            <span class="text-lg font-bold text-[#1A3C5E]">الإجمالي</span>
          </div>

          <!-- CTA -->
          <button @click="router.push('/payment')"
            class="w-full bg-[#C9A84C] hover:bg-[#b8963f] text-white py-3 rounded-lg font-semibold transition-colors text-sm flex items-center justify-center gap-2">
            تأكيد ومتابعة للدفع
            <svg class="w-4 h-4 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
          <p class="text-center text-xs text-gray-400 mt-2">إلغاء مجاني حتى 48 ساعة قبل الموعد</p>

          <!-- AI tip -->
          <div class="bg-[#B4D4FE] rounded-xl p-4 mt-4">
            <div class="flex items-center gap-1 justify-end mb-2">
              <span class="text-xs font-semibold text-[#3C5C7F]">نصيحة ذكية</span>
              <img src="https://img.icons8.com/ios-filled/50/3C5C7F/sparkling--v1.png" class="w-3.5 h-3.5" alt="" />
            </div>
            <p class="text-xs text-[#3C5C7F] text-right leading-relaxed">بناءً على تاريخ رحلتك، سيكون الطقس في سيوة مثالياً للرحلات الليلية في الصحراء. ننصح بإحضار ملابس ثقيلة للمساء.</p>
          </div>

          <!-- Nudge toward AI planner -->
          <button @click="goToAiPlanner"
            class="w-full flex items-center justify-center gap-2 border border-[#C9A84C]/40 text-[#C9A84C] text-xs font-semibold py-2.5 rounded-lg mt-3 hover:bg-[#C9A84C]/5 transition-colors">
            عايز تفاصيل يومية كاملة؟ جرّب التخطيط بالذكاء الاصطناعي
            <svg class="w-3 h-3 -scale-x-100" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>

        <!-- Right: Trip Options -->
        <div class="lg:col-span-2 space-y-4 order-1 lg:order-2">

          <!-- AI Recommended trip card -->
          <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <div class="flex items-start gap-4">
              <img src="https://i.pinimg.com/1200x/7e/88/f4/7e88f48d4f07230fc4bdf7653334f450.jpg"
                class="w-32 h-24 object-cover rounded-xl shrink-0" alt="سيوة" />
              <div class="flex-1 text-right">
                <span class="inline-block bg-[#C9A84C] text-white text-xs px-2.5 py-0.5 rounded-full mb-2">AI RECOMMENDED</span>
                <h3 class="font-bold text-[#1A3C5E] text-lg mb-1">سيوة: سحر الواحة المصرية</h3>
                <p class="text-gray-500 text-sm leading-relaxed mb-3">استمتع بتجربة فريدة في قلب الصحراء الغربية. 7 أيام من الاسترخاء، الاستكشاف، والمغامرة في واحة سيوة التاريخية.</p>
                <div class="flex items-center gap-4 justify-end text-sm text-gray-400">
                  <span>واحة سيوة، مصر</span>
                  <span>7 أيام</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Hotels -->
          <div>
            <h3 class="font-bold text-[#1A3C5E] mb-3 flex items-center justify-end gap-2">
              الإقامة (الفنادق)
              <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </h3>
            <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <!-- Toggle -->
                  <button @click="hotel = !hotel"
                    :class="hotel ? 'bg-[#C9A84C]' : 'bg-gray-200'"
                    class="relative w-11 h-6 rounded-full transition-colors shrink-0">
                    <span :class="hotel ? 'translate-x-0 right-1' : 'translate-x-0 left-1'"
                      class="absolute top-1 w-4 h-4 bg-white rounded-full transition-all"
                      :style="hotel ? 'right: 4px' : 'left: 4px'"></span>
                  </button>
                  <div class="text-right">
                    <span class="text-sm text-gray-400">السعر</span>
                    <p class="text-[#C9A84C] font-semibold text-sm">4,200 ج.م</p>
                  </div>
                </div>
                <div class="text-right flex items-center gap-3">
                  <div>
                    <p class="font-semibold text-[#1A3C5E] text-sm">فندق جعفر (Jafar Hotel)</p>
                    <p class="text-xs text-gray-400 mt-0.5">غرفة مزدوجة - إطلالة على الجبل</p>
                    <p class="text-xs text-[#C9A84C]">6 ليالي (24 فبراير - 2 مارس)</p>
                  </div>
                  <img src="https://i.pinimg.com/1200x/df/33/0b/df330b815956e31ee4f8fa3a7f3ba9dd.jpg"
                    class="w-14 h-14 object-cover rounded-xl" alt="" />
                </div>
              </div>
            </div>
          </div>

          <!-- Transport -->
          <div>
            <h3 class="font-bold text-[#1A3C5E] mb-3 flex items-center justify-end gap-2">
              الانتقالات
              <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
            </h3>
            <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <button @click="transport = !transport"
                    :class="transport ? 'bg-[#C9A84C]' : 'bg-gray-200'"
                    class="relative w-11 h-6 rounded-full transition-colors shrink-0">
                    <span class="absolute top-1 w-4 h-4 bg-white rounded-full transition-all"
                      :style="transport ? 'right: 4px' : 'left: 4px'"></span>
                  </button>
                  <div class="text-right">
                    <span class="text-sm text-gray-400">السعر</span>
                    <p class="text-[#C9A84C] font-semibold text-sm">1,100 ج.م</p>
                  </div>
                </div>
                <div class="text-right flex items-center gap-3">
                  <div>
                    <p class="font-semibold text-[#1A3C5E] text-sm">حافلة سياحية خاصة (القاهرة ⇌ سيوة)</p>
                    <p class="text-xs text-gray-400 mt-0.5">مكيفة - مقاعد مريحة - واي فاي</p>
                    <p class="text-xs text-gray-400">انطلاق من ميدان التحرير</p>
                  </div>
                  <div class="w-14 h-14 bg-gray-100 rounded-xl flex items-center justify-center">
                    <svg class="w-8 h-8 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 17H5a2 2 0 01-2-2V9a2 2 0 012-2h11l4 4v4a2 2 0 01-2 2h-3m-6 0a2 2 0 100 4 2 2 0 000-4zm8 0a2 2 0 100 4 2 2 0 000-4z"/></svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Activities -->
          <div>
            <h3 class="font-bold text-[#1A3C5E] mb-3 flex items-center justify-end gap-2">
              الأنشطة والجولات
              <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/></svg>
            </h3>
            <div class="space-y-3">

              <!-- Activity 1 -->
              <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <button @click="activity1 = !activity1"
                      :class="activity1 ? 'bg-[#C9A84C]' : 'bg-gray-200'"
                      class="relative w-11 h-6 rounded-full transition-colors shrink-0">
                      <span class="absolute top-1 w-4 h-4 bg-white rounded-full transition-all"
                        :style="activity1 ? 'right: 4px' : 'left: 4px'"></span>
                    </button>
                    <div class="text-right">
                      <span class="text-sm text-gray-400">السعر</span>
                      <p class="text-[#C9A84C] font-semibold text-sm">350 ج.م</p>
                    </div>
                  </div>
                  <div class="text-right flex items-center gap-3">
                    <div>
                      <p class="font-semibold text-[#1A3C5E] text-sm">جولة قلعة شالي القديمة</p>
                      <p class="text-xs text-gray-400 mt-0.5">مع مرشد محلي - تذاكر الدخول شاملة</p>
                    </div>
                    <img src="https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=100&q=80"
                      class="w-14 h-14 object-cover rounded-xl" alt="" />
                  </div>
                </div>
              </div>

              <!-- Activity 2 -->
              <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <button @click="activity2 = !activity2"
                      :class="activity2 ? 'bg-[#C9A84C]' : 'bg-gray-200'"
                      class="relative w-11 h-6 rounded-full transition-colors shrink-0">
                      <span class="absolute top-1 w-4 h-4 bg-white rounded-full transition-all"
                        :style="activity2 ? 'right: 4px' : 'left: 4px'"></span>
                    </button>
                    <div class="text-right">
                      <span class="text-sm text-gray-400">السعر</span>
                      <p class="text-[#C9A84C] font-semibold text-sm">850 ج.م</p>
                    </div>
                  </div>
                  <div class="text-right flex items-center gap-3">
                    <div>
                      <p class="font-semibold text-[#1A3C5E] text-sm">زيارة عين كليوباترا وجبل الموتى</p>
                      <p class="text-xs text-gray-400 mt-0.5">شامل الانتقالات الداخلية والغداء</p>
                    </div>
                    <img src="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=100&q=80"
                      class="w-14 h-14 object-cover rounded-xl" alt="" />
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>