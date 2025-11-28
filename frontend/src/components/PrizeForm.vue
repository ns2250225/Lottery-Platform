<template>
  <div class="prize-form">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>奖品列表</span>
          <el-button type="primary" @click="addPrize">添加奖品</el-button>
        </div>
      </template>

      <el-table :data="prizes" style="width: 100%">
        <el-table-column prop="name" label="奖品名称" />
        <el-table-column prop="quantity" label="数量" width="80" />
        <el-table-column prop="level" label="等级" width="100">
          <template #default="scope">
            <el-tag :type="getPrizeLevelType(scope.row.level)" size="small">
              {{ getPrizeLevelText(scope.row.level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button link type="primary" @click="editPrize(scope.$index)">编辑</el-button>
            <el-button link type="danger" @click="removePrize(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="prizes.length === 0" class="empty-state">
        <el-empty description="暂无奖品，请添加奖品" />
      </div>
    </el-card>

    <!-- 添加/编辑奖品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑奖品' : '添加奖品'"
      width="500px"
    >
      <el-form :model="prizeForm" :rules="prizeRules" ref="prizeFormRef" label-width="80px">
        <el-form-item label="奖品名称" prop="name">
          <el-input v-model="prizeForm.name" placeholder="请输入奖品名称" />
        </el-form-item>
        <el-form-item label="奖品数量" prop="quantity">
          <el-input-number
            v-model="prizeForm.quantity"
            :min="1"
            :max="100"
            placeholder="请输入奖品数量"
          />
        </el-form-item>
        <el-form-item label="奖品等级" prop="level">
          <el-select v-model="prizeForm.level" placeholder="请选择奖品等级">
            <el-option label="特等奖" value="special" />
            <el-option label="一等奖" value="first" />
            <el-option label="二等奖" value="second" />
            <el-option label="三等奖" value="third" />
            <el-option label="参与奖" value="participation" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="savePrize">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { getPrizeLevelText, getPrizeLevelType } from '@/utils/common'

interface Prize {
  name: string
  quantity: number
  level: string
}

interface Props {
  modelValue: Prize[]
}

interface Emits {
  (e: 'update:modelValue', value: Prize[]): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const prizes = ref<Prize[]>([...props.modelValue])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editIndex = ref(-1)
const prizeFormRef = ref()

const prizeForm = reactive({
  name: '',
  quantity: 1,
  level: ''
})

const prizeRules = {
  name: [
    { required: true, message: '请输入奖品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: '请输入奖品数量', trigger: 'blur' },
    { type: 'number', min: 1, max: 100, message: '数量必须在 1 到 100 之间', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择奖品等级', trigger: 'change' }
  ]
}

const addPrize = () => {
  isEdit.value = false
  prizeForm.name = ''
  prizeForm.quantity = 1
  prizeForm.level = ''
  dialogVisible.value = true
}

const editPrize = (index: number) => {
  isEdit.value = true
  editIndex.value = index
  const prize = prizes.value[index]
  prizeForm.name = prize.name
  prizeForm.quantity = prize.quantity
  prizeForm.level = prize.level
  dialogVisible.value = true
}

const savePrize = () => {
  prizeFormRef.value.validate((valid: boolean) => {
    if (valid) {
      if (isEdit.value) {
        prizes.value[editIndex.value] = { ...prizeForm }
      } else {
        prizes.value.push({ ...prizeForm })
      }
      emit('update:modelValue', [...prizes.value])
      dialogVisible.value = false
    }
  })
}

const removePrize = (index: number) => {
  prizes.value.splice(index, 1)
  emit('update:modelValue', [...prizes.value])
}
</script>

<style scoped>
.prize-form {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-state {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: center;
}
</style>