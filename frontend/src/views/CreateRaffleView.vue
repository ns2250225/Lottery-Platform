<template>
  <div class="create-raffle-view">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>创建抽奖活动</span>
        </div>
      </template>

      <el-form
        :model="raffleForm"
        :rules="raffleRules"
        ref="raffleFormRef"
        label-width="120px"
        class="raffle-form"
      >
        <el-form-item label="活动标题" prop="title">
          <el-input v-model="raffleForm.title" placeholder="请输入活动标题" />
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input
            v-model="raffleForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入活动描述"
          />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="raffleForm.start_time"
            type="datetime"
            placeholder="选择开始时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="raffleForm.end_time"
            type="datetime"
            placeholder="选择结束时间"
            format="YYYY-MM-DD HH:mm:ss"
            value-format="YYYY-MM-DD HH:mm:ss"
          />
        </el-form-item>
        <el-form-item label="创建人姓名" prop="creator_name">
          <el-input v-model="raffleForm.creator_name" placeholder="请输入创建人姓名" />
        </el-form-item>
        <el-form-item label="创建人联系方式" prop="creator_contact">
          <el-input v-model="raffleForm.creator_contact" placeholder="请输入创建人联系方式" />
        </el-form-item>
      </el-form>

      <div class="section-title">
        <h3>奖品设置</h3>
        <el-button type="primary" @click="addPrize">添加奖品</el-button>
      </div>

      <div v-if="prizes.length === 0" class="empty-prizes">
        <el-empty description="暂无奖品，请添加奖品" />
      </div>

      <div v-for="(prize, index) in prizes" :key="index" class="prize-item">
        <el-card>
          <template #header>
            <div class="prize-header">
              <span>奖品 {{ index + 1 }}</span>
              <el-button type="danger" text @click="removePrize(index)">删除</el-button>
            </div>
          </template>
          <el-form :model="prize" label-width="80px">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="奖品名称">
                  <el-input v-model="prize.name" placeholder="请输入奖品名称" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="奖品数量">
                  <el-input-number v-model="prize.quantity" :min="1" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="奖品等级">
                  <el-input-number v-model="prize.level" :min="1" />
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-card>
      </div>

      <div class="form-actions">
        <el-button @click="resetForm">重置</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">创建活动</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { raffleApi, prizeApi } from '@/api/modules'
import { ElMessage } from 'element-plus'

interface RaffleForm {
  title: string
  description: string
  start_time: string
  end_time: string
  creator_name: string
  creator_contact: string
}

interface Prize {
  name: string
  quantity: number
  level: number
}

const router = useRouter()
const raffleFormRef = ref()
const submitting = ref(false)

const raffleForm = reactive<RaffleForm>({
  title: '',
  description: '',
  start_time: '',
  end_time: '',
  creator_name: '',
  creator_contact: ''
})

const raffleRules = {
  title: [
    { required: true, message: '请输入活动标题', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  creator_name: [
    { required: true, message: '请输入创建人姓名', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  creator_contact: [
    { required: true, message: '请输入创建人联系方式', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
  ]
}

const prizes = ref<Prize[]>([])

const addPrize = () => {
  prizes.value.push({
    name: '',
    quantity: 1,
    level: 1
  })
}

const removePrize = (index: number) => {
  prizes.value.splice(index, 1)
}

const resetForm = () => {
  raffleForm.title = ''
  raffleForm.description = ''
  raffleForm.start_time = ''
  raffleForm.end_time = ''
  raffleForm.creator_name = ''
  raffleForm.creator_contact = ''
  prizes.value = []
}

const validatePrizes = () => {
  if (prizes.value.length === 0) {
    ElMessage.error('请至少添加一个奖品')
    return false
  }

  for (let i = 0; i < prizes.value.length; i++) {
    const prize = prizes.value[i]
    if (!prize.name) {
      ElMessage.error(`请输入第 ${i + 1} 个奖品的名称`)
      return false
    }
    if (prize.quantity < 1) {
      ElMessage.error(`第 ${i + 1} 个奖品的数量必须大于0`)
      return false
    }
    if (prize.level < 1) {
      ElMessage.error(`第 ${i + 1} 个奖品的等级必须大于0`)
      return false
    }
  }

  return true
}

const submitForm = async () => {
  if (!raffleFormRef.value) return
  
  await raffleFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      if (!validatePrizes()) return
      
      submitting.value = true
      try {
        // 创建抽奖活动
        const raffle = await raffleApi.createRaffle(raffleForm)
        
        // 创建奖品
        for (const prize of prizes.value) {
          await prizeApi.createPrize({
            raffle_id: raffle.id,
            ...prize
          })
        }
        
        ElMessage.success('抽奖活动创建成功')
        router.push('/raffles')
      } catch (error) {
        console.error('创建抽奖活动失败:', error)
        ElMessage.error('创建抽奖活动失败')
      } finally {
        submitting.value = false
      }
    }
  })
}
</script>

<style scoped>
.create-raffle-view {
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

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 30px 0 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--nb-black);
}

.section-title h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 900;
}

.prize-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.form-actions {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.empty-prizes {
  border: 2px dashed var(--nb-black);
  border-radius: var(--nb-radius);
  margin-bottom: 20px;
  background-color: #f9f9f9;
}
</style>