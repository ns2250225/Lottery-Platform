<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo-container">
            <h1 class="app-title" @click="navigateTo('/')">
              <el-icon class="title-icon"><Trophy /></el-icon>
              抽奖应用
            </h1>
            <div class="mobile-menu-toggle" @click="toggleMobileMenu">
              <el-icon v-if="!isMobileMenuOpen"><Menu /></el-icon>
              <el-icon v-else><Close /></el-icon>
            </div>
          </div>

          <!-- Desktop Menu -->
          <el-menu
            :default-active="activeIndex"
            class="el-menu-demo desktop-menu"
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

        <!-- Mobile Menu Overlay -->
        <transition name="fade">
          <div class="mobile-menu-overlay" v-if="isMobileMenuOpen" @click="toggleMobileMenu">
            <div class="mobile-menu-content" @click.stop>
              <div class="mobile-menu-item" :class="{ active: activeIndex === '1' }" @click="handleMobileNav('/')">
                <el-icon><House /></el-icon>
                <span>首页</span>
              </div>
              <div class="mobile-menu-item" :class="{ active: activeIndex === '2' }" @click="handleMobileNav('/raffles')">
                <el-icon><Present /></el-icon>
                <span>抽奖活动</span>
              </div>
              <div class="mobile-menu-item" :class="{ active: activeIndex === '3' }" @click="handleMobileNav('/create')">
                <el-icon><Plus /></el-icon>
                <span>创建活动</span>
              </div>
              <div class="mobile-menu-item" :class="{ active: activeIndex === '4' }" @click="handleMobileNav('/history')">
                <el-icon><Clock /></el-icon>
                <span>历史记录</span>
              </div>
            </div>
          </div>
        </transition>
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
  Clock,
  Menu,
  Close
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const activeIndex = ref('1')
const isMobileMenuOpen = ref(false)

const handleSelect = (key: string) => {
  activeIndex.value = key
}

const navigateTo = (path: string) => {
  router.push(path)
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const handleMobileNav = (path: string) => {
  navigateTo(path)
  isMobileMenuOpen.value = false
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
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: auto;
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
  cursor: pointer;
}

.mobile-menu-toggle {
  display: none;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  border: 2px solid var(--nb-black);
  box-shadow: 2px 2px 0 var(--nb-black);
  background-color: var(--nb-primary);
  transition: all 0.2s;
}

.mobile-menu-toggle:active {
  transform: translate(2px, 2px);
  box-shadow: none;
}

.title-icon {
  margin-right: 10px;
  font-size: 28px;
  color: var(--nb-black);
}

.desktop-menu {
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

/* Mobile Menu Styles */
.mobile-menu-overlay {
  position: fixed;
  top: 60px; /* Height of header */
  left: 0;
  width: 100%;
  height: calc(100vh - 60px);
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.mobile-menu-content {
  width: 100%;
  background-color: var(--nb-white);
  border-bottom: var(--nb-border);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: 0 4px 0 var(--nb-black);
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  font-size: 18px;
  font-weight: 900;
  border: 2px solid var(--nb-black);
  background-color: var(--nb-white);
  box-shadow: 4px 4px 0 var(--nb-black);
  transition: all 0.2s;
  cursor: pointer;
}

.mobile-menu-item:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 var(--nb-black);
}

.mobile-menu-item.active {
  background-color: var(--nb-primary);
}

.mobile-menu-item .el-icon {
  font-size: 24px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    padding: 10px 20px;
    height: 60px;
  }
  
  .logo-container {
    width: 100%;
  }
  
  .desktop-menu {
    display: none;
  }
  
  .mobile-menu-toggle {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .app-title {
    margin-right: 0;
    font-size: 20px;
  }
  
  .title-icon {
    font-size: 24px;
  }

  .app-main {
    padding: 20px 10px;
  }
}
</style>