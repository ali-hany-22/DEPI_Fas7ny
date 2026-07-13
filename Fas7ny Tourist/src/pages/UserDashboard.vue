<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

const userStats = {
  posts: 4,
  totalLikes: 123,
  totalViews: 320,
  name: 'أحمد محمد',
  title: 'مستكشف مصري عمري'
}
const statsCards = [
  {
    label: 'إجمالي المشاهدات',
    value: '٣٢٠',
    icon: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z'
  },
  {
    label: 'إجمالي الإعجابات',
    value: '١٢٣',
    icon: 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z'
  },
  {
    label: 'مشاورات',
    value: '٤',
    icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z'
  }
]

const tabs = ref([
  { label: 'الكل', value: 'all', active: false },
  { label: 'منشورات', value: 'posts', active: false },
  { label: 'قصص (Stories)', value: 'stories', active: false },
  { label: 'محفوظات', value: 'saved', active: true }
])

// Posts grid
const posts = [
  {
    id: 1,
    likes: 120,
    comments: 45,
    image:
      'https://images.unsplash.com/photo-1507400492013-162704c8c9c9?w=344&q=80'
  },
  {
    id: 2,
    likes: 85,
    comments: 32,
    image:
      'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=344&q=80'
  },
  {
    id: 3,
    likes: 65,
    comments: 28,
    image:
      'https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=344&q=80'
  },
  {
    id: 4,
    likes: 50,
    comments: 18,
    image:
      'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=344&q=80'
  }
]

// Navigation functions
const navigateTo = (route) => {
  router.push(route)
}

const goBack = () => {
  router.back()
}

const toggleTab = (value) => {
  tabs.value.forEach(tab => {
    tab.active = tab.value === value
  })
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">
    <Navbar />

    <div class="flex pt-18">

      <!-- Main Content -->
      <div class="flex-1 min-w-0 p-4 md:p-6 lg:p-8">
        <div class="max-w-266 mx-auto">

          <!-- Page Header -->
          <div class="flex items-center justify-between mb-6">
            <button 
              @click="navigateTo('/AddPost')"
              class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#503D00] px-4 md:px-6 py-3 md:py-4 rounded-xl font-bold text-sm md:text-base flex items-center gap-2 transition-colors"
            >
              <span>منشور جديد</span>
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
              </svg>
            </button>
            <div class="text-right flex-1 mr-4">
              <h1 class="text-xl md:text-2xl lg:text-3xl font-bold text-[#1A1C1B]">منشورات على فسحتي</h1>
              <p class="text-xs md:text-sm text-[#7E7665]">
                {{ userStats.posts }} منشورات · {{ userStats.totalLikes }} إعجاب إجمالي · {{ userStats.totalViews }} مشاهدة
              </p>
            </div>
            <button 
              @click="goBack"
              class="w-10 h-10 md:w-12 md:h-12 bg-[#F5F2E8] border border-[#C9A84C] rounded-full flex items-center justify-center hover:bg-[#C9A84C]/10 transition-colors shrink-0"
            >
              <svg class="w-4 h-4 md:w-5 md:h-5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>

          <!-- Stats Overview -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 md:gap-4 mb-6">
            <div v-for="(stat, index) in statsCards" :key="index"
              class="bg-white border border-[#D0C5B2] rounded-xl p-4 flex items-center gap-4"
              :class="index === 0 ? 'sm:col-span-1' : ''"
            >
              <div class="w-10 h-10 rounded-lg overflow-hidden bg-[#F9F9F7] flex items-center justify-center shrink-0">
                <svg class="w-5 h-5 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                  <path :d="stat.icon" fill-rule="evenodd" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="text-right">
                <p class="text-xs md:text-sm text-[#7E7665]">{{ stat.label }}</p>
                <p class="text-lg md:text-2xl font-semibold text-[#1A1C1B]">{{ stat.value }}</p>
              </div>
            </div>
          </div>

          <!-- Tabs -->
          <div class="border-b border-[#D0C5B2] mb-6">
            <div class="flex gap-4 md:gap-6">
<button
  v-for="tab in tabs"
  :key="tab.value"
  @click="toggleTab(tab.value)"
  :class="
    tab.active
      ? 'border-b-2 border-[#755B00] text-[#755B00] font-bold'
      : 'text-[#7E7665] hover:text-[#755B00]'
  "
  class="pb-3 md:pb-4 text-sm md:text-base transition-colors"
>
  {{ tab.label }}
</button>
            </div>
          </div>

          <!-- Posts Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
            <div v-for="post in posts" :key="post.id"
              class="relative group rounded-xl overflow-hidden cursor-pointer"
              @click="navigateTo('/PostDetail')"
            >
              <img :src="post.image" :alt="'Post ' + post.id" 
                class="w-full h-56 md:h-64 lg:h-72 object-cover">
              <div class="absolute top-2 right-2 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></div>
              
              <!-- Overlay on hover -->
              <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4 md:gap-6">
                <div class="flex items-center gap-1.5 text-white">
                  <span class="text-sm md:text-base">{{ post.likes }}</span>
                  <svg class="w-4 h-3 md:w-5 md:h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 3.5L12.5 8.5L18 9.2L14 13.1L15.1 18.5L10 15.8L4.9 18.5L6 13.1L2 9.2L7.5 8.5L10 3.5Z"/>
                  </svg>
                </div>
                <div class="flex items-center gap-1.5 text-white">
                  <span class="text-sm md:text-base">{{ post.comments }}</span>
                  <svg class="w-4 h-3.5 md:w-5 md:h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
                  </svg>
                </div>
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
            <h3 class="text-lg font-semibold text-[#1A1C1B]">{{ userStats.name }}</h3>
            <p class="text-xs text-[#7E7665]">{{ userStats.title }}</p>
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
          <button @click="navigateTo('/Explore')" 
            class="w-full bg-[#755B00] hover:bg-[#5C4800] text-white py-3 rounded-xl font-medium transition-colors text-sm">
            خطط رحلة جديدة
          </button>

          <!-- Footer Links -->
          <div class="border-t border-[#D0C5B2] pt-3 mt-3 space-y-0.5">
            <button @click="navigateTo('/Help')" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right">
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-sm font-medium">مركز المساعدة</span>
            </button>
            <button @click="navigateTo('/Settings')" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right">
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
              </svg>
              <span class="text-sm font-medium">إعدادات</span>
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>