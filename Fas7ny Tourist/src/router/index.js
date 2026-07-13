import { createRouter, createWebHistory } from 'vue-router'

import Home from '../pages/Home.vue'
import Search from '../pages/Search.vue'
import Login from '../pages/Login.vue'
import BookTrip from '../pages/BookTrip.vue'
import TripAlbum from '../pages/TripAlbum.vue'
import AddPost from '../pages/AddPost.vue'
import Community from '../pages/Community.vue'
import Booked from '../pages/Booked.vue'
import Payment from '../pages/Payment.vue'
import Transport from '../pages/Transport.vue'
import Restaurants from '../pages/Restaurants.vue'
import Chat from '../pages/Chat.vue'
import TripHistory from '../pages/TripHistory.vue'
import Map from '../pages/Map.vue'
import Help from '../pages/Help.vue'
import CityDetail from '../pages/CityDetail.vue'
import HotelDetail from '../pages/HotelDetail.vue'
import TripDetail from '../pages/TripDetail.vue'
import Register from '../pages/Register.vue'
import UserDashboard from '../pages/UserDashboard.vue'

const routes = [
  { path: '/', redirect: '/login' },

  { path: '/login', component: Login },
  { path: '/register', component: Register },

  { path: '/home', component: Home },
  { path: '/search', component: Search },
  { path: '/book-trip', name: 'BookTrip', component: BookTrip },
  { path: '/trip-album', component: TripAlbum },
  { path: '/add-post', component: AddPost },
  { path: '/community', component: Community },
  { path: '/booked', component: Booked },
  { path: '/payment', component: Payment },
  { path: '/transport', component: Transport },
  { path: '/restaurants', component: Restaurants },
  { path: '/chat', component: Chat },
  { path: '/trip-history', component: TripHistory },
  { path: '/map', component: Map },
  { path: '/help', component: Help },
  { path: '/city/:name', component: CityDetail },
  { path: '/hotel/:city/:id', component: HotelDetail },
  { path: '/trip/:id', component: TripDetail },

  {
    path: '/ai-trip-planner',
    name: 'AiTripPlanner',
    component: () => import('../pages/AiTripPlanner.vue'),
  },

  { path: '/user-dashboard', component: UserDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router