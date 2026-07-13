<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

/* ---------------- Toast ---------------- */
const toastMessage = ref('')
let toastTimer = null
const showToast = (msg) => {
  toastMessage.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toastMessage.value = ''), 2200)
}

/* =========================================================================
   ADD POST MODAL
   ========================================================================= */
const showAddPost = ref(false)
const openAddPost = () => { showAddPost.value = true }
const closeAddPost = () => { showAddPost.value = false; resetComposer() }

const composerImages = ref([])
const isUploadingMedia = ref(false)
const fileInput = ref(null)

const triggerFileUpload = () => {
  if (composerImages.value.length >= 6) return showToast('يمكنك إضافة ٦ صور كحد أقصى')
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = event.target.files
  if (!files || !files.length) return
  isUploadingMedia.value = true

  const remaining = 6 - composerImages.value.length
  const toProcess = Array.from(files).slice(0, remaining)
  let processed = 0

  toProcess.forEach((file) => {
    if (!file.type.startsWith('image/')) { processed++; return }
    if (file.size > 10 * 1024 * 1024) {
      showToast('حجم الصورة كبير جداً (الحد الأقصى 10 ميجابايت)')
      processed++
      if (processed === toProcess.length) isUploadingMedia.value = false
      return
    }
    const reader = new FileReader()
    reader.onload = (e) => {
      composerImages.value.push(e.target.result)
      processed++
      if (processed === toProcess.length) isUploadingMedia.value = false
    }
    reader.onerror = () => {
      showToast('حدث خطأ أثناء قراءة الملف')
      processed++
      if (processed === toProcess.length) isUploadingMedia.value = false
    }
    reader.readAsDataURL(file)
  })

  event.target.value = ''
}
const removeComposerImage = (i) => composerImages.value.splice(i, 1)

const composerCaption = ref('')
const suggestCaption = () => {
  composerCaption.value = 'لحظة ما تتنسيش وسط سحر التاريخ المصري ✨'
  showToast('تم اقتراح وصف بالذكاء الاصطناعي')
}

const composerLocation = ref('')
const composerTrip = ref('')
const tripOptions = ['بدون رحلة محددة', 'رحلة الأقصر وأسوان — أبريل ٢٠٢٥', 'رحلة سيوة الشتوية']

const composerHashtagPool = ['#معابد', '#فرعوني', '#الأقصر', '#نيل', '#شواطئ', '#تراث']
const composerHashtags = ref([])
const toggleComposerHashtag = (tag) => {
  const i = composerHashtags.value.indexOf(tag)
  if (i === -1) composerHashtags.value.push(tag)
  else composerHashtags.value.splice(i, 1)
}

const composerPrivacy = ref('public')

const resetComposer = () => {
  composerImages.value = []
  composerCaption.value = ''
  composerLocation.value = ''
  composerTrip.value = ''
  composerHashtags.value = []
  composerPrivacy.value = 'public'
}

const canPublish = computed(() => composerImages.value.length > 0 && composerCaption.value.trim().length > 0)

const publishPost = () => {
  if (!canPublish.value) {
    showToast('أضف صورة ووصف على الأقل قبل النشر')
    return
  }
  posts.value.unshift({
    id: Date.now(),
    type: composerImages.value.length > 1 ? 'album' : 'photo',
    author: myProfile.name,
    avatar: myProfile.avatar,
    time: 'الآن',
    location: composerLocation.value || null,
    image: composerImages.value[0],
    images: composerImages.value,
    extraCount: Math.max(0, composerImages.value.length - 3),
    albumTitle: composerImages.value.length > 1 ? 'ألبوم رحلة ✨' : null,
    caption: composerCaption.value,
    hashtags: composerHashtags.value,
    comments: 0, likes: 0, liked: false, saved: false,
    bookable: false,
    showComments: false, newComment: '', commentsList: [],
  })
  showToast('تم نشر منشورك!')
  closeAddPost()
}

