<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

// Active trip data
const activeTrip = {
  title: 'الأقصر: مدينة المائة باب',
  subtitle: 'استمتع بسحر التاريخ في قلب صعيد مصر.',
  progress: 43,
  todayAgenda: [
    { title: 'زيارة معبد الكرنك', time: '10:00 صباحاً - جولة إرشادية' },
    { title: 'عشاء نيلي (فلوكة)', time: '07:00 مساءً - مطعم مرسى النيل' }
  ]
}

// Upcoming trips
const upcomingTrips = [
  {
    id: 1,
    title: 'القاهرة: أسرار الأهرامات',
    date: '2 نوفمبر - 7 نوفمبر (5 ليالٍ)',
    daysUntil: 'في 24 يوم',
    tags: ['جولة ثقافية', 'إقامة كاملة'],
    progress: 20,
    people: 'شخصين',
    image: 'https://images.unsplash.com/photo-1507400492013-162704c8c9c9?w=522&q=80'
  },
  {
    id: 2,
    title: 'الإسكندرية: عروس البحر',
    date: '12 أكتوبر - 15 أكتوبر (3 ليالٍ)',
    daysUntil: 'في 15 يوم',
    tags: ['أنشطة بحرية', 'فندق 5 نجوم'],
    progress: 65,
    people: '4 أشخاص',
    image: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=522&q=80'
  }
]

