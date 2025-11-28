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
  background: linear-gradient(135deg, #409eff 0%, #1890ff 100%);
  color: white;
  padding: 0;
  box-shadow: 0 4px 20px rgba(64, 158, 255, 0.3);
  border-bottom: 3px solid rgba(255, 255, 255, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
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
  font-weight: 700;
  display: flex;
  align-items: center;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
}

.title-icon {
  margin-right: 8px;
  font-size: 28px;
  color: #ffd700;
}

.el-menu-demo {
  background-color: transparent;
  border-bottom: none;
  flex: 1;
  display: flex;
  justify-content: center;
}

.el-menu-demo .el-menu-item {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  font-size: 16px;
  padding: 0 24px;
  margin: 0 8px;
  border-radius: 8px;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  position: relative;
  overflow: hidden;
}

.el-menu-demo .el-menu-item:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.el-menu-demo .el-menu-item:hover:before {
  left: 100%;
}

.el-menu-demo .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.el-menu-demo .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.25);
  color: white;
  border-bottom-color: #ffd700;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  transform: translateY(-1px);
}

.el-menu-demo .el-menu-item .el-icon {
  font-size: 18px;
  margin-right: 4px;
}

.app-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
  min-height: calc(100vh - 80px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 0 10px;
  }
  
  .app-title {
    margin-right: 20px;
    font-size: 20px;
  }
  
  .title-icon {
    font-size: 24px;
  }
  
  .el-menu-demo .el-menu-item {
    padding: 0 16px;
    font-size: 14px;
    margin: 0 4px;
  }
  
  .el-menu-demo .el-menu-item .el-icon {
    font-size: 16px;
  }
}

@media (max-width: 576px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 10px;
  }
  
  .app-title {
    margin-right: 0;
    margin-bottom: 10px;
    font-size: 18px;
  }
  
  .el-menu-demo {
    width: 100%;
    justify-content: space-around;
  }
  
  .el-menu-demo .el-menu-item {
    flex: 1;
    text-align: center;
    padding: 10px 8px;
    margin: 0 2px;
    font-size: 12px;
  }
  
  .el-menu-demo .el-menu-item .el-icon {
    font-size: 14px;
    margin-right: 2px;
  }
  
  .app-main {
    padding: 10px;
  }
}
</style>