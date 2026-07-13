<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)

// which mega-menu / dropdown is currently open: 'cities' | 'community' | 'profile' | null
const openMenu = ref(null)
const toggleMenu = (name) => {
  openMenu.value = openMenu.value === name ? null : name
}
const closeMenus = () => { openMenu.value = null }

const navLinks = [
  { label: 'استكشف', path: '/search', menu: 'community' },
  { label: 'المدن', path: '/search', menu: 'cities' },
  { label: 'فسحني', path: '/ai-trip-planner' },
  { label: 'رحلاتي', path: '/trip-history' },
  { label: 'تواصل معنا', path: '/help' },
]

const cityGroups = [
  {
    cities: ['الغردقة', 'شرم الشيخ', 'الإسكندرية'],
    tags: ['البحر الأحمر', 'سيناء والعقبة', 'البحر المتوسط'],
  },
  {
    cities: ['العين السخنة', 'القاهرة', 'الأقصر'],
    tags: ['بحر واسترخاء', 'الأهرامات والتاريخ', 'المعابد الفرعونية'],
  },
  {
    cities: ['أسوان', 'دهب', 'سيوة'],
    tags: ['النوبة والنيل', 'الواحة والصحراء', 'الغوص والهدوء'],
  },
]

// cities that have a full CityDetail.vue page (matches citiesData keys there)
// Fix the citiesWithDetailPage array - use exact names from citiesData
const citiesWithDetailPage = [
  'القاهرة', 
  'الإسكندرية', 
  'العين السخنة', 
  'الأقصر', 
  'الغردقة', 
  'أسوان', 
  'دهب', 
  'شرم الشيخ',
  'سيوة'
]
const goToCity = (city) => {
  if (citiesWithDetailPage.includes(city)) {
    router.push(`/city/${encodeURIComponent(city)}`)
  } else {
    router.push('/search')
  }
  closeMenus()
}

const services = [
  { name: 'الاقامة', detail: 'فنادق و شقق...', path: '/hotels', query: { type: 'accommodation' } },
  { name: 'المواصلات', detail: 'طيران وسيارات وقطارات...', path: '/transport' },
  { name: 'الطعام والترفيه', detail: 'مطاعم وكافيهات...', path: 'trip-album' },
  { name: 'المعالم والانشطة', detail: 'اثار شواطئ ومغامرات...', path: '/restaurants', query: { type: 'landmarks' } },
]

const communityHighlights = [
  { title: 'ال feed', detail: 'لحظات المسافرين', path: '/community' },
  { title: 'شارك لحظة', detail: 'ضيف صور رحلتك', path: '/community' },
  { title: 'الاكثر تفاعلا', detail: 'اشهر اللحظات هذا الاسبوع', path: '/community', query: { sort: 'trending' } },
]

const goTo = (item) => {
  router.push({ path: item.path, query: item.query })
  closeMenus()
}

const searchQuery = ref('')
const runSearch = () => {
  router.push({ path: '/search', query: searchQuery.value ? { q: searchQuery.value } : {} })
  closeMenus()
}

const notifications = [
  { text: 'مريم ناصر أعجبت برحلتك إلى سيوة', time: 'منذ ساعتين' },
  { text: 'تم تأكيد حجزك في فندق جعفر الصديق', time: 'أمس' },
  { text: 'عرض خاص على رحلات الغردقة هذا الأسبوع', time: 'منذ ٣ أيام' },
]

const profileLinks = [
  'لوحة التحكم',
  'رحلاتي',
  'مجتمع فسحني',
  'المفضلة',
  'تقييماتي',
  'الاعدادات',
]
</script>

