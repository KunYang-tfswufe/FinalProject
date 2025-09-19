#!/bin/bash
# === 藏红花培育系统 - 最终部署脚本 (v2.1 - 健壮版) ===

echo "=== 藏红花培育系统 - 最终部署 (v2.1) ==="

# 核心修复: 切换到脚本文件所在的目录, 保证所有相对路径都正确
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 核心修复: 使用绝对路径激活虚拟环境
VENV_PATH=$(realpath "$SCRIPT_DIR/../.venv")
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 错误: 找不到虚拟环境: $VENV_PATH"
    exit 1
fi

echo -e "\n🔄 步骤 1/4: 重置 STM32 并检查连接..."
mpremote reset > /dev/null 2>&1
sleep 2
if ! mpremote connect /dev/ttyACM0 exec "print('✅ STM32F411 连接正常')"; then
    echo "❌ 错误: 无法连接到 STM32。请确保服务已停止(sudo systemctl stop saffron-server.service)并重新插拔设备。"
    exit 1
fi

echo -e "\n📦 步骤 2/4: 上传模块化驱动文件..."
# 使用-r参数递归复制整个drivers目录，如果mpremote版本支持
mpremote fs cp -r drivers/ :drivers/ >/dev/null 2>&1 || {
    echo "   - (备用方案) 逐个上传驱动文件..."
    mpremote fs mkdir :drivers >/dev/null 2>&1
    mpremote fs cp drivers/__init__.py :drivers/__init__.py
    mpremote fs cp drivers/sensor_base.py :drivers/sensor_base.py
    mpremote fs cp drivers/dht11.py :drivers/dht11.py
}
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
echo "1. 使用 'mpremote connect /dev/ttyACM0 repl' 确认设备正在输出包含所有传感器数据的JSON。"
echo "2. 确认无误后，启动服务器: 'sudo systemctl start saffron-server.service'"
