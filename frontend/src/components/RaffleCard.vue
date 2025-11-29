<template>
  <div class="raffle-card" @click="viewDetail">
    <el-card :body-style="{ padding: '0px' }" shadow="hover">
      <div class="card-image" v-if="raffle.image">
        <img :src="raffle.image" class="image" />
      </div>
      <div class="card-content">
        <h3 class="title">{{ raffle.title }}</h3>
        <p class="description">{{ raffle.description || '暂无描述' }}</p>
        <div class="meta-info">
          <div class="status">
            <el-tag :type="getStatusType(raffle.status)" size="small">
              {{ getStatusText(raffle.status) }}
            </el-tag>
          </div>
          <div class="time">
            <el-icon><Clock /></el-icon>
            <span>{{ formatDate(raffle.start_time) }}</span>
          </div>
        </div>
        <div class="stats">
          <div class="stat-item">
            <el-icon><User /></el-icon>
            <span>{{ raffle.participant_count || 0 }} 人参与</span>
          </div>
          <div class="stat-item">
            <el-icon><Present /></el-icon>
            <span>{{ raffle.prize_count || 0 }} 个奖品</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { Clock, User, Present } from '@element-plus/icons-vue'
import { getStatusType, getStatusText } from '@/utils/common'
import { formatDate } from '@/utils/date'

interface Raffle {
  id: number
  title: string
  description?: string
  status: string
  start_time: string
  end_time: string
  image?: string
  participant_count?: number
  prize_count?: number
}

interface Props {
  raffle: Raffle
}

const props = defineProps<Props>()
const emit = defineEmits<{
  viewDetail: [id: number]
}>()

const viewDetail = () => {
  emit('viewDetail', props.raffle.id)
}
</script>

<style scoped>
.raffle-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.raffle-card:hover {
  transform: translate(-4px, -4px);
}

.raffle-card :deep(.el-card) {
  border: var(--nb-border);
  box-shadow: var(--nb-shadow);
  border-radius: var(--nb-radius);
  transition: all 0.2s;
}

.raffle-card:hover :deep(.el-card) {
  box-shadow: 8px 8px 0px var(--nb-black);
  border-color: var(--nb-black);
}

.card-image {
  height: 160px;
  overflow: hidden;
  border-bottom: var(--nb-border);
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.raffle-card:hover .image {
  transform: scale(1.05);
}

.card-content {
  padding: 20px;
  background-color: var(--nb-white);
}

.title {
  margin: 0 0 10px;
  font-size: 1.2rem;
  font-weight: 900;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-transform: uppercase;
}

.description {
  margin: 0 0 15px;
  font-size: 1rem;
  color: var(--nb-black);
  height: 44px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.meta-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 2px dashed #ddd;
}

.time {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  font-weight: bold;
  color: #666;
}

.time .el-icon {
  margin-right: 4px;
}

.stats {
  display: flex;
  justify-content: space-between;
  background-color: #f0f0f0;
  padding: 10px;
  border: 2px solid var(--nb-black);
}

.stat-item {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  font-weight: bold;
  color: var(--nb-black);
}

.stat-item .el-icon {
  margin-right: 6px;
}
</style>