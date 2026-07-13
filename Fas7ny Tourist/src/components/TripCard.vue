<script setup>
import { useRouter } from 'vue-router'

defineProps({
  trip: { type: Object, required: true }, // { id, title, heroImage, authorName, authorAvatar, days, locations, likes, priceStart }
})
const router = useRouter()
</script>

<template>
  <button @click="router.push(`/trip/${trip.id}`)"
    class="bg-white border border-[#D0C5B2] rounded-2xl overflow-hidden text-right hover:shadow-md transition-shadow w-full">
    <div class="relative h-48">
      <img :src="trip.heroImage" class="w-full h-full object-cover" :alt="trip.title" />
      <div class="absolute inset-0 bg-linear-to-t from-black/60 via-transparent to-transparent"></div>
      <div class="absolute bottom-3 right-3 left-3 flex items-center justify-between text-white text-xs">
        <span class="flex items-center gap-1">
          {{ trip.likes.toLocaleString() }}
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
        </span>
        <span>{{ trip.days }} أيام • {{ trip.locations }} موقع</span>
      </div>
    </div>
    <div class="p-5 flex flex-col gap-3">
      <h4 class="font-bold text-[#1A3C5E] text-lg leading-snug">{{ trip.title }}</h4>
      <div class="flex items-center gap-2 justify-end">
        <span class="text-sm text-[#4D4637]">{{ trip.authorName }}</span>
        <img :src="trip.authorAvatar" class="w-7 h-7 rounded-full object-cover border border-[#755B00]" :alt="trip.authorName" />
      </div>
      <div class="flex items-center justify-between border-t border-[#F4F4F2] pt-3">
        <span class="text-[#755B00] font-semibold text-sm">عرض الرحلة ←</span>
        <p class="text-right">
          <span class="text-lg font-bold text-[#755B00]">{{ trip.priceStart.toLocaleString() }} ج.م</span>
          <span class="text-xs text-[#4D4637]"> / للفرد</span>
        </p>
      </div>
    </div>
  </button>
</template>