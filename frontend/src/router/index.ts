import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/raffles',
      name: 'raffles',
      component: () => import('../views/RafflesView.vue')
    },
    {
      path: '/raffle/:id',
      name: 'raffle-detail',
      component: () => import('../views/RaffleDetailView.vue')
    },
    {
      path: '/create',
      name: 'create',
      component: () => import('../views/CreateRaffleView.vue')
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue')
    }
  ]
})

export default router