// Wishlist
const wishlist = [
  { title: 'مرسى مطروح', subtitle: 'شواطئ فيروزية', price: '8,500 ج.م', image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=64&q=80' },
  { title: 'واحة سيوة', subtitle: 'مغامرة صحراوية', price: '12,000 ج.م', image: 'https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?w=64&q=80' },
  { title: 'الجونة', subtitle: 'استجمام فاخر', price: '15,500 ج.م', image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=64&q=80' },
  { title: 'شرم الشيخ', subtitle: 'غوص وشعب مرجانية', price: '10,200 ج.م', image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=64&q=80' }
]

// Sidebar navigation
const sidebarLinks = [
  { label: 'رحلاتي', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6', path: '/TripHistory', active: true, badge: null },
  { label: 'قائمة الأمنيات', icon: 'M5 5h14v14H5V5z', path: '/user-dashboard', active: false, badge: 4},
  { label: 'مركز المساعدة', icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z', path: '/Help', active: false, badge: null },
  { label: 'إعدادات', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z', path: '/Settings', active: false, badge: null }
]

const navigateTo = (route) => {
  router.push(route)
}

const goBack = () => {
  router.back()
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">
    <Navbar />

    <div class="flex pt-18">

      <!-- Main Content -->
      <div class="flex-1 min-w-0 p-4 md:p-6 lg:p-8">
        <div class="max-w-270 mx-auto">

          <!-- Top Header -->
          <div class="flex items-center justify-between mb-6">
            <button 
              @click="goBack"
              class="w-10 h-10 md:w-12 md:h-12 bg-[#F5F2E8] border border-[#C9A84C] rounded-full flex items-center justify-center hover:bg-[#C9A84C]/10 transition-colors shrink-0"
            >
              <svg class="w-4 h-4 md:w-5 md:h-5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>
            <div class="text-right flex-1 mr-4">
              <h1 class="text-xl md:text-2xl lg:text-3xl font-bold text-[#1A1C1B]">رحلاتي</h1>
              
              <p class="text-xs md:text-sm text-[#7E7665]">أهلاً بك مجدداً، استكشف تفاصيل مغامراتك القادمة.</p>
            </div>
          </div>

          <!-- Active Trip Banner -->
          <div class="relative bg-linear-to-l from-[#1A3C5E] to-[#2A6090] rounded-2xl p-5 md:p-6 lg:p-8 mb-6 overflow-hidden">
            <!-- Decorative pattern -->
            <div class="absolute top-0 right-0 w-20 h-20 opacity-10">
              <svg class="w-full h-full text-white" fill="currentColor" viewBox="0 0 100 100">
                <path d="M50 0L61.8 38.2L100 50L61.8 61.8L50 100L38.2 61.8L0 50L38.2 38.2Z"/>
              </svg>
            </div>

            <div class="relative z-10 flex flex-col lg:flex-row gap-4 lg:gap-6">
              <!-- Left: Trip info -->
              <div class="flex-1">
                <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm text-white text-xs md:text-sm px-3 py-1 rounded-full mb-2">
                  <span class="w-1.5 h-1.5 bg-[#C9A84C] rounded-full"></span>
                  أنت الآن في رحلة!
                </div>
                <h2 class="text-xl md:text-2xl lg:text-3xl font-semibold text-[#C9A84C] mb-1">{{ activeTrip.title }}</h2>
                <p class="text-white/80 text-sm md:text-base mb-3">{{ activeTrip.subtitle }}</p>
                
                <!-- Progress -->
                <div class="max-w-xs">
                  <div class="flex justify-between text-white text-xs md:text-sm mb-1">
                    <span>{{ activeTrip.progress }}%</span>
                    <span>تقدم الرحلة</span>
                  </div>
                  <div class="w-full h-1.5 bg-white/20 rounded-full overflow-hidden">
                    <div class="h-full bg-[#C9A84C] rounded-full transition-all" :style="{ width: activeTrip.progress + '%' }"></div>
                  </div>
                </div>
              </div>

              <!-- Right: Today's Agenda -->
              <div class="lg:w-64 xl:w-72 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-3 md:p-4">
                <h3 class="text-white text-base md:text-lg font-semibold mb-2 flex items-center gap-2">
                  أجنحة اليوم
                  <svg class="w-4 h-4 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                  </svg>
                </h3>
                <div class="space-y-2">
                  <div v-for="(item, index) in activeTrip.todayAgenda" :key="index" class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 bg-[#C9A84C] rounded-full shrink-0 mt-1.5"></span>
                    <div>
                      <p class="text-white text-xs md:text-sm font-medium">{{ item.title }}</p>
                      <p class="text-white/60 text-[10px] md:text-xs">{{ item.time }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Upcoming Trips -->
          <div class="mb-6">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-1 h-6 bg-[#C9A84C] rounded-full"></div>
              <h2 class="text-xl md:text-2xl font-semibold text-[#1A1C1B]">الرحلات القادمة</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="trip in upcomingTrips" :key="trip.id"
                class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
                @click="navigateTo('/TripDetail')"
              >
                <div class="relative h-40 md:h-48">
                  <img :src="trip.image" :alt="trip.title" class="w-full h-full object-cover">
                  <span class="absolute top-3 right-3 bg-white/90 backdrop-blur-sm px-2.5 py-0.5 rounded-lg text-xs md:text-sm text-[#1A1C1B]">
                    {{ trip.daysUntil }}
                  </span>
                </div>
                <div class="p-3 md:p-4">
                  <h3 class="text-base md:text-lg font-semibold text-[#1A1C1B] mb-0.5">{{ trip.title }}</h3>
                  <p class="text-xs md:text-sm text-[#7E7665] mb-2">{{ trip.date }}</p>
                  
                  <div class="flex flex-wrap gap-1.5 mb-2">
                    <span v-for="tag in trip.tags" :key="tag"
                      class="bg-[#EEEEEC] text-[#1A1C1B] text-[10px] md:text-xs px-2.5 py-0.5 rounded-full flex items-center gap-1">
                      {{ tag }}
                      <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                        <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
                      </svg>
                    </span>
                  </div>

                  <div class="border-t border-[#D0C5B2] pt-2 flex items-center justify-between">
                    <div class="flex items-center gap-1.5">
                      <span class="text-xs md:text-sm font-medium text-[#1A1C1B]">{{ trip.people }}</span>
                      <svg class="w-3.5 h-2.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
                      </svg>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <span class="text-[9px] md:text-xs text-[#7E7665]">اكتمال الميزانية</span>
                      <span class="text-[9px] md:text-xs font-semibold text-[#1A1C1B]">{{ trip.progress }}%</span>
                    </div>
                  </div>
                  <div class="w-full h-1 bg-[#EEEEEC] rounded-full overflow-hidden mt-1">
                    <div class="h-full bg-[#C9A84C] rounded-full transition-all" :style="{ width: trip.progress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Wishlist -->
          <div>
            <div class="flex items-center gap-3 mb-3">
              <div class="w-1 h-6 bg-[#C9A84C] rounded-full"></div>
              <h2 class="text-xl md:text-2xl font-semibold text-[#1A1C1B]">قائمة الأمنيات</h2>
              <span class="bg-[#C9A84C] text-[#503D00] text-xs font-bold px-2 py-0.5 rounded-full">4</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              <div v-for="item in wishlist" :key="item.title"
                class="bg-white border border-[#D0C5B2] rounded-xl p-3 flex items-center gap-3 hover:shadow-md transition-shadow cursor-pointer"
                @click="navigateTo('/Wishlist')"
              >
                <div class="flex-1 min-w-0">
                  <h4 class="font-semibold text-[#1A1C1B] text-sm md:text-base truncate">{{ item.title }}</h4>
                  <p class="text-[10px] md:text-xs text-[#7E7665] truncate">{{ item.subtitle }}</p>
                  <p class="text-xs md:text-sm font-semibold text-[#C9A84C] mt-0.5">{{ item.price }}</p>
                </div>
                <img :src="item.image" :alt="item.title" class="w-12 h-12 md:w-14 md:h-14 rounded-lg object-cover shrink-0">
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Sidebar -->
      <div class="hidden xl:block w-65 shrink-0 bg-[#F4F4F2] border-l border-[#D0C5B2] min-h-[calc(100vh-72px)] sticky top-18 h-[calc(100vh-72px)] overflow-y-auto">
        <div class="p-5 flex flex-col h-full">

          <!-- User Profile -->
          <div class="border-b border-[#D0C5B2] pb-5 mb-4 text-center">
            <div class="relative w-16 h-16 mx-auto mb-2">
              <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&q=80" 
                alt="Ahmed Mohamed" 
                class="w-16 h-16 rounded-full border-2 border-[#C9A84C] object-cover">
              <div class="absolute bottom-0 left-0 w-3.5 h-3.5 bg-[#C9A84C] border-2 border-[#F9F9F7] rounded-full"></div>
            </div>
            <h3 class="text-lg font-semibold text-[#1A1C1B]">أحمد محمد</h3>
            <p class="text-xs text-[#7E7665]">المسافر الدائم</p>
          </div>

          <!-- Navigation Links -->
          <nav class="flex-1 space-y-0.5">
            <button v-for="link in sidebarLinks" :key="link.label"
              @click="navigateTo(link.path)"
              :class="link.active ? 'bg-[#C9A84C] text-[#503D00]' : 'text-[#7E7665] hover:bg-[#C9A84C]/10'"
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-colors text-right"
            >
              <svg class="w-4 h-4 shrink-0" :class="link.active ? 'text-[#503D00]' : 'text-[#7E7665]'" fill="currentColor" viewBox="0 0 20 20">
                <path :d="link.icon" fill-rule="evenodd" clip-rule="evenodd"/>
              </svg>
              <span class="text-sm font-medium flex-1">{{ link.label }}</span>
              <span v-if="link.badge" class="bg-[#C9A84C] text-[#503D00] text-xs font-bold px-1.5 py-0.5 rounded-full min-w-5 text-center flex items-center gap-1">
                {{ link.badge }}
                <span class="text-[10px]">❤️</span>
              </span>
            </button>
          </nav>

          <!-- Plan New Trip Button -->
          <button @click="navigateTo('/ai-trip-planner')" 
            class="w-full bg-[#755B00] hover:bg-[#5C4800] text-white py-3 rounded-xl font-medium transition-colors text-sm">
            خطط رحلة جديدة
          </button>

          <!-- Footer Links -->
            <button @click="navigateTo('/chat')" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right">
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              </svg>
              <span class="text-sm font-medium">اتكلم مع الذكاء الاصطناعي</span>
            </button>
          </div>

        </div>
      </div>
    </div>
</template>