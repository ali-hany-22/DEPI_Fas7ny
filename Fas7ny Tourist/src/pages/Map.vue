<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const route = useRoute()

const API_BASE = 'http://localhost:8000'

/* =========================================================================
   REAL DATA (متجاب من الباك إند - /places/combined + /search/place)
   ========================================================================= */
const cityName = computed(() => route.query.city || '')
/* لو المستخدم جاي من نتيجة بحث محددة (زي فندق سما العريش)، بيبقى
   عندنا q في الرابط. بنستخدمها عشان نركّز الخريطة على المكان ده
   ونفتحله popup مباشرة، مش بس نعرضه كنقطة عادية زي الباقي. */
const searchedName = computed(() => route.query.q || '')

/* مركز افتراضي للخريطة قبل ما نجيب أي بيانات - بيتغير أوتوماتيك لو
   لقينا نتيجة بحث محددة أو أماكن فعلية في المدينة */
const cityCenter = ref([25.6997, 32.6473])

const places = ref([])
const isLoading = ref(false)
const loadError = ref('')

/* بيانات بصرية إضافية (لون + أيقونة + badge) مش جايه من الباك إند -
   بنحطها هنا بناءً على category عشان الكارت/الماركر يبان شكله كويس */
const categoryMeta = {
  hotel: { color: '#C9A84C', badgeBg: 'rgba(201,168,76,0.1)', badgeLabel: 'فندق' },
  hotels: { color: '#C9A84C', badgeBg: 'rgba(201,168,76,0.1)', badgeLabel: 'فندق' },
  restaurant: { color: '#AA3436', badgeBg: '#FFDAD7', badgeLabel: 'مطعم' },
  restaurants: { color: '#AA3436', badgeBg: '#FFDAD7', badgeLabel: 'مطعم' },
  landmark: { color: '#416084', badgeBg: '#B4D4FE', badgeLabel: 'معلم أثري' },
  place: { color: '#416084', badgeBg: '#B4D4FE', badgeLabel: 'مكان' },
}
const metaFor = (category) => categoryMeta[category] || categoryMeta.place

/*
  بتحوّل عنصر راجع من /places/combined (سواء داخلي أو خارجي) لنفس
  الشكل اللي القالب هنا محتاجه. الحقول ممكن تختلف شوية حسب المصدر
  (internal بيرجع lat/lng مباشرة، الكاش الخارجي ممكن يرجعها بأسماء
  زي latitude/longitude) فبنغطي الاحتمالين.
*/
function normalizePlace(raw, index) {
  const lat = raw.lat ?? raw.latitude
  const lng = raw.lng ?? raw.longitude
  const category = raw.category || 'place'
  const meta = metaFor(category)

  return {
    id: raw.id ?? `${raw.name}-${index}`,
    name: raw.name || 'مكان بدون اسم',
    address: raw.address || raw.city || '',
    rating: raw.rating ?? 0,
    price: raw.price ? `${Number(raw.price).toLocaleString()} ج.م` : '—',
    unit: '/ ليلة',
    image: raw.image || raw.photo_url || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80',
    lat,
    lng,
    badgeBg: meta.badgeBg,
    badgeColor: meta.color,
    badgeLabel: meta.badgeLabel,
    type: category,
    desc: raw.description || '',
    source: raw.source || 'external',
  }
}

/* الأماكن اللي ليها إحداثيات فعلية بس - أي مكان من غير lat/lng
   منقدرش نحطه على الخريطة أصلاً */
const placesWithCoords = computed(() => places.value.filter((p) => p.lat != null && p.lng != null))

