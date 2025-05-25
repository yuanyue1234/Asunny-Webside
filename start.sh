#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "开始检查服务状态..."

# 检查MySQL服务状态
echo "检查MySQL服务..."
if systemctl is-active --quiet mysql; then
    echo -e "${GREEN}MySQL服务正在运行${NC}"
else
    echo -e "${RED}MySQL服务未运行，正在启动...${NC}"
    systemctl start mysql
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}MySQL服务启动成功${NC}"
    else
        echo -e "${RED}MySQL服务启动失败，请手动检查${NC}"
        exit 1
    fi
fi

# 启动后端服务
echo "启动后端服务..."
cd backend
source venv/bin/activate  # 如果使用虚拟环境
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# 启动前端服务
echo "启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo -e "${GREEN}所有服务已启动${NC}"
echo "后端服务PID: $BACKEND_PID"
echo "前端服务PID: $FRONTEND_PID"

# 等待用户输入来停止服务
echo "按回车键停止所有服务..."
read

# 停止服务
kill $BACKEND_PID
kill $FRONTEND_PID
echo -e "${GREEN}所有服务已停止${NC}" 