/* ---------------- Stories ---------------- */
const stories = ref([
  { id: 1, name: 'ليلى', place: 'القاهرة', avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&q=80', seen: true },
  { id: 2, name: 'أحمد', place: 'سيناء', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&q=80', seen: false },
  { id: 3, name: 'مريم', place: 'أسوان', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&q=80', seen: false },
  { id: 4, name: 'ياسين', place: 'الأقصر', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&q=80', seen: false },
])
const openStory = (s) => showToast(`عرض قصة ${s.name}...`)
const addStory = () => openAddPost()

/* ---------------- Filters ---------------- */
const sortOptions = [
  { id: 'all', label: 'الكل' },
  { id: 'latest', label: 'الأحدث' },
  { id: 'trending', label: 'الأكثر تفاعلاً' },
]
const activeSort = ref('all')

const hashtagFilters = ref([
  { id: 'pharaonic', label: '#فرعوني', active: false },
  { id: 'nile', label: '#نيل', active: false },
  { id: 'beaches', label: '#شواطئ', active: false },
])
const toggleHashtag = (h) => (h.active = !h.active)

/* ---------------- Posts ---------------- */
const posts = ref([
  {
    id: 1, type: 'photo',
    author: 'ياسين المنشاوي', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&q=80',
    time: 'منذ ساعتين', location: 'معبد فيلة، أسوان',
    image: 'https://images.unsplash.com/photo-1608896862894-31d7e46b1e57?w=1200&q=80',
    caption: 'سحر معبد فيلة في الليل ملوش مثيل. التفاصيل والنور بيحسسوك إنك رجعت بالزمن.',
    hashtags: ['#تاريخ', '#أسوان', '#مصر'],
    comments: 18, likes: 245, liked: false, saved: false,
    bookable: true,
    showComments: false, newComment: '',
    commentsList: [
      { author: 'مريم ناصر', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&q=80', text: 'يا سلام على الإضاءة! لازم أزوره قريب.', time: 'منذ ساعة' },
    ],
  },
  {
    id: 2, type: 'album',
    author: 'مريم ناصر', avatar: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=200&q=80',
    time: 'منذ ٥ ساعات', albumTitle: 'ألبوم رحلة: شتاء سيوة',
    images: [
      'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&q=80',
      'https://images.unsplash.com/photo-1544025162-d76694265947?w=600&q=80',
      'https://images.unsplash.com/photo-1502680390469-be75c86b636f?w=600&q=80',
    ],
    extraCount: 5,
    comments: 6, likes: 132, liked: false, saved: false,
    showComments: false, newComment: '', commentsList: [],
  },
  {
    id: 3, type: 'video',
    author: 'أحمد جلال', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&q=80',
    time: 'منذ يوم', location: 'القاهرة المعز',
    thumbnail: 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1000&q=80',
    views: '١.٥ك',
    caption: 'أجواء شارع المعز في الشتا حاجة تانية خالص 🏮❤️',
    hashtags: ['#تراث', '#القاهرة'],
    comments: 9, likes: 88, liked: false, saved: false,
    showComments: false, newComment: '', commentsList: [],
  },
])

const toggleLike = (post) => {
  post.liked = !post.liked
  post.likes += post.liked ? 1 : -1
}
const toggleSave = (post) => {
  post.saved = !post.saved
  showToast(post.saved ? 'تم الحفظ في المفضلة' : 'تم إزالة الحفظ')
}
const toggleComments = (post) => {
  post.showComments = !post.showComments
}
const submitComment = (post) => {
  const text = post.newComment.trim()
  if (!text) return
  post.commentsList.push({
    author: myProfile.name,
    avatar: myProfile.avatar,
    text,
    time: 'الآن',
  })
  post.comments += 1
  post.newComment = ''
}
const sharePost = () => showToast('جاري تجهيز رابط المشاركة...')
const addPostToTrip = () => showToast('تمت الإضافة لرحلتك المقترحة')
const bookExperience = () => router.push('/search')
const playVideo = () => showToast('تشغيل الفيديو...')

/* ---------------- Sidebar data ---------------- */
const myProfile = { name: 'عمر فاروق', bio: 'مستكشف الأهرامات 🏺', avatar: 'https://images.unsplash.com/photo-1633332755192-727a05c4013d?w=200&q=80', posts: 42, followers: '١.٢ك', trips: 51 }

const trending = ref([
  { rank: 1, name: 'واحة سيوة', newPosts: 120, image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=200&q=80' },
  { rank: 2, name: 'معبد الكرنك', newPosts: 85, image: 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=200&q=80' },
])
const goToTrending = (t) => router.push({ path: '/search', query: { q: t.name } })

const popularHashtags = [
  { tag: '#شتاء_مصر', count: '١.٨ك' },
  { tag: '#فرعوني', count: '٢.٤ك' },
  { tag: '#دهب', count: '٩٠٠' },
  { tag: '#طعام_مصري', count: '٥٠٠' },
]

const openAiInspiration = () => router.push('/ai-trip-planner')
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">
    <Navbar />

    <Transition name="fade">
      <div v-if="toastMessage"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#1A3C5E] text-white text-sm px-5 py-3 rounded-full shadow-lg">
        {{ toastMessage }}
      </div>
    </Transition>

    <div class="max-w-360 mx-auto px-4 md:px-6 pt-20 md:pt-24 pb-16 flex flex-col gap-6">

      <!-- Hero banner -->
      <div class="relative bg-linear-to-l from-[#1A3C5E] to-[#2A5A7E] rounded-xl p-8 flex flex-col md:flex-row items-center justify-between gap-6 overflow-hidden">
        <svg class="absolute top-0 right-0 w-25 h-26 text-[#1A1C1B] opacity-10" fill="currentColor" viewBox="0 0 20 20"><path d="M12 2C8 6 6 9 6 13a6 6 0 0012 0c0-4-2-7-6-11z"/></svg>

        <div class="flex flex-col gap-1 order-1 md:order-1 text-right z-10">
          <h1 class="flex items-center justify-end gap-2 text-4xl font-bold text-white">
            فسحني
            <span class="text-3xl">📸</span>
          </h1>
          <p class="text-lg text-white/70">شارك لحظاتك السحرية في أرض الكنانة مع مجتمع المسافرين.</p>
        </div>

        <button @click="openAddPost"
          class="order-2 md:order-2 w-full md:w-80 bg-white/95 backdrop-blur-sm border border-white/20 rounded-xl p-4 flex flex-col gap-4 shadow-[0_10px_15px_-3px_rgba(0,0,0,0.1),0_4px_6px_-4px_rgba(0,0,0,0.1)] z-10 text-right">
          <div class="flex items-center justify-end gap-4">
            <div>
              <p class="font-bold text-[#1A1C1B] text-base">أضف لحظة من رحلتك</p>
              <p class="text-sm text-[#4D4637]">الصور، الفيديوهات أو الألبومات</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-[#C9A84C]/20 flex items-center justify-center shrink-0">
              <svg class="w-6 h-5.5 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><circle cx="12" cy="13" r="4"/></svg>
            </div>
          </div>
          <span class="bg-[#C9A84C] hover:bg-[#b8963f] text-[#503D00] font-bold py-2.5 rounded-xl flex items-center justify-center gap-2 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4"/></svg>
            إضافة منشور
          </span>
        </button>
      </div>

      <!-- Stories row -->
      <div class="bg-[#F9F9F7]/95 backdrop-blur-sm border-b border-[#D0C5B2]/20 py-4 flex items-center gap-6 overflow-x-auto">
        <button @click="addStory" class="flex flex-col items-center gap-1 shrink-0">
          <div class="w-16 h-16 rounded-full border-2 border-dashed border-[#D0C5B2] flex items-center justify-center">
            <svg class="w-3.5 h-3.5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          </div>
          <span class="text-sm text-[#4D4637]">قصتك</span>
        </button>
        <button v-for="s in stories" :key="s.id" @click="openStory(s)" class="flex flex-col items-center gap-1 shrink-0" :class="s.seen ? 'opacity-50' : ''">
          <div class="p-0.5 rounded-full" :class="s.seen ? '' : 'bg-linear-to-br from-[#C9A84C] to-[#AA3436]'">
            <img :src="s.avatar" class="w-15 h-15 rounded-full border-2 border-white object-cover" :alt="s.name" />
          </div>
          <span class="text-sm font-bold text-[#1A1C1B]">{{ s.name }}</span>
          <span class="bg-[#EEEEEC] text-[10px] text-[#4D4637] px-2 py-0.5 rounded-full">{{ s.place }}</span>
        </button>
      </div>

      <!-- Main layout: feed (right) + sidebar (left) -->
      <div class="flex flex-col lg:flex-row items-start gap-8">

        <!-- Feed -->
        <div class="flex-1 w-full flex flex-col gap-6 min-w-0">

          <!-- Filter bar -->
          <div class="sticky top-18 z-20 bg-[#F9F9F7]/95 backdrop-blur-md border-b border-[#D0C5B2]/20 py-2 flex items-center gap-4 overflow-x-auto">
            <button v-for="opt in sortOptions" :key="opt.id" @click="activeSort = opt.id"
              :class="activeSort === opt.id ? 'bg-[#C9A84C] text-[#503D00] font-bold' : 'bg-white border border-[#D0C5B2]/30 text-[#4D4637]'"
              class="px-6 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors">
              {{ opt.label }}
            </button>
            <div class="w-px h-6 bg-[#D0C5B2]/40 shrink-0"></div>
            <button v-for="h in hashtagFilters" :key="h.id" @click="toggleHashtag(h)"
              :class="h.active ? 'bg-[#C9A84C]/10 border-[#C9A84C] text-[#755B00]' : 'bg-white border-[#D0C5B2]/30 text-[#4D4637]'"
              class="px-6 py-1.5 rounded-full text-sm border whitespace-nowrap transition-colors">
              {{ h.label }}
            </button>
          </div>

          <!-- Posts -->
          <article v-for="post in posts" :key="post.id" class="bg-white border border-[#D0C5B2]/30 rounded-xl overflow-hidden">

            <!-- Header -->
            <div class="flex items-center justify-between p-4">
              <button class="text-[#7E7665]">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/></svg>
              </button>
              <div class="flex items-center gap-4">
                <div class="flex flex-col items-end gap-1">
                  <h4 class="font-bold text-[#1A1C1B] text-base">{{ post.author }}</h4>
                  <div class="flex items-center gap-1 text-xs text-[#D0C5B2]">
                    <span>{{ post.time }}</span>
                    <span v-if="post.location || post.albumTitle">•</span>
                    <span v-if="post.location" class="text-[#755B00] flex items-center gap-1">{{ post.location }}
                      <svg class="w-2.5 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                    </span>
                    <span v-if="post.albumTitle" class="text-[#755B00]">{{ post.albumTitle }} 📸</span>
                  </div>
                </div>
                <img :src="post.avatar" class="w-10 h-10 rounded-full object-cover" :alt="post.author" />
              </div>
            </div>

            <!-- PHOTO post -->
            <template v-if="post.type === 'photo'">
              <div class="bg-[#F4F4F2]">
                <img :src="post.image" class="w-full max-h-150 object-cover" :alt="post.caption" />
              </div>
              <div class="p-4 flex flex-col gap-4">
                <div class="flex items-center justify-between">
                  <button @click="toggleSave(post)">
                    <svg class="w-4.5 h-4.5" :class="post.saved ? 'text-[#C9A84C]' : 'text-[#7E7665]'" :fill="post.saved ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg>
                  </button>
                  <div class="flex items-center gap-6">
                    <button @click="sharePost" class="text-[#7E7665]">
                      <svg class="w-4.5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342a4 4 0 100-2.684M8.684 13.342a4 4 0 004.632 4.632m-4.632-4.632l6.632 3.316m0-8.316a4 4 0 10-4.632-4.632m4.632 4.632L8.684 10.658m8.316-4.632a4 4 0 100 2.684"/></svg>
                    </button>
                    <button @click="toggleComments(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.comments }}</span>
                      <svg class="w-5 h-5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
                    </button>
                    <button @click="toggleLike(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.likes }}</span>
                      <svg class="w-5 h-4.5" :class="post.liked ? 'text-[#AA3436]' : 'text-[#7E7665]'" :fill="post.liked ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </button>
                  </div>
                </div>
                <div class="flex flex-col gap-1">
                  <p class="text-base text-[#1A1C1B] text-right">{{ post.caption }}</p>
                  <div class="flex items-center justify-end gap-2">
                    <span v-for="tag in post.hashtags" :key="tag" class="text-sm font-bold text-[#755B00]">{{ tag }}</span>
                  </div>
                </div>
                <div v-if="post.bookable" class="bg-[#F4F4F2] rounded-lg p-2 flex items-center justify-between">
                  <button @click="addPostToTrip" class="text-sm font-bold text-[#755B00]">أضف للرحلة</button>
                  <button @click="bookExperience" class="flex items-center gap-2 text-sm text-[#1A1C1B]">
                    هذه التجربة متاحة للحجز
                    <svg class="w-4.5 h-5 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  </button>
                </div>

                <!-- Comments panel -->
                <div v-if="post.showComments" class="border-t border-[#F4F4F2] pt-4 flex flex-col gap-3">
                  <div v-for="(c, ci) in post.commentsList" :key="ci" class="flex items-start justify-end gap-2">
                    <div class="bg-[#F4F4F2] rounded-xl rounded-tl-none px-3 py-2 text-right">
                      <p class="text-xs font-bold text-[#1A1C1B]">{{ c.author }}</p>
                      <p class="text-sm text-[#1A1C1B]">{{ c.text }}</p>
                    </div>
                    <img :src="c.avatar" class="w-8 h-8 rounded-full object-cover shrink-0" alt="" />
                  </div>
                  <p v-if="!post.commentsList.length" class="text-sm text-[#7E7665] text-center py-2">لا توجد تعليقات بعد. كن أول من يعلّق!</p>
                  <div class="flex items-center gap-2">
                    <button @click="submitComment(post)" class="text-[#C9A84C] shrink-0">
                      <svg class="w-5 h-5 -rotate-90" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
                    </button>
                    <input v-model="post.newComment" @keyup.enter="submitComment(post)" type="text" placeholder="اكتب تعليقاً..."
                      class="flex-1 bg-[#F4F4F2] rounded-full px-4 py-2 text-sm text-right focus:outline-none" />
                  </div>
                </div>
              </div>
            </template>

            <!-- ALBUM post -->
            <template v-else-if="post.type === 'album'">
              <div class="grid grid-cols-2 gap-1 bg-[#D0C5B2]/20 h-100">
                <img :src="post.images[0]" class="w-full h-full object-cover" alt="" />
                <div class="grid grid-rows-2 gap-1">
                  <img :src="post.images[1]" class="w-full h-full object-cover" alt="" />
                  <div class="relative">
                    <img :src="post.images[2]" class="w-full h-full object-cover" alt="" />
                    <div class="absolute inset-0 bg-black/40 flex items-center justify-center">
                      <span class="text-2xl font-bold text-white">+{{ post.extraCount }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="p-4 flex flex-col gap-4">
                <div class="flex items-center justify-between">
                  <button @click="toggleSave(post)">
                    <svg class="w-4.5 h-4.5" :class="post.saved ? 'text-[#C9A84C]' : 'text-[#7E7665]'" :fill="post.saved ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg>
                  </button>
                  <div class="flex items-center gap-6">
                    <button @click="sharePost" class="text-[#7E7665]">
                      <svg class="w-4.5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342a4 4 0 100-2.684M8.684 13.342a4 4 0 004.632 4.632m-4.632-4.632l6.632 3.316m0-8.316a4 4 0 10-4.632-4.632m4.632 4.632L8.684 10.658m8.316-4.632a4 4 0 100 2.684"/></svg>
                    </button>
                    <button @click="toggleComments(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.comments }}</span>
                      <svg class="w-5 h-5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
                    </button>
                    <button @click="toggleLike(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.likes }}</span>
                      <svg class="w-5 h-4.5" :class="post.liked ? 'text-[#AA3436]' : 'text-[#7E7665]'" :fill="post.liked ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </button>
                  </div>
                </div>

                <div v-if="post.showComments" class="border-t border-[#F4F4F2] pt-4 flex flex-col gap-3">
                  <div v-for="(c, ci) in post.commentsList" :key="ci" class="flex items-start justify-end gap-2">
                    <div class="bg-[#F4F4F2] rounded-xl rounded-tl-none px-3 py-2 text-right">
                      <p class="text-xs font-bold text-[#1A1C1B]">{{ c.author }}</p>
                      <p class="text-sm text-[#1A1C1B]">{{ c.text }}</p>
                    </div>
                    <img :src="c.avatar" class="w-8 h-8 rounded-full object-cover shrink-0" alt="" />
                  </div>
                  <p v-if="!post.commentsList.length" class="text-sm text-[#7E7665] text-center py-2">لا توجد تعليقات بعد. كن أول من يعلّق!</p>
                  <div class="flex items-center gap-2">
                    <button @click="submitComment(post)" class="text-[#C9A84C] shrink-0">
                      <svg class="w-5 h-5 -rotate-90" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
                    </button>
                    <input v-model="post.newComment" @keyup.enter="submitComment(post)" type="text" placeholder="اكتب تعليقاً..."
                      class="flex-1 bg-[#F4F4F2] rounded-full px-4 py-2 text-sm text-right focus:outline-none" />
                  </div>
                </div>
              </div>
            </template>

            <!-- VIDEO post -->
            <template v-else-if="post.type === 'video'">
              <button @click="playVideo" class="relative w-full h-187.5 bg-black block overflow-hidden">
                <img :src="post.thumbnail" class="w-full h-full object-cover opacity-80" :alt="post.caption" />
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="w-20 h-20 rounded-full bg-white/20 border border-white/30 backdrop-blur-md flex items-center justify-center">
                    <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6.3 2.841A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" clip-rule="evenodd"/></svg>
                  </div>
                </div>
                <span class="absolute bottom-4 left-4 flex items-center gap-1 bg-black/40 backdrop-blur-sm rounded px-2 py-1 text-white text-[10px]">
                  {{ post.views }} مشاهدة
                  <svg class="w-3.5 h-2.5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/></svg>
                </span>
              </button>
              <div class="p-4 flex flex-col gap-4">
                <div class="flex flex-col gap-1">
                  <p class="text-base text-[#1A1C1B] text-right">{{ post.caption }}</p>
                  <div class="flex items-center justify-end gap-2">
                    <span v-for="tag in post.hashtags" :key="tag" class="text-sm font-bold text-[#755B00]">{{ tag }}</span>
                  </div>
                </div>

                <div class="flex items-center justify-between">
                  <button @click="toggleSave(post)">
                    <svg class="w-4.5 h-4.5" :class="post.saved ? 'text-[#C9A84C]' : 'text-[#7E7665]'" :fill="post.saved ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg>
                  </button>
                  <div class="flex items-center gap-6">
                    <button @click="sharePost" class="text-[#7E7665]">
                      <svg class="w-4.5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342a4 4 0 100-2.684M8.684 13.342a4 4 0 004.632 4.632m-4.632-4.632l6.632 3.316m0-8.316a4 4 0 10-4.632-4.632m4.632 4.632L8.684 10.658m8.316-4.632a4 4 0 100 2.684"/></svg>
                    </button>
                    <button @click="toggleComments(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.comments }}</span>
                      <svg class="w-5 h-5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
                    </button>
                    <button @click="toggleLike(post)" class="flex items-center gap-1">
                      <span class="font-bold text-sm text-[#1A1C1B]">{{ post.likes }}</span>
                      <svg class="w-5 h-4.5" :class="post.liked ? 'text-[#AA3436]' : 'text-[#7E7665]'" :fill="post.liked ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                    </button>
                  </div>
                </div>

                <div v-if="post.showComments" class="border-t border-[#F4F4F2] pt-4 flex flex-col gap-3">
                  <div v-for="(c, ci) in post.commentsList" :key="ci" class="flex items-start justify-end gap-2">
                    <div class="bg-[#F4F4F2] rounded-xl rounded-tl-none px-3 py-2 text-right">
                      <p class="text-xs font-bold text-[#1A1C1B]">{{ c.author }}</p>
                      <p class="text-sm text-[#1A1C1B]">{{ c.text }}</p>
                    </div>
                    <img :src="c.avatar" class="w-8 h-8 rounded-full object-cover shrink-0" alt="" />
                  </div>
                  <p v-if="!post.commentsList.length" class="text-sm text-[#7E7665] text-center py-2">لا توجد تعليقات بعد. كن أول من يعلّق!</p>
                  <div class="flex items-center gap-2">
                    <button @click="submitComment(post)" class="text-[#C9A84C] shrink-0">
                      <svg class="w-5 h-5 -rotate-90" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
                    </button>
                    <input v-model="post.newComment" @keyup.enter="submitComment(post)" type="text" placeholder="اكتب تعليقاً..."
                      class="flex-1 bg-[#F4F4F2] rounded-full px-4 py-2 text-sm text-right focus:outline-none" />
                  </div>
                </div>
              </div>
            </template>
          </article>
        </div>

        <!-- Sidebar -->
        <aside class="w-full lg:w-105 shrink-0 flex flex-col gap-6">

          <!-- Profile snapshot -->
          <div class="bg-white border border-[#D0C5B2]/30 rounded-xl p-6 flex flex-col gap-6">
            <div class="flex items-center justify-end gap-4">
              <div class="flex flex-col items-end">
                <h3 class="font-bold text-[#1A1C1B] text-base">{{ myProfile.name }}</h3>
                <p class="text-sm text-[#4D4637]">{{ myProfile.bio }}</p>
              </div>
              <img :src="myProfile.avatar" class="w-14 h-14 rounded-full border-2 border-[#C9A84C] object-cover" alt="" />
            </div>
            <div class="border-t border-[#D0C5B2]/20 pt-4 grid grid-cols-3 text-center gap-2">
              <div class="flex flex-col items-center gap-1">
                <span class="font-bold text-base text-[#755B00]">{{ myProfile.posts }}</span>
                <span class="text-xs text-[#4D4637]">منشور</span>
              </div>
              <div class="flex flex-col items-center gap-1">
                <span class="font-bold text-base text-[#755B00]">{{ myProfile.followers }}</span>
                <span class="text-xs text-[#4D4637]">متابع</span>
              </div>
              <div class="flex flex-col items-center gap-1">
                <span class="font-bold text-base text-[#755B00]">{{ myProfile.trips }}</span>
                <span class="text-xs text-[#4D4637]">رحلة</span>
              </div>
            </div>
          </div>

          <!-- Trending destinations -->
          <div class="bg-white border border-[#D0C5B2]/30 rounded-xl p-6 flex flex-col gap-4">
            <div class="flex items-center justify-end gap-2">
              <h3 class="font-bold text-base text-[#1A1C1B]">وجهات رائجة هذا الأسبوع</h3>
              <svg class="w-5 h-3 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
            </div>
            <button v-for="t in trending" :key="t.rank" @click="goToTrending(t)" class="flex items-center gap-4">
              <span class="text-sm text-[#4D4637] shrink-0">{{ t.rank }}٠</span>
              <img :src="t.image" class="w-12 h-12 rounded-lg object-cover shrink-0" alt="" />
              <div class="flex-1 flex flex-col items-end">
                <span class="font-bold text-base text-[#1A1C1B]">{{ t.name }}</span>
                <span class="text-sm text-[#4D4637]">{{ t.newPosts }} منشور جديد</span>
              </div>
            </button>
          </div>

          <!-- Popular hashtags -->
          <div class="bg-white border border-[#D0C5B2]/30 rounded-xl p-6 flex flex-col gap-4">
            <h3 class="font-bold text-base text-[#1A1C1B] text-right">الوسوم النشطة</h3>
            <div class="flex flex-wrap items-center justify-end gap-2">
              <button v-for="h in popularHashtags" :key="h.tag" class="bg-[#F4F4F2] rounded-full px-4 py-1 flex items-center gap-1">
                <span class="text-sm text-[#D0C5B2]">{{ h.count }}</span>
                <span class="text-sm text-[#1A1C1B]">{{ h.tag }}</span>
              </button>
            </div>
          </div>

          <!-- AI Inspiration banner -->
          <div class="relative bg-linear-to-br from-[#C9A84C] to-[#755B00] rounded-xl p-6 overflow-hidden shadow-[0_10px_15px_-3px_rgba(201,168,76,0.2),0_4px_6px_-4px_rgba(201,168,76,0.2)]">
            <div class="absolute -bottom-4 -left-4 w-23 h-23 rounded-full bg-white/10"></div>
            <div class="relative flex flex-col gap-1">
              <div class="flex items-center justify-end gap-1">
                <h4 class="font-bold text-[#503D00] text-base">اكتشافات ذكية</h4>
                <svg class="w-5.5 h-5.5 text-[#503D00]" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
              </div>
              <p class="text-sm text-[#503D00]/90 text-right leading-5 pb-3">خلي الذكاء الاصطناعي يخطط رحلتك القادمة بناءً على الصور اللي بتحبها.</p>
              <button @click="openAiInspiration" class="bg-white text-[#755B00] font-bold text-sm py-2 rounded-lg">جرّب دلوقتي</button>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-[#D0C5B2]/30 py-8 px-6">
      <div class="max-w-360 mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <nav class="flex items-center gap-6">
          <a href="#" class="text-base text-[#7E7665] hover:text-[#1A1C1B]">تواصل معنا</a>
          <a href="#" class="text-base text-[#7E7665] hover:text-[#1A1C1B]">سياسة الخصوصية</a>
          <a href="#" class="text-base text-[#7E7665] hover:text-[#1A1C1B]">الشروط والأحكام</a>
          <a href="#" class="text-base text-[#7E7665] hover:text-[#1A1C1B]">عن فسحني</a>
        </nav>
        <div class="text-right">
          <p class="text-2xl font-semibold text-[#755B00]">فسحني</p>
          <p class="text-base text-[#416084] opacity-80">© ٢٠٢٤ فسحني - اكتشف سحر مصر بروح عصرية</p>
        </div>
      </div>
    </footer>
    <!-- Add Post Modal -->
    <Transition name="fade">
      <div v-if="showAddPost" class="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4" @click.self="closeAddPost">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-198 max-h-[90vh] overflow-y-auto flex flex-col">

          <!-- Header -->
          <div class="flex items-center justify-between p-6 border-b border-[#D0C5B2]/20 shrink-0">
            <button @click="closeAddPost" class="text-[#7E7665] hover:text-[#1A1C1B]">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
            <h2 class="text-2xl font-medium text-[#1A1C1B]">شارك لحظة من رحلتك</h2>
          </div>

          <!-- Progress bar -->
          <div class="px-6 pt-4 flex flex-col gap-1 shrink-0">
            <div class="flex items-center gap-2">
              <div class="flex-1 h-1.5 rounded-full" :class="composerImages.length ? 'bg-[#C9A84C]' : 'bg-[#E8E4DC]'"></div>
              <div class="flex-1 h-1.5 rounded-full" :class="canPublish ? 'bg-[#C9A84C]' : 'bg-[#E8E4DC]'"></div>
            </div>
            <div class="flex items-center justify-between text-[10px]">
              <span :class="canPublish ? 'text-[#755B00]' : 'text-[#4D4637]'">إضافة التفاصيل</span>
              <span :class="composerImages.length ? 'text-[#755B00]' : 'text-[#4D4637]'">رفع الوسائط</span>
            </div>
          </div>

          <!-- Body -->
          <div class="p-6 flex flex-col items-end gap-6">

            <!-- Media preview grid -->
            <div class="flex items-center gap-2 flex-wrap justify-end w-full">
              <div v-for="(img, i) in composerImages" :key="i" class="relative w-20 h-20 rounded-lg border border-[#D0C5B2]/30 overflow-hidden shrink-0 group">
                <img :src="img" class="w-full h-full object-cover" alt="" />
                <button @click="removeComposerImage(i)" class="absolute top-1 left-1 w-5 h-5 rounded-full bg-black/50 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
              <button @click="triggerFileUpload" :disabled="isUploadingMedia" class="w-20 h-20 rounded-lg border-2 border-dashed border-[#D0C5B2]/40 flex items-center justify-center shrink-0 hover:border-[#C9A84C] transition-colors disabled:opacity-50">
                <svg v-if="!isUploadingMedia" class="w-3.5 h-3.5 text-[#7E7665]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                <div v-else class="w-5 h-5 border-2 border-[#C9A84C] border-t-transparent rounded-full animate-spin"></div>
              </button>
              <input ref="fileInput" type="file" accept="image/*" multiple class="hidden" @change="handleFileSelect" />
            </div>

            <!-- Caption -->
            <div class="relative w-full">
              <textarea v-model="composerCaption" rows="4" placeholder="اكتب وصف للحظة دي..."
                class="w-full bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-xl p-4 text-base text-right focus:outline-none focus:border-[#C9A84C] resize-none"></textarea>
              <button @click="suggestCaption" class="absolute bottom-4 left-4 flex items-center gap-1 bg-white/80 backdrop-blur-sm border border-[#C9A84C]/30 rounded-full px-3 py-1.5 text-sm text-[#755B00]">
                اقتراح وصف بالـ AI
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
              </button>
            </div>

            <!-- Location & Trip -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full">
              <div class="flex items-center gap-2 bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-lg px-3 py-2">
                <svg class="w-4 h-5 text-[#C9A84C] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg>
                <input v-model="composerLocation" type="text" placeholder="معبد الكرنك، الأقصر" class="flex-1 bg-transparent text-sm text-right focus:outline-none" />
                <svg class="w-3 h-3 text-[#755B00] shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
              </div>
              <div class="flex items-center gap-2 bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-lg px-3 py-2">
                <svg class="w-4 h-4 text-[#7E7665] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                <select v-model="composerTrip" class="flex-1 bg-transparent text-sm text-right focus:outline-none">
                  <option value="">اختر رحلة (اختياري)</option>
                  <option v-for="t in tripOptions" :key="t" :value="t">{{ t }}</option>
                </select>
                <svg class="w-4.5 h-4.5 text-[#7E7665] shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              </div>
            </div>

            <!-- Hashtags -->
            <div class="flex items-center justify-end gap-1 flex-wrap w-full">
              <button v-for="tag in composerHashtagPool" :key="tag" @click="toggleComposerHashtag(tag)"
                :class="composerHashtags.includes(tag) ? 'bg-[#C9A84C] text-white' : 'bg-[#C9A84C]/10 text-[#755B00]'"
                class="rounded-full px-4 py-1 text-sm transition-colors">
                {{ tag }}
              </button>
            </div>

            <!-- Privacy -->
            <div class="flex items-center justify-center gap-3 w-full text-sm">
              <label class="flex items-center gap-1 cursor-pointer">
                <span :class="composerPrivacy === 'followers' ? 'text-[#1A1C1B] font-bold' : 'text-[#7E7665]'">متابعينّي فقط</span>
                <input type="radio" value="followers" v-model="composerPrivacy" class="w-4 h-4 accent-[#755B00]" />
              </label>
              <label class="flex items-center gap-1 cursor-pointer">
                <span :class="composerPrivacy === 'public' ? 'text-[#1A1C1B] font-bold' : 'text-[#7E7665]'">ظاهر للعامة</span>
                <input type="radio" value="public" v-model="composerPrivacy" class="w-4.5 h-4.5 accent-[#755B00]" />
              </label>
            </div>
          </div>

          <!-- Footer -->
          <div class="p-6 border-t border-[#D0C5B2]/20 flex flex-col gap-4 shrink-0">
            <button @click="publishPost" :disabled="!canPublish"
              class="w-full bg-[#C9A84C] hover:bg-[#b8963f] disabled:opacity-50 text-[#503D00] font-bold py-3.5 rounded-xl transition-colors">
              نشر
            </button>
            <p class="text-center text-[11px] text-[#755B00]">بمشاركتك المحتوى انت بتساهم في بناء تقييمات حقيقية لمصر 🇪🇬</p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>