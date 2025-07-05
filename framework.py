import threading
import time
import schedule
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any, Optional
from abc import ABC, abstractmethod
from lib import WXFilehelper, Message
WX_LOGIN_HOST = "https://login.wx.qq.com"
WX_FILEHELPER_HOST = "https://szfilehelper.weixin.qq.com"
WX_FILEUPLOAD_HOST = "https://file.wx2.qq.com"

class CommandHandler(ABC):
    """指令处理器基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def handle(self, message: str) -> str:
        """处理指令，返回回复内容"""
        pass
    
    def get_help(self) -> str:
        """获取帮助信息"""
        return f"{self.name}: {self.description}"


class MenuCommandHandler(CommandHandler):
    """菜单指令处理器"""
    
    def __init__(self, command_handlers: Dict[str, CommandHandler]):
        super().__init__("菜单", "显示所有可用功能")
        self.command_handlers = command_handlers
    
    def handle(self, message: str) -> str:
        help_text = "📋 可用功能列表：\n\n"
        for name, handler in self.command_handlers.items():
            if name != "菜单":
                help_text += f"• {handler.get_help()}\n"
        help_text += "\n💡 输入功能名称即可使用对应功能"
        help_text += "\n🔙 输入 '退出' 可返回主菜单"
        help_text += "\n❌ 输入 '关闭' 可退出程序"
        return help_text


class ExitCommandHandler(CommandHandler):
    """退出指令处理器"""
    
    def __init__(self):
        super().__init__("退出", "返回主菜单")
    
    def handle(self, message: str) -> str:
        return "已返回主菜单，输入 '菜单' 查看所有功能"


class CloseCommandHandler(CommandHandler):
    """关闭程序指令处理器"""
    
    def __init__(self, framework):
        super().__init__("关闭", "退出程序")
        self.framework = framework
    
    def handle(self, message: str) -> str:
        self.framework.shutdown()
        return "程序正在关闭..."


class TimedTask:
    """定时任务类"""
    
    def __init__(self, task_id: str, script_path: str, schedule_time: str, 
                 task_type: str = "daily", enabled: bool = True, description: str = ""):
        self.task_id = task_id
        self.script_path = script_path  # 脚本文件路径
        self.schedule_time = schedule_time  # "HH:MM" 格式
        self.task_type = task_type  # "daily", "weekly", "once"
        self.enabled = enabled
        self.description = description  # 任务描述
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "script_path": self.script_path,
            "schedule_time": self.schedule_time,
            "task_type": self.task_type,
            "enabled": self.enabled,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TimedTask':
        task = cls(
            data["task_id"],
            data["script_path"],
            data["schedule_time"],
            data["task_type"],
            data["enabled"],
            data.get("description", "")
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        return task


class ScriptEnvironment:
    """脚本执行环境，为脚本提供发送消息的权限"""
    
    def __init__(self, message_instance: Message):
        self.message = message_instance
        self.globals = {
            'send_message': self.send_message,
            'send_file': self.send_file,
            'get_time': self.get_time,
            'print': self.print_with_timestamp,
            'datetime': datetime,
            'time': time,
            'json': json,
            'os': os,
            'sys': sys
        }
    
    def send_message(self, content: str):
        """发送文本消息"""
        try:
            self.message.send_msg(content=content)
            print(f"消息已发送: {content}")
        except Exception as e:
            print(f"发送消息失败: {e}")
    
    def send_file(self, file_path: str):
        """发送文件"""
        try:
            if os.path.exists(file_path):
                self.message.send_msg(file_path=file_path)
                print(f"文件已发送: {file_path}")
            else:
                print(f"文件不存在: {file_path}")
        except Exception as e:
            print(f"发送文件失败: {e}")
    
    def get_time(self):
        """获取当前时间"""
        return datetime.now()
    
    def print_with_timestamp(self, *args, **kwargs):
        """带时间戳的打印"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}]", *args, **kwargs)
    
    def execute_script(self, script_path: str):
        """执行脚本文件"""
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        try:
            # 读取脚本内容
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # 在安全环境中执行脚本
            exec(script_content, self.globals, {})
            
        except Exception as e:
            print(f"脚本执行错误: {e}")
            raise


