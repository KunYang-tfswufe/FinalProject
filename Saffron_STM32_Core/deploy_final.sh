#!/bin/bash
# === 藏红花培育系统 - 最终部署脚本 (v2.1 - 健壮版) ===

echo "=== 藏红花培育系统 - 最终部署 (v2.1) ==="

# 核心修复: 切换到脚本文件所在的目录, 保证所有相对路径都正确
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 核心修复: 使用绝对路径激活虚拟环境
source ../.venv/bin/activate

echo "🔄 步骤 1/4: 重置 STM32 并检查连接..."
mpremote reset > /dev/null 2>&1
sleep 2
if ! mpremote connect /dev/ttyACM0 exec "print('✅ STM32F411 连接正常')"; then
    echo "❌ 错误: 无法连接到 STM32。请确保服务已停止(sudo systemctl stop saffron-server.service)并重新插拔设备。"
    exit 1
fi

echo -e "\n📦 步骤 2/4: 上传模块化驱动文件..."
# 核心修复: mpremote cp -r 在某些版本下有问题，改为先创建目录再逐个复制
mpremote fs mkdir :drivers >/dev/null 2>&1
mpremote fs cp drivers/__init__.py :drivers/__init__.py
mpremote fs cp drivers/sensor_base.py :drivers/sensor_base.py
mpremote fs cp drivers/dht11.py :drivers/dht11.py
echo "✅ 驱动模块上传完成。"

echo -e "\n🚀 步骤 3/4: 上传主程序并设为自启动..."
mpremote fs cp main_modular.py :main.py
echo "✅ 主程序部署完成，STM32 将在下次重启后自动运行。"

echo -e "\n✔️  步骤 4/4: 重启设备并完成部署..."
mpremote reset
echo "✅ STM32 已重启，正在自动运行主程序。"

echo -e "\n🎉 部署完成! STM32 已设为自启动模式。"
echo "---------------------------------------------------------"
echo "下一步操作:"
echo "1. 使用 'mpremote connect /dev/ttyACM0 repl' 确认设备正在输出JSON数据。"
echo "2. 确认无误后，启动服务器: 'sudo systemctl start saffron-server.service'"
