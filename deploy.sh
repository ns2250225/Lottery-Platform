#!/bin/bash

# 抽奖应用Docker部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker和Docker Compose是否安装
check_dependencies() {
    print_message "检查依赖..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null; then
        print_error "Docker Compose未安装或不是Docker CLI插件，请先安装Docker Compose"
        exit 1
    fi
    
    print_message "依赖检查完成"
}

# 创建必要的目录
create_directories() {
    print_message "创建必要的目录..."
    
    # 创建nginx ssl目录
    mkdir -p nginx/ssl
    
    # 创建后端数据目录
    mkdir -p backend/data
    
    print_message "目录创建完成"
}

# 构建和启动服务
deploy() {
    local env=${1:-dev}
    
    print_message "开始部署抽奖应用 (环境: $env)..."
    
    if [ "$env" = "prod" ]; then
        # 生产环境部署
        print_warning "生产环境部署需要SSL证书"
        print_warning "请将SSL证书文件放置在 nginx/ssl/ 目录下"
        print_warning "证书文件名应为: cert.pem 和 key.pem"
        
        # 检查SSL证书是否存在
        if [ ! -f "nginx/ssl/cert.pem" ] || [ ! -f "nginx/ssl/key.pem" ]; then
            print_warning "未找到SSL证书，将使用HTTP模式"
            # 修改nginx配置，禁用SSL
            sed -i 's/443 ssl http2/80/' nginx/nginx.conf
            sed -i '/ssl_certificate/d' nginx/nginx.conf
            sed -i '/ssl_certificate_key/d' nginx/nginx.conf
            sed -i '/ssl_protocols/d' nginx/nginx.conf
            sed -i '/ssl_prefer_server_ciphers/d' nginx/nginx.conf
            sed -i '/ssl_ciphers/d' nginx/nginx.conf
        fi
        
        docker compose -f docker-compose.prod.yml up --build -d
    else
        # 开发环境部署
        docker compose up --build -d
    fi
    
    print_message "部署完成"
}

# 停止服务
stop() {
    local env=${1:-dev}
    
    print_message "停止服务..."
    
    if [ "$env" = "prod" ]; then
        docker compose -f docker-compose.prod.yml down
    else
        docker compose down
    fi
    
    print_message "服务已停止"
}

# 查看日志
logs() {
    local service=${1:-}
    local env=${2:-dev}
    
    if [ "$env" = "prod" ]; then
        if [ -z "$service" ]; then
            docker compose -f docker-compose.prod.yml logs -f
        else
            docker compose -f docker-compose.prod.yml logs -f "$service"
        fi
    else
        if [ -z "$service" ]; then
            docker compose logs -f
        else
            docker compose logs -f "$service"
        fi
    fi
}

# 更新服务
update() {
    local env=${1:-dev}
    
    print_message "更新服务..."
    
    if [ "$env" = "prod" ]; then
        docker compose -f docker-compose.prod.yml pull
        docker compose -f docker-compose.prod.yml up -d --build
    else
        docker compose pull
        docker compose up -d --build
    fi
    
    print_message "服务更新完成"
}

# 清理资源
cleanup() {
    local env=${1:-dev}
    
    print_message "清理Docker资源..."
    
    if [ "$env" = "prod" ]; then
        # 停止并删除容器
        docker compose -f docker-compose.prod.yml down -v
    else
        # 停止并删除容器
        docker compose down -v
    fi
    
    # 删除未使用的镜像
    docker image prune -f
    
    # 删除未使用的卷
    docker volume prune -f
    
    print_message "清理完成"
}

# 显示帮助信息
show_help() {
    echo "抽奖应用Docker部署脚本"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  deploy [env]    部署应用 (env: dev|prod, 默认: dev)"
    echo "  stop [env]      停止服务 (env: dev|prod, 默认: dev)"
    echo "  logs [service] [env]  查看日志 (service: backend|nginx, 可选; env: dev|prod, 默认: dev)"
    echo "  update [env]    更新服务 (env: dev|prod, 默认: dev)"
    echo "  cleanup [env]   清理Docker资源 (env: dev|prod, 默认: dev)"
    echo "  help            显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 deploy dev   # 部署开发环境"
    echo "  $0 deploy prod  # 部署生产环境"
    echo "  $0 logs nginx prod # 查看生产环境nginx日志"
    echo "  $0 stop prod    # 停止生产环境服务"
    echo "  $0 cleanup prod # 清理生产环境Docker资源"
}

# 主函数
main() {
    case "${1:-help}" in
        deploy)
            check_dependencies
            create_directories
            deploy "${2:-dev}"
            ;;
        stop)
            stop "${2:-dev}"
            ;;
        logs)
            logs "${2:-}" "${3:-dev}"
            ;;
        update)
            update "${2:-dev}"
            ;;
        cleanup)
            cleanup "${2:-dev}"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"