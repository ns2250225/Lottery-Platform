<template>
  <div class="history-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>历史记录</span>
          <el-button type="primary" @click="exportHistory">导出记录</el-button>
        </div>
      </template>

      <div class="filter-container">
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="活动状态">
            <el-select v-model="filterForm.status" placeholder="全部状态" clearable>
              <el-option label="未开始" value="not_started" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已结束" value="finished" />
            </el-select>
          </el-form-item>
          <el-form-item label="活动时间">
            <el-date-picker
              v-model="filterForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchHistory">查询</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="historyList" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="活动标题" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="participant_count" label="参与人数" width="100" />
        <el-table-column prop="prize_count" label="奖品数量" width="100" />
        <el-table-column prop="winner_count" label="中奖人数" width="100" />
        <el-table-column prop="start_time" label="开始时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="viewDetail(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { raffleApi } from '@/api/modules'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

interface HistoryItem {
  id: number
  title: string
  status: string
  participant_count: number
  prize_count: number
  winner_count: number
  start_time: string
  end_time: string
}

const router = useRouter()
const loading = ref(false)
const historyList = ref<HistoryItem[]>([])

const filterForm = reactive({
  status: '',
  dateRange: [] as string[]
})

const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

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

const fetchHistory = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.current - 1) * pagination.size,
      limit: pagination.size,
      status: filterForm.status || undefined,
      start_date: filterForm.dateRange?.[0] || undefined,
      end_date: filterForm.dateRange?.[1] || undefined
    }
    
    const result = await raffleApi.getRaffles(params)
    historyList.value = result.items || []
    pagination.total = result.total || 0
  } catch (error) {
    console.error('获取历史记录失败:', error)
    ElMessage.error('获取历史记录失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.status = ''
  filterForm.dateRange = []
  pagination.current = 1
  fetchHistory()
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.current = 1
  fetchHistory()
}

const handleCurrentChange = (current: number) => {
  pagination.current = current
  fetchHistory()
}

const viewDetail = (raffle: HistoryItem) => {
  router.push(`/raffle/${raffle.id}`)
}

const exportHistory = () => {
  ElMessage.info('导出功能开发中...')
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.history-view {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 900;
  font-size: 1.2rem;
}

.filter-container {
  margin-bottom: 20px;
  padding: 20px;
  background-color: var(--nb-primary);
  border: var(--nb-border);
  box-shadow: 4px 4px 0px var(--nb-black);
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>