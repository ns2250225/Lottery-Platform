import { http } from '@/utils/http'

// 抽奖活动API
export const raffleApi = {
  // 获取抽奖活动列表
  getRaffles: (params?: any) => http.get('/raffles', { params }),
  
  // 获取抽奖活动详情
  getRaffleDetail: (id: number) => http.get(`/raffles/${id}`),
  
  // 创建抽奖活动
  createRaffle: (data: any) => http.post('/raffles', data),
  
  // 更新抽奖活动
  updateRaffle: (id: number, data: any) => http.put(`/raffles/${id}`, data),
  
  // 删除抽奖活动
  deleteRaffle: (id: number) => http.delete(`/raffles/${id}`),
  
  // 开始抽奖活动
  startRaffle: (id: number, creator_name: string, creator_contact: string) => http.post(`/raffles/${id}/start`, {
    creator_name,
    creator_contact
  }),
  
  // 结束抽奖活动
  finishRaffle: (id: number, creator_name: string, creator_contact: string) => http.post(`/raffles/${id}/finish`, {
    creator_name,
    creator_contact
  })
}

// 奖品API
export const prizeApi = {
  // 获取奖品列表
  getPrizes: (params?: any) => http.get('/prizes', { params }),
  
  // 获取抽奖活动的奖品列表
  getPrizesByRaffle: (raffleId: number) => http.get(`/prizes/raffle/${raffleId}`),
  
  // 获取奖品详情
  getPrizeDetail: (id: number) => http.get(`/prizes/${id}`),
  
  // 创建奖品
  createPrize: (data: any) => http.post('/prizes', data),
  
  // 更新奖品
  updatePrize: (id: number, data: any) => http.put(`/prizes/${id}`, data),
  
  // 删除奖品
  deletePrize: (id: number) => http.delete(`/prizes/${id}`)
}

// 参与者API
export const participantApi = {
  // 获取参与者列表
  getParticipants: (params?: any) => http.get('/participants', { params }),
  
  // 获取抽奖活动的参与者列表
  getParticipantsByRaffle: (raffleId: number) => http.get(`/participants/raffle/${raffleId}`),
  
  // 获取参与者详情
  getParticipantDetail: (id: number) => http.get(`/participants/${id}`),
  
  // 创建参与者（参与抽奖）
  createParticipant: (data: any) => http.post('/participants', data),
  
  // 更新参与者
  updateParticipant: (id: number, data: any) => http.put(`/participants/${id}`, data),
  
  // 删除参与者
  deleteParticipant: (id: number) => http.delete(`/participants/${id}`)
}

// 中奖者API
export const winnerApi = {
  // 获取中奖者列表
  getWinners: (params?: any) => http.get('/winners', { params }),
  
  // 获取抽奖活动的中奖者列表
  getWinnersByRaffle: (raffleId: number) => http.get(`/winners/raffle/${raffleId}`),
  
  // 获取中奖者详情
  getWinnerDetail: (id: number) => http.get(`/winners/${id}`),
  
  // 创建中奖记录
  createWinner: (data: any) => http.post('/winners', data),
  
  // 执行抽奖
  drawRaffle: (data: any) => http.post('/raffles/draw', data)
}