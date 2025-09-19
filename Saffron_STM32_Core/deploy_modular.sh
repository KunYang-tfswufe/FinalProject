#!/bin/bash
# 模块化驱动部署脚本 (v1.1 - 修正版)
# - 修正了串口占用冲突问题，将测试步骤与部署分离。
# - 增加了 STM32 复位操作，确保部署环境干净。
# - 优化了用户提示，引导更清晰的工作流。

# --- 配置区 ---
# 定义你的 STM32 设备路径
DEVICE_PORT="/dev/ttyACM0"
# -----------------

echo "=== 藏红花培育系统 - 模块化驱动部署 (v1.1) ==="

# 检查 mpremote 是否安装
if ! command -v mpremote &> /dev/null
then
    echo "❌ 错误: 'mpremote' 命令未找到。"
    echo "   请先安装: pip install mpremote"
    exit 1
fi

# 检查是否在正确目录
if [ ! -d "drivers" ]; then
    echo "❌ 错误: 请在包含'drivers'文件夹的项目根目录中运行此脚本。"
    exit 1
fi

# --- 步骤 1: 重置设备并检查连接 ---
echo ""
echo "🔄 步骤 1/4: 尝试重置 STM32 并检查连接..."
if ! mpremote connect ${DEVICE_PORT} reset > /dev/null 2>&1; then
    echo "   ⚠️ 警告: 无法自动重置设备，将继续尝试连接..."
fi
sleep 1 # 等待设备重置后重新连接

if ! mpremote connect ${DEVICE_PORT} exec "print('✅ STM32F411 连接正常')" 2>/dev/null; then
    echo "❌ 错误: 无法连接到 STM32F411 (${DEVICE_PORT})"
    echo "   请检查:"
    echo "   1. STM32是否已通过USB连接到树莓派。"
    echo "   2. 设备路径 '${DEVICE_PORT}' 是否正确。"
    echo "   3. 检查用户是否有串口权限 (sudo usermod -a -G dialout \`whoami\`)。"
    exit 1
fi

# --- 步骤 2: 上传驱动文件 ---
echo ""
echo "📦 步骤 2/4: 上传模块化驱动文件..."

# 确保目标目录存在
mpremote fs mkdir :drivers > /dev/null 2>&1

# 定义要上传的文件列表
DRIVER_FILES=(
    "drivers/__init__.py"
    "drivers/sensor_base.py"
    "drivers/dht11.py"
    "drivers/README.md"
)

# 循环上传文件
for file in "${DRIVER_FILES[@]}"; do
    echo "   - 上传 ${file}"
    mpremote fs cp "${file}" ":${file}"
    if [ $? -ne 0 ]; then
        echo "   ❌ 上传失败: ${file}"
        exit 1
    fi
done

echo "✅ 驱动模块上传完成。"

# --- 步骤 3: 上传主程序和测试文件 ---
echo ""
echo "🔬 步骤 3/4: 上传主程序与测试程序..."

APP_FILES=(
    "test_modular_drivers.py"
    "main_modular.py"
)

for file in "${APP_FILES[@]}"; do
    echo "   - 上传 ${file}"
    mpremote fs cp "${file}" ":${file}"
    if [ $? -ne 0 ]; then
        echo "   ❌ 上传失败: ${file}"
        exit 1
    fi
done
echo "✅ 主程序与测试程序上传完成。"

# --- 步骤 4: 验证部署 ---
echo ""
echo "✔️  步骤 4/4: 验证部署结果..."
echo "   检查远程 'drivers' 目录内容:"
mpremote fs ls :drivers/ | sed 's/^/      /' # 美化输出

echo ""
echo "🧪 运行一个快速、非阻塞的模块导入测试..."
# 使用一个简短、会自动退出的 exec 命令来测试
TEST_COMMAND="from drivers import get_driver_info; info=get_driver_info(); print(f'驱动版本: {info[\"version\"]}')"
if mpremote connect ${DEVICE_PORT} exec "${TEST_COMMAND}"; then
    echo "✅ 模块导入测试成功！"
else
    echo "⚠️ 模块导入测试失败，但文件已上传。请检查代码是否存在语法错误。"
fi

# --- 完成提示 ---
echo ""
echo "🎉 部署完成! 所有文件已成功上传到 STM32。"
echo "---------------------------------------------------------"
echo "下一步操作指引:"
echo ""
echo "1️⃣ 运行并监控主程序 (在第一个终端):"
echo "   mpremote connect ${DEVICE_PORT} exec \"exec(open('main_modular.py').read())\""
echo ""
echo "2️⃣ 启动 Flask 服务器 (在第二个终端):"
echo "   cd ../Saffron_Edge_Server/"
echo "   source .venv/bin/activate"
echo "   python3 app.py"
echo ""
echo "3️⃣ 查看实时数据:"
echo "   在电脑浏览器中访问 http://<你的树莓派IP>:5000"
echo ""