class TimedTaskManager:
    """定时任务管理器"""
    
    def __init__(self, message_instance: Message):
        self.message = message_instance
        self.tasks: Dict[str, TimedTask] = {}
        self.task_file = "timed_tasks.json"
        self.load_tasks()
        self.scheduler_thread = None
        self.running = False
    
    def add_task(self, script_path: str, schedule_time: str, task_type: str = "daily", description: str = "") -> str:
        """添加定时任务"""
        task_id = f"task_{int(time.time())}"
        task = TimedTask(task_id, script_path, schedule_time, task_type, True, description)
        self.tasks[task_id] = task
        self.save_tasks()
        self._schedule_task(task)
        return task_id
    
    def remove_task(self, task_id: str) -> bool:
        """删除定时任务"""
        if task_id in self.tasks:
            schedule.clear(task_id)
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False
    
    def list_tasks(self) -> List[TimedTask]:
        """列出所有任务"""
        return list(self.tasks.values())
    
    def enable_task(self, task_id: str) -> bool:
        """启用任务"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
            self.save_tasks()
            return True
        return False
    
    def disable_task(self, task_id: str) -> bool:
        """禁用任务"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
            schedule.clear(task_id)
            self.save_tasks()
            return True
        return False
    
    def _schedule_task(self, task: TimedTask):
        """调度任务"""
        if not task.enabled:
            return
            
        def execute_script():
            try:
                # 创建脚本执行环境，提供发送消息的权限
                script_env = ScriptEnvironment(self.message)
                script_env.execute_script(task.script_path)
                print(f"定时任务已执行: {task.script_path}")
            except Exception as e:
                print(f"定时任务执行失败: {e}")
        
        if task.task_type == "daily":
            schedule.every().day.at(task.schedule_time).do(execute_script).tag(task.task_id)
        elif task.task_type == "weekly":
            # 这里可以扩展为指定星期几
            schedule.every().monday.at(task.schedule_time).do(execute_script).tag(task.task_id)
        elif task.task_type == "once":
            # 一次性任务，在指定时间执行一次
            schedule.every().day.at(task.schedule_time).do(execute_script).tag(task.task_id)
    
    def start(self):
        """启动定时任务管理器"""
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # 重新调度所有启用的任务
        for task in self.tasks.values():
            self._schedule_task(task)
    
    def stop(self):
        """停止定时任务管理器"""
        self.running = False
        schedule.clear()
    
    def _run_scheduler(self):
        """运行调度器"""
        while self.running:
            schedule.run_pending()
            time.sleep(1)
    
    def save_tasks(self):
        """保存任务到文件"""
        data = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
        with open(self.task_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_tasks(self):
        """从文件加载任务"""
        if os.path.exists(self.task_file):
            try:
                with open(self.task_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = {task_id: TimedTask.from_dict(task_data) 
                                 for task_id, task_data in data.items()}
            except Exception as e:
                print(f"加载定时任务失败: {e}")
                self.tasks = {}


class CommandFramework:
    """指令处理框架"""
    
    def __init__(self, message_instance: Message):
        self.message = message_instance
        self.command_handlers: Dict[str, CommandHandler] = {}
        self.current_handler: Optional[CommandHandler] = None
        self.running = False
        
        # 注册基础指令
        self._register_basic_commands()
    
    def register_command(self, command: str, handler: CommandHandler):
        """注册指令处理器"""
        self.command_handlers[command] = handler
    
    def _register_basic_commands(self):
        """注册基础指令"""
        self.register_command("菜单", MenuCommandHandler(self.command_handlers))
        self.register_command("退出", ExitCommandHandler())
        self.register_command("关闭", CloseCommandHandler(self))
    
    def handle_message(self, message: str) -> str:
        """处理消息"""
        # 如果当前有活跃的处理器，先尝试使用它
        if self.current_handler and self.current_handler.name != "菜单":
            if message.lower() in ["退出", "exit", "quit"]:
                self.current_handler = self.command_handlers["菜单"]
                return "已返回主菜单"
            else:
                return self.current_handler.handle(message)
        
        # 否则查找对应的指令处理器
        if message in self.command_handlers:
            handler = self.command_handlers[message]
            if handler.name != "菜单":
                self.current_handler = handler
            return handler.handle(message)
        else:
            return "❓ 未知指令，输入 '菜单' 查看所有可用功能"


class WXFramework:
    """微信文件传输助手框架"""
    
    def __init__(self):
        # 不直接初始化WXFilehelper，因为它的__init__会阻塞等待登录
        self.wx_helper = None
        self.message = Message()
        self.task_manager = TimedTaskManager(self.message)
        self.command_framework = CommandFramework(self.message)
        self.running = False
        
        # 注册示例功能
        self._register_example_commands()
    
    def _register_example_commands(self):
        """注册示例功能"""
        # 定时任务管理
        self.command_framework.register_command("定时任务", TimedTaskCommandHandler(self.task_manager))
        
        # 示例功能
        self.command_framework.register_command("天气查询", WeatherCommandHandler())
        self.command_framework.register_command("时间查询", TimeCommandHandler())
        self.command_framework.register_command("帮助", HelpCommandHandler())
    
    def start(self):
        """启动框架"""
        print("🚀 微信文件传输助手框架启动中...")
        
        # 处理登录
        if self._wait_login():
            # 启动定时任务管理器
            self.task_manager.start()
            
            # 启动消息监听器
            self._start_message_listener()
        else:
            print("❌ 登录失败，程序退出")
            return False
        
        return True
    
    def _wait_login(self):
        """等待登录"""
        try:
            # 创建WXFilehelper实例并等待登录
            self.wx_helper = WXFilehelper()
            return True
        except Exception as e:
            print(f"登录失败: {e}")
            return False
    
    def _start_message_listener(self):
        """启动消息监听器"""
        self.running = True
        
        def message_loop():
            while self.running:
                try:
                    has_msg = self.message.sync_msg_check()
                    if has_msg:
                        self._handle_incoming_message()
                    time.sleep(0.3)
                except Exception as e:
                    print(f"消息监听错误: {e}")
                    time.sleep(1)
        
        listener_thread = threading.Thread(target=message_loop, daemon=True)
        listener_thread.start()
    
    def _handle_incoming_message(self):
        """处理接收到的消息"""
        try:
            # 使用原有的receive_msg方法获取消息
            url = f"{WX_FILEHELPER_HOST}/cgi-bin/mmwebwx-bin/webwxsync"
            params = {'sid': self.message.sid, 'skey': self.message.skey,
                      'pass_ticket': self.message.pass_ticket}
            json_data = {"BaseRequest": self.message.generate_base_request(),
                         "SyncKey": self.message.sync_key}

            resp = self.message.wx_req.fetch(
                url, method="post", params=params, json=json_data)
            
            if resp:
                data = json.loads(resp.content.decode('utf-8'))
                if data['BaseResponse']['Ret'] == 0:
                    if data['AddMsgList']:
                        for msg in data['AddMsgList']:
                            if msg['MsgType'] == 1:  # 文本消息
                                user_message = msg['Content']
                                print(f"收到消息: {user_message}")
                                
                                # 处理指令
                                response = self.command_framework.handle_message(user_message)
                                
                                # 发送回复
                                self.message.send_msg(content=response)
                                
                        self.message.sync_key = data['SyncKey']
        except Exception as e:
            print(f"处理消息错误: {e}")
    
    def shutdown(self):
        """关闭框架"""
        print("🛑 正在关闭框架...")
        self.running = False
        self.task_manager.stop()
        print("✅ 框架已关闭")


# 示例指令处理器
class TimedTaskCommandHandler(CommandHandler):
    """定时任务管理指令处理器"""
    
    def __init__(self, task_manager: TimedTaskManager):
        super().__init__("定时任务", "管理定时发送的消息")
        self.task_manager = task_manager
    
    def handle(self, message: str) -> str:
        if message == "列表":
            tasks = self.task_manager.list_tasks()
            if not tasks:
                return "📝 暂无定时任务"
            
            result = "📝 定时任务列表：\n\n"
            for task in tasks:
                status = "✅ 启用" if task.enabled else "❌ 禁用"
                result += f"• {task.task_id} ({status})\n"
                result += f"  时间: {task.schedule_time} ({task.task_type})\n"
                result += f"  脚本: {task.script_path}\n"
                if task.description:
                    result += f"  描述: {task.description}\n"
                result += "\n"
            return result
        
        elif message.startswith("添加"):
            # 格式: 添加 时间 脚本路径 [描述]
            parts = message.split(" ", 2)
            if len(parts) < 3:
                return "❌ 格式错误，正确格式: 添加 HH:MM 脚本路径 [描述]"
            
            time_str = parts[1]
            script_info = parts[2]
            
            # 检查是否有描述
            if " " in script_info:
                script_parts = script_info.split(" ", 1)
                script_path = script_parts[0]
                description = script_parts[1]
            else:
                script_path = script_info
                description = ""
            
            try:
                # 验证时间格式
                datetime.strptime(time_str, "%H:%M")
                
                # 验证脚本文件是否存在
                if not os.path.exists(script_path):
                    return f"❌ 脚本文件不存在: {script_path}"
                
                task_id = self.task_manager.add_task(script_path, time_str, "daily", description)
                return f"✅ 定时任务已添加，ID: {task_id}"
            except ValueError:
                return "❌ 时间格式错误，请使用 HH:MM 格式"
        
        elif message.startswith("删除"):
            task_id = message.split(" ", 1)[1] if len(message.split(" ", 1)) > 1 else None
            if not task_id:
                return "❌ 请指定要删除的任务ID"
            
            if self.task_manager.remove_task(task_id):
                return f"✅ 任务 {task_id} 已删除"
            else:
                return "❌ 任务不存在"
        
        elif message == "脚本目录":
            scripts_dir = "scripts"
            if not os.path.exists(scripts_dir):
                os.makedirs(scripts_dir)
                return f"📁 已创建脚本目录: {scripts_dir}"
            
            scripts = []
            for file in os.listdir(scripts_dir):
                if file.endswith('.py'):
                    scripts.append(file)
            
            if not scripts:
                return f"📁 脚本目录 {scripts_dir} 为空"
            
            result = f"📁 脚本目录 ({scripts_dir}):\n\n"
            for script in scripts:
                result += f"• {script}\n"
            return result
        
        else:
            return """📅 定时任务管理：
            
• 列表 - 查看所有定时任务
• 添加 HH:MM 脚本路径 [描述] - 添加定时任务
• 删除 任务ID - 删除定时任务
• 脚本目录 - 查看可用脚本

💡 示例: 
• 添加 09:00 scripts/morning.py 早安问候
• 添加 18:00 scripts/evening.py 晚安问候

📝 脚本文件需要放在 scripts/ 目录下"""


class WeatherCommandHandler(CommandHandler):
    """天气查询指令处理器"""
    
    def __init__(self):
        super().__init__("天气查询", "查询天气信息")
    
    def handle(self, message: str) -> str:
        return "🌤️ 天气查询功能（示例）\n\n这是一个示例功能，您可以在这里集成真实的天气API。\n\n输入 '退出' 返回主菜单"


class TimeCommandHandler(CommandHandler):
    """时间查询指令处理器"""
    
    def __init__(self):
        super().__init__("时间查询", "查询当前时间")
    
    def handle(self, message: str) -> str:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"🕐 当前时间：{current_time}"


class HelpCommandHandler(CommandHandler):
    """帮助指令处理器"""
    
    def __init__(self):
        super().__init__("帮助", "显示帮助信息")
    
    def handle(self, message: str) -> str:
        return """📖 帮助信息

这是一个微信文件传输助手框架，支持以下功能：

1. 📅 定时任务管理
   - 设置定时发送消息
   - 管理定时任务列表

2. 🎯 指令处理系统
   - 菜单式功能选择
   - 模块化功能扩展

3. 🔄 自动回复
   - 根据用户指令自动回复
   - 支持功能切换和退出

💡 输入 '菜单' 查看所有可用功能"""


if __name__ == "__main__":
    # 启动框架
    framework = WXFramework()
    try:
        framework.start()
        print("✅ 框架启动成功，等待消息...")
        
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 收到退出信号")
        framework.shutdown() 