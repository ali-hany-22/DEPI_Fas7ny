<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

const destinations = [
  { name: 'القاهرة', desc: 'مدينة الألف مئذنة، حيث يلتقي التاريخ بالحياة العصرية', activities: 45, badge: 'فرعوني', temp: '24°', img: 'https://i.pinimg.com/736x/09/c6/a4/09c6a4529fc49166840b1d2571b081ea.jpg' },
  { name: 'الأقصر', desc: 'أكبر متحف مفتوح في العالم في قلب مصر القديمة', activities: 32, badge: 'فرعوني', temp: '28°', img: 'https://i.pinimg.com/736x/c7/c9/f6/c7c9f67dc65f021d04b7778877e6094b.jpg' },
  { name: 'أسوان', desc: 'أجمل غروب الشمس وجمال النوبة بطبيعة خلابة', activities: 28, badge: 'استجمام', temp: '28°', img: 'https://i.pinimg.com/1200x/f0/22/f1/f022f1e758cad6193f895adc14a8700d.jpg' },
  { name: 'سيوة', desc: 'واحة النجوم والسكون والمغامرة الصحراوية', activities: 15, badge: null, temp: '22°', img: 'https://i.pinimg.com/736x/79/16/79/791679f6b7657079b1dabdf541964e06.jpg' },
  { name: 'الإسكندرية', desc: 'عروس البحر المتوسط وتاريخ من أعماق الزمن', activities: 22, badge: 'بام', temp: '20°', img: 'https://i.pinimg.com/1200x/2b/22/a1/2b22a1538fc771aa9e2ffa724220b8ea.jpg' },
  { name: 'شرم الشيخ', desc: 'جنة الغوص والشعاب المرجانية على البحر الأحمر', activities: 60, badge: 'شاطئ', temp: '26°', img: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=600&q=80' },
]

const tripTypes = [
  { label: 'فرعوني وثقافي', desc: 'رحلة معرفية وتاريخ مع مرشدين متخصصين', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/ankh.png', path: '/search?type=cultural' },
  { label: 'شاطئ وغوص', desc: 'استمتع بأجمل الشواطئ وعالم البحار الساحر في البحر الأحمر', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/sunbathe.png', path: '/search?type=beach', featuredLabel: 'الأكثر طلبا' },
  { label: 'صحراء ومغامرة', desc: 'تجربة السفاري الفريدة في أعماق الصحراء', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/pyramids.png', path: '/search?type=desert' },
]

const recommended = [
  { name: 'معبد الأقصر', type: 'تذكرة', price: 100, rating: 4.9, badge: 'تاريخي', img: 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=400&q=80', path: '/city/الأقصر' },
  { name: 'مطعم أبو طارق', type: 'من', price: 150, rating: 4.1, badge: 'هلال', img: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&q=80', path: '/restaurants' },
  { name: 'فندق أولد كاتاراكت', type: 'من', price: 4200, rating: 5.0, badge: 'هلال', img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80', path: '/hotel/old-cataract' },
  { name: 'فندق ماريوت مينا هاوس', type: 'من', price: 3500, rating: 4.8, badge: 'هلال', img: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80', path: '/hotel/marriott-mena-house' },
]

const features = [
  { title: 'تقييمات موثوقة', desc: 'آلاف التقييمات الأصيلة من مسافرين حقيقيين', icon: 'https://img.icons8.com/ios/50/C9A84C/security-checked--v1.png' },
  { title: 'منصة متكاملة', desc: 'كل ما تحتاجه في منصة واحدة من الحجز حتى العودة', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/centralized-network.png' },
  { title: 'ذكاء اصطناعي منظور', desc: 'نظام ذكي يتعلم من تفضيلاتك ليرشح أفضل الخيارات', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/sparkling--v1.png' },
  { title: 'مرشدون معتمدون', desc: 'شبكة من أفضل المرشدين وشركات السياحة المعتمدة', icon: 'https://img.icons8.com/ios-filled/50/C9A84C/goal--v1.png' },
]

const steps = [
  { num: '1', title: 'اختر وجهتك', desc: 'حدد المدن التي تريد زيارتها وفقاً لاهتماماتك' },
  { num: '2', title: 'خطط الذكاء الاصطناعي', desc: 'يقوم نظامنا الذكي بتحليل الإقامة والأنشطة والمكان' },
  { num: '3', title: 'احجز واستمتع', desc: 'قم بحجز رحلتك بنقرة واحدة وادخل عالم المغامرة' },
]

const footerLinks = {
  استكشف: ['أفضل الوجهات', 'المسارات', 'التجارب', 'أكمل المقارنة'],
  الخدمات: ['الاقامة (فنادق و شقق...)', 'المواصلات (طيران وسيارات...)', 'الطعام والترفيه (مطاعم...)', 'المعالم والانشطة'],
  فسحني: ['الـ feed (لحظات المسافرين)', 'شارك لحظة (ضيف صور رحلتك)', 'الأكثر تفاعلا (اشهر اللحظات)'],
  المساعدة: ['مركز الدعم', 'سياسة الخصوصية', 'الشروط والأحكام', 'أمن بنا'],
}

const aiForm = ref({ destination: 'القاهرة', days: 5, people: 2, budget: 'متوسطة' })
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8] font-cairo">
    <Navbar />

    <!-- Hero -->
    <section class="relative min-h-140 md:h-160 flex items-center pt-16">
      <img src="https://i.pinimg.com/1200x/db/b7/f8/dbb7f898533d90d71cdfeaf121792798.jpg" class="absolute inset-0 w-full h-full object-cover" alt="" />
      <div class="relative z-10 w-full max-w-7xl mx-auto px-4 md:px-8 py-10 md:py-0 flex flex-col md:flex-row items-center justify-between gap-8">

        <!-- Hero Text -->
        <div class="text-white w-full md:max-w-lg text-center md:text-right">
          <h1 class="text-3xl md:text-5xl font-bold leading-tight mb-4">خطط رحلتك المثالية في مصر بكل سهولة</h1>
          <p class="text-gray-200 text-sm md:text-base leading-relaxed mb-6">اكتشف عجائب الحضارة المصرية من خلال خطط رحلة مدعومة بالذكاء الاصطناعي مخصصة لاهتماماتك وميزانيتك.</p>
          <div class="flex gap-3 justify-center md:justify-start">
            <button @click="router.push('/book-trip')" class="bg-[#C9A84C] hover:bg-[#b8963f] text-white px-6 py-3 rounded-lg font-semibold transition-colors text-sm">
              ابدأ خطط رحلتك
            </button>
            <button @click="router.push('/chat')" class="flex items-center gap-2 border border-white/70 text-white px-6 py-3 rounded-lg hover:bg-white/10 transition-colors text-sm backdrop-blur-sm">
<img width="24" height="24" src="https://img.icons8.com/forma-thin/24/bard.png" alt="bard"/>  
         اتكلم مع الذكاء الاصطناعي
            </button>
          </div>
        </div>

        <!-- AI Card -->
        <div class="bg-white rounded-2xl p-5 shadow-2xl w-full max-w-sm shrink-0">
          <div class="flex items-center justify-between mb-4">
            <span class="font-bold text-sm text-[#1A3C5E]">مساعد الرحلة الذكي</span>
            <span class="text-xs bg-green-100 text-green-600 px-2 py-0.5 rounded-full">متاح دائماً</span>
          </div>
          <div class="mb-3">
            <label class="text-xs text-gray-500 block mb-2">إلى أين تريد الذهاب؟</label>
            <div class="flex gap-2 flex-wrap">
              <button v-for="d in ['القاهرة','الأقصر','أسوان','المزيد']" :key="d"
                @click="aiForm.destination = d"
                :class="aiForm.destination === d ? 'bg-[#C9A84C] text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                class="text-xs px-3 py-1.5 rounded-full transition-colors">{{ d }}</button>
            </div>
          </div>
          <div class="flex gap-3 mb-3">
            <div class="flex-1">
              <label class="text-xs text-gray-500 block mb-1">المدة</label>
              <input v-model="aiForm.days" type="number" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#C9A84C]" />
            </div>
            <div class="flex-1">
              <label class="text-xs text-gray-500 block mb-1">عدد الأفراد</label>
              <input v-model="aiForm.people" type="number" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#C9A84C]" />
            </div>
          </div>
          <div class="mb-4">
            <label class="text-xs text-gray-500 block mb-1">الميزانية التقديرية</label>
            <select v-model="aiForm.budget" class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#C9A84C]">
              <option>اقتصادية</option>
              <option>متوسطة</option>
              <option>فاخرة</option>
            </select>
          </div>
          <button @click="router.push('/book-trip')" class="w-full bg-[#C9A84C] hover:bg-[#b8963f] text-white py-3 rounded-lg font-semibold transition-colors text-sm">
            اعمل خطتك الآن
          </button>
        </div>
      </div>
    </section>

    <!-- Destinations -->
    <section class="max-w-7xl mx-auto px-4 md:px-8 py-12 md:py-16">
      <div class="flex items-start justify-between mb-6 md:mb-8">
        <div>
          <h2 class="text-xl md:text-2xl font-bold text-[#1A3C5E]">وجهات مختارة لك</h2>
          <p class="text-gray-500 text-xs md:text-sm mt-1">اكتشف أفضل المدن المصرية التي تجمع بين التاريخ والجمال</p>
        </div>
        <button @click="router.push('/search')" class="text-[#C9A84C] text-sm font-medium hover:underline whitespace-nowrap">عرض الكل</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="city in destinations" :key="city.name"
          @click="router.push('/city/' + city.name)"
          class="relative rounded-xl overflow-hidden cursor-pointer group"
          style="height: 220px;">
          <img :src="city.img" class="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500" :alt="city.name" />
          <div class="absolute inset-0 bg-linear-to-t from-black/80 via-black/20 to-transparent"></div>
          <div class="absolute top-3 left-3 bg-black/40 text-white text-xs px-2 py-0.5 rounded backdrop-blur-sm">{{ city.temp }}</div>
          <div v-if="city.badge" class="absolute top-3 right-3 bg-[#C9A84C] text-white text-xs px-2.5 py-1 rounded font-medium">{{ city.badge }}</div>
          <div class="absolute bottom-4 right-4 text-white">
            <h3 class="font-bold text-lg leading-tight">{{ city.name }}</h3>
            <p class="text-xs text-gray-300 mt-0.5 max-w-50 leading-snug">{{ city.desc }}</p>
            <p class="text-xs text-[#C9A84C] mt-1.5">{{ city.activities }} نشاط متاح</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Trip Types -->
    <section class="bg-white py-12 md:py-14">
      <div class="max-w-7xl mx-auto px-4 md:px-8 flex flex-col sm:flex-row justify-center gap-5 md:gap-8 items-stretch">
        <div v-for="type in tripTypes" :key="type.label"
          class="relative rounded-xl p-6 md:p-8 text-center w-full sm:w-52 md:w-60 transition-all duration-300 bg-[#FAFAF8] border border-gray-100 shadow-sm hover:bg-[#1A3C5E] hover:shadow-xl group">
          <span v-if="type.featuredLabel" class="absolute top-3 left-3 bg-[#C9A84C] text-white text-xs px-2.5 py-1 rounded font-medium">{{ type.featuredLabel }}</span>
          <div class="w-14 h-14 rounded-full mx-auto mb-4 bg-[#C9A84C]/15 group-hover:bg-[#C9A84C]/20 flex items-center justify-center transition-colors duration-300">
            <img :src="type.icon" class="w-7 h-7" :alt="type.label" />
          </div>
          <h3 class="font-bold text-base mb-2 text-gray-800 group-hover:text-white transition-colors duration-300">{{ type.label }}</h3>
          <p class="text-xs leading-relaxed text-gray-500 group-hover:text-blue-200 transition-colors duration-300 mb-4">{{ type.desc }}</p>
          <button
            @click.stop="router.push(type.path)"
            class="border border-transparent text-transparent group-hover:border-white group-hover:text-white text-xs px-5 py-2 rounded-lg transition-all duration-300 hover:bg-white/10">
            استكشف العروض
          </button>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="bg-[#1A3C5E] text-white py-12 md:py-16">
      <div class="max-w-7xl mx-auto px-4 md:px-8 text-center">
        <h2 class="text-xl md:text-2xl font-bold mb-10 md:mb-14">كيف نبني رحلتك؟</h2>
        <div class="flex flex-col sm:flex-row justify-center gap-10 md:gap-16">
          <div v-for="step in steps" :key="step.num" class="max-w-xs mx-auto sm:mx-0">
            <div class="w-12 h-12 rounded-full bg-[#C9A84C] flex items-center justify-center text-lg font-bold mx-auto mb-4 text-white">{{ step.num }}</div>
            <h3 class="font-bold mb-2 text-base">{{ step.title }}</h3>
            <p class="text-blue-200 text-sm leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Recommended -->
    <section class="max-w-7xl mx-auto px-4 md:px-8 py-12 md:py-16">
      <h2 class="text-xl md:text-2xl font-bold text-[#1A3C5E] mb-6 md:mb-8 text-center">أماكن نوصي بها</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="place in recommended" :key="place.name"
          @click="router.push(place.path)"
          class="rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer bg-white border border-gray-100">
          <div class="relative">
            <img :src="place.img" class="w-full h-32 md:h-36 object-cover" :alt="place.name" />
            <span v-if="place.badge" class="absolute top-2 right-2 bg-[#C9A84C] text-white text-xs px-2 py-0.5 rounded-full">{{ place.badge }}</span>
          </div>
          <div class="p-3">
            <div class="flex items-center gap-1 mb-1">
              <svg class="w-3.5 h-3.5 fill-[#C9A84C]" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span class="text-xs text-gray-500">{{ place.rating }}</span>
            </div>
            <h3 class="font-bold text-xs md:text-sm text-[#1A3C5E] mb-1">{{ place.name }}</h3>
            <p class="text-[#C9A84C] text-xs md:text-sm font-semibold">{{ place.type }} {{ place.price }} ج.م</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-white py-12 md:py-14">
      <div class="max-w-7xl mx-auto px-4 md:px-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-10 text-center">
          <div v-for="f in features" :key="f.title">
            <div class="w-14 h-14 rounded-full bg-[#C9A84C]/15 mx-auto mb-4 flex items-center justify-center">
              <img :src="f.icon" class="w-7 h-7" :alt="f.title" />
            </div>
            <h3 class="font-bold text-[#1A3C5E] mb-2 text-sm md:text-base">{{ f.title }}</h3>
            <p class="text-gray-500 text-xs md:text-sm leading-relaxed">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-[#1A3C5E] text-white py-12 md:py-14">
      <div class="max-w-7xl mx-auto px-4 md:px-8">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8 mb-10">
          <!-- Brand -->
          <div class="col-span-2 md:col-span-1">
            <div class="flex items-center gap-2 mb-3">
              <img src="https://img.icons8.com/ios/50/C9A84C/world-map.png" class="w-6 h-6" alt="logo" />
              <h3 class="text-[#C9A84C] font-bold text-xl">فسحني</h3>
            </div>
            <p class="text-blue-200 text-xs leading-relaxed">منصة لاكتشاف الحضارة المصرية وتجارب سياحية مخصصة بالذكاء الاصطناعي.</p>
          </div>
          <!-- Links -->
          <div v-for="(links, title) in footerLinks" :key="title">
            <h4 class="font-semibold mb-4 text-sm text-[#C9A84C]">{{ title }}</h4>
            <ul class="space-y-2.5 text-blue-200 text-xs">
              <li v-for="link in links" :key="link">
                <a href="#" class="hover:text-white transition-colors">{{ link }}</a>
              </li>
            </ul>
          </div>
        </div>
        <div class="border-t border-[#1A3C5E]/50 pt-6 flex flex-col md:flex-row justify-between items-center gap-2 text-blue-300 text-xs">
          <span>2024 فسحني - جميع الحقوق محفوظة</span>
          <span>اكتشف سحر مصر بروح عصرية ذكية</span>
        </div>
      </div>
    </footer>
  </div>
</template>