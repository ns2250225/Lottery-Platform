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
  transition: transform 0.3s;
}

.raffle-card:hover {
  transform: translateY(-5px);
}

.card-image {
  height: 160px;
  overflow: hidden;
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
  padding: 14px;
}

.title {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.description {
  margin: 0 0 12px;
  font-size: 14px;
  color: #606266;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.meta-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.time {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.time .el-icon {
  margin-right: 4px;
}

.stats {
  display: flex;
  justify-content: space-between;
}

.stat-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.stat-item .el-icon {
  margin-right: 4px;
}
</style>