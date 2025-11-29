<template>
  <div class="raffles-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>抽奖活动列表</span>
          <el-button type="primary" @click="navigateTo('/create')">创建活动</el-button>
        </div>
      </template>

      <div class="filter-bar">
        <el-form :inline="true" :model="filterForm" class="filter-form">
          <el-form-item label="活动状态">
            <el-select v-model="filterForm.status" placeholder="全部状态" clearable>
              <el-option label="未开始" value="not_started" />
              <el-option label="进行中" value="in_progress" />
              <el-option label="已结束" value="finished" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchRaffles">查询</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="raffles" style="width: 100%" v-loading="loading">
        <el-table-column prop="title" label="活动名称" />
        <el-table-column prop="description" label="活动描述" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
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
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" text @click="viewRaffle(scope.row.id)">
              查看
            </el-button>
            <el-button 
              v-if="scope.row.status === 'in_progress'" 
              type="success" 
              text 
              @click="participateRaffle(scope.row.id)"
            >
              参与
            </el-button>
            <el-button 
              v-if="scope.row.status === 'not_started'" 
              type="warning" 
              text 
              @click="startRaffle(scope.row.id)"
            >
              开始
            </el-button>
            <el-button 
              v-if="scope.row.status === 'in_progress'" 
              type="danger" 
              text 
              @click="drawRaffle(scope.row.id)"
            >
              抽奖
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 参与抽奖对话框 -->
    <el-dialog v-model="participateDialogVisible" title="参与抽奖" width="500px">
      <el-form :model="participantForm" :rules="participantRules" ref="participantFormRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="participantForm.name" placeholder="请输入您的姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="participantForm.email" placeholder="请输入您的邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="participantForm.phone" placeholder="请输入您的电话号码（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="participateDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitParticipate">确认参与</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 抽奖结果对话框 -->
    <el-dialog v-model="drawResultDialogVisible" title="抽奖结果" width="800px">
      <div v-if="drawResult.winners && drawResult.winners.length > 0">
        <el-alert
          :title="drawResult.message"
          type="success"
          :closable="false"
          style="margin-bottom: 20px"
        />
        <el-table :data="drawResult.winners" style="width: 100%">
          <el-table-column prop="participant.name" label="中奖者" />
          <el-table-column prop="participant.email" label="邮箱" />
          <el-table-column prop="participant.phone" label="电话" />
          <el-table-column prop="prize.name" label="奖品" />
          <el-table-column prop="prize.level" label="奖品等级" />
        </el-table>
      </div>
      <div v-else>
        <el-empty description="暂无中奖者" />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="drawResultDialogVisible = false">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { raffleApi, participantApi, winnerApi } from '@/api/modules'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

interface Raffle {
  id: number
  title: string
  description: string
  status: string
  start_time: string
  end_time: string
  created_at: string
}

interface Participant {
  name: string
  phone: string
  email: string
}

interface Winner {
  participant: {
    name: string
    email: string
    phone: string
  }
  prize: {
    name: string
    level: string
  }
}

interface DrawResult {
  winners: Winner[]
  message: string
}

const router = useRouter()
const loading = ref(false)
const raffles = ref<Raffle[]>([])
const participateDialogVisible = ref(false)
const drawResultDialogVisible = ref(false)
const currentRaffleId = ref(0)
const participantFormRef = ref()

const filterForm = reactive({
  status: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const participantForm = reactive<Participant>({
  name: '',
  phone: '',
  email: ''
})

const participantRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const drawResult = reactive<DrawResult>({
  winners: [],
  message: ''
})

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

const fetchRaffles = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      ...filterForm
    }
    const response = await raffleApi.getRaffles(params)
    raffles.value = response.items || []
    pagination.total = response.total || 0
  } catch (error) {
    console.error('获取抽奖活动失败:', error)
    ElMessage.error('获取抽奖活动失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.status = ''
  pagination.page = 1
  fetchRaffles()
}

const handleSizeChange = (size: number) => {
  pagination.size = size
  fetchRaffles()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchRaffles()
}

const participateRaffle = (id: number) => {
  currentRaffleId.value = id
  participateDialogVisible.value = true
  // 重置表单
  participantForm.name = ''
  participantForm.phone = ''
  participantForm.email = ''
}

const submitParticipate = async () => {
  if (!participantFormRef.value) return
  
  await participantFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        await participantApi.createParticipant({
          raffle_id: currentRaffleId.value,
          ...participantForm
        })
        ElMessage.success('参与抽奖成功')
        participateDialogVisible.value = false
        fetchRaffles()
      } catch (error: any) {
        console.error('参与抽奖失败:', error)
        ElMessage.error(error.response?.data?.detail || '参与抽奖失败')
      }
    }
  })
}

