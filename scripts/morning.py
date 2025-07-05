#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早安问候脚本示例

这个脚本演示了如何使用框架提供的API发送消息
"""

# 获取当前时间
current_time = get_time()
hour = current_time.hour

# 根据时间发送不同的问候语
if 5 <= hour < 12:
    greeting = "早上好！新的一天开始了，祝您心情愉快！"
elif 12 <= hour < 18:
    greeting = "下午好！工作辛苦了，记得休息一下哦！"
else:
    greeting = "晚上好！今天过得怎么样？"

# 发送问候消息
send_message(greeting)

# 发送一些有用的信息
weather_info = "今天天气不错，适合外出活动！"
send_message(weather_info)

# 发送提醒
reminder = "记得喝水，保持健康！"
send_message(reminder)

print("早安问候脚本执行完成") 