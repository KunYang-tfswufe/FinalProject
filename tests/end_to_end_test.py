#!/usr/bin/env python3
# 端到端系统测试
import requests
import json
import time
import subprocess
import sys

def test_web_api():
    """测试Web API"""
    print("🌐 测试Web API...")
    try:
        # 测试API端点
        response = requests.get('http://localhost:5000/api/v1/sensors/latest', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API响应正常: {data}")
            return True
        else:
            print(f"   ❌ API响应错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ API测试失败: {e}")
        return False

def test_web_interface():
    """测试Web界面"""
    print("🖥️ 测试Web界面...")
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200 and '藏红花培育系统' in response.text:
            print("   ✅ Web界面正常")
            return True
        else:
            print(f"   ❌ Web界面错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Web界面测试失败: {e}")
        return False

def test_data_flow():
    """测试数据流"""
    print("📊 测试数据流...")
    try:
        # 连续测试5次
        for i in range(5):
            response = requests.get('http://localhost:5000/api/v1/sensors/latest', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   第{i+1}次: 温度={data.get('temperature', 'N/A')}°C, 湿度={data.get('humidity', 'N/A')}%, 光照={data.get('lux', 'N/A')} lux")
            else:
                print(f"   第{i+1}次: 请求失败")
            time.sleep(2)
        
        print("   ✅ 数据流测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 数据流测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 端到端系统测试")
    print("=" * 60)
    
    # 检查服务是否运行
    print("检查服务状态...")
    try:
        response = requests.get('http://localhost:5000/', timeout=2)
        print("   ✅ Flask服务正在运行")
    except:
        print("   ❌ Flask服务未运行，请先启动服务")
        return
    
    # 运行测试
    tests = [
        test_web_api,
        test_web_interface,
        test_data_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # 输出结果
    print("=" * 60)
    print("📊 端到端测试结果")
    print("=" * 60)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有端到端测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查系统")

if __name__ == "__main__":
    main()
