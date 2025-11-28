<template>
  <div class="layout-footer">
    <el-divider />
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
  padding: 20px 0;
}

.footer-content {
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.footer-content p {
  margin: 5px 0;
}

.separator {
  margin: 0 10px;
  color: #dcdfe6;
}
</style>