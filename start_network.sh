#!/bin/bash

# WCOIN多节点网络启动脚本

echo "🌐 Starting WCOIN Multi-Node Network..."

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

# 启动种子节点
echo "🌱 Starting Seed Node (Port 9333, Dashboard 5000)..."
python main.py --port 9333 --dashboard-port 5000 > logs/node1.log 2>&1 &
NODE1_PID=$!
echo "   PID: $NODE1_PID"

sleep 3

# 启动节点2
echo "🔗 Starting Node 2 (Port 9334, Dashboard 5001)..."
python main.py --port 9334 --dashboard-port 5001 --peers localhost:9333 > logs/node2.log 2>&1 &
NODE2_PID=$!
echo "   PID: $NODE2_PID"

sleep 2

# 启动节点3
echo "🔗 Starting Node 3 (Port 9335, Dashboard 5002)..."
python main.py --port 9335 --dashboard-port 5002 --peers localhost:9333 > logs/node3.log 2>&1 &
NODE3_PID=$!
echo "   PID: $NODE3_PID"

echo ""
echo "✅ WCOIN Network Started!"
echo ""
echo "📊 Dashboards:"
echo "   Node 1: http://localhost:5000"
echo "   Node 2: http://localhost:5001"
echo "   Node 3: http://localhost:5002"
echo ""
echo "📝 Logs:"
echo "   Node 1: logs/node1.log"
echo "   Node 2: logs/node2.log"
echo "   Node 3: logs/node3.log"
echo ""
echo "🛑 To stop all nodes, run: ./stop_network.sh"
echo ""

# 保存PIDs
mkdir -p .pids
echo $NODE1_PID > .pids/node1.pid
echo $NODE2_PID > .pids/node2.pid
echo $NODE3_PID > .pids/node3.pid
