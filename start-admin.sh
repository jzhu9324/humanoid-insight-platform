#!/bin/bash

# Start Netlify CMS local backend and VitePress dev server

echo "🚀 启动人形机器人洞察平台管理后台"
echo "=================================="
echo ""

# Check if npx is available
if ! command -v npx &> /dev/null; then
    echo "❌ 错误: 需要安装 Node.js 和 npm"
    exit 1
fi

# Install netlify-cms-proxy-server if not already installed
if ! npm list -g netlify-cms-proxy-server &> /dev/null; then
    echo "📦 安装 Netlify CMS 本地代理服务器..."
    npm install -g netlify-cms-proxy-server
fi

echo "✓ 准备就绪"
echo ""
echo "启动服务..."
echo "  - VitePress 开发服务器: http://localhost:5173"
echo "  - 后台管理界面: http://localhost:5173/admin/"
echo "  - CMS 代理服务器: http://localhost:8081"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# Start both servers in parallel
npx netlify-cms-proxy-server &
PROXY_PID=$!

npm run docs:dev &
VITEPRESS_PID=$!

# Wait for both processes
wait $PROXY_PID $VITEPRESS_PID
