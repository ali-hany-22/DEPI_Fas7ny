<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'

const router = useRouter()

// Form data
const caption = ref('')
const selectedTrip = ref('رحلة الأقصر وأسوان — أبريل ٢٠٢٥')
const selectedLocation = ref('معبد الكرنك، الأقصر')
const privacy = ref('public') // 'public' or 'followers'
const hashtags = ref(['معابد', 'فرعوني', 'الأقصر'])

// Uploaded images (preview)
const uploadedImages = ref([])

// Loading state
const isSubmitting = ref(false)
const isUploading = ref(false)

// File input reference
const fileInput = ref(null)

// Trigger file input
const triggerFileUpload = () => {
  fileInput.value.click()
}

// Handle file selection
const handleFileSelect = (event) => {
  const files = event.target.files
  if (files.length === 0) return

  isUploading.value = true

  // Process each selected file
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    
    // Check if file is an image
    if (!file.type.startsWith('image/')) {
      continue
    }

    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('حجم الصورة كبير جداً. الحد الأقصى 10 ميجابايت')
      continue
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImages.value.push(e.target.result)
      // Reset loading when all images are processed
      if (uploadedImages.value.length === files.length) {
        isUploading.value = false
      }
    }
    reader.onerror = () => {
      alert('حدث خطأ في قراءة الملف')
      isUploading.value = false
    }
    reader.readAsDataURL(file)
  }

  // Reset file input
  event.target.value = ''
}

// Remove image
const removeImage = (index) => {
  uploadedImages.value.splice(index, 1)
}

// Submit post
const submitPost = () => {
  if (!caption.value.trim() && uploadedImages.value.length === 0) {
    alert('يرجى إضافة وصف أو صورة للحظة')
    return
  }

  isSubmitting.value = true
  setTimeout(() => {
    isSubmitting.value = false
    router.push('/UserDashboard')
  }, 1500)
}

// Generate AI caption
const generateAICaption = () => {
  const suggestions = [
    'رحلة لا تُنسى بين معابد الأقصر وأسوان، حيث يروي كل حجر قصة من عظمة الفراعنة. ✨🏛️',
    'لحظة سحرية في قلب التاريخ، بين أعمدة الكرنك الشامخة وأسرار النيل الخالدة. 🌅',
    'كل زاوية في الأقصر تحكي قصة، وكل خطوة هنا تخطو في حضارة عمرها آلاف السنين. 🏺',
    'سحر مصر لا يوصف، جمالها في تفاصيلها الصغيرة وكرم أهلها الكبير. 🇪🇬❤️'
  ]
  caption.value = suggestions[Math.floor(Math.random() * suggestions.length)]
}

// Navigate back
const goBack = () => {
  router.back()
}
</script>

