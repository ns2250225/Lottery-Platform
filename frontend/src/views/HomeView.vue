<template>
  <div class="home-view">
    <el-card class="welcome-card">
      <h1>欢迎使用抽奖应用</h1>
      <p>这是一个简单易用的抽奖平台，您可以创建抽奖活动、参与抽奖，并查看抽奖结果。</p>
    </el-card>

    <el-row :gutter="20" class="feature-row">
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="feature-card" shadow="hover" @click="navigateTo('/create')">
          <div class="feature-icon">
            <el-icon size="48"><Plus /></el-icon>
          </div>
          <h3>创建抽奖活动</h3>
          <p>设置活动信息、奖品和规则，创建您的抽奖活动</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="feature-card" shadow="hover" @click="navigateTo('/raffles')">
          <div class="feature-icon">
            <el-icon size="48"><Trophy /></el-icon>
          </div>
          <h3>参与抽奖</h3>
          <p>浏览正在进行中的抽奖活动，填写信息参与抽奖</p>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8">
        <el-card class="feature-card" shadow="hover" @click="navigateTo('/history')">
          <div class="feature-icon">
            <el-icon size="48"><Clock /></el-icon>
          </div>
          <h3>历史记录</h3>
          <p>查看已结束的抽奖活动和中奖结果</p>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="recent-activities">
      <template #header>
        <div class="card-header">
          <span>最近的抽奖活动</span>
          <el-button type="primary" text @click="navigateTo('/raffles')">查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="recentRaffles" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="活动名称" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" text @click="viewRaffle(scope.row.id)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { raffleApi } from '@/api/modules'
import { ElMessage } from 'element-plus'
import { Plus, Trophy, Clock } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

interface Raffle {
  id: number
  title: string
  status: string
  created_at: string
}

const router = useRouter()
const loading = ref(false)
const recentRaffles = ref<Raffle[]>([])

const navigateTo = (path: string) => {
  router.push(path)
}

const viewRaffle = (id: number) => {
  router.push(`/raffle/${id}`)
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'not_started':
      return 'info'
    case 'in_progress':
      return 'success'
    case 'finished':
      return 'warning'
    default:
      return ''
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'not_started':
      return '未开始'
    case 'in_progress':
      return '进行中'
    case 'finished':
      return '已结束'
    default:
      return ''
  }
}

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('YYYY-MM-DD HH:mm')
}

const fetchRecentRaffles = async () => {
  loading.value = true
  try {
    const response = await raffleApi.getRaffles({ limit: 5 })
    recentRaffles.value = response.items || []
  } catch (error) {
    console.error('获取抽奖活动失败:', error)
    ElMessage.error('获取抽奖活动失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecentRaffles()
})
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  margin-bottom: 40px;
  text-align: center;
  background-color: var(--nb-primary) !important;
  border: var(--nb-border);
}

.welcome-card h1 {
  margin-bottom: 16px;
  color: var(--nb-black);
  font-size: 3rem;
  text-transform: uppercase;
  text-shadow: none;
}

.feature-row {
  margin-bottom: 40px;
}

.feature-card {
  height: 280px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 30px;
  background-color: var(--nb-white);
  transition: all 0.2s;
}

.feature-card:hover {
  background-color: var(--nb-secondary) !important;
  color: var(--nb-white);
  transform: translate(-4px, -4px);
  box-shadow: 8px 8px 0px var(--nb-black) !important;
}

.feature-card:hover .feature-icon {
  background-color: var(--nb-primary);
  color: var(--nb-black);
  box-shadow: 4px 4px 0px var(--nb-black);
}

.feature-card:hover h3, 
.feature-card:hover p {
  color: var(--nb-white);
}

.feature-icon {
  margin-bottom: 20px;
  color: var(--nb-black);
  border: 3px solid var(--nb-black);
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--nb-white);
  box-shadow: 4px 4px 0px var(--nb-black);
  transition: all 0.2s;
}

.feature-card h3 {
  margin-bottom: 12px;
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--nb-black);
}

.feature-card p {
  font-size: 1rem;
  line-height: 1.5;
}

.recent-activities {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.2rem;
  font-weight: 900;
}

@media (max-width: 768px) {
  .welcome-card h1 {
    font-size: 2rem;
  }
  
  .feature-card {
    height: auto;
    margin-bottom: 20px;
    padding: 20px;
  }
  
  .feature-icon {
    width: 60px;
    height: 60px;
  }
  
  :deep(.el-icon) {
    font-size: 32px !important;
  }
}
</style>