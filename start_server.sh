#!/bin/bash
echo "启动藏红花培育系统边缘服务器..."

# 切换到脚本所在目录，确保路径正确
cd "$(dirname "$0")"

# 激活虚拟环境
source .venv/bin/activate

# 切换到服务器代码目录并运行
cd Saffron_Edge_Server/
python3 app.py