async function fetchPlaces() {
  if (!cityName.value.trim()) {
    loadError.value = 'مفيش مدينة محددة للبحث فيها.'
    places.value = []
    return
  }

  isLoading.value = true
  loadError.value = ''
  try {
    /* لو فيه بحث محدد (q)، بنجيب المكان ده تحديدًا الأول عشان نركّز
       الخريطة عليه ونفتحله popup - حتى لو مش موجود في /places/combined
       لسبب ما (زي لو لسه معندوش lat/lng محفوظة بشكل مختلف) */
    let highlighted = null
    if (searchedName.value.trim()) {
      const params = new URLSearchParams({ name: searchedName.value.trim() })
      if (cityName.value) params.set('city', cityName.value)
      const res = await fetch(`${API_BASE}/search/place?${params.toString()}`)
      if (res.ok) {
        const data = await res.json()
        if (data.found) highlighted = normalizePlace(data.result, 0)
      }
    }

    /* كل أماكن المدينة (داخلية + خارجية) */
    const params = new URLSearchParams({ city: cityName.value })
    const res = await fetch(`${API_BASE}/places/combined?${params.toString()}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    let list = (data.results || []).map(normalizePlace)

    /* لو المكان اللي المستخدم دور عليه مش موجود أصلاً في القائمة
       (مثلاً مفيش lat/lng له في /places/combined بس رجع من
       /search/place)، بنضيفه يدويًا في الأول */
    if (highlighted && highlighted.lat != null && highlighted.lng != null) {
      const alreadyIn = list.some((p) => p.name === highlighted.name)
      if (!alreadyIn) list = [highlighted, ...list]
    }

    places.value = list

    /* لو فيه مكان محدد بحثنا عليه وله إحداثيات، الخريطة تتمركز عليه.
       غير كده، تتمركز على أول مكان عنده إحداثيات، وإلا تفضل زي ما هي */
    if (highlighted && highlighted.lat != null && highlighted.lng != null) {
      cityCenter.value = [highlighted.lat, highlighted.lng]
    } else if (placesWithCoords.value.length) {
      const first = placesWithCoords.value[0]
      cityCenter.value = [first.lat, first.lng]
    }
  } catch (err) {
    console.error('Failed to fetch places for map:', err)
    loadError.value = 'تعذّر تحميل الأماكن من الخادم.'
    places.value = []
  } finally {
    isLoading.value = false
  }
}

/* ---------------- Filters ---------------- */
const filters = [
  { id: 'all', label: 'الكل' },
  { id: 'hotel', label: 'فنادق' },
  { id: 'restaurant', label: 'مطاعم' },
  { id: 'landmark', label: 'معالم سياحية' },
]
const activeFilter = ref('all')
const searchQuery = ref('')

const filteredPlaces = computed(() =>
  placesWithCoords.value.filter((p) => {
    if (activeFilter.value !== 'all' && p.type !== activeFilter.value) return false
    if (searchQuery.value && !p.name.includes(searchQuery.value) && !p.address.includes(searchQuery.value)) return false
    return true
  })
)

/* ---------------- Leaflet map ---------------- */
const mapEl = ref(null)
let map = null
let markers = {}

const typeIconPath = {
  hotel: '<path d="M2 21h20M4 21V7a1 1 0 011-1h4a1 1 0 011 1v14M14 21V4a1 1 0 011-1h4a1 1 0 011 1v17M9 8h.01M9 12h.01M9 16h.01" stroke-width="1.7" stroke-linecap="round"/>',
  hotels: '<path d="M2 21h20M4 21V7a1 1 0 011-1h4a1 1 0 011 1v14M14 21V4a1 1 0 011-1h4a1 1 0 011 1v17M9 8h.01M9 12h.01M9 16h.01" stroke-width="1.7" stroke-linecap="round"/>',
  restaurant: '<path d="M18 8h1a4 4 0 010 8h-1M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8zM6 1v3M10 1v3M14 1v3" stroke-width="1.7" stroke-linecap="round"/>',
  restaurants: '<path d="M18 8h1a4 4 0 010 8h-1M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8zM6 1v3M10 1v3M14 1v3" stroke-width="1.7" stroke-linecap="round"/>',
  landmark: '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
  place: '<path d="M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>',
}

const buildIcon = (place, active = false) => {
  const color = place.badgeColor
  const size = active ? 50 : 40
  return L.divIcon({
    className: 'fasahny-marker',
    html: `
      <div style="width:${size}px;height:${size}px;border-radius:9999px;background:#fff;border:2px solid ${color};
        display:flex;align-items:center;justify-content:center;box-shadow:0 10px 15px -3px rgba(0,0,0,.1),0 4px 6px -4px rgba(0,0,0,.1);">
        <svg width="${size * 0.45}" height="${size * 0.45}" viewBox="0 0 24 24" fill="none" stroke="${color}">${typeIconPath[place.type] || typeIconPath.place}</svg>
      </div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  })
}

const popupHtml = (place) => `
  <div style="width:220px;font-family:'Cairo',sans-serif;direction:rtl;">
    <img src="${place.image}" style="width:100%;height:110px;object-fit:cover;border-radius:8px 8px 0 0;" />
    <div style="padding:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
        <span style="color:#C9A84C;font-weight:700;font-size:12px;">${place.rating} ★</span>
        <span style="color:#1A1C1B;font-size:14px;">${place.name}</span>
      </div>
      <p style="color:#7E7665;font-size:11px;line-height:1.5;margin:0 0 10px;text-align:right;">${place.desc}</p>
      <button id="popup-detail-${place.id}" style="width:100%;padding:8px 0;border:1px solid #C9A84C;border-radius:8px;
        background:transparent;color:#C9A84C;font-family:'Cairo',sans-serif;font-size:12px;cursor:pointer;">
        عرض التفاصيل
      </button>
    </div>
  </div>`