<template>
  <nav class="fixed top-0 w-full z-50 bg-white border-b border-[#E8E4DC] shadow-[0_2px_12px_rgba(0,0,0,0.06)]" dir="rtl">
    <div class="max-w-360 mx-auto px-10 h-18 flex items-center justify-between">

      <!-- Logo -->
      <button @click="router.push('/home'); closeMenus()" class="flex items-center gap-2 shrink-0">
        <img src="https://img.icons8.com/ios/50/C9A84C/world-map.png" class="w-7 h-7" alt="logo" />
        <span class="text-xl font-bold text-[#1A3C5E]">فسحني</span>
      </button>

      <!-- Desktop Links -->
      <div class="hidden md:flex items-center gap-8 text-base">
        <div v-for="link in navLinks" :key="link.label" class="relative">
          <button
            @click="link.menu ? toggleMenu(link.menu) : (router.push(link.path), closeMenus())"
            :class="route.path === link.path
              ? 'text-[#1A3C5E] font-bold border-b-2 border-[#1A3C5E] pb-6 -mb-6'
              : 'text-[#4D4637] hover:text-[#1A3C5E]'"
            class="relative transition-colors flex items-center gap-1">
            <span v-if="link.label === 'فسحني'"
              class="absolute -top-2 -right-3.5 text-[8px] font-bold bg-[#FF7F50] text-white px-1.5 py-0.5 rounded-full leading-none">جديد</span>
            {{ link.label }}
            <svg v-if="link.menu" :class="openMenu === link.menu ? 'rotate-180' : ''"
              class="w-2.25 h-1.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>

          <!-- المدن Mega Menu -->
          <div v-if="link.menu === 'cities' && openMenu === 'cities'"
            class="fixed left-1/2 -translate-x-1/2 top-18 mt-2 w-187.5 bg-[#F4F4F2] rounded-2xl shadow-xl p-8 text-right z-50">
            <div class="flex items-center justify-between mb-6">
              <button class="text-sm text-[#4D4637] hover:text-[#755B00]">عرض الكل</button>
              <h3 class="text-xl font-bold text-[#C9A84C]">الوجهات المميزة</h3>
            </div>
            <div class="space-y-5">
              <div v-for="(group, gi) in cityGroups" :key="gi">
                <div class="flex flex-wrap justify-end gap-x-6 gap-y-1">
                  <button v-for="city in group.cities" :key="city"
                    @click="goToCity(city)"
                    class="text-lg font-semibold text-[#1A1C1B] hover:text-[#755B00] transition-colors">
                    {{ city }}
                  </button>
                </div>
                <div class="flex flex-wrap justify-end gap-x-5 gap-y-1 mt-1">
                  <span v-for="tag in group.tags" :key="tag" class="text-sm text-[#4D4637]/70">{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- استكشف: Services + Community Menu -->
          <div v-if="link.menu === 'community' && openMenu === 'community'"
            class="fixed left-1/2 -translate-x-1/2 top-18 mt-2 w-290 bg-[#F4F4F2] rounded-2xl shadow-xl p-8 z-50">
            <div class="grid grid-cols-2 gap-8">
              <!-- Services -->
              <div class="text-right">
                <h3 class="text-xl font-bold text-[#755B00] mb-5">الخدمات</h3>
                <div class="space-y-4">
                  <button v-for="s in services" :key="s.name" @click="goTo(s)"
                    class="block w-full text-right text-lg text-[#1A1C1B] hover:text-[#755B00] transition-colors">
                    {{ s.name }} <span class="text-[#4D4637]/60 text-base">({{ s.detail }})</span>
                  </button>
                </div>
              </div>
              <!-- Community card -->
              <div class="bg-[#FDF8EC] rounded-2xl p-6 text-right">
                <h3 class="text-xl font-bold text-[#C9A84C] mb-5">فسحني</h3>
                <div class="space-y-4">
                  <button v-for="c in communityHighlights" :key="c.title" @click="goTo(c)"
                    class="block w-full text-right text-lg text-[#1A1C1B] hover:text-[#755B00] transition-colors">
                    {{ c.title }} <span class="text-[#4D4637]/60 text-base">({{ c.detail }})</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Actions -->
      <div class="flex items-center gap-2 md:gap-4">
        <!-- Search -->
        <div class="relative">
          <button @click="toggleMenu('search')" class="p-2 text-[#4D4637] hover:text-[#755B00] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </button>
          <div v-if="openMenu === 'search'"
            class="absolute left-0 top-12 mt-1 w-72 bg-[#F4F4F2] rounded-2xl shadow-xl p-4 z-50" dir="rtl">
            <div class="flex items-center gap-2 bg-white border border-[#D0C5B2] rounded-xl px-3 py-2">
              <button @click="runSearch" class="text-[#755B00]">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
              </button>
              <input v-model="searchQuery" @keyup.enter="runSearch" type="text" autofocus
                placeholder="ابحث عن وجهة أو رحلة..."
                class="flex-1 text-sm text-right text-[#1A1C1B] placeholder:text-[#4D4637]/50 focus:outline-none" />
            </div>
          </div>
        </div>

        <!-- Notifications -->
        <div class="relative hidden md:block">
          <button @click="toggleMenu('notifications')" class="relative p-2 text-[#4D4637] hover:text-[#755B00] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
            <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-[#BA1A1A] rounded-full"></span>
          </button>
          <div v-if="openMenu === 'notifications'"
            class="absolute left-0 top-12 mt-1 w-80 bg-[#F4F4F2] rounded-2xl shadow-xl overflow-hidden text-right z-50" dir="rtl">
            <div class="p-4 border-b border-[#D0C5B2]">
              <h3 class="font-bold text-[#755B00]">الإشعارات</h3>
            </div>
            <div v-if="notifications.length" class="divide-y divide-[#D0C5B2]/60">
              <div v-for="n in notifications" :key="n.text" class="p-4 hover:bg-white/60 transition-colors">
                <p class="text-sm text-[#1A1C1B]">{{ n.text }}</p>
                <p class="text-xs text-[#4D4637]/60 mt-1">{{ n.time }}</p>
              </div>
            </div>
            <p v-else class="p-4 text-sm text-[#4D4637]">لا توجد إشعارات جديدة</p>
          </div>
        </div>
        <button @click="router.push('/ai-trip-planner')" class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#503D00] text-base font-bold px-6 py-2 rounded-xl transition-colors">
          خطط رحلتك
        </button>

        <!-- Profile avatar + dropdown -->
        <div class="relative hidden md:block">
          <button @click="toggleMenu('profile')"
            class="w-10 h-10 rounded-full bg-[#F5ECD7] border border-[#D0C5B2] flex items-center justify-center text-sm font-bold text-[#755B00] hover:border-[#755B00] transition-colors">
            أح
          </button>

          <div v-if="openMenu === 'profile'"
            class="absolute left-0 top-12 mt-1 w-64 bg-[#F4F4F2] rounded-2xl shadow-xl overflow-hidden text-right z-50" dir="rtl">
            <div class="flex items-center justify-between gap-3 p-5">
              <div class="w-11 h-11 rounded-full bg-[#F5ECD7] border border-[#D0C5B2] flex items-center justify-center text-sm font-bold text-[#755B00] shrink-0">
                أح
              </div>
              <div>
                <p class="font-bold text-[#755B00]">أحمد محمد</p>
                <p class="text-sm text-[#4D4637]">ahmed@example.com</p>
              </div>
            </div>
            <div class="border-t border-[#D0C5B2]"></div>
            <div class="py-2">
              <button v-for="item in profileLinks" :key="item"
                @click="closeMenus()"
                class="block w-full text-right px-5 py-2.5 text-[#4D4637] hover:bg-white/60 transition-colors">
                {{ item }}
              </button>
            </div>
            <div class="border-t border-[#D0C5B2]"></div>
            <button @click="router.push('/login'); closeMenus()"
              class="block w-full text-right px-5 py-3.5 text-[#C94B4B] font-bold hover:bg-white/60 transition-colors">
              تسجيل الخروج
            </button>
          </div>
        </div>

        <!-- Mobile hamburger -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 text-[#4D4637]">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t border-[#E8E4DC] px-4 py-4">
      <div class="flex flex-col gap-4 text-sm text-[#4D4637]">
        <button v-for="link in navLinks" :key="link.label"
          @click="router.push(link.path); mobileMenuOpen = false"
          class="text-right hover:text-[#755B00] transition-colors py-1">
          {{ link.label }}
        </button>
        <button @click="router.push('/login')" class="text-right text-[#755B00] font-medium">تسجيل الدخول</button>
      </div>
    </div>

    <!-- Click-away overlay for open menus -->
    <div v-if="openMenu" class="fixed inset-0 z-40" @click="closeMenus"></div>
  </nav>
</template>