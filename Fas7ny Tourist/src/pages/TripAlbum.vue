<script setup>
import { ref } from 'vue'
import Navbar from '../components/Navbar.vue'

const message = ref('')
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">
    <Navbar />

    <!-- Hero Section -->
    <div class="relative w-full h-150 overflow-hidden">
      <!-- Background Image -->
      <div class="absolute inset-0">
        <img 
          src="https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=1440&q=80" 
          alt="Siwa Oasis"
          class="w-full h-full object-cover"
        />
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-linear-to-t from-black/80 via-black/30 to-transparent"></div>
      </div>

      <!-- Content -->
      <div class="relative h-full flex flex-col justify-end items-end px-16 pb-16">
        <div class="flex flex-col items-start mb-4">
          <h1 class="text-5xl font-bold text-white max-w-2xl text-right leading-15">
            أسبوع في واحة سيوة: رمال وسكون
          </h1>
        </div>

        <div class="flex items-center justify-between w-full">
          <!-- Book Button -->
          <button class="bg-[#755B00] hover:bg-[#5C4800] text-white px-8 py-4 rounded-xl flex items-center gap-2 transition-colors">
            <span>احجز الرحلة كاملة</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>

          <!-- Trip Info -->
          <div class="flex items-center gap-6 text-white">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-1">
                <span>٢.٤ ألف</span>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>
              <div class="flex items-center gap-1">
                <span>١٤ موقع</span>
                <svg class="w-4 h-5 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="flex items-center gap-1">
                <span>٧ أيام</span>
                <svg class="w-4.5 h-5 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                </svg>
              </div>
            </div>

            <div class="w-px h-4 bg-white/30"></div>

            <div class="flex items-center gap-2">
              <span class="font-semibold text-lg">مريم ناصر</span>
              <img 
                src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=40&q=80" 
                alt="Mariam Nasser"
                class="w-10 h-10 rounded-full border-2 border-[#755B00] object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-16 py-16 flex gap-16">
      
      <!-- Left Column: Timeline -->
      <div class="flex-1">
        <div class="flex items-center justify-between mb-8">
          <h2 class="text-3xl font-semibold text-[#755B00]">١٠ يوميات الرحلة</h2>
          <svg class="w-6 h-6 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
          </svg>
        </div>

        <div class="space-y-16">
          <!-- Day 1 -->
          <div class="relative pr-8">
            <!-- Timeline dot -->
            <div class="absolute right-0 top-1 w-6 h-6 bg-[#755B00] rounded-full border-4 border-white shadow-sm"></div>
            <!-- Timeline line -->
            <div class="absolute right-2.75 top-7 bottom-0 w-0.5 bg-[#E2E3E1]"></div>

            <h3 class="text-2xl font-semibold text-[#416084] mb-2">اليوم ١: الوصول والاسترخاء</h3>
            <p class="text-[#4D4637] leading-relaxed mb-4 max-w-3xl">
              وصلنا إلى واحة سيوة بعد رحلة طويلة ولكنها ممتعة. بدأنا يومنا الأول بهدوء، حيث توجهنا للفندق وقمنا بجولة سريعة في شالي سيوة القديمة عند الغروب. الهدوء هنا لا يوصف.
            </p>

            <!-- Images -->
            <div class="grid grid-cols-2 gap-0 rounded-xl overflow-hidden mb-4">
              <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?w=437&q=80" alt="Hotel Siwa" class="w-full h-64 object-cover relative">
              <div class="relative">
                <img src="https://images.unsplash.com/photo-1601142634808-38923eb7c560?w=437&q=80" alt="Shali Fortress" class="w-full h-64 object-cover">
                <span class="absolute bottom-4 right-4 bg-black/50 backdrop-blur-sm text-white text-sm px-3 py-1 rounded-lg flex items-center gap-1">
                  قلعة شالي
                  <svg class="w-3 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z" clip-rule="evenodd"/>
                  </svg>
                </span>
              </div>
            </div>

            <!-- Stop Card -->
            <div class="bg-white border border-[#D0C5B2] rounded-xl p-4 flex items-center justify-between">
              <button class="border border-[#755B00] text-[#755B00] px-6 py-2 rounded-lg flex items-center gap-1 hover:bg-[#755B00] hover:text-white transition-colors">
                أضف للخطة
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-center gap-4">
                <div class="text-right">
                  <h4 class="text-lg text-[#1A1C1B]">فندق جعفر</h4>
                  <p class="text-sm text-[#4D4637]">تقييم: ٤.٨/٥ • طراز سيوة التقليدي</p>
                </div>
                <div class="w-16 h-16 bg-[#F9F9F7] rounded-lg overflow-hidden">
                  <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?w=64&q=80" alt="Hotel" class="w-full h-full object-cover">
                </div>
              </div>
            </div>
          </div>

          <!-- Day 2 -->
          <div class="relative pr-8">
            <div class="absolute right-0 top-1 w-6 h-6 bg-[#C9A84C] rounded-full border-4 border-white shadow-sm"></div>
            <div class="absolute right-2.75 top-7 bottom-0 w-0.5 bg-[#E2E3E1]"></div>

            <h3 class="text-2xl font-semibold text-[#416084] mb-2">اليوم ٢: عيون المياه وجزيرة فطناس</h3>
            <p class="text-[#4D4637] leading-relaxed mb-4 max-w-201.5">
              انطلقنا مبكراً لزيارة عين كليوباترا، ثم قضينا فترة بعد الظهر في جزيرة فطناس. الاستمتاع بكوب من الشاي السيوي أثناء مشاهدة الشمس تغوص في البحيرة كان لحظة لا تنسى.
            </p>

            <!-- 3 Images -->
            <div class="grid grid-cols-3 gap-0 rounded-xl overflow-hidden mb-4 h-48">
              <img src="https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=286&q=80" alt="Siwa Tea" class="w-full h-full object-cover">
              <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=286&q=80" alt="Fatnas Island" class="w-full h-full object-cover">
              <img src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=286&q=80" alt="Cleopatra's Bath" class="w-full h-full object-cover">
            </div>

            <!-- Stop Card -->
            <div class="bg-white border border-[#D0C5B2] rounded-xl p-4 flex items-center justify-between">
              <button class="border border-[#755B00] text-[#755B00] px-6 py-2 rounded-lg flex items-center gap-1 hover:bg-[#755B00] hover:text-white transition-colors">
                أضف للخطة
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
                </svg>
              </button>
              <div class="flex items-center gap-4">
                <div class="text-right">
                  <h4 class="text-lg text-[#1A1C1B]">عين كليوباترا</h4>
                  <p class="text-sm text-[#4D4637]">موقع تاريخي • سباحة طبيعية</p>
                </div>
                <div class="w-16 h-16 bg-[#F9F9F7] rounded-lg overflow-hidden">
                  <img src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=64&q=80" alt="Cleopatra's Bath" class="w-full h-full object-cover">
                </div>
              </div>
            </div>
          </div>

          <!-- Day 3 (Placeholder) -->
          <div class="relative pr-8">
            <div class="absolute right-0 top-1 w-6 h-6 bg-[#D0C5B2] rounded-full border-4 border-white shadow-sm"></div>

            <h3 class="text-2xl font-semibold text-[#4D4637]/60 mb-1">اليوم ٣: استكشاف بحيرات الملح</h3>
            <p class="text-[#4D4637]/50">استكشاف بحيرات الملح، رحلة السفاري الكبرى، وجبل الموتى.</p>
          </div>
        </div>
      </div>

      <!-- Right Column: Sidebar -->
      <div class="w-81.5 shrink-0 space-y-8">
        <!-- Trip Summary -->
        <div class="bg-white border border-[#D0C5B2] rounded-xl p-6">
          <h3 class="text-xl text-[#755B00] mb-4">ملخص الرحلة</h3>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="bg-[#EEEEEC] text-[#1A1C1B] text-sm font-semibold px-3 py-1 rounded-full">اقتصادي</span>
              <span class="text-[#4D4637]">الميزانية</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-[#1A1C1B] text-sm font-semibold">شتاء ٢٠٢٥</span>
              <span class="text-[#4D4637]">التوقيت</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-[#1A1C1B] text-sm font-semibold">استجمام / مغامرة</span>
              <span class="text-[#4D4637]">نوع الرحلة</span>
            </div>
          </div>

          <hr class="my-4 border-[#D0C5B2]" />

          <p class="text-[#4D4637] leading-relaxed">
            تجربة فريدة من نوعها لمحبي الهدوء والابتعاد عن صخب المدينة. سيوة عالم آخر يسكنه الصمت والجمال الطبيعي.
          </p>
        </div>

        <!-- Map Widget -->
        <div class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden">
          <div class="bg-[#EEEEEC] p-4 flex items-center justify-between">
            <svg class="w-4.5 h-4.5 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
            </svg>
            <h4 class="text-lg text-[#416084]">خريطة الرحلة</h4>
          </div>
          <div class="h-64 bg-[#E8E8E6] relative flex items-center justify-center">
            <div class="text-center">
              <svg class="w-8 h-10 text-[#755B00] mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
              </svg>
              <span class="bg-white px-4 py-1 rounded-lg shadow-sm text-sm font-medium">واحة سيوة</span>
            </div>
          </div>
        </div>

        <!-- Book This Trip -->
        <div class="bg-[#FDF8EC] border-2 border-[#755B00]/30 rounded-2xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-xl font-bold text-[#755B00]">احجز نفس الرحلة دي</h4>
            <svg class="w-6 h-6 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
            </svg>
          </div>
          <p class="text-[#4D4637] mb-4">كل الفنادق، المواصلات، والتذاكر اللي مريم استخدمتها في مكان واحد.</p>
          <div class="mb-4">
            <p class="text-sm text-[#4D4637]">تبدأ من</p>
            <div class="flex items-baseline">
              <span class="text-3xl font-semibold text-[#755B00]">١٢,٤٠٠ ج.م</span>
              <span class="text-[#4D4637] mr-2">/ للفرد</span>
            </div>
          </div>
          <button class="w-full bg-[#755B00] text-white py-4 rounded-xl font-semibold hover:bg-[#5C4800] transition-colors flex items-center justify-center gap-1 mb-2">
            احجز الرحلة كاملة
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
            </svg>
          </button>
          <button class="w-full text-[#755B00] font-semibold py-2 hover:underline">
            عدل في الخطة الأول
          </button>
        </div>

        <!-- Travelers -->
        <div class="bg-white border border-[#D0C5B2] rounded-xl p-6">
          <h4 class="text-lg text-[#416084] mb-4">المسافرون</h4>
          <div class="flex items-center -space-x-2">
            <div class="w-12 h-12 rounded-full border-2 border-white bg-[#EEEEEC] flex items-center justify-center text-sm font-semibold text-[#4D4637]">+٢</div>
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=48&q=80" alt="User" class="w-12 h-12 rounded-full border-2 border-white object-cover">
            <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=48&q=80" alt="User" class="w-12 h-12 rounded-full border-2 border-white object-cover">
            <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=48&q=80" alt="User" class="w-12 h-12 rounded-full border-2 border-white object-cover">
          </div>
        </div>

        <!-- Suggested Gear -->
        <div class="bg-white border border-[#D0C5B2] rounded-xl p-6">
          <h4 class="text-lg text-[#416084] mb-4">معدات مشتركة</h4>
          <div class="flex flex-wrap gap-2">
            <span class="bg-[#F4F4F2] px-3 py-2 rounded-lg text-sm flex items-center gap-1">
              كريم شمس
              <svg class="w-4 h-4 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
            </span>
            <span class="bg-[#F4F4F2] px-3 py-2 rounded-lg text-sm flex items-center gap-1">
              نظارة شمس
              <svg class="w-4 h-4 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
            </span>
            <span class="bg-[#F4F4F2] px-3 py-2 rounded-lg text-sm flex items-center gap-1">
              حذاء مريح
              <svg class="w-3 h-4 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
            </span>
            <span class="bg-[#F4F4F2] px-3 py-2 rounded-lg text-sm flex items-center gap-1">
              مطرة مياه
              <svg class="w-3 h-4 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
            </span>
          </div>
        </div>

        <!-- Ask Creator -->
        <div class="bg-[#755B00]/5 border border-[#755B00]/20 rounded-xl p-6">
          <h4 class="text-lg text-[#755B00] mb-4">سؤال للمسافر</h4>
          <div class="space-y-4">
            <textarea 
              v-model="message"
              placeholder="اسأل مريم عن تفاصيل الرحلة..."
              class="w-full px-4 py-4 border border-[#D0C5B2] rounded-xl resize-none text-right min-h-26.5 focus:outline-none focus:border-[#755B00]"
            ></textarea>
            <button class="w-full bg-[#755B00] text-white py-2 rounded-lg hover:bg-[#5C4800] transition-colors">
              إرسال السؤال
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>