const goToPlace = (place) => {
  if (place.type === 'hotel' || place.type === 'hotels') router.push(`/hotel/${encodeURIComponent(cityName.value)}/${place.id}`)
  else router.push('/search')
}

const openPopup = (place) => {
  const m = markers[place.id]
  if (!m) return
  map.flyTo([place.lat, place.lng], 15, { duration: 0.6 })
  m.openPopup()
}

function renderMarkers() {
  if (!map) return
  Object.values(markers).forEach((m) => map.removeLayer(m))
  markers = {}

  filteredPlaces.value.forEach((place) => {
    const isHighlighted = place.name === searchedName.value
    const marker = L.marker([place.lat, place.lng], { icon: buildIcon(place, isHighlighted) }).addTo(map)
    marker.bindPopup(popupHtml(place), { closeButton: true, className: 'fasahny-popup' })
    marker.on('popupopen', () => {
      nextTick(() => {
        const btn = document.getElementById(`popup-detail-${place.id}`)
        if (btn) btn.onclick = () => goToPlace(place)
      })
    })
    markers[place.id] = marker
    if (isHighlighted) {
      map.flyTo([place.lat, place.lng], 15, { duration: 0.6 })
      marker.openPopup()
    }
  })
}

onMounted(async () => {
  map = L.map(mapEl.value, { zoomControl: false }).setView(cityCenter.value, 14)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)

  await fetchPlaces()
  map.setView(cityCenter.value, 14)
  renderMarkers()
})

/* لو المدينة أو البحث المحدد اتغيروا، نجيب البيانات تاني */
watch([cityName, searchedName], async () => {
  await fetchPlaces()
  if (map) {
    map.setView(cityCenter.value, 14)
    renderMarkers()
  }
})

/* لو المستخدم غيّر الفلتر المحلي (فنادق/مطاعم/معالم)، نعيد رسم
   الماركرز بس من غير ما نعمل fetch جديد */
watch(filteredPlaces, () => {
  renderMarkers()
})

onBeforeUnmount(() => {
  if (map) map.remove()
})

const zoomIn = () => map && map.zoomIn()
const zoomOut = () => map && map.zoomOut()
const locateMe = () => map && map.locate({ setView: true, maxZoom: 15 })

