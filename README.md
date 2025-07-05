# 微信文件传输助手框架
<iframe style="width:100%;height:auto;min-width:600px;min-height:400px;" src="https://www.star-history.com/embed?secret=#jiangmuran/filehelper_chatbot&Date" frameBorder="0"></iframe>

## 功能特性

### 🕐 定时任务管理
- 设置每日定时执行脚本
- 脚本具有发送消息的权限
- 管理定时任务列表
- 支持启用/禁用任务
- 任务持久化存储

### 🎯 指令处理系统
- 菜单式功能选择
- 模块化功能扩展
- 支持功能切换和退出
- 自动回复机制

### 🔧 框架特性
- 基于原有微信文件传输助手库
- 线程安全的定时任务调度
- 可扩展的指令处理器架构
- 完整的错误处理机制

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 基础使用

```python
from framework import WXFramework

# 创建框架实例
framework = WXFramework()

# 启动框架
framework.start()
```

### 2. 运行示例

```bash
python example.py
```

## 使用说明

### 登录流程
1. 运行程序后，会显示登录二维码
2. 使用微信扫描二维码登录
3. 登录成功后，程序开始监听消息

### 基本操作
- 向文件传输助手发送 `菜单` 查看所有功能
- 输入功能名称进入对应功能
- 在功能内输入 `退出` 返回主菜单
- 输入 `关闭` 退出程序

### 定时任务管理
```
定时任务
├── 列表 - 查看所有定时任务
├── 添加 HH:MM 脚本路径 [描述] - 添加定时任务
├── 删除 任务ID - 删除定时任务
└── 脚本目录 - 查看可用脚本
```

示例：
- `添加 09:00 scripts/morning.py 早安问候` - 设置每天早上9点执行早安脚本
- `添加 18:00 scripts/evening.py 晚安问候` - 设置每天晚上6点执行晚安脚本
- `列表` - 查看所有定时任务
- `删除 task_1234567890` - 删除指定任务
- `脚本目录` - 查看可用的脚本文件

## 框架架构

### 核心组件

#### 1. WXFramework
主框架类，负责协调各个组件：
- 微信登录和消息监听
- 定时任务管理
- 指令处理系统

#### 2. TimedTaskManager
定时任务管理器：
- 脚本任务的增删改查
- 任务调度和脚本执行
- 任务持久化存储
- 脚本执行环境管理

#### 3. CommandFramework
指令处理框架：
- 指令注册和分发
- 功能切换管理
- 自动回复处理

### 扩展自定义功能

#### 1. 创建指令处理器

```python
from framework import CommandHandler

class MyCommandHandler(CommandHandler):
    def __init__(self):
        super().__init__("我的功能", "功能描述")
    
    def handle(self, message: str) -> str:
        # 处理用户消息，返回回复内容
        if message == "操作1":
            return "执行操作1"
        elif message == "操作2":
            return "执行操作2"
        else:
            return "可用操作：操作1、操作2"
```

#### 2. 注册功能

```python
from framework import WXFramework

framework = WXFramework()
framework.command_framework.register_command("我的功能", MyCommandHandler())
```

#### 3. 完整示例

```python
from framework import WXFramework, CommandHandler

class WeatherCommandHandler(CommandHandler):
    def __init__(self):
        super().__init__("天气", "查询天气信息")
    
    def handle(self, message: str) -> str:
        if message.startswith("查询"):
            city = message[2:].strip()
            # 这里集成真实的天气API
            return f"查询{city}的天气信息"
        else:
            return "请输入：查询 城市名"

# 创建框架并注册功能
framework = WXFramework()
framework.command_framework.register_command("天气", WeatherCommandHandler())
framework.start()
```

## 内置功能

### 基础功能
- **菜单** - 显示所有可用功能
- **退出** - 返回主菜单
- **关闭** - 退出程序
- **帮助** - 显示帮助信息

### 示例功能
- **定时任务** - 管理定时发送的消息
- **天气查询** - 查询天气信息（示例）
- **时间查询** - 查询当前时间

## 文件结构

```
wxfilehelper/
├── lib.py              # 原始微信文件传输助手库
├── framework.py        # 框架核心代码
├── example.py          # 使用示例
├── requirements.txt    # 依赖包列表
├── README.md          # 说明文档
├── timed_tasks.json   # 定时任务存储文件（运行时生成）
└── scripts/           # 脚本目录
    ├── README.md      # 脚本使用说明
    ├── morning.py     # 早安问候脚本
    ├── evening.py     # 晚安问候脚本
    ├── weather_report.py # 天气报告脚本
    └── reminder.py    # 提醒脚本
```

## 注意事项

1. **安全性**：示例中的计算器功能使用了`eval()`，生产环境中应使用更安全的方法
2. **稳定性**：框架包含完整的错误处理，但网络异常时可能需要重新登录
3. **扩展性**：所有功能都基于`CommandHandler`基类，便于扩展
4. **持久化**：定时任务会自动保存到`timed_tasks.json`文件中

## 故障排除

### 常见问题

1. **登录失败**
   - 检查网络连接
   - 确保微信账号正常
   - 重新运行程序

2. **消息发送失败**
   - 检查登录状态
   - 确认微信文件传输助手可用
   - 查看错误日志

3. **定时任务不执行**
   - 检查任务是否启用
   - 确认时间格式正确（HH:MM）
   - 查看控制台日志

### 调试模式

在代码中添加日志输出来调试问题：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 许可证

本项目基于原有微信文件传输助手库开发，请遵守相关使用条款。 
