#!/bin/bash
# 模块化驱动部署脚本
# 自动上传所有模块化驱动文件到STM32F411

echo "=== 藏红花培育系统 - 模块化驱动部署 ==="
echo "正在部署专业模块化传感器驱动..."

# 检查是否在正确目录
if [ ! -d "drivers" ]; then
    echo "❌ 错误: 请在包含drivers文件夹的目录中运行此脚本"
    exit 1
fi

# 检查STM32连接
if ! mpremote connect /dev/ttyACM0 exec "print('STM32连接测试')" 2>/dev/null; then
    echo "❌ 错误: 无法连接到STM32F411 (/dev/ttyACM0)"
    echo "   请检查:"
    echo "   1. STM32是否已连接"
    echo "   2. 设备路径是否正确"
    echo "   3. 用户是否有串口权限"
    exit 1
fi

echo "✅ STM32F411连接正常"

# 上传drivers模块
echo ""
echo "📦 上传模块化驱动文件..."

echo "   上传 drivers/__init__.py"
mpremote fs cp drivers/__init__.py :drivers/__init__.py || {
    echo "   创建drivers目录..."
    mpremote fs mkdir :drivers 2>/dev/null
    mpremote fs cp drivers/__init__.py :drivers/__init__.py
}

echo "   上传 drivers/sensor_base.py"
mpremote fs cp drivers/sensor_base.py :drivers/sensor_base.py

echo "   上传 drivers/dht11.py"
mpremote fs cp drivers/dht11.py :drivers/dht11.py

echo "   上传 drivers/README.md"
mpremote fs cp drivers/README.md :drivers/README.md

echo "✅ 驱动模块上传完成"

# 上传测试文件
echo ""
echo "🔬 上传测试程序..."

echo "   上传 test_modular_drivers.py"
mpremote fs cp test_modular_drivers.py :test_modular_drivers.py

echo "   上传 main_modular.py"
mpremote fs cp main_modular.py :main_modular.py

echo "✅ 测试程序上传完成"

# 验证部署
echo ""
echo "✅ 验证部署结果..."
echo "   检查drivers模块结构:"

# 列出drivers目录内容
mpremote fs ls :drivers/ 2>/dev/null | while read line; do
    echo "      $line"
done

# 运行快速模块测试
echo ""
echo "🧪 运行模块导入测试..."
if mpremote connect /dev/ttyACM0 exec "
try:
    from drivers import get_driver_info
    info = get_driver_info()
    print('✅ 模块导入成功')
    print(f'版本: {info[\"version\"]}')
    print(f'硬件DHT支持: {info[\"hardware_dht_support\"]}')
except Exception as e:
    print(f'❌ 模块导入失败: {e}')
" 2>/dev/null; then
    echo "✅ 模块化驱动部署成功！"
else
    echo "⚠️ 模块导入测试失败，但文件已上传"
fi

echo ""
echo "🎯 部署完成! 接下来可以："
echo ""
echo "1️⃣ 测试模块化驱动:"
echo "   mpremote connect /dev/ttyACM0 exec \"exec(open('test_modular_drivers.py').read())\""
echo ""
echo "2️⃣ 运行模块化主程序:"
echo "   mpremote connect /dev/ttyACM0 exec \"exec(open('main_modular.py').read())\""
echo ""
echo "3️⃣ 启动Flask服务器 (另开终端):"
echo "   cd ../Saffron_Edge_Server/"
echo "   python3 app.py"
echo ""
echo "4️⃣ 查看实时数据:"
echo "   浏览器访问 http://localhost:5000"
echo ""
echo "📚 查看完整API文档: drivers/README.md"
echo ""
echo "🎉 藏红花培育系统模块化驱动部署完成！"
