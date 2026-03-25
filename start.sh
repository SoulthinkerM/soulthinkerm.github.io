#!/bin/bash

echo "========================================"
echo "  Hexo 博客一键启动脚本 (Linux/Mac)"
echo "========================================"
echo ""

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "[错误] 未检测到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查Python是否安装
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "[错误] 未检测到 Python，请先安装 Python"
    exit 1
fi

echo "[1/4] 检查并安装依赖..."
if [ ! -d "node_modules" ]; then
    echo "首次运行，正在安装依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
else
    echo "依赖已存在，跳过安装"
fi

echo ""
echo "[2/4] 清理缓存..."
npx hexo clean

echo ""
echo "[3/4] 生成静态文件..."
npx hexo generate
if [ $? -ne 0 ]; then
    echo "[错误] Hexo 生成失败"
    exit 1
fi

echo ""
echo "[4/4] 运行更新脚本..."
$PYTHON_CMD update-pages.py
if [ $? -ne 0 ]; then
    echo "[警告] 更新脚本执行失败，但网站仍可访问"
fi

echo ""
echo "========================================"
echo "  启动本地服务器..."
echo "========================================"
echo "访问地址：http://localhost:4000"
echo "按 Ctrl+C 停止服务器"
echo ""

npx hexo server
