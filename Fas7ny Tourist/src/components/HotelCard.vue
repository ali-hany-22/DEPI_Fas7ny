<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  hotel: { type: Object, required: true }, // { id, name, badge, rating, stars, pricePerNight, category, image, favorite }
  city: { type: String, required: true },  // must match a key in CityDetail.vue's citiesAccommodations / HotelDetail.vue's citiesAccommodations
})
const emit = defineEmits(['toggle-favorite'])

const router = useRouter()

const openHotel = () => {
  router.push(`/hotel/${encodeURIComponent(props.city)}/${props.hotel.id}`)
}
</script>

<template>
  <div class="bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden">
    <button @click="openHotel" class="relative h-56 w-full block">
      <img :src="hotel.image" class="w-full h-full object-cover" :alt="hotel.name" />
      <span v-if="hotel.badge" class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm text-[#1A3C5E] text-xs font-bold px-3 py-1 rounded-full">{{ hotel.badge }}</span>
      <button @click.stop="emit('toggle-favorite', hotel)"
        class="absolute bottom-4 right-4 w-9 h-9 rounded-full bg-white/80 flex items-center justify-center">
        <svg class="w-5 h-5" :class="hotel.favorite ? 'text-[#C94B4B]' : 'text-[#1A3C5E]'" :fill="hotel.favorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
      </button>
    </button>
    <div class="p-6 flex flex-col gap-2">
      <div class="flex items-start justify-between gap-2">
        <span class="flex items-center gap-1 bg-[#F0FDF4] text-[#15803D] text-xs font-bold px-2 py-1 rounded-lg shrink-0">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
          {{ hotel.rating }}
        </span>
        <button @click="openHotel" class="font-bold text-[#1A3C5E] text-lg text-right hover:text-[#755B00] transition-colors">{{ hotel.name }}</button>
      </div>
      <div class="flex items-center gap-1 justify-end">
        <svg v-for="n in hotel.stars" :key="n" class="w-3.5 h-3.5 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
      </div>
      <div class="flex items-center justify-between pt-2">
        <button @click="openHotel" class="bg-[#1A3C5E] hover:bg-[#152f4a] text-white text-sm font-bold px-4 py-2 rounded-xl transition-colors">عرض التفاصيل</button>
        <p class="text-right">
          <span class="text-2xl font-bold text-[#1A3C5E]">{{ hotel.pricePerNight.toLocaleString() }}</span>
          <span class="text-sm text-[#1A3C5E]/60"> ج.م / ليلة</span>
        </p>
      </div>
    </div>
  </div>
</template>