<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import RestaurantCard from '../components/RestaurantCard.vue'

const router = useRouter()

/* ---------------- Toast feedback ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* ---------------- Category tabs (top nav pills) ---------------- */
const categories = [
  { id: 'nightlife', label: 'حياة ليلية', emoji: '🌙' },
  { id: 'shopping', label: 'تسوق', emoji: '🛍' },
  { id: 'amusement', label: 'ملاهي', emoji: '🎡' },
  { id: 'entertainment', label: 'ترفيه', emoji: '🎭' },
  { id: 'cafes', label: 'كافيهات', emoji: '☕' },
  { id: 'restaurants', label: 'مطاعم', emoji: '🍽' },
]
const activeCategory = ref('restaurants')
const selectCategory = (id) => {
  if (id === 'restaurants') {
    activeCategory.value = id
    return
  }
  // TODO: route to the relevant page once built, e.g. router.push(`/${id}`)
  showToast('هذا القسم قيد التطوير قريباً')
}

/* ---------------- Data ---------------- */
const trending = ref([
  {
    id: 1, name: 'صبحي كابر', cuisine: 'أكل مصري', area: 'روض الفرج',
    visitors: '12k', rating: 4.8, photoCount: '+2k',
    image: 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=500&q=80',
  },
  {
    id: 2, name: 'كريم دي لا كريم', cuisine: 'حلويات فرنسية', area: 'الزمالك',
    visitors: '5.4k', rating: 4.7, photoCount: '+85',
    image: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=500&q=80',
  },
  {
    id: 3, name: 'ذا ميت كومباني', cuisine: 'مشويات فاخرة', area: 'التجمع الخامس',
    visitors: '8.2k', rating: 4.9, photoCount: '+150',
    image: 'https://images.unsplash.com/photo-1544025162-d76694265947?w=500&q=80',
  },
])

const restaurants = ref([
  {
    id: 4, name: 'كافيه استريد', cuisine: 'قهوة مختصة', area: 'المعادي',
    rating: 4.5, priceLevel: 'E£££', quote: null,
    availableNow: true, wifiNote: 'سرعة نت ممتازة للعمل', instagramActive: true,
    favorite: false, tags: [{ label: 'موصى به', color: 'bg-[#B4D4FE] text-[#3C5C7F]' }, { label: 'بحرية', color: 'bg-[#C9A84C] text-[#503D00]' }],
    image: 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=600&q=80',
  },
  {
    id: 5, name: 'أسماك البرج', cuisine: 'مأكولات بحرية', area: 'وسط البلد',
    rating: 4.5, priceLevel: 'E£££', quote: 'أفضل ملوخية بالجمبري ممكن تكلها في حياتك، والمكان نظيف والخدمة ممتازة.',
    availableNow: true, wifiNote: 'سرعة نت ممتازة للعمل', instagramActive: true,
    favorite: false, tags: [{ label: 'موصى به', color: 'bg-[#B4D4FE] text-[#3C5C7F]' }],
    image: 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=600&q=80',
  },
])

const wideRestaurants = ref([
  {
    id: 6, name: 'إل', cuisine: 'إيطالي كلاسيك', area: 'الجيزة',
    rating: 4.0, priceLevel: 'E£££',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80',
  },
])

const toggleFavorite = (restaurant) => {
  restaurant.favorite = !restaurant.favorite
  showToast(restaurant.favorite ? 'أُضيف للمفضلة' : 'أُزيل من المفضلة')
}

const openRestaurant = (restaurant) => {
  // TODO: route to a RestaurantDetail page once it exists, e.g. router.push(`/restaurants/${restaurant.id}`)
  showToast(`سيتم فتح تفاصيل ${restaurant.name} قريباً`)
}

/* ---------------- Events ---------------- */
const events = ref([
  {
    id: 1, title: 'مهرجان الأكل الشعبي',
    desc: 'تجمع لأكبر مطاعم الأكل الشعبي في مصر بمكان واحد (حديقة الأزهر).',
    day: '25', month: 'ديسمبر', weekday: 'الاثنين',
    status: 'تذاكر متاحة', statusColor: 'text-[#16A34A]', badgeBg: 'bg-[#1A3C5E]',
  },
  {
    id: 2, title: 'ليلة الجاز',
    desc: 'استمتع بأجمل ألحان الجاز مع فرقة النيل الزرقاء في قلب القاهرة.',
    day: '22', month: 'ديسمبر', weekday: 'الجمعة',
    status: 'شارفت على النفاذ', statusColor: 'text-[#EF4444]', badgeBg: 'bg-[#755B00]',
  },
])
const bookEventTicket = (event) => {
  showToast(`جاري حجز تذكرة لفعالية "${event.title}"...`)
}

/* ---------------- View toggle ---------------- */
const viewMode = ref('grid') // 'grid' | 'list'

/* ---------------- Sidebar filters ---------------- */
const searchQuery = ref('')
const cuisineOptions = ['مصري', 'مشويات', 'إيطالي', 'مأكولات بحرية', 'شامي']
const selectedCuisines = ref(['مصري'])
const toggleCuisine = (c) => {
  selectedCuisines.value = selectedCuisines.value.includes(c)
    ? selectedCuisines.value.filter((x) => x !== c)
    : [...selectedCuisines.value, c]
}

