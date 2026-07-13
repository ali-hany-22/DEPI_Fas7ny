<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const route = useRoute()

/* ---------------- Toast ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* =========================================================================
   BASE ACCOMMODATION DATA
   Mirrors the `accommodations` arrays inside CityDetail.vue's citiesData.
   Keep these two in sync — id + name + image + price should match.
   ========================================================================= */
const citiesAccommodations = {
  'القاهرة': [
    { id: 1, name: 'فندق فورسيزونز نايل بلازا', badge: 'إطلالة على النيل', rating: 4.9, stars: 5, pricePerNight: 3500, category: 'hotel', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80' },
  ],
  'الأقصر': [
    { id: 1, name: 'منتجع جزيرة الموز', badge: 'تراثي', rating: 4.6, stars: 4, pricePerNight: 1200, category: 'resort', image: 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=1200&q=80' },
    { id: 2, name: 'سونستا سانت جورج', badge: 'إطلالة على النيل', rating: 4.8, stars: 5, pricePerNight: 850, category: 'hotel', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200&q=80' },
  ],
  'الغردقة': [
    { id: 1, name: 'ستيغنبرغر الجزيرة الغردقة', badge: 'شاطئ خاص', rating: 4.7, stars: 5, pricePerNight: 1800, category: 'resort', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1200&q=80' },
    { id: 2, name: 'فندق مارينا الغردقة', badge: 'إطلالة على المارينا', rating: 4.4, stars: 4, pricePerNight: 950, category: 'hotel', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200&q=80' },
  ],
  'أسوان': [
    { id: 1, name: 'موفنبيك جزيرة النخيل أسوان', badge: 'إطلالة على النيل', rating: 4.7, stars: 5, pricePerNight: 1600, category: 'resort', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200&q=80' },
    { id: 2, name: 'أولد كتراكت أسوان', badge: 'تراثي فاخر', rating: 4.9, stars: 5, pricePerNight: 2200, category: 'hotel', image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=1200&q=80' },
  ],
  'دهب': [
    { id: 1, name: 'لاجونا دهب ريزورت', badge: 'شاطئ خاص', rating: 4.5, stars: 4, pricePerNight: 1100, category: 'resort', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200&q=80' },
    { id: 2, name: 'فندق نيو ديزرت دهب', badge: 'أجواء بدوية', rating: 4.3, stars: 3, pricePerNight: 500, category: 'hotel', image: 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=1200&q=80' },
  ],
  'شرم الشيخ': [
    { id: 1, name: 'فور سيزونز شرم الشيخ', badge: 'شاطئ خاص', rating: 4.9, stars: 5, pricePerNight: 3200, category: 'resort', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=1200&q=80' },
    { id: 2, name: 'ريتز كارلتون شرم الشيخ', badge: 'إطلالة على البحر', rating: 4.8, stars: 5, pricePerNight: 2100, category: 'hotel', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200&q=80' },
  ],
  'الإسكندرية': [
    { id: 1, name: 'فندق تريانون كورنيش الإسكندرية', badge: 'إطلالة بحرية', rating: 4.5, stars: 4, pricePerNight: 1400, category: 'hotel', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=1200&q=80' },
  ],
  'العين السخنة': [
    { id: 1, name: 'منتجع بورتو السخنة', badge: 'شاطئ خاص', rating: 4.4, stars: 4, pricePerNight: 1600, category: 'resort', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1200&q=80' },
  ],
  'سيوة': [
    { id: 1, name: 'أدرار سيوة لودج', badge: 'تراثي', rating: 4.6, stars: 4, pricePerNight: 900, category: 'resort', image: 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=1200&q=80' },
  ],
}

/* Nearby landmarks per city, used as fallback location chips */
const nearbyByCity = {
  'الأقصر': [
    { name: 'معبد الأقصر', duration: '١٥ دقيقة سيراً' },
    { name: 'متحف الأقصر', duration: '١٠ دقائق بالسيارة' },
    { name: 'مطار الأقصر', duration: '٢٠ دقيقة بالسيارة' },
    { name: 'مرسى العبارات', duration: '٥ دقائق سيراً' },
  ],
  'القاهرة': [
    { name: 'أهرامات الجيزة', duration: '٢٥ دقيقة بالسيارة' },
    { name: 'المتحف المصري الكبير', duration: '٢٠ دقيقة بالسيارة' },
  ],
  'الغردقة': [
    { name: 'مارينا الغردقة', duration: '١٠ دقائق بالسيارة' },
    { name: 'مطار الغردقة', duration: '١٥ دقيقة بالسيارة' },
  ],
  'أسوان': [
    { name: 'معبد فيلة', duration: '١٥ دقيقة بالقارب' },
    { name: 'السد العالي', duration: '٢٠ دقيقة بالسيارة' },
  ],
  'دهب': [
    { name: 'الحفرة الزرقاء', duration: '٢٠ دقيقة بالسيارة' },
    { name: 'مقاهي الشاطئ', duration: '٥ دقائق سيراً' },
  ],
  'شرم الشيخ': [
    { name: 'خليج نعمة', duration: '١٠ دقائق سيراً' },
    { name: 'مطار شرم الشيخ', duration: '٢٥ دقيقة بالسيارة' },
  ],
  'الإسكندرية': [
    { name: 'مكتبة الإسكندرية', duration: '١٠ دقائق بالسيارة' },
    { name: 'قلعة قايتباي', duration: '١٥ دقيقة بالسيارة' },
  ],
  'العين السخنة': [
    { name: 'شاطئ السخنة', duration: '٥ دقائق سيراً' },
  ],
  'سيوة': [
    { name: 'جبل الدكرور', duration: '١٥ دقيقة بالسيارة' },
    { name: 'بحيرات الملح', duration: '٢٠ دقيقة بالسيارة' },
  ],
}

/* =========================================================================
   RICH DETAIL OVERRIDES
   Add a key "CityName::id" for any hotel you want fully fleshed out.
   Anything not listed here falls back to sensible generated defaults.
   ========================================================================= */
const hotelExtras = {
  'الأقصر::2': {
    gallery: [
      'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=900&q=80',
      'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=900&q=80',
      'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1400&q=80',
      'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=700&q=80',
      'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=700&q=80',
    ],
    address: 'كورنيش الأقصر، الأقصر، مصر',
    verified: true,
    externalRatings: [
      { source: 'Google', value: 4.8 },
      { source: 'TripAdvisor', value: 4.7 },
      { source: 'Booking.com', value: 4.9 },
    ],
    amenities: [
      { label: 'واي فاي مجاني', icon: 'wifi' },
      { label: 'مسبح خارجي', icon: 'pool' },
      { label: 'مطاعم فاخرة', icon: 'restaurant' },
      { label: 'منتجع صحي', icon: 'spa' },
      { label: 'صالة ألعاب', icon: 'gym' },
      { label: 'قاعات اجتماعات', icon: 'meeting' },
      { label: 'موقف سيارات', icon: 'parking' },
      { label: 'خدمة غرف', icon: 'room-service' },
    ],
    description: [
      'يقع فندق سونستا سانت جورج في قلب مدينة الأقصر التاريخية، ويوفر إطلالات ساحرة ومباشرة على نهر النيل الخالد. يجمع الفندق بين الفخامة العصرية واللمسات المصرية الكلاسيكية، مما يجعله وجهة مثالية للمسافرين الباحثين عن الراحة والجمال.',
      'استمتع بتجربة إقامة راقية في غرف مصممة بعناية لتناسب أرقى الأذواق، حيث تتميز الوحدات بأثاث مريح وشرفات تطل على أجمل مناظر النيل والبر الغربي، مع سهولة الوصول إلى المعابد الفرعونية الشهيرة ومواقع التراث العالمي.',
    ],
    socialProof: { title: 'الخيار الأول للمسافرين في الأقصر', subtitle: 'تم حجز هذا الفندق أكثر من ١٥٠ مرة في آخر ٢٤ ساعة' },
    rooms: [
      { id: 1, name: 'غرفة ديلوكس مطلة على النيل', desc: 'سرير كينج، شرفة خاصة، خدمة غرف على مدار الساعة', size: 42, guests: 2, price: 850, image: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=500&q=80' },
      { id: 2, name: 'غرفة مزدوجة كلاسيكية', desc: 'سريران منفصلان، إطلالة على الحديقة، مكتب عمل', size: 38, guests: 2, price: 720, image: 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=500&q=80' },
    ],
    ratingBreakdown: [
      { label: 'القيمة مقابل السعر', value: 4.6 },
      { label: 'النظافة', value: 4.9 },
      { label: 'المرافق', value: 4.8 },
      { label: 'الموقع', value: 4.8 },
      { label: 'الخدمة', value: 4.7 },
    ],
    reviews: [
      { name: 'John D.', source: 'عبر تريب أدفايزر', initial: 'T', color: '#16A34A', bg: '#DCFCE7', text: 'موقع مثالي لزيارة المعابد. الغرفة المطلة على النيل تستحق التجربة.', hasPhoto: false },
      { name: 'Sara_Tours', source: 'عبر انستجرام', initial: 'I', color: '#DB2777', bg: '#FCE7F3', text: 'أجمل مسبح في الأقصر بلا منازع. الخدمة فاخرة جداً.', hasPhoto: true },
      { name: 'محمد علي', source: 'عبر جوجل', initial: 'G', color: '#2563EB', bg: '#DBEAFE', text: 'إقامة رائعة وطاقم عمل ودود للغاية. المنظر من الشرفة لا يصدق.', hasPhoto: true },
    ],
    moments: [
      { image: 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400&q=80', caption: 'الحمام فخم جداً والنظافة ١٠/١٠', date: 'يونيو ٢٠٢٤', initial: 'T', color: '#EF4444' },
      { image: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=400&q=80', caption: 'الغرفة واسعة والفيو بجد يشرح القلب', date: 'يوليو ٢٠٢٤', initial: 'K', color: '#6366F1' },
      { image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400&q=80', caption: 'الجو كان خيالي النهاردة في البيسين', date: 'أغسطس ٢٠٢٤', initial: 'Y', color: '#10B981' },
      { image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80', caption: 'عشا رايق ع النيل في البلكونة بجد تحفة', date: 'سبتمبر ٢٠٢٤', initial: 'A', color: '#F59E0B' },
      { image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80', caption: 'منظر الفندق وقت الغروب حكاية تانية', date: 'أكتوبر ٢٠٢٤', initial: 'S', color: '#EC4899' },
    ],
  },
}

/* ---------------- Icon paths for amenities ---------------- */
const amenityIcons = {
  wifi: 'M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01M5 12.859a10 10 0 0114 0M1.394 9.393a15 15 0 0121.212 0',
  pool: 'M2 21c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0 3 1 4.5 0M4 17c1.5-1 3-1 4.5 0s3 1 4.5 0 3-1 4.5 0M13 5a3 3 0 11-6 0 3 3 0 016 0z',
  restaurant: 'M18 8h1a4 4 0 010 8h-1M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8zM6 1v3M10 1v3M14 1v3',
  spa: 'M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z',
  gym: 'M6.5 6.5l11 11M21 21l-1-1M4 4L3 3M18 8l3-3M3 3l3-3M6 22l3-3M2 18l3-3',
  meeting: 'M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m5-3.13a4 4 0 100-8 4 4 0 000 8zm6 2a4 4 0 100-8',
  parking: 'M4 4h16v16H4V4zm4 3v10m0-5h4a2.5 2.5 0 000-5H8',
  'room-service': 'M3 17h18M4 17V9a8 8 0 0116 0v8M12 3v1',
  default: 'M12 6v6l4 2',
}

/* =========================================================================
   RESOLVE HOTEL FROM ROUTE
   ========================================================================= */
const cityName = computed(() => route.params.city || 'الأقصر')
const hotelId = computed(() => Number(route.params.id) || 1)

const baseHotel = computed(() => {
  const list = citiesAccommodations[cityName.value] || citiesAccommodations['الأقصر']
  return list.find((h) => h.id === hotelId.value) || list[0]
})

const extra = computed(() => hotelExtras[`${cityName.value}::${baseHotel.value.id}`] || {})

const hotel = computed(() => {
  const b = baseHotel.value
  const e = extra.value
  return {
    ...b,
    address: e.address || `وسط البلد، ${cityName.value}، مصر`,
    verified: e.verified ?? true,
    externalRatings: e.externalRatings || [
      { source: 'Google', value: b.rating },
      { source: 'Booking.com', value: Math.min(5, (b.rating + 0.1).toFixed(1)) },
    ],
    gallery: e.gallery && e.gallery.length ? e.gallery : [b.image, b.image, b.image, b.image, b.image],
    amenities: e.amenities || [
      { label: 'واي فاي مجاني', icon: 'wifi' },
      { label: 'مسبح خارجي', icon: 'pool' },
      { label: 'مطاعم', icon: 'restaurant' },
      { label: 'موقف سيارات', icon: 'parking' },
      { label: 'خدمة غرف', icon: 'room-service' },
      { label: 'صالة ألعاب', icon: 'gym' },
    ],
    description: e.description || [
      `يوفر ${b.name} إقامة مريحة في ${cityName.value}، مع مزيج من الخدمة المتميزة والموقع المتميز القريب من أبرز المعالم السياحية.`,
      'تتميز الوحدات بتصميم أنيق ووسائل راحة حديثة تناسب المسافرين الباحثين عن الجودة والراحة على حدٍ سواء.',
    ],
    socialProof: e.socialProof || { title: `خيار موصى به في ${cityName.value}`, subtitle: 'ضمن الفنادق الأعلى تقييماً من ضيوف فسحني' },
    rooms: e.rooms && e.rooms.length ? e.rooms : [
      { id: 1, name: 'غرفة قياسية', desc: 'سرير كوين، حمام خاص، تكييف', size: 30, guests: 2, price: b.pricePerNight, image: b.image },
    ],
    ratingBreakdown: e.ratingBreakdown || [
      { label: 'القيمة مقابل السعر', value: b.rating - 0.2 },
      { label: 'النظافة', value: b.rating },
      { label: 'المرافق', value: b.rating - 0.1 },
      { label: 'الموقع', value: b.rating },
      { label: 'الخدمة', value: b.rating - 0.1 },
    ],
    reviews: e.reviews || [
      { name: 'ضيف فسحني', source: 'عبر فسحني', initial: 'ف', color: '#C9A84C', bg: '#FDF8EC', text: 'إقامة جيدة جداً وموقع قريب من كل حاجة. هرجع تاني أكيد.', hasPhoto: false },
    ],
    moments: e.moments || [],
  }
})

const nearby = computed(() => nearbyByCity[cityName.value] || [])

/* ---------------- Booking widget state ---------------- */
const checkIn = ref('١٤ أكتوبر ٢٠٢٤')
const checkOut = ref('٢١ أكتوبر ٢٠٢٤')
const adults = ref(2)
const children = ref(1)
const guestsPanelOpen = ref(false)
const nights = 7

const selectedRoom = ref(null)
const selectRoom = (room) => {
  selectedRoom.value = room
  showToast(`تم اختيار ${room.name}`)
}

const activeRoomPrice = computed(() => (selectedRoom.value || hotel.value.rooms[0]).price)
const totalPrice = computed(() => activeRoomPrice.value * nights)

const confirmBooking = () => {
  showToast('جاري تأكيد حجزك...')
  const room = selectedRoom.value || hotel.value.rooms[0]
  setTimeout(() => {
    router.push({
      path: '/payment',
      query: {
        hotel: hotel.value.name,
        city: cityName.value,
        room: room.name,
        checkIn: checkIn.value,
        checkOut: checkOut.value,
        adults: adults.value,
        children: children.value,
        total: totalPrice.value,
      },
    })
  }, 700)
}

const goBack = () => router.push(`/city/${encodeURIComponent(cityName.value)}`)

const openInteractiveMap = () => {
  router.push({ path: '/map', query: { city: city.value.name } })
}
const openReviewPhotos = () => showToast('عرض صور هذا التقييم قريباً')
const openAllMoments = () => router.push('/community')
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-white">
    <Navbar />

    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <div class="max-w-360 mx-auto px-6 md:px-8 pt-24 md:pt-28 pb-16 flex flex-col gap-6">

      <!-- Breadcrumb -->
      <nav class="flex items-center justify-end gap-2 text-sm">
        <button @click="router.push('/')" class="text-[#4D4637] hover:text-[#1A3C5E]">الرئيسية</button>
        <span class="text-[#4D4637]/50">/</span>
        <button @click="goBack" class="text-[#4D4637] hover:text-[#1A3C5E]">{{ cityName }}</button>
        <span class="text-[#4D4637]/50">/</span>
        <span class="text-[#C9A84C] font-semibold">الفنادق</span>
      </nav>

      <!-- Photo gallery -->
      <div class="relative w-full h-125 md:h-150 rounded-2xl overflow-hidden grid grid-cols-4 grid-rows-2 gap-2">
        <div class="col-span-2 row-span-2 relative">
          <img :src="hotel.gallery[2] || hotel.image" class="w-full h-full object-cover" :alt="hotel.name" />
        </div>
        <div v-for="(img, i) in [hotel.gallery[0], hotel.gallery[1], hotel.gallery[3], hotel.gallery[4]]" :key="i"
          class="relative overflow-hidden">
          <img :src="img" class="w-full h-full object-cover" :alt="hotel.name" />
        </div>
        <button @click="showToast('عرض جميع الصور قريباً')"
          class="absolute bottom-4 left-4 flex items-center gap-2 bg-white/90 backdrop-blur-sm border border-[#D0C5B2] rounded-lg px-4 py-2.5 text-sm font-bold text-[#1A1C1B] shadow-sm">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M14 8h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          عرض كل الصور
        </button>
      </div>

      <!-- Content grid: content (right, RTL-first) + sticky booking card (left) -->
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_453px] gap-10 items-start">

        <!-- ===================== LEFT/MAIN CONTENT ===================== -->
        <div class="flex flex-col gap-8 order-2 lg:order-1">

          <!-- Header -->
          <div class="flex flex-col gap-2">
            <div class="flex items-center justify-end gap-2 flex-wrap">
              <span class="bg-[#E8E8E6] text-[#1A3C5E] text-xs font-semibold px-3 py-1 rounded-full">{{ hotel.category === 'resort' ? 'منتجع' : 'فندق' }}</span>
              <span class="bg-[#E8E8E6] text-[#1A3C5E] text-xs font-semibold px-3 py-1 rounded-full">{{ hotel.stars }} نجوم</span>
              <span v-if="hotel.badge" class="bg-[#C9A84C]/10 text-[#C9A84C] text-xs font-bold px-3 py-1 rounded-full">{{ hotel.badge }}</span>
              <span v-if="hotel.verified" class="flex items-center gap-1 bg-[#C9A84C]/5 text-[#C9A84C] text-xs font-bold px-2 py-1 rounded-md">
                موثق
                <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              </span>
            </div>

            <h1 class="text-4xl md:text-5xl font-bold text-[#1A1C1B] text-right">{{ hotel.name }}</h1>

            <div class="flex items-center justify-end gap-2 text-[#4D4637] text-base">
              <span>{{ hotel.address }}</span>
              <svg class="w-5 h-5 text-[#C9A84C] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
            </div>
          </div>

          <!-- Ratings summary -->
          <div class="bg-white border border-[#D0C5B2] rounded-xl px-6 py-5 flex flex-wrap items-center justify-end gap-6">
            <div v-for="r in hotel.externalRatings" :key="r.source" class="flex items-center gap-1">
              <svg class="w-5 h-5 text-[#EAB308]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span class="text-sm text-[#71717A] font-medium">{{ r.source }} ({{ r.value }})</span>
            </div>
            <div class="border-r border-[#D0C5B2] pr-6 flex flex-col items-center">
              <p class="text-2xl font-bold text-[#1A3C5E]">{{ hotel.rating }}</p>
              <p class="text-xs font-bold text-[#C9A84C] uppercase">ممتاز</p>
            </div>
          </div>

          <!-- Amenities -->
          <section class="flex flex-col gap-4">
            <h3 class="text-2xl font-semibold text-[#1A1C1B] text-right">المرافق والخدمات</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div v-for="a in hotel.amenities" :key="a.label"
                class="border border-[#D0C5B2] rounded-xl p-4 flex flex-col items-center gap-2 text-center">
                <svg class="w-6 h-6 text-[#1A3C5E]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" :d="amenityIcons[a.icon] || amenityIcons.default"/>
                </svg>
                <span class="text-sm text-[#1A1C1B]">{{ a.label }}</span>
              </div>
            </div>
          </section>

          <!-- Description -->
          <section class="flex flex-col gap-4">
            <p v-for="(p, i) in hotel.description" :key="i" class="text-lg leading-8 text-[#4D4637] text-right">{{ p }}</p>
          </section>

          <!-- Room types -->
          <section class="flex flex-col gap-6">
            <h3 class="text-2xl font-semibold text-[#1A1C1B] text-right">أنواع الغرف المتاحة</h3>
            <div class="flex flex-col gap-4">
              <div v-for="room in hotel.rooms" :key="room.id"
                class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden flex flex-col sm:flex-row">
                <img :src="room.image" class="w-full sm:w-48 h-44 sm:h-auto object-cover" :alt="room.name" />
                <div class="flex-1 p-5 flex flex-col justify-between gap-3">
                  <div class="flex flex-col gap-1">
                    <h4 class="text-lg font-bold text-[#1A1C1B] text-right">{{ room.name }}</h4>
                    <p class="text-sm text-[#4D4637] text-right">{{ room.desc }}</p>
                    <div class="flex items-center justify-end gap-4 pt-1 text-xs text-[#4D4637]">
                      <span class="flex items-center gap-1">{{ room.guests }} شخصين
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87m5-3.13a4 4 0 100-8 4 4 0 000 8z"/></svg>
                      </span>
                      <span class="flex items-center gap-1">{{ room.size }} م²
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4"/></svg>
                      </span>
                    </div>
                  </div>
                  <div class="flex items-end justify-between">
                    <button @click="selectRoom(room)"
                      :class="selectedRoom && selectedRoom.id === room.id ? 'bg-[#1A3C5E] text-white' : 'bg-[#C9A84C] text-[#503D00]'"
                      class="px-6 py-2 rounded-lg text-sm font-bold transition-colors">
                      {{ selectedRoom && selectedRoom.id === room.id ? 'تم الاختيار ✓' : 'اختيار' }}
                    </button>
                    <p class="text-right">
                      <span class="text-2xl font-bold text-[#1A3C5E]">{{ room.price.toLocaleString() }} ج.م</span>
                      <span class="block text-xs text-[#4D4637]">/ الليلة</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Social proof banner -->
          <div class="bg-[#C9A84C] rounded-xl px-6 py-6 flex items-center justify-between gap-4">
            <svg class="w-6 h-6 text-[#503D00] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
            <div class="text-right">
              <h4 class="text-xl font-bold text-[#503D00]">{{ hotel.socialProof.title }}</h4>
              <p class="text-sm text-[#503D00]/90">{{ hotel.socialProof.subtitle }}</p>
            </div>
          </div>

          <!-- Reviews summary -->
          <section class="flex flex-col gap-6">
            <h3 class="text-2xl font-semibold text-[#1A1C1B] text-right">تقييمات الضيوف</h3>

            <div class="bg-[#F4F4F2] rounded-xl p-6 grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
              <div v-for="rb in hotel.ratingBreakdown" :key="rb.label" class="flex flex-col gap-1">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-sm text-[#1A1C1B]">{{ rb.value }}</span>
                  <span class="text-sm text-[#1A1C1B]">{{ rb.label }}</span>
                </div>
                <div class="w-full h-2 bg-[#E8E8E6] rounded-full overflow-hidden">
                  <div class="h-full bg-[#C9A84C] rounded-full" :style="{ width: (rb.value / 5 * 100) + '%' }"></div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="(rev, i) in hotel.reviews" :key="i"
                class="bg-white border border-[#D0C5B2] rounded-xl p-4 flex flex-col gap-3 shadow-sm">
                <div class="flex items-center justify-end gap-2">
                  <div class="text-right">
                    <p class="text-xs font-bold text-[#1A1C1B]">{{ rev.name }}</p>
                    <p class="text-[10px] text-[#4D4637]">{{ rev.source }}</p>
                  </div>
                  <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm shrink-0"
                    :style="{ background: rev.bg, color: rev.color }">{{ rev.initial }}</div>
                </div>
                <p class="text-sm text-[#1A1C1B] text-right leading-5">{{ rev.text }}</p>
                <button v-if="rev.hasPhoto" @click="openReviewPhotos"
                  class="flex items-center justify-end gap-1 text-xs font-bold text-[#C9A84C] pt-2 border-t border-[#F4F4F2]">
                  صور من هذا التقييم
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M14 8h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                </button>
              </div>
            </div>
          </section>

          <!-- Fasahny moments -->
          <section v-if="hotel.moments.length" class="bg-[#F4F4F2]/50 border border-[#D0C5B2]/30 rounded-2xl p-6 flex flex-col gap-4">
            <div class="flex items-center justify-between">
              <button @click="openAllMoments" class="flex items-center gap-1 text-sm font-bold text-[#C9A84C]">
                عرض الكل
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7 7-7m9 14l-7-7 7-7"/></svg>
              </button>
              <div class="flex items-center gap-3">
                <h3 class="text-xl font-bold text-[#1A1C1B]">لحظات من فسحني</h3>
                <span class="bg-[#C9A84C]/10 text-[#C9A84C] text-[10px] font-bold px-3 py-1 rounded-full">{{ hotel.moments.length }} منشور من مسافرين حقيقيين</span>
              </div>
            </div>
            <div class="flex items-stretch gap-4 overflow-x-auto pb-2">
              <div v-for="(m, i) in hotel.moments" :key="i"
                class="relative w-45 h-55 shrink-0 rounded-xl overflow-hidden border border-[#D0C5B2] group cursor-pointer">
                <img :src="m.image" class="w-full h-40 object-cover" alt="" />
                <div class="absolute top-2 right-2 w-6 h-6 rounded-full flex items-center justify-center text-[8px] font-bold text-white border border-white/50"
                  :style="{ background: m.color }">{{ m.initial }}</div>
                <div class="p-2 flex flex-col gap-1">
                  <p class="text-[10px] text-[#1A1C1B] text-right leading-tight">{{ m.caption }}</p>
                  <p class="text-[8px] text-[#4D4637] text-right">{{ m.date }}</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Map -->
          <section class="flex flex-col gap-4">
            <h3 class="text-2xl font-semibold text-[#1A1C1B] text-right">الموقع</h3>
            <div class="relative h-75 border border-[#D0C5B2] rounded-xl overflow-hidden flex items-center justify-center">
              <div class="absolute inset-0 opacity-40" :style="{ background: `linear-gradient(#fff,#fff), url('${hotel.image}')`, backgroundBlendMode: 'saturation', backgroundSize: 'cover' }"></div>
              <button @click="openMap"
                class="relative flex items-center gap-2 bg-[#1A3C5E] hover:bg-[#152f4a] text-white font-bold px-6 py-2.5 rounded-full transition-colors">
                استكشاف الخريطة التفاعلية
                <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
              </button>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div v-for="n in nearby" :key="n.name" class="bg-[#EEEEEC] rounded-lg p-3 flex items-center justify-end gap-3">
                <div class="text-right">
                  <p class="text-sm font-bold text-[#1A1C1B]">{{ n.name }}</p>
                  <p class="text-xs text-[#4D4637]">{{ n.duration }}</p>
                </div>
                <svg class="w-5 h-5 text-[#C9A84C] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
              </div>
            </div>
          </section>
        </div>

        <!-- ===================== BOOKING CARD (sticky) ===================== -->
        <aside class="order-1 lg:order-2 w-full lg:sticky lg:top-24">
          <div class="bg-white border border-[#D0C5B2] rounded-2xl p-6 pb-8 flex flex-col gap-6 shadow-[0_20px_25px_-5px_rgba(228,228,231,0.5),0_8px_10px_-6px_rgba(228,228,231,0.5)]">

            <div class="flex items-center justify-between">
              <span class="flex items-center gap-1 text-[#C9A84C] font-bold text-sm">
                تأكيد فوري
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/></svg>
              </span>
              <p class="text-right">
                <span class="text-3xl font-bold text-[#1A3C5E]">{{ activeRoomPrice.toLocaleString() }} ج.م</span>
                <span class="text-sm text-[#4D4637]"> / الليلة</span>
              </p>
            </div>

            <!-- Dates -->
            <div class="border border-[#D0C5B2] rounded-xl overflow-hidden flex">
              <div class="flex-1 bg-[#F4F4F2] p-3 flex flex-col gap-1 items-end">
                <label class="text-[10px] font-bold text-[#4D4637]">تسجيل المغادرة</label>
                <input v-model="checkOut" class="text-sm font-bold text-[#1A1C1B] bg-transparent text-right w-full focus:outline-none" />
              </div>
              <div class="flex-1 bg-[#F4F4F2] border-l border-[#D0C5B2] p-3 flex flex-col gap-1 items-end">
                <label class="text-[10px] font-bold text-[#4D4637]">تسجيل الوصول</label>
                <input v-model="checkIn" class="text-sm font-bold text-[#1A1C1B] bg-transparent text-right w-full focus:outline-none" />
              </div>
            </div>

            <!-- Guests -->
            <div class="border border-[#D0C5B2] rounded-xl">
              <button @click="guestsPanelOpen = !guestsPanelOpen" class="w-full flex items-center justify-between p-4">
                <svg :class="guestsPanelOpen ? 'rotate-180' : ''" class="w-3 h-2 text-[#4D4637] transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"/></svg>
                <div class="text-right">
                  <p class="text-xs font-bold text-[#4D4637]">الضيوف</p>
                  <p class="text-sm font-bold text-[#1A1C1B]">{{ adults }} بالغين، {{ children }} طفل</p>
                </div>
              </button>
              <div v-if="guestsPanelOpen" class="border-t border-[#D0C5B2] p-4 flex flex-col gap-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <button @click="adults = Math.min(10, adults + 1)" class="w-7 h-7 rounded-full border border-[#D0C5B2] text-[#1A3C5E] font-bold">+</button>
                    <span class="text-sm w-4 text-center">{{ adults }}</span>
                    <button @click="adults = Math.max(1, adults - 1)" class="w-7 h-7 rounded-full border border-[#D0C5B2] text-[#1A3C5E] font-bold">−</button>
                  </div>
                  <span class="text-sm text-[#1A1C1B]">بالغين</span>
                </div>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <button @click="children = Math.min(6, children + 1)" class="w-7 h-7 rounded-full border border-[#D0C5B2] text-[#1A3C5E] font-bold">+</button>
                    <span class="text-sm w-4 text-center">{{ children }}</span>
                    <button @click="children = Math.max(0, children - 1)" class="w-7 h-7 rounded-full border border-[#D0C5B2] text-[#1A3C5E] font-bold">−</button>
                  </div>
                  <span class="text-sm text-[#1A1C1B]">أطفال</span>
                </div>
              </div>
            </div>

            <!-- Selected room -->
            <div v-if="selectedRoom" class="flex items-center justify-between text-sm bg-[#FDF8EC] rounded-lg px-3 py-2">
              <span class="text-[#C9A84C] font-bold">{{ selectedRoom.price.toLocaleString() }} ج.م</span>
              <span class="text-[#1A1C1B]">{{ selectedRoom.name }}</span>
            </div>

            <!-- Price breakdown -->
            <div class="flex flex-col gap-2 border-t border-[#E8E4DC] pt-4 text-sm">
              <div class="flex items-center justify-between text-[#4D4637]">
                <span>{{ activeRoomPrice.toLocaleString() }} ج.م × {{ nights }} ليالٍ</span>
                <span>{{ totalPrice.toLocaleString() }} ج.م</span>
              </div>
              <div class="flex items-center justify-between font-bold text-[#1A1C1B] pt-2 border-t border-[#E8E4DC]">
                <span>{{ totalPrice.toLocaleString() }} ج.م</span>
                <span>الإجمالي</span>
              </div>
            </div>

            <button @click="confirmBooking"
              class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#503D00] font-bold py-3.5 rounded-xl transition-colors">
              تأكيد الحجز
            </button>
          </div>
        </aside>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-[#FAFAF8] border-t border-[#E8E4DC] py-12 px-8 flex flex-col md:flex-row items-center justify-between gap-6 max-w-360 mx-auto">
      <div class="text-right">
        <p class="text-lg font-bold text-[#C9A84C]">فسحني</p>
        <p class="text-sm text-[#71717A]">© 2024 فسحني مصر. تجربة مصرية كلاسيكية.</p>
      </div>
      <nav class="flex flex-wrap items-center justify-center gap-6">
        <a href="#" class="text-sm text-[#71717A] hover:text-[#1A3C5E]">تواصل معنا</a>
        <a href="#" class="text-sm text-[#71717A] hover:text-[#1A3C5E]">سياسة الإلغاء</a>
        <a href="#" class="text-sm text-[#71717A] hover:text-[#1A3C5E]">الأسئلة الشائعة</a>
        <a href="#" class="text-sm text-[#71717A] hover:text-[#1A3C5E]">عن الفندق</a>
      </nav>
    </footer>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>