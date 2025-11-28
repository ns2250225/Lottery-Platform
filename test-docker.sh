#!/bin/bash

# Docker部署测试脚本
# 用于验证Docker部署是否正常工作

set -e

echo "=== Docker部署测试 ==="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    exit 1
fi

# 检查Docker Compose是否安装
if ! docker compose version &> /dev/null; then
    echo "错误: Docker Compose未安装或不是Docker CLI插件"
    exit 1
fi

# 检查Docker服务是否运行
if ! docker info &> /dev/null; then
    echo "错误: Docker服务未运行"
    exit 1
fi

echo "✓ Docker环境检查通过"

# 构建镜像
echo "构建Docker镜像..."
docker compose build

echo "✓ 镜像构建完成"

# 启动服务
echo "启动服务..."
docker compose up -d

echo "✓ 服务启动完成"

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 检查服务状态
echo "检查服务状态..."
docker compose ps

# 测试后端API
echo "测试后端API..."
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✓ 后端API测试通过"
else
    echo "✗ 后端API测试失败"
fi

# 测试前端
echo "测试前端..."
if curl -f http://localhost:3000 &> /dev/null; then
    echo "✓ 前端测试通过"
else
    echo "✗ 前端测试失败"
fi

# 停止服务
echo "停止服务..."
docker compose down

echo "=== 测试完成 ==="