# 改进的BH1750光照传感器驱动
import machine
import time

class ImprovedBH1750:
    """改进的BH1750光照传感器驱动"""
    
    def __init__(self, i2c, addr=0x23):
        self.i2c = i2c
        self.addr = addr
        self.is_initialized = False
        self.last_raw_value = None
        self.stable_count = 0
        
        # 初始化传感器
        self._initialize()
    
    def _initialize(self):
        """初始化传感器"""
        try:
            # 1. 重置传感器
            self.i2c.writeto(self.addr, b'\x07')  # Reset
            time.sleep_ms(10)
            
            # 2. 电源开启
            self.i2c.writeto(self.addr, b'\x01')  # Power On
            time.sleep_ms(10)
            
            # 3. 设置连续高分辨率模式
            self.i2c.writeto(self.addr, b'\x10')  # 连续高分辨率模式
            time.sleep_ms(180)  # 等待第一次测量完成
            
            # 4. 测试读取
            data = self.i2c.readfrom(self.addr, 2)
            raw_value = (data[0] << 8) | data[1]
            
            if raw_value > 0:
                self.is_initialized = True
                self.last_raw_value = raw_value
                print(f"✅ BH1750初始化成功，初始值: {raw_value}")
            else:
                print("❌ BH1750初始化失败，读取值为0")
                
        except Exception as e:
            print(f"❌ BH1750初始化错误: {e}")
    
    def read_lux(self):
        """读取光照值"""
        if not self.is_initialized:
            return None
            
        try:
            # 读取数据
            data = self.i2c.readfrom(self.addr, 2)
            raw_value = (data[0] << 8) | data[1]
            lux = raw_value / 1.2
            
            # 检查数据是否变化
            if self.last_raw_value is not None:
                if raw_value == self.last_raw_value:
                    self.stable_count += 1
                else:
                    self.stable_count = 0
                    self.last_raw_value = raw_value
            else:
                self.last_raw_value = raw_value
            
            return {
                'raw': raw_value,
                'lux': lux,
                'stable_count': self.stable_count,
                'is_stable': self.stable_count > 3
            }
            
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return None
    
    def force_new_measurement(self):
        """强制新的测量"""
        try:
            # 重新设置测量模式
            self.i2c.writeto(self.addr, b'\x01')  # Power On
            time.sleep_ms(10)
            self.i2c.writeto(self.addr, b'\x10')  # 连续高分辨率模式
            time.sleep_ms(180)
            print("🔄 强制新测量完成")
        except Exception as e:
            print(f"❌ 强制测量失败: {e}")
    
    def test_sensitivity(self):
        """测试传感器灵敏度"""
        print("=== 传感器灵敏度测试 ===")
        print("请用手遮挡传感器，观察数值变化...")
        
        for i in range(10):
            result = self.read_lux()
            if result:
                status = "🔒 稳定" if result['is_stable'] else "📊 变化"
                print(f"第{i+1:2d}次: 原始={result['raw']:3d}, 光照={result['lux']:6.2f} lux {status}")
            else:
                print(f"第{i+1:2d}次: 读取失败")
            time.sleep_ms(1000)

# 测试程序
def test_improved_sensor():
    """测试改进的传感器"""
    print("=== 改进的BH1750传感器测试 ===")
    
    # 初始化I2C
    i2c = machine.I2C(1, freq=100000)
    
    # 创建传感器实例
    sensor = ImprovedBH1750(i2c)
    
    if sensor.is_initialized:
        print("\n开始灵敏度测试...")
        sensor.test_sensitivity()
        
        print("\n强制新测量测试...")
        sensor.force_new_measurement()
        result = sensor.read_lux()
        if result:
            print(f"强制测量结果: 原始={result['raw']}, 光照={result['lux']:.2f} lux")
    else:
        print("❌ 传感器初始化失败，无法进行测试")

# 运行测试
if __name__ == "__main__":
    test_improved_sensor()
