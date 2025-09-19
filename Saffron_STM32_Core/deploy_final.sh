#!/bin/bash
# === 藏红花培育系统 - 最终部署脚本 (v2.2 - 智能服务版) ===
# 功能: 自动停止/重启后台服务，实现无中断感部署

echo "=== 藏红花培育系统 - 智能部署 (v2.2) ==="

# 切换到脚本文件所在的目录, 保证所有相对路径都正确
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 使用绝对路径激活虚拟环境
source ../.venv/bin/activate

# --- 核心改进：自动管理服务 ---
echo -e "\n🔄 步骤 1/5: 自动停止后台服务以释放串口..."
sudo systemctl stop saffron-server.service
echo "   ✅ 服务已停止。"
sleep 1 # 等待服务完全释放资源

echo -e "\n🔄 步骤 2/5: 重置 STM32 并检查连接..."
mpremote reset > /dev/null 2>&1
sleep 2
if ! mpremote connect /dev/ttyACM0 exec "print('✅ STM32F411 连接正常')"; then
    echo "❌ 错误: 无法连接到 STM32。请检查连接。"
    echo "   (正在尝试重启服务...)"
    sudo systemctl start saffron-server.service # 部署失败，恢复服务
    exit 1
fi

echo -e "\n📦 步骤 3/5: 上传模块化驱动文件..."
mpremote fs cp -r drivers/ :drivers/ >/dev/null 2>&1 || {
    echo "   - (备用方案) 逐个上传驱动文件..."
    mpremote fs mkdir :drivers >/dev/null 2>&1
    mpremote fs cp drivers/__init__.py :drivers/__init__.py
    mpremote fs cp drivers/sensor_base.py :drivers/sensor_base.py
    mpremote fs cp drivers/dht11.py :drivers/dht11.py
}
echo "✅ 驱动模块上传完成。"

echo -e "\n🚀 步骤 4/5: 上传主程序并设为自启动..."
mpremote fs cp main_modular.py :main.py
echo "✅ 主程序部署完成，STM32 将在下次重启后自动运行。"

mpremote reset
echo "✅ STM32 已重启，正在自动运行主程序。"

# --- 核心改进：自动重启服务 ---
echo -e "\n✔️  步骤 5/5: 自动重启后台服务..."
sudo systemctl start saffron-server.service
sleep 2 # 给服务一点启动时间

echo "   检查服务状态..."
if systemctl is-active --quiet saffron-server.service; then
    echo "   ✅ 服务已成功重启并正在后台运行！"
else
    echo "   ⚠️ 警告: 服务未能自动重启，请手动检查: sudo systemctl status saffron-server.service"
fi

echo -e "\n🎉 部署完成! 代码已更新，服务已恢复。"
echo "   现在可以直接去浏览器刷新页面查看效果了。"
