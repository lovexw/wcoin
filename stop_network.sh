#!/bin/bash

# WCOIN网络停止脚本

echo "🛑 Stopping WCOIN Network..."

if [ -d ".pids" ]; then
    for pidfile in .pids/*.pid; do
        if [ -f "$pidfile" ]; then
            PID=$(cat "$pidfile")
            if kill -0 $PID 2>/dev/null; then
                echo "   Stopping process $PID..."
                kill $PID
            fi
            rm "$pidfile"
        fi
    done
    rmdir .pids 2>/dev/null
fi

# 备用方法：通过进程名杀死
pkill -f "python main.py"

echo "✅ All nodes stopped!"
