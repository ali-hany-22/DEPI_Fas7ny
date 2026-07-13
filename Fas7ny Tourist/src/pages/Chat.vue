<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

/* =========================================================
   إعداد الـ API - غيّر القيمة دي لعنوان السيرفر بتاعك وقت الدمج
   ========================================================= */
const API_BASE_URL = 'http://127.0.0.1:8000'
const CHAT_ENDPOINT = `${API_BASE_URL}/chat/message`

/* ---------------- Sidebar: conversation history ---------------- */
// كل محادثة بتخزن نفسها في localStorage تحت مفتاح مستقل، عشان لو
// المستخدم رجع تاني يلاقي المحادثات القديمة زي ما هي.
const STORAGE_PREFIX = 'fas7ny_chat_'
const CONV_LIST_KEY = 'fas7ny_chat_list'

function loadConversationList() {
  try {
    const raw = localStorage.getItem(CONV_LIST_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (e) {
    return []
  }
}

function saveConversationList(list) {
  localStorage.setItem(CONV_LIST_KEY, JSON.stringify(list))
}

const conversations = ref(loadConversationList())

function saveCurrentMessages() {
  const active = conversations.value.find((c) => c.active)
  if (!active) return
  localStorage.setItem(STORAGE_PREFIX + active.id, JSON.stringify(messages.value))
}

const selectConversation = (c) => {
  saveCurrentMessages()
  conversations.value.forEach((x) => (x.active = x.id === c.id))
  saveConversationList(conversations.value)
  loadMessagesFor(c.id)
}

function loadMessagesFor(id) {
  try {
    const raw = localStorage.getItem(STORAGE_PREFIX + id)
    messages.value = raw ? JSON.parse(raw) : []
  } catch (e) {
    messages.value = []
  }
  scrollDown()
}

const newChat = () => {
  saveCurrentMessages()
  const id = Date.now()
  conversations.value.unshift({ id, title: 'محادثة جديدة', active: true })
  conversations.value.forEach((x) => (x.active = x.id === id))
  saveConversationList(conversations.value)
  messages.value = []
}

/* ---------------- Messages ---------------- */
const now = () => new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })

// أول رسالة ترحيبية بس - مفيش أي بيانات وهمية تانية، كل حاجة بعد كده
// بتيجي من الـ API الحقيقي.
const WELCOME_MESSAGE = {
  role: 'ai',
  text: 'أهلاً بيك! أنا دليلك للسفر في مصر. اسألني عن فنادق أو مطاعم أو أماكن سياحية في أي مدينة، وهجيبلك أفضل الأماكن الحقيقية المتاحة.',
  time: now(),
}

const messages = ref([])

onMounted(() => {
  if (conversations.value.length === 0) {
    const id = Date.now()
    conversations.value = [{ id, title: 'محادثة جديدة', active: true }]
    saveConversationList(conversations.value)
    messages.value = [WELCOME_MESSAGE]
    saveCurrentMessages()
  } else {
    const active = conversations.value.find((c) => c.active) || conversations.value[0]
    active.active = true
    loadMessagesFor(active.id)
    if (messages.value.length === 0) {
      messages.value = [WELCOME_MESSAGE]
    }
  }
})

const typing = ref(false)
const chatEnd = ref(null)
const scrollDown = () => nextTick(() => chatEnd.value?.scrollIntoView({ behavior: 'smooth' }))

const quickReplies = [
  'فنادق في الأقصر',
  'مطاعم في القاهرة',
  'أماكن ترفيهية في الغردقة',
]

const goToPlace = (place) => {
  // النافيجيشن هنا افتراضي - عدّلها حسب الـ route الفعلي في مشروعك.
  // بنبعت الإحداثيات والاسم كـ query عشان صفحة التفاصيل تقدر تعرضهم
  // من غير ما تحتاج تنادي الـ API تاني.
  router.push({
    path: `/place/${encodeURIComponent(place.name)}`,
    query: { lat: place.latitude, lng: place.longitude },
  })
}

const inputText = ref('')
const errorMessage = ref('')

