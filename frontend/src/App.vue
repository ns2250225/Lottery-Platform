<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">
            <el-icon class="title-icon"><Trophy /></el-icon>
            抽奖应用
          </h1>
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
          >
            <el-menu-item index="1" @click="navigateTo('/')">
              <el-icon><House /></el-icon>
              首页
            </el-menu-item>
            <el-menu-item index="2" @click="navigateTo('/raffles')">
              <el-icon><Present /></el-icon>
              抽奖活动
            </el-menu-item>
            <el-menu-item index="3" @click="navigateTo('/create')">
              <el-icon><Plus /></el-icon>
              创建活动
            </el-menu-item>
            <el-menu-item index="4" @click="navigateTo('/history')">
              <el-icon><Clock /></el-icon>
              历史记录
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Trophy, 
  House, 
  Present, 
  Plus, 
  Clock 
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const activeIndex = ref('1')

const handleSelect = (key: string) => {
  activeIndex.value = key
}

const navigateTo = (path: string) => {
  router.push(path)
}

// 根据当前路由设置激活的菜单项
const updateActiveIndex = () => {
  const path = route.path
  if (path === '/') activeIndex.value = '1'
  else if (path === '/raffles' || path.startsWith('/raffle/')) activeIndex.value = '2'
  else if (path === '/create') activeIndex.value = '3'
  else if (path === '/history') activeIndex.value = '4'
}

// 监听路由变化
router.afterEach(() => {
  updateActiveIndex()
})

// 初始化时设置激活的菜单项
updateActiveIndex()
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.app-header {
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--nb-white);
  border-bottom: var(--nb-border) !important;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.app-title {
  margin-right: 40px;
  font-size: 24px;
  font-weight: 900;
  display: flex;
  align-items: center;
  color: var(--nb-black);
  text-transform: uppercase;
  text-shadow: none;
}

.title-icon {
  margin-right: 10px;
  font-size: 28px;
  color: var(--nb-black);
}

.el-menu-demo {
  flex: 1;
  display: flex;
  justify-content: flex-end;
  border-bottom: none;
  background-color: transparent;
}

/* Menu Items are handled globally in main.css, but we add some spacing here */
:deep(.el-menu-item) {
  margin: 0 5px;
  height: 40px;
  line-height: 40px;
}

.app-main {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: transparent;
  min-height: calc(100vh - 80px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 10px;
    flex-direction: column;
    height: auto;
  }
  
  .app-title {
    margin-right: 0;
    margin-bottom: 15px;
    width: 100%;
    justify-content: center;
  }
  
  .el-menu-demo {
    width: 100%;
    overflow-x: auto;
    justify-content: flex-start;
  }
}
</style>