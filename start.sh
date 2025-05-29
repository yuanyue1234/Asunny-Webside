#!/bin/bash

export LANG=en_US.UTF-8  # 或其他UTF-8语言环境
export LC_ALL=en_US.UTF-8

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 检查MySQL服务状态
if ! netstat -an | grep -q ":3306.*LISTEN"; then
    echo -e "${RED}MySQL服务未运行，请先启动MySQL服务${NC}"
    exit 1
fi


echo -e "${GREEN}MySQL服务运行正常${NC}"



# 激活虚拟环境
echo "激活虚拟环境..."
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac


# 启动后端服务
echo "启动后端服务..."
cd myproject

# 安装依赖
# pip install -r requirements.txt

# 迁移数据库
python manage.py makemigrations lyb
python manage.py migrate

# 启动服务
python manage.py runserver 127.0.0.1:8000 &
BACKEND_PID=$!

# 启动前端服务
echo "启动前端服务..."
cd ../web
# 安装依赖
npm install
# 运行前端服务
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

# 退出虚拟环境
deactivate 