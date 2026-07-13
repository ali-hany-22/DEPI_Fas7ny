<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

// Search query
const searchQuery = ref('')
const selectedCategory = ref('all')

// Help categories
const categories = [
  { id: 'all', label: 'الكل', icon: 'M4 6a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6z' },
  { id: 'booking', label: 'الحجوزات', icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' },
  { id: 'payments', label: 'المدفوعات', icon: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z' },
  { id: 'trips', label: 'الرحلات', icon: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7' },
  { id: 'account', label: 'الحساب', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' },
  { id: 'technical', label: 'مشاكل تقنية', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
]

// FAQ data
const faqs = ref([
  {
    id: 1,
    category: 'booking',
    question: 'كيف يمكنني حجز رحلة؟',
    answer: 'يمكنك حجز رحلة من خلال الذهاب إلى صفحة "خطط رحلتك" واختيار الوجهة والمدة ونوع الرحلة المفضل لديك. ستقوم منصتنا بتوليد خطة سفر مخصصة لك تشمل الفنادق والمواصلات والأنشطة.',
    expanded: false
  },
  {
    id: 2,
    category: 'booking',
    question: 'هل يمكنني تعديل حجزي بعد التأكيد؟',
    answer: 'نعم، يمكنك تعديل حجك حتى 48 ساعة قبل موعد الرحلة مجاناً. للتعديل، اذهب إلى صفحة "رحلاتي" واختر الرحلة التي تريد تعديلها، ثم اضغط على "تعديل الرحلة".',
    expanded: false
  },
  {
    id: 3,
    category: 'payments',
    question: 'ما هي طرق الدفع المتاحة؟',
    answer: 'نقبل الدفع عبر بطاقات الائتمان (فيزا، ماستركارد)، والمحافظ الإلكترونية (فودافون كاش، أورانج كاش)، والتحويل البنكي. جميع عمليات الدفع مشفرة وآمنة 100%.',
    expanded: false
  },
  {
    id: 4,
    category: 'payments',
    question: 'كيف يمكنني استرداد المبلغ المدفوع؟',
    answer: 'يمكنك طلب استرداد المبلغ خلال 48 ساعة من الحجز. سيتم استرداد المبلغ خلال 5-7 أيام عمل على نفس طريقة الدفع التي استخدمتها. للاسترداد، تواصل مع فريق الدعم عبر صفحة "تواصل معنا".',
    expanded: false
  },
  {
    id: 5,
    category: 'trips',
    question: 'كيف أستطيع مشاركة رحلتي مع الأصدقاء؟',
    answer: 'يمكنك مشاركة رحلتك عبر الضغط على زر "مشاركة" في صفحة تفاصيل الرحلة. ستظهر لك خيارات المشاركة عبر واتساب، فيسبوك، تويتر، أو نسخ الرابط. يمكنك أيضاً مشاركة لحظاتك عبر "فسحني" في صفحة المجتمع.',
    expanded: false
  },
  {
    id: 6,
    category: 'trips',
    question: 'ما هي مدة الرحلة المثالية؟',
    answer: 'المدة المثالية تعتمد على وجهتك ونوع الرحلة. نوصي بـ 5-7 أيام للرحلات التاريخية والثقافية، و7-10 أيام للرحلات التي تجمع بين الاستكشاف والاستجمام. يمكنك تخصيص المدة حسب رغبتك في صفحة "خطط رحلتك".',
    expanded: false
  },
  {
    id: 7,
    category: 'account',
    question: 'كيف يمكنني حذف حسابي؟',
    answer: 'لحذف حسابك، اذهب إلى "الإعدادات" ثم "حذف الحساب". سيُطلب منك تأكيد كلمة المرور. بعد الحذف، ستُحذف جميع بياناتك من نظامنا خلال 30 يوماً.',
    expanded: false
  },
  {
    id: 8,
    category: 'account',
    question: 'كيف يمكنني تغيير كلمة المرور؟',
    answer: 'يمكنك تغيير كلمة المرور من خلال الذهاب إلى "الإعدادات" ثم "تغيير كلمة المرور". ستحتاج إلى إدخال كلمة المرور الحالية ثم الجديدة. نوصي باستخدام كلمة مرور قوية تحتوي على حروف وأرقام ورموز.',
    expanded: false
  },
  {
    id: 9,
    category: 'technical',
    question: 'واجهت مشكلة تقنية، كيف أبلغ عنها؟',
    answer: 'يمكنك الإبلاغ عن المشاكل التقنية عبر زر "الإبلاغ عن مشكلة" في صفحة المساعدة أو من خلال التواصل مع فريق الدعم الفني عبر البريد الإلكتروني support@fasahny.com. يرجى تقديم شرح مفصل للمشكلة وصورة شاشة إن أمكن.',
    expanded: false
  },
  {
    id: 10,
    category: 'technical',
    question: 'لماذا لا تعمل صفحة الحجز معي؟',
    answer: 'تأكد من تحديث متصفحك إلى آخر إصدار، وحذف ملفات الكوكيز والكاش للموقع. إذا استمرت المشكلة، جرب استخدام متصفح آخر أو وضع التصفح الخاص. يمكنك أيضاً التواصل مع الدعم الفني للمساعدة.',
    expanded: false
  }
])

// Contact options
const contactOptions = [
  { label: 'واتساب', icon: 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h.01M12 21a9 9 0 110-18 9 9 0 010 18z' },
  { label: 'البريد الإلكتروني', icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { label: 'الدعم الفني', icon: 'M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a5 5 0 01-7.072 0m0 0L5.636 15.536m-2.829 2.829L3 21m4.243-12.536a5 5 0 017.072 0m0 0L12.486 7.536' },
  { label: 'مركز المساعدة', icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' }
]

// Quick links
const quickLinks = [
  { label: 'سياسة الخصوصية', path: '/Privacy' },
  { label: 'شروط الخدمة', path: '/Terms' },
  { label: 'من نحن', path: '/About' },
  { label: 'تواصل معنا', path: '/Contact' }
]

// Computed filtered FAQs
const filteredFaqs = computed(() => {
  let result = faqs.value
  if (selectedCategory.value !== 'all') {
    result = result.filter(f => f.category === selectedCategory.value)
  }
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.trim().toLowerCase()
    result = result.filter(f => 
      f.question.includes(query) || 
      f.answer.includes(query)
    )
  }
  return result
})

// Toggle FAQ expansion
const toggleFaq = (id) => {
  const faq = faqs.value.find(f => f.id === id)
  if (faq) {
    faq.expanded = !faq.expanded
  }
}

// Navigation functions
const navigateTo = (route) => {
  router.push(route)
}

const goBack = () => {
  router.back()
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
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
              @click="goBack"
              class="w-10 h-10 md:w-12 md:h-12 bg-[#F5F2E8] border border-[#C9A84C] rounded-full flex items-center justify-center hover:bg-[#C9A84C]/10 transition-colors shrink-0"
            >
              <svg class="w-4 h-4 md:w-5 md:h-5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>
            <div class="text-right flex-1 mr-4">
              <h1 class="text-xl md:text-2xl lg:text-3xl font-bold text-[#1A1C1B]">مركز المساعدة</h1>
              <p class="text-xs md:text-sm text-[#7E7665]">نحن هنا لمساعدتك في أي وقت</p>
            </div>
            <div class="w-10 md:w-12"></div>
          </div>

          <!-- Search Bar -->
          <div class="relative mb-8">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="ابحث عن سؤال..."
              class="w-full bg-white border border-[#D0C5B2] rounded-xl py-3 md:py-4 px-12 text-right text-sm md:text-base focus:outline-none focus:border-[#C9A84C] transition-colors"
            />
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>

          <!-- Categories -->
          <div class="flex flex-wrap gap-2 md:gap-3 mb-8">
            <button 
              v-for="category in categories" 
              :key="category.id"
              @click="selectCategory(category.id)"
              :class="selectedCategory === category.id ? 'bg-[#C9A84C] text-[#503D00] border-[#C9A84C]' : 'bg-white text-[#4D4637] border-[#D0C5B2] hover:border-[#C9A84C]'"
              class="flex items-center gap-1.5 md:gap-2 px-3 md:px-4 py-1.5 md:py-2 border rounded-full text-xs md:text-sm font-medium transition-all cursor-pointer"
            >
              <svg class="w-3.5 h-3.5 md:w-4 md:h-4" :class="selectedCategory === category.id ? 'text-[#503D00]' : 'text-[#7E7665]'" fill="currentColor" viewBox="0 0 20 20">
                <path :d="category.icon" fill-rule="evenodd" clip-rule="evenodd"/>
              </svg>
              {{ category.label }}
            </button>
          </div>

          <!-- Results Count -->
          <p class="text-sm text-[#7E7665] mb-4 text-right">
            {{ filteredFaqs.length }} سؤال
            <span v-if="selectedCategory !== 'all'"> في {{ categories.find(c => c.id === selectedCategory)?.label }}</span>
          </p>

          <!-- FAQ Accordion -->
          <div class="space-y-3 md:space-y-4">
            <div v-for="faq in filteredFaqs" :key="faq.id" 
              class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden transition-shadow hover:shadow-md"
            >
              <button 
                @click="toggleFaq(faq.id)"
                class="w-full flex items-center justify-between p-4 md:p-5 text-right hover:bg-[#F9F9F7] transition-colors cursor-pointer"
              >
                <span class="text-sm md:text-base font-medium text-[#1A1C1B] flex-1 ml-4">{{ faq.question }}</span>
                <svg class="w-5 h-5 text-[#7E7665] transition-transform" 
                  :class="faq.expanded ? 'rotate-180' : ''"
                  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>
              <div v-if="faq.expanded" class="px-4 md:px-5 pb-4 md:pb-5">
                <div class="border-t border-[#D0C5B2] pt-3 md:pt-4">
                  <p class="text-sm md:text-base text-[#4D4637] leading-relaxed">{{ faq.answer }}</p>
                  <div class="mt-3 flex items-center gap-3">
                    <button class="text-xs text-[#C9A84C] hover:underline cursor-pointer">هل هذا مفيد؟</button>
                    <span class="text-[#D0C5B2]">|</span>
                    <button class="text-xs text-[#C9A84C] hover:underline cursor-pointer">الإبلاغ عن مشكلة</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- No Results -->
          <div v-if="filteredFaqs.length === 0" class="text-center py-12">
            <div class="text-5xl mb-4">🔍</div>
            <h3 class="text-xl font-semibold text-[#1A1C1B] mb-2">لم نجد نتائج</h3>
            <p class="text-[#7E7665] mb-4">حاول تعديل كلمات البحث أو اختيار تصنيف آخر</p>
            <button 
              @click="searchQuery = ''; selectedCategory = 'all'"
              class="text-[#C9A84C] font-medium hover:underline cursor-pointer"
            >
              عرض الكل
            </button>
          </div>

          <!-- Contact Section -->
          <div class="mt-10 p-6 md:p-8 bg-[#F5ECD7] rounded-2xl border border-[#D0C5B2]">
            <h3 class="text-lg md:text-xl font-bold text-[#1A1C1B] text-center mb-4">لم تجد إجابة؟ تواصل معنا</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
              <button 
                v-for="option in contactOptions" 
                :key="option.label"
                class="bg-white border border-[#D0C5B2] rounded-xl p-3 md:p-4 text-center hover:border-[#C9A84C] hover:shadow-md transition-all cursor-pointer group"
                @click="navigateTo('/Contact')"
              >
                <svg class="w-6 h-6 md:w-8 md:h-8 mx-auto text-[#755B00] group-hover:text-[#C9A84C] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="option.icon"/>
                </svg>
                <p class="text-xs md:text-sm font-medium text-[#1A1C1B] mt-1.5">{{ option.label }}</p>
              </button>
            </div>
          </div>

          <!-- Quick Links -->
          <div class="mt-6 flex flex-wrap justify-center gap-4 md:gap-6 text-sm">
            <button 
              v-for="link in quickLinks" 
              :key="link.label"
              @click="navigateTo(link.path)"
              class="text-[#7E7665] hover:text-[#755B00] transition-colors cursor-pointer"
            >
              {{ link.label }}
            </button>
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
                alt="User" 
                class="w-16 h-16 rounded-full border-2 border-[#C9A84C] object-cover">
              <div class="absolute bottom-0 left-0 w-3.5 h-3.5 bg-[#C9A84C] border-2 border-[#F9F9F7] rounded-full"></div>
            </div>
            <h3 class="text-lg font-semibold text-[#1A1C1B]">أحمد محمد</h3>
            <p class="text-xs text-[#7E7665]">المسافر الدائم</p>
          </div>

          <!-- Navigation Links -->
          <nav class="flex-1 space-y-0.5">
            <button 
              @click="navigateTo('trip-history')" 
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right"
            >
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
              </svg>
              <span class="text-sm font-medium">رحلاتي</span>
            </button>
            <button 
              @click="navigateTo('/UserDashboard')" 
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right"
            >
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 6a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm4 3a1 1 0 011-1h6a1 1 0 110 2H9a1 1 0 01-1-1zm0 4a1 1 0 011-1h6a1 1 0 110 2H9a1 1 0 01-1-1zm0 4a1 1 0 011-1h4a1 1 0 110 2H9a1 1 0 01-1-1z"/>
              </svg>
              <span class="text-sm font-medium">منشوراتي</span>
            </button>
            <button 
              @click="navigateTo('/Wishlist')" 
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right"
            >
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              </svg>
              <span class="text-sm font-medium flex-1">قائمة الأمنيات</span>
              <span class="bg-[#C9A84C] text-[#503D00] text-xs font-bold px-1.5 py-0.5 rounded-full">4 ❤️</span>
            </button>
            <button 
              @click="navigateTo('/Community')" 
              class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-[#7E7665] hover:bg-[#C9A84C]/10 transition-colors text-right"
            >
              <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/>
              </svg>
              <span class="text-sm font-medium">المجتمع</span>
            </button>
          </nav>

          <!-- Plan New Trip Button -->
          <button @click="navigateTo('/ai-trip-planner')" 
            class="w-full bg-[#755B00] hover:bg-[#5C4800] text-white py-3 rounded-xl font-medium transition-colors text-sm">
            خطط رحلة جديدة
          </button>

          <!-- Footer Links -->
          <div class="border-t border-[#D0C5B2] pt-3 mt-3 space-y-0.5">
            <button 
              @click="navigateTo('/Help')" 
              class="w-full flex items-center gap-3 px-3 py-2 rounded-xl bg-[#C9A84C] text-[#503D00] transition-colors text-right"
            >
              <svg class="w-4 h-4 text-[#503D00]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-sm font-medium">مركز المساعدة</span>
            </button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>