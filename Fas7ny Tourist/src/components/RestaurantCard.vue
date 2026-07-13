<script setup>
defineProps({
  restaurant: { type: Object, required: true },
  variant: { type: String, default: 'grid' }, // 'trending' | 'grid' | 'wide'
})
defineEmits(['toggle-favorite', 'open'])
</script>

<template>
  <!-- Trending variant: compact card used in the horizontal "trending" row -->
  <div v-if="variant === 'trending'" @click="$emit('open', restaurant)"
    class="bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden cursor-pointer hover:shadow-md transition-shadow">
    <div class="relative h-48">
      <img :src="restaurant.image" class="w-full h-full object-cover" :alt="restaurant.name" />
      <span class="absolute top-3 right-3 flex items-center gap-1 bg-white/90 backdrop-blur-sm text-[#1A3C5E] text-xs font-semibold px-3 py-1.5 rounded-full">
        {{ restaurant.visitors }} زائر
        <svg class="w-3 h-2 text-[#C9A84C]" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd"/></svg>
      </span>
    </div>
    <div class="p-4 flex flex-col gap-1">
      <h4 class="font-bold text-[#1A1C1B] text-lg text-right">{{ restaurant.name }}</h4>
      <p class="text-sm text-[#7E7665] text-right">{{ restaurant.cuisine }} • {{ restaurant.area }}</p>
      <div class="flex items-center justify-end gap-4 border-t border-[#FAFAF8] pt-3 mt-2">
        <div class="flex items-center gap-1">
          <span class="text-sm font-semibold text-[#1A1C1B]">{{ restaurant.rating }}</span>
          <svg class="w-3.5 h-3.5 text-[#F97316]" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
        </div>
        <div class="flex items-center gap-1 text-sm text-[#94A3B8]">
          <span>{{ restaurant.photoCount }} صورة</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M14 8h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        </div>
      </div>
    </div>
  </div>

  <!-- Wide variant: full-width masonry card with quote & price -->
  <div v-else-if="variant === 'wide'" @click="$emit('open', restaurant)"
    class="bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden cursor-pointer hover:shadow-md transition-shadow">
    <div class="h-44">
      <img :src="restaurant.image" class="w-full h-full object-cover" :alt="restaurant.name" />
    </div>
    <div class="p-4 flex flex-col gap-1">
      <h4 class="font-bold text-[#1A1C1B] text-base text-right">{{ restaurant.name }}</h4>
      <p class="text-xs text-[#7E7665] text-right">{{ restaurant.cuisine }} • {{ restaurant.area }}</p>
      <div class="flex items-center justify-between pt-2">
        <span class="bg-[#C9A84C] text-white text-xs font-semibold px-3 py-1 rounded-lg">{{ restaurant.priceLevel }}</span>
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-0.5">
            <span v-for="n in 5" :key="n" class="w-2 h-2 rounded-full" :class="n <= Math.round(restaurant.rating) ? 'bg-[#16A34A]' : 'bg-[#E8E4DC]'"></span>
          </div>
          <span class="text-sm font-semibold text-[#1A1C1B]">{{ restaurant.rating.toFixed(1) }}</span>
          <span class="text-[10px] text-[#94A3B8]">تقييم TripAdvisor</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Grid variant (default): richer card with quote, availability, wifi note, footer links -->
  <div v-else class="bg-white border border-[#E8E4DC] rounded-2xl overflow-hidden">
    <div class="relative h-52">
      <img :src="restaurant.image" class="w-full h-full object-cover" :alt="restaurant.name" />
      <div v-if="restaurant.tags && restaurant.tags.length" class="absolute bottom-3 right-3 flex items-center gap-1">
        <span v-for="tag in restaurant.tags" :key="tag.label"
          :class="tag.color || 'bg-[#C9A84C] text-[#503D00]'"
          class="text-[10px] font-semibold px-2.5 py-1 rounded-full">{{ tag.label }}</span>
      </div>
      <button @click.stop="$emit('toggle-favorite', restaurant)"
        class="absolute top-3 left-3 w-7 h-7 bg-white rounded-lg shadow flex items-center justify-center">
        <svg class="w-4 h-4" :class="restaurant.favorite ? 'text-[#C9A84C]' : 'text-[#1A1C1B]/40'" :fill="restaurant.favorite ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
      </button>
    </div>
    <div class="p-4 flex flex-col gap-3">
      <h4 class="font-bold text-[#1A1C1B] text-lg text-right">{{ restaurant.name }}</h4>

      <p v-if="restaurant.quote" class="text-xs font-semibold text-[#7E7665] text-right leading-relaxed">
        "{{ restaurant.quote }}"
      </p>

      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-2 justify-end">
          <span class="text-xs font-medium" :class="restaurant.availableNow ? 'text-[#16A34A]' : 'text-[#94A3B8]'">
            {{ restaurant.availableNow ? 'متاح الآن' : 'مغلق حالياً' }}
          </span>
          <span class="w-2 h-2 rounded-full" :class="restaurant.availableNow ? 'bg-[#22C55E]' : 'bg-[#94A3B8]'"></span>
        </div>
        <div v-if="restaurant.wifiNote" class="flex items-center justify-end gap-2 bg-[#F4F4F2] rounded-lg px-3 py-2">
          <span class="text-[10px] text-[#1A1C1B]">{{ restaurant.wifiNote }}</span>
          <svg class="w-3.5 h-2.5 text-[#755B00]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01M5.636 12.929a9 9 0 0112.728 0M2.929 9.343a13 13 0 0118.142 0"/></svg>
        </div>
      </div>

      <div class="flex items-center justify-between border-t border-[#FAFAF8] pt-3">
        <button @click.stop="$emit('open', restaurant)" class="text-xs font-semibold text-[#755B00]">التفاصيل ←</button>
        <span v-if="restaurant.instagramActive" class="flex items-center gap-1 text-[10px] text-[#3B82F6]">
          نشط على انستجرام
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0z"/></svg>
        </span>
      </div>
    </div>
  </div>
</template>