/* ---------------- إرسال رسالة فعلي للـ API ---------------- */
const sendMessage = async (text) => {
  const value = (text || inputText.value).trim()
  if (!value || typing.value) return

  errorMessage.value = ''
  messages.value.push({ role: 'user', text: value, time: now() })
  inputText.value = ''
  saveCurrentMessages()
  scrollDown()

  typing.value = true
  scrollDown()

  try {
    const response = await fetch(CHAT_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: value }),
    })

    if (!response.ok) {
      throw new Error(`فشل الاتصال بالسيرفر (${response.status})`)
    }

    const data = await response.json()

    // نحدث عنوان المحادثة تلقائيًا من أول رسالة لو لسه "محادثة جديدة"
    const active = conversations.value.find((c) => c.active)
    if (active && active.title === 'محادثة جديدة') {
      active.title = value.length > 30 ? value.slice(0, 30) + '…' : value
      saveConversationList(conversations.value)
    }

    messages.value.push({
      role: 'ai',
      text: data.reply,
      places: data.places && data.places.length > 0 ? data.places : null,
      time: now(),
    })
  } catch (e) {
    errorMessage.value = 'حصل مشكلة في الاتصال بالسيرفر. تأكد إن الباك اند شغال وجرّب تاني.'
    messages.value.push({
      role: 'ai',
      text: 'معنديش رد دلوقتي - في مشكلة في الاتصال. جرّب تاني كمان شوية.',
      time: now(),
    })
    console.error('Chat API error:', e)
  } finally {
    typing.value = false
    saveCurrentMessages()
    scrollDown()
  }
}
</script>

