#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文件传输助手框架使用示例

这个示例展示了如何使用框架的基本功能：
1. 定时任务管理
2. 指令处理系统
3. 自定义功能扩展
"""

from framework import WXFramework, CommandHandler, TimedTaskManager


class CustomCommandHandler(CommandHandler):
    """自定义指令处理器示例"""
    
    def __init__(self):
        super().__init__("自定义功能", "这是一个自定义功能示例")
        self.counter = 0
    
    def handle(self, message: str) -> str:
        if message == "计数":
            self.counter += 1
            return f"当前计数: {self.counter}"
        elif message == "重置":
            self.counter = 0
            return "计数已重置为0"
        else:
            return f"""🔧 自定义功能菜单：
            
• 计数 - 增加计数器
• 重置 - 重置计数器
• 退出 - 返回主菜单

当前计数: {self.counter}"""


class CalculatorCommandHandler(CommandHandler):
    """计算器功能示例"""
    
    def __init__(self):
        super().__init__("计算器", "简单的数学计算功能")
    
    def handle(self, message: str) -> str:
        try:
            # 简单的数学表达式计算
            if message.startswith("计算"):
                expression = message[2:].strip()
                result = eval(expression)  # 注意：生产环境中应该使用更安全的方法
                return f"计算结果: {expression} = {result}"
            else:
                return """🧮 计算器功能：
                
• 计算 1+1 - 计算数学表达式
• 计算 2*3+4 - 支持复杂表达式
• 退出 - 返回主菜单

💡 示例: 计算 10+5*2"""
        except Exception as e:
            return f"❌ 计算错误: {str(e)}"


def main():
    """主函数"""
    print("🚀 启动微信文件传输助手框架...")
    
    # 创建框架实例
    framework = WXFramework()
    
    # 注册自定义功能
    framework.command_framework.register_command("自定义功能", CustomCommandHandler())
    framework.command_framework.register_command("计算器", CalculatorCommandHandler())
    
    # 启动框架
    try:
        framework.start()
        print("✅ 框架启动成功！")
        print("\n📋 可用功能：")
        print("• 菜单 - 查看所有功能")
        print("• 定时任务 - 管理定时消息")
        print("• 天气查询 - 查询天气（示例）")
        print("• 时间查询 - 查询当前时间")
        print("• 自定义功能 - 自定义功能示例")
        print("• 计算器 - 简单计算功能")
        print("• 帮助 - 显示帮助信息")
        print("• 关闭 - 退出程序")
        
        print("\n💡 使用说明：")
        print("1. 扫描二维码登录微信")
        print("2. 向文件传输助手发送消息")
        print("3. 输入功能名称使用对应功能")
        print("4. 在功能内输入 '退出' 返回主菜单")
        print("5. 输入 '关闭' 退出程序")
        
        # 保持程序运行
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 收到退出信号")
        framework.shutdown()
    except Exception as e:
        print(f"❌ 程序运行错误: {e}")
        framework.shutdown()


if __name__ == "__main__":
    main() 