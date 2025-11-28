import { defineStore } from 'pinia'
import { ref } from 'vue'
import { participantApi } from '@/api/modules'

// 定义类型
interface Participant {
  id: number
  name: string
  phone: string
  email: string
  raffle_id: number
  created_at: string
  updated_at: string
}

export const useParticipantStore = defineStore('participant', () => {
  // 状态
  const participants = ref<Participant[]>([])
  const currentParticipant = ref<Participant | null>(null)
  const loading = ref(false)

  // 方法
  const fetchParticipants = async (params = {}) => {
    loading.value = true
    try {
      const response = await participantApi.getParticipants(params)
      participants.value = response.items || []
      return response
    } catch (error) {
      console.error('获取参与者列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createParticipant = async (participantData: any) => {
    loading.value = true
    try {
      const newParticipant = await participantApi.createParticipant(participantData)
      participants.value.push(newParticipant)
      return newParticipant
    } catch (error) {
      console.error('创建参与者失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const updateParticipant = async (id: number, participantData: any) => {
    loading.value = true
    try {
      const updatedParticipant = await participantApi.updateParticipant(id, participantData)
      const index = participants.value.findIndex(p => p.id === id)
      if (index !== -1) {
        participants.value[index] = updatedParticipant
      }
      if (currentParticipant.value && currentParticipant.value.id === id) {
        currentParticipant.value = updatedParticipant
      }
      return updatedParticipant
    } catch (error) {
      console.error('更新参与者失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const deleteParticipant = async (id: number) => {
    loading.value = true
    try {
      await participantApi.deleteParticipant(id)
      participants.value = participants.value.filter(p => p.id !== id)
      if (currentParticipant.value && currentParticipant.value.id === id) {
        currentParticipant.value = null
      }
    } catch (error) {
      console.error('删除参与者失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const getParticipantsByRaffleId = async (raffleId: number) => {
    loading.value = true
    try {
      const response = await participantApi.getParticipants({ raffle_id: raffleId })
      return response.items || []
    } catch (error) {
      console.error('获取抽奖活动参与者失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    participants,
    currentParticipant,
    loading,
    
    // 方法
    fetchParticipants,
    createParticipant,
    updateParticipant,
    deleteParticipant,
    getParticipantsByRaffleId
  }
})