<template>
  <div dir="rtl" class="h-screen w-full flex bg-[#F9F9F7] overflow-hidden">

    <!-- Main chat area -->
    <div class="flex-1 flex flex-col h-full min-w-0">

      <!-- Header -->
      <header class="h-20 bg-white border-b border-[#D0C5B2] flex items-center justify-between px-8 shrink-0">
        <button @click="router.back()" class="w-12 h-12 rounded-full bg-[#F5F2E8] border border-[#C9A84C] flex items-center justify-center">
          <svg class="w-4 h-4 text-[#C9A84C]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/></svg>
        </button>
        <div class="flex items-center gap-4">
          <div class="text-right">
            <h1 class="text-lg font-bold text-[#1A1C1B]">دليل الذكاء الاصطناعي</h1>
            <div class="flex items-center justify-end gap-1.5">
              <span class="text-xs text-[#7E7665]">متاح دائماً</span>
              <span class="w-2 h-2 rounded-full bg-[#10B981]"></span>
            </div>
          </div>
        </div>
      </header>

      <!-- Error banner -->
      <div v-if="errorMessage" class="bg-red-50 border-b border-red-200 text-red-700 text-sm px-8 py-2 text-center">
        {{ errorMessage }}
      </div>

      <!-- Messages -->
      <div class="flex-1 overflow-y-auto px-8 py-8 flex flex-col gap-8">

        <template v-for="(m, i) in messages" :key="i">

          <!-- User bubble -->
          <div v-if="m.role === 'user'" class="flex flex-col items-start gap-1 max-w-2xl">
            <div class="bg-[#416084] text-white rounded-2xl rounded-tl-none px-6 py-4 shadow-sm">
              <p class="text-base text-right">{{ m.text }}</p>
            </div>
            <span class="text-[10px] text-[#1A1C1B]/50 px-1">{{ m.time }}</span>
          </div>

          <!-- AI message -->
          <div v-else class="flex items-start justify-end gap-4 w-full">
            <div class="flex flex-col items-end gap-3 max-w-4xl flex-1">
              <div class="bg-white border border-[#D0C5B2] rounded-2xl rounded-tr-none px-6 py-4 shadow-sm w-full">
                <p class="text-base text-[#1A1C1B] text-right leading-6">{{ m.text }}</p>
              </div>

              <!-- Bento place cards (من الـ API الحقيقي) -->
              <div v-if="m.places" class="grid grid-cols-1 sm:grid-cols-3 gap-4 w-full">
                <div v-for="place in m.places" :key="place.name + place.latitude"
                  class="bg-white border border-[#D0C5B2] rounded-xl overflow-hidden flex flex-col">
                  <div class="relative h-32 bg-[#F4F4F2]">
                    <img v-if="place.image_url" :src="place.image_url" class="w-full h-full object-cover" :alt="place.name" />
                    <span v-if="place.popularity === 'High'" class="absolute top-2 right-2 text-[10px] font-semibold px-2 py-1 rounded-full"
                      style="background:#C9A84C; color:#503D00">الأعلى تقييماً</span>
                  </div>
                  <div class="p-4 flex flex-col gap-1">
                    <h3 class="text-base font-bold text-[#1A1C1B] text-right">{{ place.name }}</h3>
                    <div v-if="place.rating" class="flex items-center justify-end gap-1 text-xs text-[#7E7665]">
                      <span>{{ place.rating }} ({{ place.reviews ?? 0 }} تقييم)</span>
                      <svg class="w-3 h-3 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    </div>
                    <p v-else class="text-xs text-[#7E7665] text-right">لا يوجد تقييم متاح</p>
                    <button @click="goToPlace(place)"
                      class="mt-2 border border-[#C9A84C] text-[#C9A84C] text-xs font-semibold py-2 rounded-lg hover:bg-[#C9A84C]/5 transition-colors">
                      عرض على الخريطة
                    </button>
                  </div>
                </div>
              </div>

              <span class="text-[10px] text-[#1A1C1B]/50 px-1">{{ m.time }}</span>
            </div>
            <div class="w-10 h-10 rounded-full bg-[#C9A84C]/10 border border-[#C9A84C] flex items-center justify-center shrink-0">
              <svg class="w-4.5 h-4.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
            </div>
          </div>
        </template>

        <!-- Typing indicator -->
        <div v-if="typing" class="flex items-center justify-end gap-2">
          <div class="bg-white border border-[#D0C5B2] rounded-full px-6 py-2 flex items-center gap-1">
            <span v-for="n in 3" :key="n" class="w-1.5 h-1.5 rounded-full bg-[#D0C5B2] animate-bounce" :style="{ animationDelay: (n * 0.15) + 's' }"></span>
          </div>
          <div class="w-10 h-10 rounded-full bg-[#C9A84C]/10 border border-[#C9A84C] opacity-50 flex items-center justify-center shrink-0">
            <svg class="w-4.5 h-4.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z"/></svg>
          </div>
        </div>

        <div ref="chatEnd"></div>
      </div>

      <!-- Footer: suggestions + input -->
      <footer class="bg-[#F9F9F7] border-t border-[#D0C5B2] px-8 py-6 flex flex-col gap-6 shrink-0">
        <div class="flex items-center justify-end gap-4 flex-wrap">
          <button v-for="q in quickReplies" :key="q" @click="sendMessage(q)" :disabled="typing"
            class="bg-[#C9A84C]/10 border border-[#C9A84C]/20 text-[#C9A84C] text-sm font-semibold px-6 py-2 rounded-full hover:bg-[#C9A84C]/15 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
            {{ q }}
          </button>
        </div>

        <div class="flex items-center gap-4">
          <button @click="sendMessage()" :disabled="typing || !inputText.trim()"
            class="w-14 h-14 rounded-full bg-[#C9A84C] hover:bg-[#b8963f] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shrink-0 shadow-[0_10px_15px_-3px_rgba(201,168,76,0.2),0_4px_6px_-4px_rgba(201,168,76,0.2)] transition-colors">
            <svg class="w-5 h-5 text-[#503D00] -rotate-90" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg>
          </button>
          <div class="flex-1 flex items-center gap-4 bg-[#F4F4F2] border border-[#D0C5B2] rounded-2xl px-6 py-4">
            <input v-model="inputText" @keyup.enter="sendMessage()" type="text" placeholder="اسأل عن فنادق أو مطاعم أو أماكن سياحية..."
              :disabled="typing"
              class="flex-1 bg-transparent text-base text-right focus:outline-none placeholder:text-[#7E7665]/50 disabled:opacity-60" />
          </div>
        </div>
      </footer>
    </div>

    <!-- Sidebar: chat history -->
    <aside class="hidden lg:flex flex-col w-80 h-full bg-[#F4F4F2] border-l border-[#D0C5B2] shrink-0">
      <div class="p-6 flex flex-col gap-6">
        <div class="flex items-center justify-between">
          <button @click="newChat" class="w-10 h-10 rounded-xl bg-[#C9A84C] hover:bg-[#b8963f] flex items-center justify-center transition-colors">
            <svg class="w-5 h-5 text-[#503D00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
          </button>
          <span class="text-3xl font-bold text-[#C9A84C]">فسحني</span>
        </div>

        <div class="flex flex-col gap-4">
          <h4 class="text-xs font-semibold tracking-wider uppercase text-[#7E7665] text-right px-2">سجل المحادثات</h4>
          <nav class="flex flex-col gap-2">
            <button v-for="c in conversations" :key="c.id" @click="selectConversation(c)"
              :class="c.active ? 'bg-[#C9A84C] text-[#503D00] font-bold' : 'text-[#4D4637] hover:bg-white/60'"
              class="flex items-center justify-between px-4 py-4 rounded-xl transition-colors text-right">
              <svg class="w-4.5 h-4.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <span class="truncate">{{ c.title }}</span>
            </button>
          </nav>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.animate-bounce {
  animation: chat-bounce 1.2s infinite;
}
@keyframes chat-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40% { transform: translateY(-4px); opacity: 1; }
}
</style>