const startRaffle = async (id: number) => {
  // 首先获取抽奖活动信息
  const raffle = raffles.value.find(r => r.id === id)
  if (!raffle) {
    ElMessage.error('抽奖活动不存在')
    return
  }
  
  try {
    // 第一步：输入创建人姓名
    const { value: creatorName } = await ElMessageBox.prompt(
      '请输入创建人姓名', 
      '开始活动验证', 
      {
        confirmButtonText: '下一步',
        cancelButtonText: '取消',
        type: 'info',
        inputPattern: /.+/,
        inputErrorMessage: '请输入创建人姓名',
        inputPlaceholder: '创建人姓名'
      }
    )
    
    // 第二步：输入联系方式
    const { value: creatorContact } = await ElMessageBox.prompt(
      '请输入联系方式', 
      '开始活动验证', 
      {
        confirmButtonText: '确认开始',
        cancelButtonText: '取消',
        type: 'info',
        inputPattern: /.+/,
        inputErrorMessage: '请输入联系方式',
        inputPlaceholder: '联系方式'
      }
    )
    
    await raffleApi.startRaffle(id, creatorName, creatorContact)
    ElMessage.success('抽奖活动已开始')
    fetchRaffles()
  } catch (error: any) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('开始抽奖活动失败:', error)
      ElMessage.error(error.response?.data?.detail || '开始抽奖活动失败')
    }
  }
}

const drawRaffle = async (id: number) => {
  // 首先获取抽奖活动信息
  const raffle = raffles.value.find(r => r.id === id)
  if (!raffle) {
    ElMessage.error('抽奖活动不存在')
    return
  }
  
  try {
    // 第一步：输入创建人姓名
    const { value: creatorName } = await ElMessageBox.prompt(
      '请输入创建人姓名', 
      '验证身份', 
      {
        confirmButtonText: '下一步',
        cancelButtonText: '取消',
        type: 'info',
        inputPattern: /.+/,
        inputErrorMessage: '请输入创建人姓名',
        inputPlaceholder: '创建人姓名'
      }
    )
    
    // 第二步：输入联系方式
    const { value: creatorContact } = await ElMessageBox.prompt(
      '请输入联系方式', 
      '验证身份', 
      {
        confirmButtonText: '执行抽奖',
        cancelButtonText: '取消',
        type: 'info',
        inputPattern: /.+/,
        inputErrorMessage: '请输入联系方式',
        inputPlaceholder: '联系方式'
      }
    )
    
    // 第三步：确认执行
    await ElMessageBox.confirm('确定要执行抽奖吗？', '确认抽奖', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const result = await winnerApi.drawRaffle({
      raffle_id: id,
      creator_name: creatorName,
      creator_contact: creatorContact
    })
    
    drawResult.winners = result.winners || []
    drawResult.message = result.message || ''
    drawResultDialogVisible.value = true
    fetchRaffles()
  } catch (error: any) {
    if (error !== 'cancel' && error !== 'close') {
      console.error('抽奖失败:', error)
      ElMessage.error(error.response?.data?.detail || '抽奖失败')
    }
  }
}

onMounted(() => {
  fetchRaffles()
})
</script>

<style scoped>
.raffles-view {
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

.filter-bar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: var(--nb-primary);
  border: var(--nb-border);
  box-shadow: 4px 4px 0px var(--nb-black);
}

.filter-form {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .filter-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .el-form-item {
    margin-right: 0 !important;
    margin-bottom: 10px;
  }
  
  .el-button {
    width: 100%;
    margin-left: 0 !important;
    margin-bottom: 10px;
  }
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>