<template>
  <div dir="rtl" class="min-h-screen bg-[#F9F9F7]">
    <Navbar />

    <div class="flex items-center justify-center min-h-[calc(100vh-72px)] p-4">
      
      <!-- Modal Card -->
      <div class="bg-white rounded-xl shadow-lg max-w-198 w-full max-h-[90vh] overflow-y-auto">
        
        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-[#D0C5B2]/20">
          <button 
            @click="goBack" 
            class="p-1 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer"
          >
            <svg class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
          <h2 class="text-xl md:text-2xl font-medium text-[#1A1C1B]">شارك لحظة من رحلتك</h2>
          <div class="w-4"></div>
        </div>

        <!-- Progress Bar -->
        <div class="px-6 pt-4 pb-2">
          <div class="flex gap-2">
            <div class="h-1.5 flex-1 bg-[#C9A84C] rounded-full"></div>
            <div class="h-1.5 flex-1 bg-[#C9A84C] rounded-full"></div>
          </div>
          <div class="flex justify-between mt-1 text-[10px]">
            <span class="text-[#755B00]">إضافة التفاصيل</span>
            <span class="text-[#4D4637]">رفع الوسائط</span>
          </div>
        </div>

        <!-- Content -->
        <div class="p-6 space-y-6">
          
          <!-- Media Preview Grid -->
          <div class="flex items-center gap-2 overflow-x-auto pb-2">
            <!-- Add Image Button -->
            <button 
              @click="triggerFileUpload"
              :disabled="isUploading"
              class="w-20 h-20 border-2 border-dashed border-[#D0C5B2]/40 rounded-lg flex items-center justify-center hover:border-[#C9A84C] transition-colors shrink-0 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="!isUploading" class="w-4 h-4 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/>
              </svg>
              <div v-else class="w-4 h-4 border-2 border-[#C9A84C] border-t-transparent rounded-full animate-spin"></div>
            </button>
            
            <!-- Hidden File Input -->
            <input 
              ref="fileInput"
              type="file"
              accept="image/*"
              multiple
              class="hidden"
              @change="handleFileSelect"
            />

            <!-- Uploaded Images -->
            <div v-for="(img, index) in uploadedImages" :key="index" 
              class="relative w-20 h-20 rounded-lg overflow-hidden border border-[#D0C5B2]/30 shrink-0 group"
            >
              <img :src="img" alt="Upload" class="w-full h-full object-cover">
              <button 
                @click="removeImage(index)"
                class="absolute top-1 right-1 bg-black/60 hover:bg-black/80 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
              >
                ✕
              </button>
            </div>

            <!-- Uploading indicator -->
            <div v-if="isUploading" class="w-20 h-20 rounded-lg border-2 border-dashed border-[#C9A84C]/40 flex items-center justify-center shrink-0">
              <div class="w-6 h-6 border-2 border-[#C9A84C] border-t-transparent rounded-full animate-spin"></div>
            </div>
          </div>

          <!-- Caption Textarea -->
          <div class="relative">
            <textarea 
              v-model="caption"
              placeholder="اكتب وصف للحظة دي..."
              class="w-full h-36 p-4 bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-xl resize-none text-right focus:outline-none focus:border-[#C9A84C] transition-colors"
            ></textarea>
            
            <!-- AI Suggestion Button -->
            <button 
              @click="generateAICaption"
              class="absolute left-4 bottom-4 bg-white/80 backdrop-blur-sm border border-[#C9A84C]/30 rounded-full px-3 py-1.5 flex items-center gap-2 hover:bg-white transition-colors cursor-pointer"
            >
              <span class="text-sm text-[#755B00]">اقتراح وصف بالـ AI</span>
              <svg class="w-4 h-4 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </button>
          </div>

          <!-- Location & Trip -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <!-- Trip Selector -->
            <div class="bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-lg p-2.5 flex items-center gap-2 cursor-pointer hover:border-[#C9A84C] transition-colors">
              <svg class="w-3.5 h-3.5 text-[#7E7665]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 3a2 2 0 00-2 2v14l7-3.5L17 19V5a2 2 0 00-2-2H5z"/>
              </svg>
              <select v-model="selectedTrip" class="bg-transparent text-sm text-[#1A1C1B] focus:outline-none flex-1 text-right cursor-pointer">
                <option>رحلة الأقصر وأسوان — أبريل ٢٠٢٥</option>
                <option>رحلة القاهرة والإسكندرية — مارس ٢٠٢٥</option>
                <option>رحلة الغردقة وشرم الشيخ — فبراير ٢٠٢٥</option>
              </select>
              <svg class="w-4 h-4 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M7 5l5 5-5 5-1.5-1.5L9 10 5.5 6.5 7 5z"/>
              </svg>
            </div>

            <!-- Location Selector -->
            <div class="bg-[#F4F4F2] border border-[#D0C5B2]/30 rounded-lg p-2.5 flex items-center gap-2 cursor-pointer hover:border-[#C9A84C] transition-colors">
              <svg class="w-3.5 h-3.5 text-[#755B00]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
              </svg>
              <select v-model="selectedLocation" class="bg-transparent text-sm text-[#1A1C1B] focus:outline-none flex-1 text-right cursor-pointer">
                <option>معبد الكرنك، الأقصر</option>
                <option>أهرامات الجيزة، القاهرة</option>
                <option>مكتبة الإسكندرية، الإسكندرية</option>
              </select>
              <svg class="w-4 h-4 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20">
                <path d="M7 5l5 5-5 5-1.5-1.5L9 10 5.5 6.5 7 5z"/>
              </svg>
            </div>
          </div>

          <!-- Hashtags -->
          <div class="flex flex-wrap gap-1.5">
            <span v-for="tag in hashtags" :key="tag" 
              class="bg-[#C9A84C]/10 text-[#755B00] text-sm px-4 py-1 rounded-full cursor-pointer hover:bg-[#C9A84C]/20 transition-colors">
              #{{ tag }}
            </span>
          </div>

          <!-- Privacy -->
          <div class="flex items-center justify-end gap-4 pt-1">
            <label class="flex items-center gap-2 cursor-pointer hover:text-[#755B00] transition-colors">
              <span class="text-sm text-[#1A1C1B]">متابعينّي فقط</span>
              <input type="radio" v-model="privacy" value="followers" class="w-4 h-4 accent-[#755B00] cursor-pointer">
            </label>
            <label class="flex items-center gap-2 cursor-pointer hover:text-[#755B00] transition-colors">
              <span class="text-sm text-[#1A1C1B]">ظاهر للعامة</span>
              <input type="radio" v-model="privacy" value="public" class="w-4 h-4 accent-[#755B00] cursor-pointer">
            </label>
          </div>

        </div>

        <!-- Footer -->
        <div class="border-t border-[#D0C5B2]/20 p-6 space-y-3">
          <button 
            @click="submitPost"
            :disabled="isSubmitting || (!caption.trim() && uploadedImages.length === 0)"
            class="w-full bg-[#C9A84C] hover:bg-[#b8963f] disabled:bg-[#D0C5B2] disabled:cursor-not-allowed text-[#503D00] font-bold py-3.5 rounded-xl transition-colors text-sm cursor-pointer"
          >
            <span v-if="!isSubmitting">نشر</span>
            <span v-else class="flex items-center justify-center gap-2">
              <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              جاري النشر...
            </span>
          </button>
          <p class="text-center text-xs text-[#755B00]">
            بمشاركتك المحتوى انت بتساهم في بناء تقييمات حقيقية لمصر 🇪🇬
          </p>
        </div>

      </div>
    </div>
  </div>
</template>