/* ---------------- AI prompt ---------------- */
const aiPromptOpen = ref(true)
const openAiPlanner = () => router.push({ path: '/ai-trip-planner', query: { city: cityName.value } })
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8]">
    <Navbar />

    <!-- Sub-header: filters + search -->
    <div class="fixed top-18 left-0 right-0 z-30 bg-[#FAFAF8] border-b border-[#E8E4DC] px-6 py-4 flex items-center justify-between gap-6 flex-wrap">
      <div class="flex items-center gap-2">
        <button v-for="f in filters" :key="f.id" @click="activeFilter = f.id"
          :class="activeFilter === f.id ? 'bg-[#C9A84C] text-white border-[#C9A84C]' : 'border-[#E8E4DC] text-[#4D4637] hover:border-[#C9A84C]/50'"
          class="border rounded-full px-6 py-2.5 text-sm transition-colors">
          {{ f.label }}
        </button>
      </div>
      <div class="relative w-full sm:w-96">
        <input v-model="searchQuery" type="text" placeholder="ابحث عن مطعم، فندق، أو معلم..."
          class="w-full bg-white border border-[#E8E4DC] rounded-xl py-3.5 pr-4 pl-11 text-base text-right focus:outline-none focus:border-[#C9A84C]" />
        <svg class="w-4.5 h-4.5 text-[#7E7665] absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
      </div>
    </div>

    <!-- Split layout -->
    <div class="pt-38.5 flex" style="height: 100vh;">

      <!-- Map panel -->
      <div class="relative flex-1 h-full">
        <div ref="mapEl" class="w-full h-full"></div>

        <!-- Loading / error overlay -->
        <div v-if="isLoading" class="absolute inset-0 bg-white/60 flex items-center justify-center z-500">
          <p class="text-sm text-[#7E7665]">جاري تحميل الأماكن...</p>
        </div>
        <div v-else-if="loadError" class="absolute top-6 left-1/2 -translate-x-1/2 z-500 bg-white border border-[#C94B4B] text-[#C94B4B] text-sm px-4 py-2 rounded-xl shadow">
          {{ loadError }}
        </div>

        <!-- Floating AI prompt -->
        <Transition name="fade">
          <div v-if="aiPromptOpen"
            class="absolute top-6 right-6 z-400 w-80 bg-white/80 backdrop-blur-md border border-[#C9A84C] rounded-2xl p-4
              shadow-[0_20px_25px_-5px_rgba(0,0,0,0.1),0_8px_10px_-6px_rgba(0,0,0,0.1)] flex items-start gap-3">
            <button @click="aiPromptOpen = false" class="absolute top-2 left-2 text-[#7E7665] hover:text-[#1A1C1B]">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
            <button @click="openAiPlanner" class="w-8 h-8 rounded-full bg-[#C9A84C] flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </button>
            <p @click="openAiPlanner" class="text-xs leading-5 text-[#1A1C1B] text-right cursor-pointer">
              أهلاً بك! هل ترغب في اقتراح مسار سياحي يجمع بين المواقع الأثرية وأفضل المطاعم المحلية في {{ cityName }}؟
            </p>
          </div>
        </Transition>

        <!-- Map controls -->
        <div class="absolute bottom-6 left-6 z-400 flex flex-col gap-2">
          <button @click="zoomIn" class="w-10 h-10 bg-white border border-[#E8E4DC] rounded-xl shadow-sm flex items-center justify-center hover:bg-[#F4F4F2]">
            <svg class="w-4 h-4 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          </button>
          <button @click="zoomOut" class="w-10 h-10 bg-white border border-[#E8E4DC] rounded-xl shadow-sm flex items-center justify-center hover:bg-[#F4F4F2]">
            <svg class="w-4 h-4 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 12h16"/></svg>
          </button>
          <button @click="locateMe" class="w-10 h-10 bg-white border border-[#E8E4DC] rounded-xl shadow-sm flex items-center justify-center hover:bg-[#F4F4F2] mt-2">
            <svg class="w-5 h-5 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8a4 4 0 100 8 4 4 0 000-8zM12 2v3m0 14v3M2 12h3m14 0h3"/></svg>
          </button>
        </div>
      </div>

      <!-- Results panel -->
      <aside class="hidden lg:flex flex-col w-120 h-full bg-white border-l border-[#E8E4DC] overflow-y-auto shrink-0">
        <div class="p-6 flex flex-col gap-1 border-b border-[#F4F4F2]">
          <h1 class="text-xl text-[#1A1C1B] text-right">{{ filteredPlaces.length }} مكان في {{ cityName }}</h1>
          <p class="text-sm text-[#7E7665] text-right">اكتشف أفضل الوجهات المختارة بعناية</p>
        </div>

        <div class="p-6 flex flex-col gap-4">
          <div v-for="place in filteredPlaces" :key="place.id" @click="openPopup(place)"
            class="flex items-start gap-4 p-3 rounded-xl cursor-pointer hover:bg-[#FAFAF8] transition-colors">
            <img :src="place.image" class="w-24 h-24 object-cover rounded-lg shrink-0" :alt="place.name" />
            <div class="flex-1 flex flex-col gap-2 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <div class="flex items-center gap-1 shrink-0">
                  <svg class="w-3 h-3 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                  <span class="text-xs font-bold text-[#C9A84C]">{{ place.rating }}</span>
                </div>
                <h3 class="text-base text-[#1A1C1B] text-right truncate">{{ place.name }}</h3>
              </div>
              <p class="text-xs text-[#7E7665] text-right">{{ place.address }}</p>
              <div class="flex items-center justify-between">
                <span class="text-[10px] px-2 py-0.5 rounded-full font-normal"
                  :style="{ background: place.badgeBg, color: place.badgeColor }">{{ place.badgeLabel }}</span>
                <p class="text-sm text-[#1A3C5E]">{{ place.price }} <span class="text-[10px] text-[#7E7665]">{{ place.unit }}</span></p>
              </div>
            </div>
          </div>

          <p v-if="!filteredPlaces.length && !isLoading" class="text-center text-sm text-[#7E7665] py-10">لا توجد نتائج مطابقة لبحثك.</p>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

<style>
/* Leaflet popup theming (global, since Leaflet renders outside Vue's scoped styles) */
.fasahny-popup .leaflet-popup-content-wrapper {
  padding: 0;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #E8E4DC;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
.fasahny-popup .leaflet-popup-content {
  margin: 0;
  width: 220px !important;
}
.fasahny-popup .leaflet-popup-tip {
  background: #fff;
  border: 1px solid #E8E4DC;
}
.leaflet-marker-icon.fasahny-marker { background: none; border: none; }
</style>