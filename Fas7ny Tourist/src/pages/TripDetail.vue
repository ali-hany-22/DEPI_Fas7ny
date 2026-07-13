<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const route = useRoute()

/* =========================================================================
   TRIPS DATA
   Add a new key here for every shareable trip. TripCard.vue links to
   `/trip/:id` using these same ids, so keep them in sync with any place
   that renders a TripCard (Community.vue, Search.vue, TripHistory.vue...).
   ========================================================================= */
const tripsData = {
  'siwa-oasis': {
    id: 'siwa-oasis',
    title: 'أسبوع في واحة سيوة: رمال وسكون',
    heroImage: 'https://i.pinimg.com/1200x/7c/a3/d4/7ca3d48f965c5c48c448ae85a9eb21c0.jpg',
    authorName: 'مريم ناصر',
    authorAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&q=80',
    days: 7,
    locations: 14,
    likes: 2400,
    priceStart: 12400,
    budget: 'اقتصادي',
    timing: 'شتاء ٢٠٢٥',
    tripType: 'استجمام / مغامرة',
    about: 'تجربة فريدة من نوعها لمحبي الهدوء والابتعاد عن صخب المدينة. سيوة عالم آخر يسكنه الصمت والجمال الطبيعي.',
    mapLabel: 'واحة سيوة',
    travelers: [
      { name: 'أحمد', img: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&q=80' },
      { name: 'نور', img: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=80&q=80' },
    ],
    travelersExtra: 2,
    gear: ['نظارة شمس', 'كريم شمس', 'حذاء مريح', 'مطرة مياه'],
    days_detail: [
      {
        num: 1,
        title: 'اليوم ١: الوصول والاستجمام',
        dotColor: '#755B00',
        desc: 'وصلنا إلى واحة سيوة بعد رحلة طويلة ولكنها ممتعة. بدأنا يومنا الأول بهدوء، حيث توجهنا للفندق وقمنا بجولة سريعة في شالي سيوة القديمة عند الغروب. الهدوء هنا لا يوصف.',
        images: [
          { src: 'https://i.pinimg.com/736x/35/64/3c/35643c804281c69c9612202aea3b58e3.jpg', label: 'فندق جعفر' },
          { src: 'https://i.pinimg.com/1200x/0b/71/53/0b7153f7b71bea24ae049c0176f9ae28.jpg', label: 'قلعة شالي' },
        ],
        place: { name: 'فندق جعفر الصديق', rating: 4.8, type: 'طراز سيوة التقليدي' },
      },
      {
        num: 2,
        title: 'اليوم ٢: عيون المياه وجزيرة فطناس',
        dotColor: '#C9A84C',
        desc: 'انطلقنا مبكراً لزيارة عين كليوباترا، ثم قضينا فترة بعد الظهر في جزيرة فطناس. الاستمتاع بكوب من الشاي السيوي أثناء مشاهدة الشمس تغوص في البحيرة كان لحظة لا تُنسى.',
        images: [
          { src: 'https://i.pinimg.com/736x/e1/44/64/e14464b8ec4cba89d7f5f7c3ef514aab.jpg', label: 'عين كليوباترا' },
          { src: 'https://i.pinimg.com/736x/c3/03/6d/c3036dd215b840d92a14984b0ecea6ff.jpg', label: 'جزيرة فطناس' },
          { src: 'https://i.pinimg.com/736x/61/cb/c0/61cbc04418568668a946b2cdd27be246.jpg', label: 'شمس تغوص' },
        ],
        place: { name: 'عين كليوباترا', rating: 4.5, type: 'موقع تاريخي • سباحة طبيعية' },
      },
      {
        num: 3,
        title: 'بقية أيام الرحلة (٣ - ٧)...',
        dotColor: '#D0C5B2',
        desc: 'استكشاف بحيرات الملح، رحلة السفاري الكبرى، وجبل الموتى.',
        images: [],
        place: null,
        locked: true,
      },
    ],
  },

  'luxor-aswan-4days': {
    id: 'luxor-aswan-4days',
    title: '٤ أيام بين معابد الأقصر وأسوان',
    heroImage: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=1200&q=80',
    authorName: 'أحمد سمير',
    authorAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&q=80',
    days: 4,
    locations: 9,
    likes: 1560,
    priceStart: 9800,
    budget: 'متوسط',
    timing: 'خريف ٢٠٢٤',
    tripType: 'تاريخي / ثقافي',
    about: 'رحلة مكثفة بين عاصمتي مصر الفرعونية القديمة، من معابد الكرنك إلى معبد فيلة، مع ليلة على متن مركب نيلي تقليدي.',
    mapLabel: 'الأقصر وأسوان',
    travelers: [
      { name: 'مريم', img: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&q=80' },
    ],
    travelersExtra: 1,
    gear: ['قبعة شمس', 'كريم شمس', 'حذاء مشي', 'كاميرا'],
    days_detail: [
      {
        num: 1,
        title: 'اليوم ١: الأقصر - عبق التاريخ',
        dotColor: '#755B00',
        desc: 'بدأنا برحلة إلى معبد الكرنك عند الفجر لتفادي الزحام، ثم توجهنا لمعبد الأقصر عند الغروب حيث الإضاءة الذهبية الساحرة.',
        images: [
          { src: 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80', label: 'معابد الكرنك' },
          { src: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80', label: 'معبد الأقصر' },
        ],
        place: { name: 'مجمع معابد الكرنك', rating: 4.9, type: 'موقع أثري • يونسكو' },
      },
      {
        num: 2,
        title: 'اليوم ٢: وادي الملوك وأسوان',
        dotColor: '#C9A84C',
        desc: 'زيارة وادي الملوك في الصباح، ثم انتقلنا مساءً إلى أسوان لبدء رحلة الفلوكة بين الجزر الخضراء.',
        images: [
          { src: 'https://images.unsplash.com/photo-1568402102990-bc541580b59f?w=800&q=80', label: 'وادي الملوك' },
          { src: 'https://images.unsplash.com/photo-1591608971362-f08b2a75731a?w=800&q=80', label: 'فلوكة أسوان' },
        ],
        place: { name: 'وادي الملوك', rating: 4.8, type: 'مقابر فرعونية' },
      },
      {
        num: 3,
        title: 'بقية أيام الرحلة (٣ - ٤)...',
        dotColor: '#D0C5B2',
        desc: 'معبد فيلة، السد العالي، وليلة على متن مركب نيلي تقليدي.',
        images: [],
        place: null,
        locked: true,
      },
    ],
  },

  'cairo-weekend': {
    id: 'cairo-weekend',
    title: 'نهاية أسبوع في القاهرة القديمة',
    heroImage: 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200&q=80',
    authorName: 'نور حسن',
    authorAvatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=80&q=80',
    days: 2,
    locations: 6,
    likes: 890,
    priceStart: 3200,
    budget: 'اقتصادي',
    timing: 'طوال العام',
    tripType: 'ثقافي / تسوق',
    about: 'جولة سريعة ومكثفة بين الأهرامات وخان الخليلي، مثالية لمن عنده يومين بس في القاهرة.',
    mapLabel: 'القاهرة الكبرى',
    travelers: [
      { name: 'أحمد', img: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&q=80' },
      { name: 'مريم', img: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&q=80' },
    ],
    travelersExtra: 0,
    gear: ['حذاء مريح', 'مياه', 'كاميرا موبايل'],
    days_detail: [
      {
        num: 1,
        title: 'اليوم ١: الأهرامات والمتحف المصري الكبير',
        dotColor: '#755B00',
        desc: 'يوم كامل بين أهرامات الجيزة وأبو الهول، وزيارة مسائية للمتحف المصري الكبير الجديد.',
        images: [
          { src: 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800&q=80', label: 'أهرامات الجيزة' },
        ],
        place: { name: 'أهرامات الجيزة وأبو الهول', rating: 4.9, type: 'عجائب الدنيا السبع' },
      },
      {
        num: 2,
        title: 'اليوم ٢: خان الخليلي ووسط البلد',
        dotColor: '#D0C5B2',
        desc: 'تسوق وأكل شعبي في خان الخليلي، ونزهة مسائية في وسط البلد التاريخي.',
        images: [],
        place: null,
        locked: true,
      },
    ],
  },
}

/* =========================================================================
   RESOLVE TRIP FROM ROUTE — falls back to the Siwa trip if the id
   is missing or unknown, so old links / direct visits never break.
   ========================================================================= */
const trip = computed(() => tripsData[route.params.id] || tripsData['siwa-oasis'])
const days = computed(() => trip.value.days_detail)

const expandedDay = ref(0)
const question = ref('')

const askQuestion = () => {
  if (!question.value.trim()) return
  // TODO: send the question to the trip author, e.g. api.post(`/trips/${trip.value.id}/questions`, { text: question.value })
  question.value = ''
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7] font-[Cairo]">
    <Navbar />

    <!-- Hero -->
    <div class="relative w-full h-150 mt-18">
      <img :src="trip.heroImage" class="w-full h-full object-cover" :alt="trip.title" />

      <!-- Trip meta bottom -->
      <div class="absolute bottom-16 right-0 left-0 max-w-328 mx-auto px-16 flex items-end justify-between">
        <button @click="router.push('/book-trip')"
          class="flex items-center gap-2 bg-[#755B00] hover:bg-[#634c00] text-white px-5 py-3 rounded-xl text-sm font-semibold transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          احجز رحلة مشابهة
        </button>

        <div class="text-right text-white">
          <h1 class="text-[48px] leading-15 font-bold mb-4">{{ trip.title }}</h1>
          <div class="flex items-center gap-4 text-sm justify-end mb-3">
            <div class="flex items-center gap-2">
              <span>{{ trip.authorName }}</span>
              <img :src="trip.authorAvatar" class="w-10 h-10 rounded-full object-cover border-2 border-[#755B00]" alt="" />
            </div>
          </div>
          <div class="flex items-center gap-4 text-sm justify-end">
            <div class="flex items-center gap-2">
              <span>{{ trip.days }} أيام</span>
              <svg class="w-4.5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            </div>
            <span class="w-px h-4 bg-white/30"></span>
            <div class="flex items-center gap-2">
              <span>{{ trip.locations }} موقع</span>
              <svg class="w-4 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            </div>
            <span class="w-px h-4 bg-white/30"></span>
            <div class="flex items-center gap-2">
              <span>{{ trip.likes.toLocaleString() }}</span>
              <svg class="w-5 h-4.5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            </div>
            <span class="w-px h-4 bg-white/30"></span>
            <div class="flex items-center gap-2">
              <span>مشاركة</span>
              <svg class="w-4 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-360 mx-auto px-16 py-16">
      <div class="grid grid-cols-1 lg:grid-cols-[326px_1fr] gap-16 items-start">

        <!-- Right / Sidebar -->
        <div class="space-y-8 order-2 lg:order-1">

          <!-- Trip info -->
          <div class="bg-white rounded-xl p-6 border border-[#D0C5B2]">
            <h3 class="font-normal text-lg text-[#755B00] mb-4 text-right">عن الرحلة</h3>
            <div class="space-y-4 text-sm">
              <div class="flex justify-between items-center">
                <span class="text-[#4D4637]">الميزانية</span>
                <span class="bg-[#EEEEEC] text-[#1A1C1B] font-semibold px-2 py-1 rounded-full">{{ trip.budget }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-[#4D4637]">التوقيت</span>
                <span class="text-[#1A1C1B] font-semibold">{{ trip.timing }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-[#4D4637]">نوع الرحلة</span>
                <span class="text-[#1A1C1B] font-semibold">{{ trip.tripType }}</span>
              </div>
            </div>
            <div class="border-t border-[#D0C5B2] my-4"></div>
            <p class="text-sm text-[#4D4637] leading-6.5 text-right">{{ trip.about }}</p>
          </div>

          <!-- Map -->
          <div class="bg-white rounded-xl border border-[#D0C5B2] overflow-hidden">
            <div class="flex items-center gap-2 justify-end bg-[#EEEEEC] px-4 py-4">
              <h3 class="font-normal text-lg text-[#416084]">خريطة الرحلة</h3>
              <svg class="w-4.5 h-4.5 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
            </div>
            <div class="relative w-full h-64 bg-[#E8E8E6] flex items-center justify-center overflow-hidden">
              <div class="absolute inset-0 opacity-30"
                style="background: radial-gradient(circle at 50% 50%, #C9A84C 0%, rgba(201,168,76,0) 70%);"></div>
              <div class="relative text-center">
                <div class="w-7 h-7 bg-[#755B00] rounded-full mx-auto mb-2 flex items-center justify-center shadow">
                  <svg class="w-3.5 h-3.5 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                </div>
                <p class="text-xs bg-white text-[#1A1C1B] font-medium px-2 py-1 rounded-lg shadow-sm">{{ trip.mapLabel }}</p>
              </div>
            </div>
          </div>

          <!-- Book same trip -->
          <div class="bg-[#FDF8EC] rounded-[20px] p-6 text-right border-2 border-[#755B00]/30 shadow-sm">
            <div class="flex items-center gap-2 justify-end mb-2">
              <h3 class="font-bold text-lg text-[#755B00]">احجز نفس الرحلة دي</h3>
              <svg class="w-6 h-6 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </div>
            <p class="text-sm text-[#4D4637] leading-6.5 mb-4">كل الفنادق، المواصلات، والتذاكر اللي {{ trip.authorName.split(' ')[0] }} استخدمتها في مكان واحد.</p>
            <p class="text-sm text-[#4D4637] mb-1">تبدأ من</p>
            <p class="text-[#755B00] font-semibold text-2xl mb-4">{{ trip.priceStart.toLocaleString() }} ج.م <span class="text-base font-normal text-[#4D4637]">/ للفرد</span></p>
            <button @click="router.push('/book-trip')"
              class="w-full bg-[#755B00] hover:bg-[#634c00] text-white py-3.5 rounded-xl text-sm font-semibold transition-colors flex items-center justify-center gap-2">
              احجز الرحلة كاملة
              <svg class="w-5 h-5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>
            <button @click="router.push('/ai-trip-planner')" class="w-full text-[#755B00] py-2 rounded-lg text-sm font-semibold mt-2 hover:bg-[#755B00]/5 transition-colors">
              عدل في الخطة الأول
            </button>
          </div>

          <!-- Travelers -->
          <div class="bg-white rounded-xl p-6 border border-[#D0C5B2]">
            <h3 class="font-normal text-lg text-[#416084] mb-4 text-right">المسافرين</h3>
            <div class="flex items-center justify-end -space-x-3 space-x-reverse">
              <div v-if="trip.travelersExtra" class="w-12 h-12 rounded-full bg-[#EEEEEC] border-2 border-white flex items-center justify-center text-sm font-semibold text-[#4D4637] z-10">+{{ trip.travelersExtra }}</div>
              <img v-for="t in trip.travelers" :key="t.name" :src="t.img"
                class="w-12 h-12 rounded-full object-cover border-2 border-white" :alt="t.name" />
            </div>
          </div>

          <!-- Recommended gear -->
          <div class="bg-white rounded-xl p-6 border border-[#D0C5B2]">
            <h3 class="font-normal text-lg text-[#416084] mb-4 text-right">معدات مقترحة</h3>
            <div class="grid grid-cols-2 gap-2">
              <span v-for="item in trip.gear" :key="item"
                class="flex items-center justify-end gap-1.5 text-sm bg-[#F4F4F2] text-[#1A1C1B] font-medium px-3 py-2 rounded-lg">
                {{ item }}
                <svg class="w-4 h-4 text-[#755B00] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </span>
            </div>
          </div>

          <!-- Ask the traveler -->
          <div class="bg-[#755B00]/5 rounded-xl p-6 border border-[#755B00]/20">
            <h3 class="font-normal text-lg text-[#755B00] mb-4 text-right">سؤال للمسافر</h3>
            <textarea v-model="question" :placeholder="`اسأل ${trip.authorName.split(' ')[0]} عن تفاصيل الرحلة...`"
              class="w-full bg-white border border-[#D0C5B2] rounded-xl p-4 text-sm text-right focus:outline-none focus:border-[#755B00] resize-none h-26.5"></textarea>
            <button @click="askQuestion" class="w-full bg-[#755B00] hover:bg-[#634c00] text-white py-2.5 rounded-lg text-sm font-medium transition-colors mt-4">
              إرسال السؤال
            </button>
          </div>
        </div>

        <!-- Left: Trip diary / Timeline -->
        <div class="order-1 lg:order-2">
          <div class="flex items-center justify-end gap-2 mb-8">
            <h2 class="text-[32px] leading-10.5 font-semibold text-[#755B00]">يوميات الرحلة</h2>
            <svg class="w-6 h-6 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332-.477-4.5-1.253"/></svg>
          </div>

          <div class="flex flex-col gap-16">
            <div v-for="(day, i) in days" :key="i" class="relative pl-8">

              <!-- Vertical connecting line -->
              <div v-if="i !== days.length - 1" class="absolute right-2.75 top-6 -bottom-16 w-0.5 bg-[#E2E3E1]"></div>

              <!-- Timeline dot -->
              <div class="absolute right-0 top-1 w-6 h-6 rounded-full border-4 border-[#F9F9F7] shadow-sm"
                :style="{ background: day.dotColor }"></div>

              <!-- Day header -->
              <div class="pr-10 text-right">
                <button v-if="!day.locked" @click="expandedDay = expandedDay === i ? -1 : i"
                  class="flex items-center gap-2 justify-end w-full mb-3">
                  <h3 class="text-2xl font-semibold text-[#416084]">{{ day.title }}</h3>
                </button>
                <h3 v-else class="text-2xl font-semibold text-[#4D4637]/60 mb-1">{{ day.title }}</h3>

                <p v-if="day.locked" class="text-base text-[#4D4637]/50">{{ day.desc }}</p>

                <template v-else-if="expandedDay === i">
                  <p class="text-[#4D4637] text-base leading-6.5 mb-4">{{ day.desc }}</p>

                  <!-- Images -->
                  <div v-if="day.images.length" class="grid gap-2 mb-4"
                    :class="day.images.length === 2 ? 'grid-cols-2' : 'grid-cols-3'">
                    <div v-for="(img, j) in day.images" :key="j" class="relative rounded-xl overflow-hidden">
                      <img :src="img.src" class="w-full h-64 object-cover" alt="" />
                      <div v-if="img.label"
                        class="absolute bottom-4 right-4 flex items-center gap-1 bg-black/50 backdrop-blur-sm text-white text-sm px-2 py-1 rounded-lg">
                        <span>{{ img.label }}</span>
                        <svg class="w-3 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      </div>
                    </div>
                  </div>

                  <!-- Place card -->
                  <div v-if="day.place" class="flex items-center justify-between bg-white border border-[#D0C5B2] rounded-xl p-4">
                    <button @click="router.push('/book-trip')"
                      class="border border-[#755B00] text-[#755B00] text-base px-6 py-2.5 rounded-lg hover:bg-[#755B00] hover:text-white transition-colors shrink-0">
                      + أضف للخطة
                    </button>
                    <div class="flex items-center gap-4">
                      <div class="text-right">
                        <p class="font-normal text-[#1A1C1B] text-lg mb-1">{{ day.place.name }}</p>
                        <div class="flex items-center gap-1 justify-end text-sm text-[#4D4637] font-medium">
                          <span>تقييم: {{ day.place.rating }}/٥ • {{ day.place.type }}</span>
                        </div>
                      </div>
                      <img :src="day.images[0].src" class="w-16 h-16 object-cover rounded-lg bg-[#F9F9F7]" alt="" />
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-[#D0C5B2]">
      <div class="max-w-360 mx-auto px-16 py-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <nav class="flex items-center gap-6 order-2 md:order-1">
          <a href="#" class="text-sm font-medium text-[#4D4637] hover:text-[#755B00]">Support</a>
          <a href="#" class="text-sm font-medium text-[#4D4637] hover:text-[#755B00]">Help Center</a>
          <a href="#" class="text-sm font-medium text-[#4D4637] hover:text-[#755B00]">Privacy Policy</a>
          <a href="#" class="text-sm font-medium text-[#4D4637] hover:text-[#755B00]">Terms of Service</a>
          <a href="#" class="text-sm font-medium text-[#4D4637] hover:text-[#755B00]">About Us</a>
        </nav>
        <div class="text-right order-1 md:order-2">
          <p class="text-2xl font-bold text-[#755B00]">Rehla</p>
          <p class="text-sm font-medium text-[#4D4637]">© 2024 Rehla Egyptian Tourism platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap');
</style>