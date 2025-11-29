<template>
  <div class="raffle-detail-view" v-loading="loading">
    <el-card v-if="raffle">
      <template #header>
        <div class="card-header">
          <span>{{ raffle.title }}</span>
          <el-tag :type="getStatusType(raffle.status)">
            {{ getStatusText(raffle.status) }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="descriptionColumns" border>
        <el-descriptions-item label="活动描述" :span="descriptionColumns">
          {{ raffle.description || '暂无描述' }}
        </el-descriptions-item>
        <el-descriptions-item label="开始时间">
          {{ formatDate(raffle.start_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间">
          {{ formatDate(raffle.end_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(raffle.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="活动状态">
          <el-tag :type="getStatusType(raffle.status)">
            {{ getStatusText(raffle.status) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="action-buttons" v-if="raffle.status === 'in_progress'">
        <el-button type="success" @click="participateRaffle">参与抽奖</el-button>
        <el-button type="warning" @click="drawRaffle">执行抽奖</el-button>
      </div>
      <div class="action-buttons" v-if="raffle.status === 'not_started'">
        <el-button type="primary" @click="startRaffle">开始活动</el-button>
      </div>
      <div class="action-buttons" v-if="raffle.status === 'in_progress'">
        <el-button type="warning" @click="finishRaffle">结束活动</el-button>
      </div>
    </el-card>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :xs="24" :sm="24" :md="8">
        <el-card>
          <template #header>
            <span>奖品列表</span>
          </template>
          <el-table :data="raffle?.prizes || []" style="width: 100%">
            <el-table-column prop="name" label="奖品名称" />
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column prop="level" label="等级" width="80" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8">
        <el-card>
          <template #header>
            <span>参与者列表</span>
          </template>
          <el-table :data="raffle?.participants || []" style="width: 100%">
            <el-table-column prop="name" label="姓名" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>中奖名单</span>
              <el-button 
                v-if="raffle?.winners && raffle.winners.length > 0"
                type="success" 
                size="small" 
                @click="exportWinners"
              >
                导出中奖者
              </el-button>
            </div>
          </template>
          <el-table :data="raffle?.winners || []" style="width: 100%">
            <el-table-column prop="participant.name" label="姓名" />
            <el-table-column prop="prize.name" label="奖品" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

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
          <el-table-column prop="prize.name" label="奖品" />
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

    <!-- 创建人验证对话框 -->
    <el-dialog v-model="creatorVerificationDialogVisible" :title="getCreatorActionTitle()" width="500px">
      <el-alert
        :title="getCreatorActionAlert()"
        type="info"
        :closable="false"
        style="margin-bottom: 20px"
      />
      <el-form :model="creatorForm" :rules="creatorRules" ref="creatorFormRef" label-width="100px">
        <el-form-item label="创建人姓名" prop="creator_name">
          <el-input v-model="creatorForm.creator_name" placeholder="请输入创建人姓名" />
        </el-form-item>
        <el-form-item label="联系方式" prop="creator_contact">
          <el-input v-model="creatorForm.creator_contact" placeholder="请输入创建人联系方式" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="creatorVerificationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmCreatorAction">{{ getConfirmButtonText() }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { raffleApi, participantApi, winnerApi } from '@/api/modules'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import * as XLSX from 'xlsx'

interface Raffle {
  id: number
  title: string
  description: string
  status: string
  start_time: string
  end_time: string
  created_at: string
  creator_name: string
  creator_contact: string
  prizes?: any[]
  participants?: any[]
  winners?: any[]
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

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const raffle = ref<Raffle | null>(null)
const participateDialogVisible = ref(false)
const drawResultDialogVisible = ref(false)
const creatorVerificationDialogVisible = ref(false)
const participantFormRef = ref()
const creatorFormRef = ref()
const currentAction = ref<'start' | 'finish' | 'draw' | 'export' | ''>('')
const windowWidth = ref(window.innerWidth)

const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}

const descriptionColumns = computed(() => {
  return windowWidth.value < 768 ? 1 : 2
})

const participantForm = reactive<Participant>({
  name: '',
  phone: '',
  email: ''
})

const creatorForm = reactive({
  creator_name: '',
  creator_contact: ''
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
    { required: false, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const creatorRules = {
  creator_name: [
    { required: true, message: '请输入创建人姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  creator_contact: [
    { required: true, message: '请输入创建人联系方式', trigger: 'blur' }
  ]
}

const drawResult = reactive<DrawResult>({
  winners: [],
  message: ''
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

const getCreatorActionTitle = () => {
  switch (currentAction.value) {
    case 'start':
      return '开始活动验证'
    case 'finish':
      return '结束活动验证'
    case 'draw':
      return '执行抽奖验证'
    case 'export':
      return '导出名单验证'
    default:
      return '创建人验证'
  }
}

const getCreatorActionAlert = () => {
  switch (currentAction.value) {
    case 'start':
      return '请输入抽奖活动的创建人信息以验证开始权限'
    case 'finish':
      return '请输入抽奖活动的创建人信息以验证结束权限'
    case 'draw':
      return '请输入抽奖活动的创建人信息以验证抽奖权限'
    case 'export':
      return '请输入抽奖活动的创建人信息以验证导出权限'
    default:
      return '请输入抽奖活动的创建人信息以验证权限'
  }
}

const getConfirmButtonText = () => {
  switch (currentAction.value) {
    case 'start':
      return '确认开始'
    case 'finish':
      return '确认结束'
    case 'draw':
      return '确认抽奖'
    case 'export':
      return '确认导出'
    default:
      return '确认'
  }
}

const fetchRaffleDetail = async () => {
  const id = Number(route.params.id)
  if (isNaN(id)) {
    ElMessage.error('无效的活动ID')
    router.push('/raffles')
    return
  }

  loading.value = true
  try {
    raffle.value = await raffleApi.getRaffleDetail(id)
  } catch (error) {
    console.error('获取抽奖活动详情失败:', error)
    ElMessage.error('获取抽奖活动详情失败')
    router.push('/raffles')
  } finally {
    loading.value = false
  }
}

const participateRaffle = () => {
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
          raffle_id: raffle.value!.id,
          ...participantForm
        })
        ElMessage.success('参与抽奖成功')
        participateDialogVisible.value = false
        fetchRaffleDetail() // 刷新数据
      } catch (error: any) {
        console.error('参与抽奖失败:', error)
        ElMessage.error(error.response?.data?.detail || '参与抽奖失败')
      }
    }
  })
}

const startRaffle = async () => {
  // 重置创建人验证表单
  creatorForm.creator_name = ''
  creatorForm.creator_contact = ''
  
  // 显示创建人验证对话框
  creatorVerificationDialogVisible.value = true
  
  // 记录当前操作类型，用于确认按钮区分不同操作
  currentAction.value = 'start'
}

const finishRaffle = async () => {
  // 重置创建人验证表单
  creatorForm.creator_name = ''
  creatorForm.creator_contact = ''
  
  // 显示创建人验证对话框
  creatorVerificationDialogVisible.value = true
  
  // 记录当前操作类型，用于确认按钮区分不同操作
  currentAction.value = 'finish'
}

const confirmCreatorAction = async () => {
  if (!creatorFormRef.value) return
  
  await creatorFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 关闭验证对话框
        creatorVerificationDialogVisible.value = false
        
        const creatorData = {
          creator_name: creatorForm.creator_name,
          creator_contact: creatorForm.creator_contact
        }
        
        if (currentAction.value === 'start') {
          // 开始抽奖活动
          await raffleApi.startRaffle(raffle.value!.id, creatorData.creator_name, creatorData.creator_contact)
          ElMessage.success('抽奖活动已开始')
        } else if (currentAction.value === 'finish') {
          // 结束抽奖活动
          await raffleApi.finishRaffle(raffle.value!.id, creatorData.creator_name, creatorData.creator_contact)
          ElMessage.success('抽奖活动已结束')
        } else if (currentAction.value === 'draw') {
          // 执行抽奖
          const result = await winnerApi.drawRaffle({
            raffle_id: raffle.value!.id,
            ...creatorData
          })
          
          drawResult.winners = result.winners || []
          drawResult.message = result.message || ''
          drawResultDialogVisible.value = true
        } else if (currentAction.value === 'export') {
          // 导出名单（前端验证）
          if (creatorData.creator_name !== raffle.value!.creator_name || 
              creatorData.creator_contact !== raffle.value!.creator_contact) {
            throw new Error('创建人信息验证失败，无权导出名单')
          }
          doExportWinners()
          return // 导出不需要刷新数据
        }
        
        fetchRaffleDetail() // 刷新数据
      } catch (error: any) {
        console.error('操作失败:', error)
        // 如果是 Error 对象（前端抛出的错误），直接显示 message
        const errorMessage = error instanceof Error ? error.message : (error.response?.data?.detail || '操作失败')
        ElMessage.error(errorMessage)
      }
    }
  })
}

const drawRaffle = async () => {
  // 重置创建人验证表单
  creatorForm.creator_name = ''
  creatorForm.creator_contact = ''
  
  // 显示创建人验证对话框
  creatorVerificationDialogVisible.value = true
  
  // 记录当前操作类型，用于确认按钮区分不同操作
  currentAction.value = 'draw'
}

const doExportWinners = () => {
  if (!raffle.value?.winners || raffle.value.winners.length === 0) {
    ElMessage.warning('暂无中奖者数据可导出')
    return
  }

  try {
    // 准备导出数据
    const exportData = raffle.value.winners.map((winner, index) => ({
      '序号': index + 1,
      '中奖者姓名': winner.participant?.name || '',
      '邮箱': winner.participant?.email || '',
      '联系电话': winner.participant?.phone || '',
      '奖品名称': winner.prize?.name || '',
      '奖品等级': winner.prize?.level || ''
    }))

    // 创建工作簿
    const wb = XLSX.utils.book_new()
    const ws = XLSX.utils.json_to_sheet(exportData)

    // 设置列宽
    const cols = [
      { wch: 8 },   // 序号
      { wch: 15 },  // 中奖者姓名
      { wch: 25 },  // 邮箱
      { wch: 15 },  // 联系电话
      { wch: 20 },  // 奖品名称
      { wch: 10 }   // 奖品等级
    ]
    ws['!cols'] = cols

    // 添加工作表到工作簿
    XLSX.utils.book_append_sheet(wb, ws, '中奖名单')

    // 生成文件名
    const fileName = `${raffle.value.title}_中奖名单_${dayjs().format('YYYY-MM-DD_HH-mm-ss')}.xlsx`

    // 导出文件
    XLSX.writeFile(wb, fileName)

    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请重试')
  }
}

const exportWinners = () => {
  if (!raffle.value?.winners || raffle.value.winners.length === 0) {
    ElMessage.warning('暂无中奖者数据可导出')
    return
  }

  // 重置创建人验证表单
  creatorForm.creator_name = ''
  creatorForm.creator_contact = ''
  
  // 显示创建人验证对话框
  creatorVerificationDialogVisible.value = true
  
  // 记录当前操作类型
  currentAction.value = 'export'
}

onMounted(() => {
  fetchRaffleDetail()
  window.addEventListener('resize', updateWindowWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWindowWidth)
})

// 导出所有方法和数据
defineExpose({
  fetchRaffleDetail
})
</script>

<style scoped>
.raffle-detail-view {
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

.action-buttons {
  margin-top: 30px;
  text-align: center;
  padding: 20px;
  border: 2px dashed var(--nb-black);
  background-color: #f0f0f0;
}

.action-buttons .el-button {
  margin: 0 15px;
  min-width: 120px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .action-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
  }

  .action-buttons .el-button {
    width: 100%;
    margin: 0 !important;
  }

  .dialog-footer {
    flex-direction: column;
    gap: 10px;
  }
  
  .dialog-footer .el-button {
    width: 100%;
    margin-left: 0 !important;
  }
}
</style>