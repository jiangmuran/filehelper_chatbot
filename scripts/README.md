# 脚本使用说明

这个目录包含了定时任务可以执行的脚本文件。

## 脚本编写规范

### 1. 基本结构
每个脚本都应该包含以下基本结构：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本描述
"""

# 脚本内容
```

### 2. 可用的API函数

框架为脚本提供了以下API函数：

#### `send_message(content: str)`
发送文本消息到微信文件传输助手
```python
send_message("你好，这是一条测试消息！")
```

#### `send_file(file_path: str)`
发送文件到微信文件传输助手
```python
send_file("path/to/your/file.jpg")
```

#### `get_time()`
获取当前时间，返回datetime对象
```python
current_time = get_time()
hour = current_time.hour
day = current_time.strftime("%A")
```

#### `print(*args, **kwargs)`
带时间戳的打印函数
```python
print("脚本开始执行")
print("处理完成")
```

### 3. 可用的模块

脚本中可以使用以下Python模块：
- `datetime` - 日期时间处理
- `time` - 时间相关函数
- `json` - JSON数据处理
- `os` - 操作系统接口
- `sys` - 系统相关参数

### 4. 示例脚本

#### morning.py - 早安问候
- 根据时间发送不同的问候语
- 发送天气信息和健康提醒

#### evening.py - 晚安问候
- 发送晚安祝福
- 提供温馨提醒

#### weather_report.py - 天气报告
- 模拟天气数据
- 根据天气情况给出建议

#### reminder.py - 提醒脚本
- 根据星期几发送不同提醒
- 根据时间发送工作提醒
- 随机发送健康提醒

## 创建自定义脚本

### 1. 创建新脚本
在 `scripts/` 目录下创建新的 `.py` 文件：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
我的自定义脚本
"""

# 获取当前时间
current_time = get_time()

# 发送自定义消息
send_message(f"现在是 {current_time.strftime('%H:%M')}，该做某事了！")

print("脚本执行完成")
```

### 2. 注册定时任务
使用框架的定时任务功能注册脚本：
```
添加 09:00 scripts/my_script.py 我的自定义任务
```

### 3. 脚本调试
- 脚本执行时会显示执行日志
- 如果脚本出错，会在控制台显示错误信息
- 可以使用 `print()` 函数输出调试信息

## 注意事项

1. **安全性**：脚本在受限环境中执行，只能访问框架提供的API
2. **错误处理**：建议在脚本中添加适当的错误处理
3. **性能**：避免在脚本中执行耗时操作，以免影响消息发送
4. **编码**：确保脚本文件使用UTF-8编码

## 高级用法

### 条件执行
```python
current_time = get_time()
if current_time.weekday() < 5:  # 工作日
    send_message("工作日提醒")
else:
    send_message("周末愉快")
```

### 多消息发送
```python
messages = [
    "第一条消息",
    "第二条消息", 
    "第三条消息"
]

for msg in messages:
    send_message(msg)
    time.sleep(1)  # 间隔1秒发送
```

### 文件操作
```python
# 检查文件是否存在
if os.path.exists("data.txt"):
    with open("data.txt", "r", encoding="utf-8") as f:
        content = f.read()
    send_message(f"文件内容: {content}")
else:
    send_message("文件不存在")
``` 