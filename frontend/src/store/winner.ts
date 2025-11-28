import { defineStore } from 'pinia'
import { ref } from 'vue'
import { winnerApi } from '@/api/modules'

// 定义类型
interface Winner {
  id: number
  name: string
  email: string
  phone: string
  prize_name: string
  prize_level: number
  raffle_id: number
  created_at: string
}

interface DrawResult {
  winners: Winner[]
  total_count: number
}

export const useWinnerStore = defineStore('winner', () => {
  // 状态
  const winners = ref<Winner[]>([])
  const currentWinner = ref<Winner | null>(null)
  const loading = ref(false)
  const drawResult = ref<DrawResult | null>(null)

  // 方法
  const fetchWinners = async (params = {}) => {
    loading.value = true
    try {
      const response = await winnerApi.getWinners(params)
      winners.value = response.items || []
      return response
    } catch (error) {
      console.error('获取中奖者列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createWinner = async (winnerData: any) => {
    loading.value = true
    try {
      const newWinner = await winnerApi.createWinner(winnerData)
      winners.value.push(newWinner)
      return newWinner
    } catch (error) {
      console.error('创建中奖者记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const drawRaffle = async (drawData: any) => {
    loading.value = true
    try {
      const result = await winnerApi.drawRaffle(drawData)
      drawResult.value = result
      // 将新的中奖者添加到列表中
      if (result.winners && result.winners.length > 0) {
        winners.value.push(...result.winners)
      }
      return result
    } catch (error) {
      console.error('抽奖失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const getWinnersByRaffleId = async (raffleId: number) => {
    loading.value = true
    try {
      const response = await winnerApi.getWinners({ raffle_id: raffleId })
      return response.items || []
    } catch (error) {
      console.error('获取抽奖活动中奖者失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const clearDrawResult = () => {
    drawResult.value = null
  }

  return {
    // 状态
    winners,
    currentWinner,
    loading,
    drawResult,
    
    // 方法
    fetchWinners,
    createWinner,
    drawRaffle,
    getWinnersByRaffleId,
    clearDrawResult
  }
})