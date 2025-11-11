#!/bin/bash

# WCOIN启动脚本

echo "🚀 Starting WCOIN Node..."

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# 启动节点
echo "✨ Launching WCOIN..."
python main.py "$@"
