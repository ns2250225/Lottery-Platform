<template>
  <div class="layout-footer">
    <!-- Removed el-divider as we have a border-top now -->
    <div class="footer-content">
      <p>&copy; 2023 抽奖应用. All rights reserved.</p>
      <p>
        <el-link href="https://github.com" target="_blank">GitHub</el-link>
        <span class="separator">|</span>
        <el-link href="#" target="_blank">关于我们</el-link>
        <span class="separator">|</span>
        <el-link href="#" target="_blank">联系方式</el-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
// 页脚组件，不需要额外逻辑
</script>

<style scoped>
.layout-footer {
  width: 100%;
  padding: 40px 0;
  background-color: var(--nb-primary);
  border-top: var(--nb-border);
  margin-top: 40px;
}

.footer-content {
  text-align: center;
  color: var(--nb-black);
  font-size: 1rem;
  font-weight: bold;
  text-transform: uppercase;
}

.footer-content p {
  margin: 10px 0;
}

.separator {
  margin: 0 10px;
  color: var(--nb-black);
  font-weight: 900;
}
</style>