const ambianceOptions = ['عائلي', 'رومانسي', 'إطلالة على النيل']
const selectedAmbiance = ref([])
const toggleAmbiance = (a) => {
  selectedAmbiance.value = selectedAmbiance.value.includes(a)
    ? selectedAmbiance.value.filter((x) => x !== a)
    : [...selectedAmbiance.value, a]
}

const priceOptions = ['E£', 'E££', 'E£££']
const selectedPrice = ref(null)
const togglePrice = (p) => {
  selectedPrice.value = selectedPrice.value === p ? null : p
}

const showGoogleRatings = ref(true)
const showInstagramPhotos = ref(true)

/* ---------------- Combined filtering ---------------- */
const allListItems = computed(() => [...restaurants.value, ...wideRestaurants.value])
const filteredRestaurants = computed(() =>
  restaurants.value.filter((r) => {
    if (searchQuery.value && !r.name.includes(searchQuery.value) && !r.cuisine.includes(searchQuery.value)) return false
    if (selectedCuisines.value.length && !selectedCuisines.value.some((c) => r.cuisine.includes(c))) return false
    if (selectedPrice.value && r.priceLevel !== selectedPrice.value) return false
    return true
  })
)

const suggestRestaurant = () => {
  showToast('شكراً! سنراجع اقتراحك قريباً 🍽️')
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8] pb-24">
    <Navbar />

    <!-- Toast -->
    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <!-- Hero banner -->
    <div class="pt-16">
      <div class="w-full h-48 flex items-center justify-end px-12"
        style="background: linear-gradient(270deg, #F5ECD7 0%, #FAFAF8 100%);">
        <div class="text-right">
          <h1 class="text-[32px] leading-10.5 font-semibold text-[#1A3C5E]">اكتشف أشهى المأكولات في القاهرة</h1>
          <p class="text-base text-[#7E7665] mt-1">من الأكلات الشعبية الأصيلة إلى أرقى المطاعم العالمية</p>
        </div>
      </div>

      <!-- Sticky category tabs -->
      <div class="sticky top-16 z-30 bg-[#FAFAF8]/90 backdrop-blur-md border-b border-[#D0C5B2]">
        <div class="max-w-360 mx-auto px-10 py-4 flex items-center justify-end gap-4 overflow-x-auto">
          <button v-for="cat in categories" :key="cat.id" @click="selectCategory(cat.id)"
            :class="activeCategory === cat.id
              ? 'bg-[#C9A84C] text-[#503D00] font-semibold shadow-sm'
              : 'bg-[#EEEEEC] text-[#4D4637]'"
            class="flex items-center gap-2 px-6 py-2 rounded-full text-base whitespace-nowrap transition-colors">
            {{ cat.label }}
            <span>{{ cat.emoji }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main -->
    <div class="max-w-360 mx-auto px-10 py-8 flex flex-col lg:flex-row-reverse gap-8 items-start">

      <!-- Sidebar filters -->
      <aside class="w-full lg:w-72 shrink-0 flex flex-col gap-8">
        <div class="flex flex-col gap-4">
          <h3 class="text-xl text-[#1A1C1B] text-right">ابحث عن مكانك</h3>
          <div class="relative">
            <input v-model="searchQuery" type="text" placeholder="اسم المطعم أو الوجبة..."
              class="w-full bg-[#FAFAF8] border border-[#E8E4DC] rounded-xl py-3.5 pr-4 pl-10 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
            <svg class="w-4.5 h-4.5 text-[#7E7665] absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
        </div>

        <div class="flex flex-col gap-4">
          <h3 class="text-xl text-[#1A1C1B] text-right">نوع المطبخ</h3>
          <div class="flex flex-wrap gap-2 justify-end">
            <button v-for="c in cuisineOptions" :key="c" @click="toggleCuisine(c)"
              :class="selectedCuisines.includes(c)
                ? 'bg-[#C9A84C]/10 border-[#C9A84C] text-[#755B00]'
                : 'border-[#E8E4DC] text-[#7E7665]'"
              class="border px-4 py-2 rounded-lg text-sm transition-colors">{{ c }}</button>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-xl text-[#1A1C1B] text-right">الأجواء</h3>
          <label v-for="a in ambianceOptions" :key="a" class="flex items-center justify-end gap-3 cursor-pointer">
            <span class="text-base text-[#1A1C1B]">{{ a }}</span>
            <input type="checkbox" :checked="selectedAmbiance.includes(a)" @change="toggleAmbiance(a)"
              class="w-4 h-4 rounded border-[#E8E4DC] accent-[#C9A84C]" />
          </label>
        </div>

        <div class="flex flex-col gap-3">
          <h3 class="text-xl text-[#1A1C1B] text-right">مستوى السعر</h3>
          <div class="flex items-center gap-2 justify-end">
            <button v-for="p in priceOptions" :key="p" @click="togglePrice(p)"
              :class="selectedPrice === p ? 'border-[#C9A84C] bg-[#C9A84C]/10 text-[#755B00]' : 'border-[#E8E4DC] text-[#7E7665]'"
              class="flex-1 border rounded-lg py-2.5 text-base font-semibold transition-colors">{{ p }}</button>
          </div>
        </div>

        <div class="border-t border-[#E8E4DC] pt-6 flex flex-col gap-3">
          <h3 class="text-xl text-[#1A1C1B] text-right">المصادر الاجتماعية</h3>
          <div class="flex items-center justify-between">
            <button @click="showGoogleRatings = !showGoogleRatings"
              :class="showGoogleRatings ? 'bg-[#C9A84C] justify-start' : 'bg-[#E8E4DC] justify-end'"
              class="w-10 h-5 rounded-full flex items-center p-0.5 transition-colors">
              <span class="w-4 h-4 bg-white rounded-full"></span>
            </button>
            <span class="text-base text-[#1A1C1B]">تقييمات Google</span>
          </div>
          <div class="flex items-center justify-between">
            <button @click="showInstagramPhotos = !showInstagramPhotos"
              :class="showInstagramPhotos ? 'bg-[#C9A84C] justify-start' : 'bg-[#E8E4DC] justify-end'"
              class="w-10 h-5 rounded-full flex items-center p-0.5 transition-colors">
              <span class="w-4 h-4 bg-white rounded-full"></span>
            </button>
            <span class="text-base text-[#1A1C1B]">صور Instagram</span>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <div class="flex-1 w-full flex flex-col gap-12">

        <!-- Trending this week -->
        <section class="flex flex-col gap-6">
          <div class="flex items-center justify-between">
            <button class="text-base font-bold text-[#755B00]">عرض الكل</button>
            <div class="flex items-center gap-2">
              <h2 class="text-[28px] text-[#1A1C1B]">الأكثر طلباً هذا الأسبوع</h2>
              <span>🔥</span>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <RestaurantCard v-for="r in trending" :key="r.id" :restaurant="r" variant="trending" @open="openRestaurant" />
          </div>
        </section>

        <!-- All restaurants -->
        <section class="flex flex-col gap-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <button @click="viewMode = 'list'" :class="viewMode === 'list' ? 'bg-[#F4F4F2] border-[#1A1C1B]' : 'border-[#E8E4DC]'"
                class="w-9 h-9 border rounded-lg flex items-center justify-center">
                <svg class="w-4.5 h-4.5 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
              </button>
              <button @click="viewMode = 'grid'" :class="viewMode === 'grid' ? 'bg-[#F4F4F2] border-[#1A1C1B]' : 'border-[#E8E4DC]'"
                class="w-9 h-9 border rounded-lg flex items-center justify-center">
                <svg class="w-4.5 h-4.5 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
              </button>
            </div>
            <h2 class="text-[28px] text-[#1A1C1B]">جميع المطاعم</h2>
          </div>

          <p v-if="filteredRestaurants.length === 0" class="text-sm text-[#7E7665] text-center py-10">
            لا توجد مطاعم مطابقة لهذه الفلاتر.
          </p>

          <div :class="viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 gap-6' : 'flex flex-col gap-6'">
            <RestaurantCard v-for="r in filteredRestaurants" :key="r.id" :restaurant="r" variant="grid"
              @open="openRestaurant" @toggle-favorite="toggleFavorite" />
          </div>

          <RestaurantCard v-for="r in wideRestaurants" :key="r.id" :restaurant="r" variant="wide" @open="openRestaurant" />
        </section>

        <!-- Events -->
        <section class="flex flex-col gap-6">
          <h2 class="text-[28px] text-[#1A1C1B] text-right">فعاليات هذا الأسبوع</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="e in events" :key="e.id" class="bg-white border border-[#E8E4DC] rounded-2xl flex overflow-hidden">
              <div :class="e.badgeBg" class="w-40 shrink-0 flex flex-col items-center justify-center text-white p-6 gap-1">
                <span class="text-3xl font-bold">{{ e.day }}</span>
                <span class="text-sm">{{ e.month }}</span>
                <span class="w-8 h-1 bg-white/30 my-2 rounded-full"></span>
                <span class="text-[10px] tracking-widest uppercase font-semibold">{{ e.weekday }}</span>
              </div>
              <div class="flex-1 p-6 flex flex-col gap-2 text-right">
                <h4 class="font-normal text-lg text-[#1A1C1B]">{{ e.title }}</h4>
                <p class="text-sm text-[#7E7665]">{{ e.desc }}</p>
                <div class="flex items-center justify-between pt-2">
                  <button @click="bookEventTicket(e)" class="bg-[#1A3C5E] hover:bg-[#152f4a] text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors">احجز تذكرتك</button>
                  <span class="text-xs font-semibold" :class="e.statusColor">{{ e.status }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Floating action button: suggest a restaurant -->
    <button @click="suggestRestaurant"
      class="fixed bottom-8 left-8 w-14 h-14 bg-[#C9A84C] hover:bg-[#b8963f] rounded-full shadow-xl flex items-center justify-center transition-colors z-40">
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
    </button>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>