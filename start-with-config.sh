#!/bin/bash

# 启动人形机器人洞察平台（带配置管理功能）

echo "🚀 启动人形机器人洞察平台"
echo "=================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要安装 Python 3"
    exit 1
fi

# 检查 Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 需要安装 Node.js 和 npm"
    exit 1
fi

echo "✓ 环境检查通过"
echo ""
echo "启动服务..."
echo "  - VitePress 开发服务器: http://localhost:5173"
echo "  - 配置管理页面: http://localhost:5173/config"
echo "  - 配置 API 服务器: http://localhost:3001"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 启动 API 服务器（后台）
python3 scripts/config_api.py &
API_PID=$!

# 等待 API 服务器启动
sleep 2

# 启动 VitePress
npm run docs:dev &
VITEPRESS_PID=$!

# 捕获退出信号
trap "echo ''; echo '正在停止服务...'; kill $API_PID $VITEPRESS_PID 2>/dev/null; exit" INT TERM

# 等待进程
wait $API_PID $VITEPRESS_PID
