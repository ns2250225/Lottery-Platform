import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { raffleApi } from '@/api/modules'

// 定义类型
interface Raffle {
  id: number
  title: string
  description: string
  status: string
  start_time: string
  end_time: string
  created_at: string
  updated_at: string
}

interface Pagination {
  current: number
  size: number
  total: number
}

export const useRaffleStore = defineStore('raffle', () => {
  // 状态
  const raffles = ref<Raffle[]>([])
  const currentRaffle = ref<Raffle | null>(null)
  const loading = ref(false)
  const pagination = ref<Pagination>({
    current: 1,
    size: 10,
    total: 0
  })

  // 计算属性
  const activeRaffles = computed(() => {
    return raffles.value.filter(raffle => raffle.status === 'in_progress')
  })

  const finishedRaffles = computed(() => {
    return raffles.value.filter(raffle => raffle.status === 'finished')
  })

  // 方法
  const fetchRaffles = async (params = {}) => {
    loading.value = true
    try {
      const defaultParams = {
        skip: (pagination.value.current - 1) * pagination.value.size,
        limit: pagination.value.size
      }
      
      const response = await raffleApi.getRaffles({ ...defaultParams, ...params })
      raffles.value = response.items || []
      pagination.value.total = response.total || 0
      return response
    } catch (error) {
      console.error('获取抽奖活动列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchRaffleDetail = async (id: number) => {
    loading.value = true
    try {
      const raffle = await raffleApi.getRaffleDetail(id)
      currentRaffle.value = raffle
      return raffle
    } catch (error) {
      console.error('获取抽奖活动详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createRaffle = async (raffleData: any) => {
    loading.value = true
    try {
      const newRaffle = await raffleApi.createRaffle(raffleData)
      raffles.value.unshift(newRaffle)
      return newRaffle
    } catch (error) {
      console.error('创建抽奖活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const updateRaffle = async (id: number, raffleData: any) => {
    loading.value = true
    try {
      const updatedRaffle = await raffleApi.updateRaffle(id, raffleData)
      const index = raffles.value.findIndex(r => r.id === id)
      if (index !== -1) {
        raffles.value[index] = updatedRaffle
      }
      if (currentRaffle.value && currentRaffle.value.id === id) {
        currentRaffle.value = updatedRaffle
      }
      return updatedRaffle
    } catch (error) {
      console.error('更新抽奖活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const deleteRaffle = async (id: number) => {
    loading.value = true
    try {
      await raffleApi.deleteRaffle(id)
      raffles.value = raffles.value.filter(r => r.id !== id)
      if (currentRaffle.value && currentRaffle.value.id === id) {
        currentRaffle.value = null
      }
    } catch (error) {
      console.error('删除抽奖活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const startRaffle = async (id: number, creator_name: string, creator_contact: string) => {
    loading.value = true
    try {
      const updatedRaffle = await raffleApi.startRaffle(id, creator_name, creator_contact)
      const index = raffles.value.findIndex(r => r.id === id)
      if (index !== -1) {
        raffles.value[index] = updatedRaffle
      }
      if (currentRaffle.value && currentRaffle.value.id === id) {
        currentRaffle.value = updatedRaffle
      }
      return updatedRaffle
    } catch (error) {
      console.error('开始抽奖活动失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const resetPagination = () => {
    pagination.value.current = 1
    pagination.value.total = 0
  }

  return {
    // 状态
    raffles,
    currentRaffle,
    loading,
    pagination,
    
    // 计算属性
    activeRaffles,
    finishedRaffles,
    
    // 方法
    fetchRaffles,
    fetchRaffleDetail,
    createRaffle,
    updateRaffle,
    deleteRaffle,
    startRaffle,
    resetPagination
  }
})