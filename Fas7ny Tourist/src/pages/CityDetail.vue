<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()
const route = useRoute()

/* ---------------- Toast feedback ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* ---------------- City data (each city fully self-contained) ---------------- */
const citiesData = reactive({
 'القاهرة': {
  name: 'القاهرة',
  tagline: 'مدينة الألف مئذنة',
  heroImage: 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1600&q=80',
  distanceFromCairo: '0 كم',
  bestSeason: 'أكتوبر - أبريل',
  landmarksCount: '+500',
  unescoStatus: 'عالمي',
  population: '10M+',
  areaKm2: '528',
  bestMonth: 'نوفمبر',
  avgWinterTemp: '20°م',
  about: 'القاهرة هي عاصمة مصر وأكبر مدنها، وتجمع بين التاريخ الفرعوني والإسلامي والحديث.',
  weather: {
    temp: 32,
    condition: 'مشمس',
    forecast: [
      { day: 'الأحد', high: 33, low: 21 },
      { day: 'الاثنين', high: 32, low: 20 },
      { day: 'الثلاثاء', high: 31, low: 20 },
    ],
    bestMonthsBars: [40, 80, 100, 70, 35]
  },
  accommodations: [
    { id: 1, name: 'فندق فورسيزونز نايل بلازا', badge: 'إطلالة على النيل', rating: 4.9, stars: 5, pricePerNight: 3500, category: 'hotel', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&q=80', favorite: false }
  ],
  landmarks: [
    { id: 1, name: 'أهرامات الجيزة', desc: 'أحد عجائب الدنيا السبع.', price: 540, unit: '/ تذكرة', badge: 'UNESCO', image: 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=500&q=80' },
    { id: 2, name: 'المتحف المصري الكبير', desc: 'أكبر متحف للآثار المصرية.', price: 500, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=500&q=80' }
  ],
  communityPhotos: [
    { id: 1, tag: 'الأهرامات', image: 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=300&q=80', likes: 288 },
    { id: 2, tag: 'خان الخليلي', image: 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=300&q=80', likes: 154 }
  ],
  quickInfo: [
    { label: 'مطار القاهرة الدولي (CAI)', icon: 'plane' },
    { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
    { label: 'الجنيه المصري (EGP)', icon: 'currency' },
    { label: 'مفتاح الاتصال: +20 2', icon: 'phone' },
  ],
  gettingThere: [
    { label: 'مترو', duration: 'داخل المدينة', icon: 'train' },
    { label: 'طيران', duration: 'حسب نقطة الانطلاق', icon: 'plane' },
  ]
},

'الإسكندرية': {
  name: 'الإسكندرية',
  tagline: 'عروس البحر المتوسط',
  heroImage: 'https://images.unsplash.com/photo-1621886292650-520f76c747d6?w=1600&q=80',
  distanceFromCairo: '220 كم',
  bestSeason: 'مارس - نوفمبر',
  landmarksCount: '+150',
  unescoStatus: 'تراثي',
  population: '5M',
  areaKm2: '2679',
  bestMonth: 'مايو',
  avgWinterTemp: '18°م',
  about: 'مدينة ساحلية أسسها الإسكندر الأكبر وتتميز بالكورنيش والقلعة والمكتبة.',
  weather: {
    temp: 29,
    condition: 'نسيم بحري لطيف',
    forecast: [
      { day: 'الأحد', high: 30, low: 22 },
      { day: 'الاثنين', high: 29, low: 21 },
      { day: 'الثلاثاء', high: 28, low: 21 },
    ],
    bestMonthsBars: [50, 85, 100, 80, 40]
  },
  accommodations: [
    { id: 1, name: 'فندق تريانون كورنيش الإسكندرية', badge: 'إطلالة بحرية', rating: 4.5, stars: 4, pricePerNight: 1400, category: 'hotel', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&q=80', favorite: false }
  ],
  landmarks: [
    { id: 1, name: 'مكتبة الإسكندرية', desc: 'صرح ثقافي عالمي.', price: 70, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=500&q=80' },
    { id: 2, name: 'قلعة قايتباي', desc: 'واحدة من أشهر معالم المدينة.', price: 60, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1621886292650-520f76c747d6?w=500&q=80' }
  ],
  communityPhotos: [
    { id: 1, tag: 'الكورنيش', image: 'https://images.unsplash.com/photo-1621886292650-520f76c747d6?w=300&q=80', likes: 176 },
    { id: 2, tag: 'المكتبة', image: 'https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=300&q=80', likes: 132 }
  ],
  quickInfo: [
    { label: 'مطار برج العرب (HBE)', icon: 'plane' },
    { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
    { label: 'الجنيه المصري (EGP)', icon: 'currency' },
    { label: 'مفتاح الاتصال: +20 3', icon: 'phone' },
  ],
  gettingThere: [
    { label: 'قطار', duration: '2.5 ساعة', icon: 'train' },
    { label: 'سيارة', duration: '3 ساعات', icon: 'car' },
  ]
},

'العين السخنة': {
  name: 'العين السخنة',
  tagline: 'الاسترخاء على البحر الأحمر',
  heroImage: 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=1600&q=80',
  distanceFromCairo: '120 كم',
  bestSeason: 'طوال العام',
  landmarksCount: '+25',
  unescoStatus: 'طبيعي',
  population: '30K',
  areaKm2: '17',
  bestMonth: 'أكتوبر',
  avgWinterTemp: '22°م',
  about: 'واحدة من أقرب الوجهات الساحلية للقاهرة وتشتهر بالمنتجعات والشواطئ الرملية.',
  weather: {
    temp: 31,
    condition: 'مشمس',
    forecast: [
      { day: 'الأحد', high: 32, low: 23 },
      { day: 'الاثنين', high: 31, low: 22 },
      { day: 'الثلاثاء', high: 31, low: 22 },
    ],
    bestMonthsBars: [60, 90, 100, 75, 45]
  },
  accommodations: [
    { id: 1, name: 'منتجع بورتو السخنة', badge: 'شاطئ خاص', rating: 4.4, stars: 4, pricePerNight: 1600, category: 'resort', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&q=80', favorite: false }
  ],
  landmarks: [
    { id: 1, name: 'شاطئ السخنة', desc: 'شاطئ مناسب للعائلات.', price: 0, unit: 'مجاني', badge: null, image: 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=500&q=80' }
  ],
  communityPhotos: [
    { id: 1, tag: 'شاطئ', image: 'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=300&q=80', likes: 121 }
  ],
  quickInfo: [
    { label: 'البحر الأحمر', icon: 'plane' },
    { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
    { label: 'الجنيه المصري (EGP)', icon: 'currency' },
  ],
  gettingThere: [
    { label: 'سيارة', duration: 'ساعتان', icon: 'car' },
    { label: 'حافلة', duration: 'ساعتان ونصف', icon: 'bus' },
  ]
},

'سيوة': {
  name: 'سيوة',
  tagline: 'جنة الواحات المصرية',
  heroImage: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1600&q=80',
  distanceFromCairo: '750 كم',
  bestSeason: 'أكتوبر - مارس',
  landmarksCount: '+40',
  unescoStatus: 'طبيعي',
  population: '35K',
  areaKm2: '82',
  bestMonth: 'فبراير',
  avgWinterTemp: '21°م',
  about: 'واحة فريدة تتميز بالعيون الطبيعية وجبل الدكرور وبحيرات الملح.',
  weather: {
    temp: 28,
    condition: 'جاف ومعتدل',
    forecast: [
      { day: 'الأحد', high: 29, low: 15 },
      { day: 'الاثنين', high: 28, low: 14 },
      { day: 'الثلاثاء', high: 27, low: 14 },
    ],
    bestMonthsBars: [35, 90, 100, 60, 20]
  },
  accommodations: [
    { id: 1, name: 'أدرار سيوة لودج', badge: 'تراثي', rating: 4.6, stars: 4, pricePerNight: 900, category: 'resort', image: 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&q=80', favorite: false }
  ],
  landmarks: [
    { id: 1, name: 'جبل الدكرور', desc: 'أحد أشهر معالم الواحة.', price: 0, unit: 'مجاني', badge: null, image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500&q=80' },
    { id: 2, name: 'بحيرات الملح', desc: 'مناظر طبيعية مذهلة.', price: 100, unit: '/ زيارة', badge: null, image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=80' }
  ],
  communityPhotos: [
    { id: 1, tag: 'جبل الدكرور', image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=300&q=80', likes: 143 },
    { id: 2, tag: 'بحيرات الملح', image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=300&q=80', likes: 98 }
  ],
  quickInfo: [
    { label: 'واحة سيوة', icon: 'phone' },
    { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
    { label: 'الجنيه المصري (EGP)', icon: 'currency' },
  ],
  gettingThere: [
    { label: 'حافلة', duration: '10 ساعات', icon: 'bus' },
  ]
},
  'الأقصر': {
    name: 'الأقصر',
    tagline: 'عاصمة الحضارة الفرعونية',
    heroImage: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=1600&q=80',
    distanceFromCairo: '670 كم',
    bestSeason: 'أكتوبر - أبريل',
    landmarksCount: '+320',
    unescoStatus: 'عالمي',
    population: '1.3M',
    areaKm2: '416',
    bestMonth: 'ديسمبر',
    avgWinterTemp: '22°م',
    about: 'تُلقب مدينة الأقصر بـ"متحف الهواء الطلق العالمي"، حيث تضم ثلث آثار العالم. كانت تُعرف قديماً باسم "طيبة"، عاصمة مصر في أوج مجدها خلال الدولة الحديثة. تنقسم المدينة بضفتيها الشرقية (مدينة الأحياء) والغربية (مدينة الأموات) لتروي قصة حضارة لم تعرف المستحيل.',
    weather: {
      temp: 38,
      condition: 'مشمس في الغالب',
      forecast: [
        { day: 'الأحد', high: 39, low: 24 },
        { day: 'الاثنين', high: 37, low: 23 },
        { day: 'الثلاثاء', high: 38, low: 25 },
      ],
      bestMonthsBars: [40, 100, 100, 55, 25],
    },
    accommodations: [
      { id: 1, name: 'منتجع جزيرة الموز', badge: 'تراثي', rating: 4.6, stars: 4, pricePerNight: 1200, category: 'resort', image: 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=500&q=80', favorite: false },
      { id: 2, name: 'فندق سونستا سانت جورج', badge: 'إطلالة على النيل', rating: 4.8, stars: 5, pricePerNight: 850, category: 'hotel', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500&q=80', favorite: false },
    ],
    landmarks: [
      { id: 1, name: 'جولة بالفلوكة عند الغروب', desc: 'تجربة هادئة في قلب النيل للاستمتاع بمنظر الغروب التاريخي.', price: 200, unit: '/ ساعة', badge: null, image: 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=500&q=80' },
      { id: 2, name: 'وادي الملوك', desc: 'المثوى الأخير لعظماء فراعنة الدولة الحديثة وتوت عنخ آمون.', price: 450, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1568402102990-bc541580b59f?w=500&q=80' },
      { id: 3, name: 'مجمع معابد الكرنك', desc: 'أكبر دار للعبادة بنيت على وجه الأرض، يمتد على مساحة 200 فدان.', price: 300, unit: '/ تذكرة', badge: 'UNESCO', image: 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=500&q=80' },
    ],
    communityPhotos: [
      { id: 1, tag: 'فنادق', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=300&q=80', likes: 214 },
      { id: 2, tag: 'تراثي', image: 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=300&q=80', likes: 98 },
      { id: 3, tag: 'الكرنك', image: 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=300&q=80', likes: 342 },
      { id: 4, tag: 'وادي الملوك', image: 'https://images.unsplash.com/photo-1568402102990-bc541580b59f?w=300&q=80', likes: 176 },
      { id: 5, tag: 'غروب النيل', image: 'https://images.unsplash.com/photo-1544644181-1484b3fdfc62?w=300&q=80', likes: 265 },
      { id: 6, tag: 'معبد لكسور', image: 'https://images.unsplash.com/photo-1583417319070-4a69db38a482?w=300&q=80', likes: 401 },
    ],
    quickInfo: [
      { label: 'مطار الأقصر الدولي (LXR)', icon: 'plane' },
      { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
      { label: 'الجنيه المصري (EGP)', icon: 'currency' },
      { label: 'مفتاح الاتصال: +20 95', icon: 'phone' },
    ],
    gettingThere: [
      { label: 'حافلة', duration: '10 ساعات', icon: 'bus' },
      { label: 'قطار', duration: '9 ساعات', icon: 'train' },
      { label: 'طيران', duration: 'ساعة', icon: 'plane' },
    ],
  },

  'الغردقة': {
    name: 'الغردقة',
    tagline: 'لؤلؤة البحر الأحمر',
    heroImage: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1600&q=80',
    distanceFromCairo: '460 كم',
    bestSeason: 'سبتمبر - مايو',
    landmarksCount: '+120',
    unescoStatus: 'طبيعي',
    population: '250K',
    areaKm2: '40',
    bestMonth: 'أكتوبر',
    avgWinterTemp: '24°م',
    about: 'الغردقة هي عاصمة الغوص والرياضات المائية على البحر الأحمر، وتضم واحدة من أغنى النظم البيئية المرجانية في العالم. تحولت من قرية صيد صغيرة إلى وجهة سياحية عالمية بفضل شواطئها الرملية الذهبية ومياهها الفيروزية الصافية، وتستقبل اليوم ملايين الزوار سنوياً بحثاً عن الشمس والاسترخاء ومغامرات الغوص.',
    weather: {
      temp: 34,
      condition: 'صافٍ ومشمس',
      forecast: [
        { day: 'الأحد', high: 35, low: 26 },
        { day: 'الاثنين', high: 34, low: 25 },
        { day: 'الثلاثاء', high: 33, low: 25 },
      ],
      bestMonthsBars: [50, 90, 100, 80, 45],
    },
    accommodations: [
      { id: 1, name: 'ستيغنبرغر الجزيرة الغردقة', badge: 'شاطئ خاص', rating: 4.7, stars: 5, pricePerNight: 1800, category: 'resort', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=500&q=80', favorite: false },
      { id: 2, name: 'فندق مارينا الغردقة', badge: 'إطلالة على المارينا', rating: 4.4, stars: 4, pricePerNight: 950, category: 'hotel', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&q=80', favorite: false },
    ],
    landmarks: [
      { id: 1, name: 'الغطس في جزيرة الجفتون', desc: 'رحلة يومية بالقارب لاستكشاف الشعاب المرجانية والأسماك الاستوائية.', price: 600, unit: '/ رحلة', badge: 'محمية طبيعية', image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=500&q=80' },
      { id: 2, name: 'سفاري صحراوي بالكوادر', desc: 'مغامرة في الصحراء الشرقية مع زيارة لقرية بدوية وشاي أعرابي.', price: 350, unit: '/ رحلة', badge: null, image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=80' },
      { id: 3, name: 'الغوص عند السفن الغارقة', desc: 'استكشاف حطام السفن التاريخية في أعماق البحر الأحمر مع مدرب معتمد.', price: 900, unit: '/ غطسة', badge: null, image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500&q=80' },
    ],
    communityPhotos: [
      { id: 1, tag: 'غطس', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&q=80', likes: 356 },
      { id: 2, tag: 'شاطئ', image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300&q=80', likes: 289 },
      { id: 3, tag: 'جفتون', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=300&q=80', likes: 178 },
      { id: 4, tag: 'سفاري', image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=300&q=80', likes: 142 },
      { id: 5, tag: 'غروب البحر', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=300&q=80', likes: 233 },
      { id: 6, tag: 'فنادق', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=300&q=80', likes: 97 },
    ],
    quickInfo: [
      { label: 'مطار الغردقة الدولي (HRG)', icon: 'plane' },
      { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
      { label: 'الجنيه المصري (EGP)', icon: 'currency' },
      { label: 'مفتاح الاتصال: +20 65', icon: 'phone' },
    ],
    gettingThere: [
      { label: 'حافلة', duration: '6 ساعات', icon: 'bus' },
      { label: 'قطار', duration: '8 ساعات', icon: 'train' },
      { label: 'طيران', duration: '55 دقيقة', icon: 'plane' },
    ],
  },

  'أسوان': {
    name: 'أسوان',
    tagline: 'سحر النوبة والنيل',
    heroImage: 'https://images.unsplash.com/photo-1591608971362-f08b2a75731a?w=1600&q=80',
    distanceFromCairo: '870 كم',
    bestSeason: 'أكتوبر - مارس',
    landmarksCount: '+200',
    unescoStatus: 'عالمي',
    population: '500K',
    areaKm2: '62',
    bestMonth: 'يناير',
    avgWinterTemp: '25°م',
    about: 'أسوان هي أهدأ مدن مصر وأكثرها سحراً، حيث يلتقي النيل بالجبال الذهبية والقرى النوبية الملونة. تشتهر بمعبد فيلة الذي أُنقذ من الغرق ونُقل حجراً حجراً، وبالسد العالي الذي غيّر وجه مصر الحديثة، وبنمط حياة هادئ تحدده رحلات الفلوكة وأسواق التوابل والحرف النوبية.',
    weather: {
      temp: 36,
      condition: 'جاف ومشمس',
      forecast: [
        { day: 'الأحد', high: 37, low: 23 },
        { day: 'الاثنين', high: 36, low: 22 },
        { day: 'الثلاثاء', high: 35, low: 21 },
      ],
      bestMonthsBars: [35, 95, 100, 60, 20],
    },
    accommodations: [
      { id: 1, name: 'موفنبيك جزيرة النخيل أسوان', badge: 'إطلالة على النيل', rating: 4.7, stars: 5, pricePerNight: 1600, category: 'resort', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500&q=80', favorite: false },
      { id: 2, name: 'أولد كتراكت أسوان', badge: 'تراثي فاخر', rating: 4.9, stars: 5, pricePerNight: 2200, category: 'hotel', image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500&q=80', favorite: false },
    ],
    landmarks: [
      { id: 1, name: 'معبد فيلة', desc: 'معبد إيزيس الأثري الذي نُقل من جزيرته الأصلية لإنقاذه من مياه السد.', price: 400, unit: '/ تذكرة', badge: 'UNESCO', image: 'https://images.unsplash.com/photo-1608896862894-31d7e46b1e57?w=500&q=80' },
      { id: 2, name: 'السد العالي', desc: 'أحد أعظم المشروعات الهندسية في القرن العشرين وشريان حياة مصر.', price: 150, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=500&q=80' },
      { id: 3, name: 'جولة بالفلوكة للقرى النوبية', desc: 'إبحار هادئ بين الجزر الخضراء وزيارة منزل نوبي تقليدي وتناول الشاي.', price: 250, unit: '/ ساعة', badge: null, image: 'https://images.unsplash.com/photo-1591608971362-f08b2a75731a?w=500&q=80' },
    ],
    communityPhotos: [
      { id: 1, tag: 'فيلة', image: 'https://images.unsplash.com/photo-1608896862894-31d7e46b1e57?w=300&q=80', likes: 312 },
      { id: 2, tag: 'فلوكة', image: 'https://images.unsplash.com/photo-1591608971362-f08b2a75731a?w=300&q=80', likes: 268 },
      { id: 3, tag: 'قرية نوبية', image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=300&q=80', likes: 189 },
      { id: 4, tag: 'السد العالي', image: 'https://images.unsplash.com/photo-1608889825205-eebdb9fc5806?w=300&q=80', likes: 121 },
      { id: 5, tag: 'غروب النيل', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=300&q=80', likes: 245 },
      { id: 6, tag: 'فنادق', image: 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=300&q=80', likes: 88 },
    ],
    quickInfo: [
      { label: 'مطار أسوان الدولي (ASW)', icon: 'plane' },
      { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
      { label: 'الجنيه المصري (EGP)', icon: 'currency' },
      { label: 'مفتاح الاتصال: +20 97', icon: 'phone' },
    ],
    gettingThere: [
      { label: 'حافلة', duration: '12 ساعة', icon: 'bus' },
      { label: 'قطار', duration: '11 ساعة', icon: 'train' },
      { label: 'طيران', duration: 'ساعة و20 د', icon: 'plane' },
    ],
  },

  'دهب': {
    name: 'دهب',
    tagline: 'مدينة البحر والهدوء',
    heroImage: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600&q=80',
    distanceFromCairo: '550 كم',
    bestSeason: 'أكتوبر - أبريل',
    landmarksCount: '+50',
    unescoStatus: 'طبيعي',
    population: '30K',
    areaKm2: '25',
    bestMonth: 'نوفمبر',
    avgWinterTemp: '23°م',
    about: 'دهب قرية غوص صغيرة على خليج العقبة، تجمع بين طابع بدوي أصيل وأجواء عالمية استرخائية. تشتهر بموقع "الحفرة الزرقاء" الأسطوري لعشاق الغطس الحر، ومقاهي الشاطئ التي تفرش وسائدها على الرمال مباشرة، وهي الوجهة المفضلة لمن يبحث عن سرعة أبطأ من باقي مدن البحر الأحمر.',
    weather: {
      temp: 33,
      condition: 'صافٍ ومعتدل',
      forecast: [
        { day: 'الأحد', high: 34, low: 24 },
        { day: 'الاثنين', high: 33, low: 23 },
        { day: 'الثلاثاء', high: 32, low: 22 },
      ],
      bestMonthsBars: [45, 85, 100, 90, 40],
    },
    accommodations: [
      { id: 1, name: 'لاجونا دهب ريزورت', badge: 'شاطئ خاص', rating: 4.5, stars: 4, pricePerNight: 1100, category: 'resort', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&q=80', favorite: false },
      { id: 2, name: 'فندق نيو ديزرت دهب', badge: 'أجواء بدوية', rating: 4.3, stars: 3, pricePerNight: 500, category: 'hotel', image: 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&q=80', favorite: false },
    ],
    landmarks: [
      { id: 1, name: 'الحفرة الزرقاء (Blue Hole)', desc: 'واحد من أشهر مواقع الغطس الحر في العالم بعمق يتجاوز 100 متر.', price: 300, unit: '/ رحلة', badge: null, image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500&q=80' },
      { id: 2, name: 'سفاري بالجمال في الصحراء', desc: 'رحلة عند الغروب على ظهر الجمال وسط جبال سيناء مع عشاء بدوي.', price: 400, unit: '/ رحلة', badge: null, image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=500&q=80' },
      { id: 3, name: 'جزيرة الفراعنة', desc: 'قلعة صلاح الدين الأثرية على جزيرة صغيرة قبالة ساحل دهب.', price: 250, unit: '/ تذكرة', badge: null, image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&q=80' },
    ],
    communityPhotos: [
      { id: 1, tag: 'الحفرة الزرقاء', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&q=80', likes: 401 },
      { id: 2, tag: 'مقاهي الشاطئ', image: 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=300&q=80', likes: 198 },
      { id: 3, tag: 'سفاري', image: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=300&q=80', likes: 156 },
      { id: 4, tag: 'جزيرة الفراعنة', image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=80', likes: 132 },
      { id: 5, tag: 'غروب البحر', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=300&q=80', likes: 210 },
      { id: 6, tag: 'غطس', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&q=80', likes: 267 },
    ],
    quickInfo: [
      { label: 'أقرب مطار: شرم الشيخ (SSH)', icon: 'plane' },
      { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
      { label: 'الجنيه المصري (EGP)', icon: 'currency' },
      { label: 'مفتاح الاتصال: +20 69', icon: 'phone' },
    ],
    gettingThere: [
      { label: 'حافلة', duration: '9 ساعات', icon: 'bus' },
      { label: 'سيارة أجرة من شرم', duration: 'ساعة ونصف', icon: 'car' },
      { label: 'طيران لشرم', duration: '50 دقيقة', icon: 'plane' },
    ],
  },
  'شرم الشيخ': {
    name: 'شرم الشيخ',
    tagline: 'جوهرة البحر الأحمر',
    heroImage: 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=1600&q=80',
    distanceFromCairo: '500 كم',
    bestSeason: 'أكتوبر - مايو',
    landmarksCount: '+150',
    unescoStatus: 'طبيعي',
    population: '75K',
    areaKm2: '480',
    bestMonth: 'نوفمبر',
    avgWinterTemp: '25°م',
    about: 'شرم الشيخ واحدة من أشهر الوجهات السياحية في مصر وتتميز بالشعاب المرجانية والغوص والمنتجعات العالمية. تجمع المدينة بين شواطئ خليج نعمة الصاخبة ومحمية رأس محمد الطبيعية الهادئة، وتُعد نقطة انطلاق مثالية لاستكشاف جزيرة تيران وأعماق البحر الأحمر على مدار العام.',
    weather: {
      temp: 35,
      condition: 'مشمس ومعتدل الرطوبة',
      forecast: [
        { day: 'الأحد', high: 36, low: 25 },
        { day: 'الاثنين', high: 35, low: 24 },
        { day: 'الثلاثاء', high: 34, low: 24 },
      ],
      bestMonthsBars: [55, 90, 100, 85, 50],
    },
    accommodations: [
      { id: 1, name: 'فور سيزونز شرم الشيخ', badge: 'شاطئ خاص', rating: 4.9, stars: 5, pricePerNight: 3200, category: 'resort', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=500&q=80', favorite: false },
      { id: 2, name: 'ريتز كارلتون شرم الشيخ', badge: 'إطلالة على البحر', rating: 4.8, stars: 5, pricePerNight: 2100, category: 'hotel', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&q=80', favorite: false },
    ],
    landmarks: [
      { id: 1, name: 'محمية رأس محمد', desc: 'واحدة من أجمل محميات الغوص في العالم عند ملتقى خليجي السويس والعقبة.', price: 500, unit: '/ رحلة', badge: 'محمية طبيعية', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=500&q=80' },
      { id: 2, name: 'جزيرة تيران للغوص', desc: 'رحلة بحرية لأربعة شعاب مرجانية أسطورية وسط تيارات مياه صافية.', price: 700, unit: '/ رحلة', badge: null, image: 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=500&q=80' },
      { id: 3, name: 'سوق خليج نعمة الليلي', desc: 'أمسية تسوق وترفيه بين المطاعم والمقاهي المطلة على البحر مباشرة.', price: 0, unit: 'مجاني', badge: null, image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500&q=80' },
    ],
    communityPhotos: [
      { id: 1, tag: 'رأس محمد', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&q=80', likes: 389 },
      { id: 2, tag: 'خليج نعمة', image: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=300&q=80', likes: 224 },
      { id: 3, tag: 'تيران', image: 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=300&q=80', likes: 301 },
      { id: 4, tag: 'فنادق', image: 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=300&q=80', likes: 145 },
      { id: 5, tag: 'غطس', image: 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=300&q=80', likes: 276 },
      { id: 6, tag: 'غروب البحر', image: 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=300&q=80', likes: 198 },
    ],
    quickInfo: [
      { label: 'مطار شرم الشيخ الدولي (SSH)', icon: 'plane' },
      { label: 'GMT+2 (توقيت القاهرة)', icon: 'clock' },
      { label: 'الجنيه المصري (EGP)', icon: 'currency' },
      { label: 'مفتاح الاتصال: +20 69', icon: 'phone' },
    ],
    gettingThere: [
      { label: 'حافلة', duration: '8 ساعات', icon: 'bus' },
      { label: 'سيارة خاصة', duration: '6 ساعات', icon: 'car' },
      { label: 'طيران', duration: '50 دقيقة', icon: 'plane' },
    ],
  },
})

const city = computed(() => {
  return citiesData[route.params.name] || citiesData['الأقصر']
})

const addedToTrip = ref(false)
const toggleAddToTrip = () => {
  addedToTrip.value = !addedToTrip.value
  showToast(addedToTrip.value ? `تمت إضافة ${city.value.name} لرحلتك` : `تم حذف ${city.value.name} من رحلتك`)
}

const planTripForCity = () => {
  router.push({ path: '/ai-trip-planner', query: { city: city.value.name } })
}

/* ---------------- Sticky tabs / search ---------------- */
const tabs = [
  { id: 'all', label: 'الكل' },
  { id: 'accommodation', label: 'الإقامة' },
  { id: 'restaurants', label: 'المطاعم' },
  { id: 'transport', label: 'مواصلات' },
  { id: 'landmarks', label: 'معالم وأنشطة' },
  { id: 'info', label: 'معلومات عامة' },
]
const activeTab = ref('all')
const searchQuery = ref('')

const selectTab = (id) => {
  activeTab.value = id
  const el = document.getElementById(`section-${id}`)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

/* ---------------- Filters ---------------- */
const filterCategory = ref(null) // null = show all, 'hotel' | 'resort'
const filterMaxPrice = ref(5000)
const filterMinRating = ref(0)
const amenityOptions = ['واي فاي مجاني', 'مسبح', 'إطلالة على البحر/النيل']
const selectedAmenities = ref([])
const toggleAmenity = (a) => {
  selectedAmenities.value = selectedAmenities.value.includes(a)
    ? selectedAmenities.value.filter((x) => x !== a)
    : [...selectedAmenities.value, a]
}
const toggleCategoryFilter = (cat) => {
  filterCategory.value = filterCategory.value === cat ? null : cat
}

const filteredAccommodations = computed(() =>
  city.value.accommodations.filter((h) => {
    if (filterCategory.value && h.category !== filterCategory.value) return false
    if (h.pricePerNight > filterMaxPrice.value) return false
    if (h.rating < filterMinRating.value) return false
    return true
  })
)

const toggleFavorite = (hotel) => {
  hotel.favorite = !hotel.favorite
  showToast(hotel.favorite ? 'أُضيف للمفضلة' : 'أُزيل من المفضلة')
}

const bookHotel = (hotel) => {
  router.push(`/hotel/${encodeURIComponent(city.value.name)}/${hotel.id}`)
}

/* ---------------- Landmarks ---------------- */
const landmarksScroll = ref(null)
const scrollLandmarks = (dir) => {
  if (!landmarksScroll.value) return
  landmarksScroll.value.scrollBy({ left: dir * 340, behavior: 'smooth' })
}

const viewLandmark = (landmark) => {
  showToast(`سيتم فتح تفاصيل ${landmark.name} قريباً`)
}

/* ---------------- Community photos ---------------- */
const openCommunityPost = () => {
  router.push('/community')
}
const openCommunityFeed = () => {
  router.push('/community')
}

const openInteractiveMap = () => {
  router.push({ path: '/map', query: { city: city.value.name } })
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#FAFAF8]">
    <Navbar />

    <!-- Toast -->
    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <!-- Hero -->
    <div class="relative w-full h-175 mt-16 overflow-hidden">
      <img :src="city.heroImage" class="absolute inset-0 w-full h-full object-cover" :alt="city.name" />
      <div class="absolute inset-0" style="background: linear-gradient(0deg, #1A3C5E 0%, rgba(26,60,94,0) 60%);"></div>

      <div class="relative h-full flex items-end justify-center px-6 md:px-16 pb-8">
        <div class="w-full max-w-328 flex flex-col md:flex-row items-end justify-between gap-10">

          <!-- Weather widget -->
          <div class="w-full md:w-80 bg-white/10 border border-white/20 backdrop-blur-md rounded-2xl p-6 flex flex-col gap-6 order-2 md:order-1">
            <div class="flex items-start justify-between">
              <div class="text-right">
                <p class="text-4xl font-bold text-white">{{ city.weather.temp }}°م</p>
                <p class="text-sm text-white/80">{{ city.weather.condition }}</p>
              </div>
              <svg class="w-8 h-8 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.464 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/></svg>
            </div>

            <div class="flex flex-col gap-3">
              <div v-for="f in city.weather.forecast" :key="f.day" class="flex items-center justify-between text-sm">
                <span class="text-white/60">{{ f.day }}</span>
                <span class="text-white">{{ f.high }}° / {{ f.low }}°</span>
              </div>
            </div>

            <div class="border-t border-white/10 pt-4 flex flex-col gap-3">
              <p class="text-xs text-[#C9A84C] tracking-wide uppercase text-right">أفضل وقت للزيارة</p>
              <div class="flex items-end justify-center gap-1 h-12">
                <div v-for="(h, i) in city.weather.bestMonthsBars" :key="i" class="flex-1 rounded-sm"
                  :style="{ height: h + '%', background: h >= 80 ? '#C9A84C' : 'rgba(255,255,255,0.2)' }"></div>
              </div>
            </div>
          </div>

          <!-- Heading & stats -->
          <div class="w-full md:max-w-2xl flex flex-col gap-4 order-1 md:order-2">
            <div class="flex items-center gap-2 justify-end text-sm">
              <button @click="router.push('/')" class="text-white/80 hover:text-white">الرئيسية</button>
              <span class="text-white/50">/</span>
              <button @click="router.push('/search')" class="text-white/80 hover:text-white">المدن</button>
              <span class="text-white/50">/</span>
              <span class="text-[#C9A84C] font-semibold">{{ city.name }}</span>
            </div>

            <h1 class="text-6xl font-bold text-white text-right" style="text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{{ city.name }}</h1>
            <p class="text-xl text-[#C9A84C] text-right">{{ city.tagline }}</p>

            <div class="border-t border-white/20 pt-6 flex flex-wrap items-start justify-end gap-8 text-right">
              <div>
                <p class="text-xs text-white/60 uppercase mb-1">المسافة من القاهرة</p>
                <p class="text-xl font-bold text-white">{{ city.distanceFromCairo }}</p>
              </div>
              <div>
                <p class="text-xs text-white/60 uppercase mb-1">أفضل موسم</p>
                <p class="text-xl font-bold text-white">{{ city.bestSeason }}</p>
              </div>
              <div>
                <p class="text-xs text-white/60 uppercase mb-1">معالم سياحية</p>
                <p class="text-xl font-bold text-white">{{ city.landmarksCount }}</p>
              </div>
              <div>
                <p class="text-xs text-white/60 uppercase mb-1">مواقع اليونسكو</p>
                <p class="text-xl font-bold text-white">{{ city.unescoStatus }}</p>
              </div>
            </div>

            <div class="flex items-center gap-4 justify-end">
              <button @click="toggleAddToTrip"
                :class="addedToTrip ? 'bg-white text-[#1A3C5E] border-white' : 'border-white text-white hover:bg-white/10'"
                class="border-2 px-8 py-3 rounded-xl font-bold transition-colors">
                {{ addedToTrip ? '✓ أُضيفت لرحلتي' : 'أضفها لرحلتي' }}
              </button>
              <button @click="planTripForCity"
                class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#1A3C5E] font-bold px-8 py-3.5 rounded-xl transition-colors">
                خطط رحلة لـ{{ city.name }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sticky tab nav -->
    <div class="sticky top-16 z-30 bg-[#FAFAF8] border-b border-[#E8E4DC] shadow-sm">
      <div class="max-w-7xl mx-auto px-8 flex items-center justify-between gap-8 overflow-x-auto">
        <div class="relative w-72 shrink-0 py-3">
          <input v-model="searchQuery" type="text" :placeholder="`ابحث في ${city.name}...`"
            class="w-full bg-[#F4F4F2] rounded-xl py-3 pr-4 pl-10 text-base text-right focus:outline-none" />
          <svg class="w-4.5 h-4.5 text-[#1A3C5E]/40 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
        <nav class="flex items-center gap-8 shrink-0">
          <button v-for="tab in tabs" :key="tab.id" @click="selectTab(tab.id)"
            :class="activeTab === tab.id ? 'text-[#C9A84C] font-bold border-b-2 border-[#C9A84C]' : 'text-[#1A3C5E]/60 hover:text-[#1A3C5E]'"
            class="py-5 text-base whitespace-nowrap transition-colors">
            {{ tab.label }}
          </button>
        </nav>
      </div>
    </div>

    <!-- Main content -->
    <div class="max-w-360 mx-auto px-8 py-8 flex flex-col lg:flex-row-reverse gap-8 items-start">

      <!-- Sidebar filters -->
      <aside class="w-full lg:w-80 shrink-0 flex flex-col gap-8">
        <div class="bg-white border border-[#E8E4DC] rounded-2xl p-6 flex flex-col gap-6">
          <h3 class="text-lg text-[#1A3C5E] text-right">تصفية النتائج</h3>

          <div class="flex flex-col gap-3">
            <label class="text-sm font-bold text-[#1A3C5E]/80 text-right block">الفئة</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="toggleCategoryFilter('resort')"
                :class="filterCategory === 'resort' ? 'bg-[#C9A84C]/10 border-[#C9A84C]/20 text-[#C9A84C]' : 'bg-[#FAFAF8] border-[#E8E4DC] text-[#1A3C5E]/60'"
                class="border rounded-lg py-2 text-sm transition-colors">منتجعات</button>
              <button @click="toggleCategoryFilter('hotel')"
                :class="filterCategory === 'hotel' ? 'bg-[#C9A84C]/10 border-[#C9A84C]/20 text-[#C9A84C]' : 'bg-[#FAFAF8] border-[#E8E4DC] text-[#1A3C5E]/60'"
                class="border rounded-lg py-2 text-sm transition-colors">فنادق</button>
            </div>
          </div>

          <div class="flex flex-col gap-2">
            <label class="text-sm font-bold text-[#1A3C5E]/80 text-right block">نطاق السعر</label>
            <input v-model="filterMaxPrice" type="range" min="200" max="5000" step="100" class="w-full accent-[#C9A84C]" />
            <div class="flex items-center justify-between text-xs text-[#1A3C5E]/40">
              <span>{{ Number(filterMaxPrice).toLocaleString() }}+ ج.م</span>
              <span>200 ج.م</span>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <label class="text-sm font-bold text-[#1A3C5E]/80 text-right block">التقييم</label>
            <div class="flex items-center gap-1 justify-end">
              <button v-for="n in 5" :key="n" @click="filterMinRating = filterMinRating === n ? 0 : n">
                <svg class="w-5 h-5" :class="n <= filterMinRating ? 'text-[#C9A84C]' : 'text-[#E8E4DC]'" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              </button>
            </div>
          </div>

          <div class="flex flex-col gap-3">
            <label class="text-sm font-bold text-[#1A3C5E]/80 text-right block">المميزات</label>
            <div class="flex items-center gap-2 flex-wrap justify-end">
              <button v-for="a in amenityOptions" :key="a" @click="toggleAmenity(a)"
                :class="selectedAmenities.includes(a) ? 'bg-[#C9A84C]/10 border-[#C9A84C]/30 text-[#C9A84C]' : 'bg-[#FAFAF8] border-[#E8E4DC] text-[#1A1C1B]'"
                class="border text-xs px-3 py-1.5 rounded-full transition-colors">{{ a }}</button>
            </div>
          </div>
        </div>

        <!-- Quick info -->
        <div class="relative bg-[#1A3C5E] rounded-2xl p-6 overflow-hidden">
          <div class="absolute inset-0 opacity-10" style="background: radial-gradient(circle at 50% 50%, #C9A84C 0%, rgba(201,168,76,0) 70%);"></div>
          <div class="relative flex flex-col gap-4">
            <h4 class="text-lg text-[#C9A84C] text-right">معلومات سريعة</h4>
            <div v-for="info in city.quickInfo" :key="info.label" class="flex items-center gap-3 justify-end text-white text-sm">
              <span>{{ info.label }}</span>
              <svg v-if="info.icon === 'plane'" class="w-5 h-5 text-[#C9A84C] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
              <svg v-else-if="info.icon === 'clock'" class="w-5 h-5 text-[#C9A84C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <svg v-else-if="info.icon === 'currency'" class="w-5 h-5 text-[#C9A84C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V6m0 8v2m9-4a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <svg v-else class="w-5 h-5 text-[#C9A84C] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main listings -->
      <div class="flex-1 w-full flex flex-col gap-10">

        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-sm text-[#1A3C5E]/40">ترتيب حسب:</span>
            <button class="flex items-center gap-1 text-base text-[#1A3C5E]">
              الأعلى تقييماً
              <svg class="w-3 h-3" fill="none" stroke="#6B7280" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
          </div>
          <p class="text-base text-[#1A3C5E]">{{ filteredAccommodations.length + city.landmarks.length }} نتيجة وجدناها لك</p>
        </div>

        <!-- Accommodation -->
        <section id="section-accommodation" class="flex flex-col gap-6">
          <div class="flex items-center justify-between border-b border-[#E8E4DC] pb-4">
            <button class="text-sm font-bold text-[#C9A84C]">عرض الكل</button>
            <div class="flex items-center gap-2">
              <h3 class="text-base text-[#1A3C5E]">الإقامة المميزة</h3>
              <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            </div>
          </div>

          <p v-if="filteredAccommodations.length === 0" class="text-sm text-[#7E7665] text-center py-10">
            لا توجد نتائج مطابقة لهذه الفلاتر.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="hotel in filteredAccommodations" :key="hotel.id"
              class="bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden">
              <div class="relative h-56">
                <img :src="hotel.image" class="w-full h-full object-cover" :alt="hotel.name" />
                <span class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm text-[#1A3C5E] text-xs font-bold px-3 py-1 rounded-full">{{ hotel.badge }}</span>
                <button @click="toggleFavorite(hotel)"
                  class="absolute bottom-4 right-4 w-9 h-9 rounded-full bg-white/80 flex items-center justify-center">
                  <svg class="w-5 h-5" :class="hotel.favorite ? 'text-[#C94B4B]' : 'text-[#1A3C5E]'" :fill="hotel.favorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                </button>
              </div>
              <div class="p-6 flex flex-col gap-2">
                <div class="flex items-start justify-between">
                  <span class="flex items-center gap-1 bg-[#F0FDF4] text-[#15803D] text-xs font-bold px-2 py-1 rounded-lg">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    {{ hotel.rating }}
                  </span>
                  <h4 class="font-bold text-[#1A3C5E] text-lg">{{ hotel.name }}</h4>
                </div>
                <div class="flex items-center gap-1 justify-end">
                  <svg v-for="n in hotel.stars" :key="n" class="w-3.5 h-3.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                </div>
                <div class="flex items-center justify-between pt-2">
                  <button @click="bookHotel(hotel)" class="bg-[#1A3C5E] hover:bg-[#152f4a] text-white text-sm font-bold px-4 py-2 rounded-xl transition-colors">حجز الآن</button>
                  <p class="text-right">
                    <span class="text-2xl font-bold text-[#1A3C5E]">{{ hotel.pricePerNight.toLocaleString() }}</span>
                    <span class="text-sm text-[#1A3C5E]/60"> ج.م / ليلة</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Landmarks -->
        <section id="section-landmarks" class="flex flex-col gap-6">
          <div class="flex items-center justify-between border-b border-[#E8E4DC] pb-4">
            <div class="flex items-center gap-2">
              <button @click="scrollLandmarks(-1)" class="w-10 h-10 rounded-full border border-[#E8E4DC] flex items-center justify-center hover:bg-[#F4F4F2]">
                <svg class="w-3 h-3 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </button>
              <button @click="scrollLandmarks(1)" class="w-10 h-10 rounded-full border border-[#E8E4DC] flex items-center justify-center hover:bg-[#F4F4F2]">
                <svg class="w-3 h-3 text-[#1A1C1B]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
              </button>
            </div>
            <div class="flex items-center gap-2">
              <h3 class="text-base text-[#1A3C5E]">المعالم والأنشطة</h3>
              <svg class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-2 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            </div>
          </div>

          <div ref="landmarksScroll" class="flex items-stretch gap-6 overflow-x-auto pb-2 scroll-smooth">
            <div v-for="lm in city.landmarks" :key="lm.id" @click="viewLandmark(lm)"
              class="w-80 shrink-0 bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden cursor-pointer hover:shadow-md transition-shadow">
              <div class="relative h-48">
                <img :src="lm.image" class="w-full h-full object-cover" :alt="lm.name" />
                <span v-if="lm.badge" class="absolute top-4 right-4 bg-[#C9A84C] text-white text-[10px] font-bold tracking-wider uppercase px-3 py-1 rounded-lg">{{ lm.badge }}</span>
              </div>
              <div class="p-6 flex flex-col gap-2">
                <h4 class="font-bold text-[#1A3C5E] text-base text-right">{{ lm.name }}</h4>
                <p class="text-sm text-[#1A3C5E]/60 text-right leading-relaxed">{{ lm.desc }}</p>
                <div class="border-t border-[#E8E4DC] pt-3 flex items-center justify-between">
                  <svg class="w-4 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
                  <p class="text-sm font-bold text-[#1A3C5E]">
                    <template v-if="lm.price > 0">{{ lm.price }} ج.م <span class="text-xs font-normal opacity-60">{{ lm.unit }}</span></template>
                    <template v-else>{{ lm.unit }}</template>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Community section -->
        <section id="section-community" class="bg-[#FDF8EE] border border-[#C9A84C]/10 rounded-2xl p-6 flex flex-col gap-6">
          <div class="flex items-center justify-between">
            <button @click="openCommunityFeed" class="text-sm font-bold text-[#C9A84C]">عرض الكل في فسحني ←</button>
            <h3 class="text-lg font-medium text-[#1A3C5E] text-right">📸 شايفين {{ city.name }} إزاي من عين المسافرين؟</h3>
          </div>
          <div class="flex items-center gap-4 overflow-x-auto pb-2">
            <button v-for="p in city.communityPhotos" :key="p.id" @click="openCommunityPost(p)"
              class="relative w-36 h-32 shrink-0 rounded-xl overflow-hidden shadow-sm group">
              <img :src="p.image" class="w-full h-full object-cover" alt="" />
              <div class="absolute inset-0 bg-linear-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <span class="absolute top-2 right-1/2 translate-x-1/2 bg-[#C9A84C] text-white text-[8px] px-2 py-0.5 rounded-full whitespace-nowrap">{{ p.tag }}</span>
              <div class="absolute bottom-2 left-2 right-2 flex items-center justify-end gap-1 text-white text-[9px]">
                <span>{{ p.likes }}</span>
                <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20"><path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"/></svg>
              </div>
            </button>
          </div>
        </section>
      </div>
    </div>

    <!-- About the city (dark section) -->
    <section id="section-info" class="bg-[#001D36] text-white">
      <div class="max-w-360 mx-auto px-8 py-16 flex flex-col lg:flex-row gap-16">

        <!-- Map & stats -->
        <div class="w-full lg:w-164 flex flex-col gap-8">
          <div class="relative h-80 bg-white/5 border border-white/10 rounded-2xl overflow-hidden flex items-center justify-center">
            <div class="absolute inset-0 opacity-50" :style="{ background: `linear-gradient(#fff,#fff), url('${city.heroImage}')`, backgroundBlendMode: 'saturation', backgroundSize: 'cover' }"></div>
            <button @click="openInteractiveMap"
              class="relative flex items-center gap-2 bg-[#C9A84C] hover:bg-[#b8963f] text-[#1A3C5E] font-bold px-6 py-2.5 rounded-full transition-colors">
              استكشاف الخريطة التفاعلية
              <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg>
            </button>
            <div class="absolute bottom-4 left-4 bg-black/30 backdrop-blur-sm rounded-xl px-4 py-2 flex items-center gap-2 text-sm">
              <svg class="w-5 h-5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg>
              <span>{{ city.weather.temp }}°م</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-x-6 gap-y-8">
            <div class="border-r-2 border-[#C9A84C]/30 pr-6">
              <p class="text-3xl font-bold text-[#C9A84C]">{{ city.population }}</p>
              <p class="text-sm text-white/60">تعداد السكان</p>
            </div>
            <div class="border-r-2 border-[#C9A84C]/30 pr-6">
              <p class="text-3xl font-bold text-[#C9A84C]">{{ city.areaKm2 }}</p>
              <p class="text-sm text-white/60">المساحة كم²</p>
            </div>
            <div class="border-r-2 border-[#C9A84C]/30 pr-6">
              <p class="text-3xl font-bold text-[#C9A84C]">{{ city.bestMonth }}</p>
              <p class="text-sm text-white/60">أفضل شهر للزيارة</p>
            </div>
            <div class="border-r-2 border-[#C9A84C]/30 pr-6">
              <p class="text-3xl font-bold text-[#C9A84C]">{{ city.avgWinterTemp }}</p>
              <p class="text-sm text-white/60">متوسط حرارة الشتاء</p>
            </div>
          </div>
        </div>

        <!-- About text & getting there -->
        <div class="w-full lg:flex-1 flex flex-col gap-6">
          <h2 class="text-lg text-[#C9A84C] text-right">عن {{ city.name }}</h2>
          <p class="text-lg leading-7.25 text-white/80 text-right">{{ city.about }}</p>

          <div class="flex flex-col gap-4 mt-4">
            <h4 class="font-bold text-white text-right">خيارات الوصول</h4>
            <div class="grid grid-cols-3 gap-4">
              <div v-for="g in city.gettingThere" :key="g.label" class="bg-white/10 rounded-xl p-4 flex flex-col items-center gap-2">
                <svg v-if="g.icon === 'bus'" class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 17H5a2 2 0 01-2-2V9a2 2 0 012-2h11l4 4v4a2 2 0 01-2 2h-3m-6 0a2 2 0 100 4 2 2 0 000-4zm8 0a2 2 0 100 4 2 2 0 000-4z"/></svg>
                <svg v-else-if="g.icon === 'train'" class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7h8m-8 4h8m-6 8l-2 2m8-2l2 2M6 17h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v9a2 2 0 002 2z"/></svg>
                <svg v-else-if="g.icon === 'car'" class="w-5 h-5 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 17h14M5 17a2 2 0 01-2-2v-2.5a1 1 0 01.257-.67L5.5 9.25A2 2 0 017 8.5h10a2 2 0 011.5.75l2.243 2.58a1 1 0 01.257.67V15a2 2 0 01-2 2M5 17a2 2 0 002 2h1a2 2 0 002-2m8 0a2 2 0 002 2h1a2 2 0 002-2M8 13h8"/></svg>
                <svg v-else class="w-5 h-5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
                <span class="text-xs text-white text-center">{{ g.label }} ({{ g.duration }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="border-t border-[#C9A84C]/20 py-12 px-8 flex flex-col items-center gap-6">
        <p class="text-lg font-bold text-[#C9A84C] tracking-widest uppercase">فسحني</p>
        <nav class="flex flex-wrap items-center justify-center gap-6">
          <a href="#" class="text-xs text-white/70 tracking-widest uppercase hover:text-white">Contact Us</a>
          <a href="#" class="text-xs text-white/70 tracking-widest uppercase hover:text-white">Heritage Conservation</a>
          <a href="#" class="text-xs text-white/70 tracking-widest uppercase hover:text-white">Terms of Service</a>
          <a href="#" class="text-xs text-white/70 tracking-widest uppercase hover:text-white">Privacy Policy</a>
        </nav>
        <p class="text-xs text-white/70 tracking-widest uppercase text-center">© 2024 fas7ny. Timeless majesty meets modern intelligence.</p>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>