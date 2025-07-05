#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晚安问候脚本示例

这个脚本演示了如何使用框架提供的API发送消息
"""

# 获取当前时间
current_time = get_time()
hour = current_time.hour

# 根据时间发送不同的问候语
if 18 <= hour < 22:
    greeting = "晚上好！今天辛苦了，记得放松一下！"
elif 22 <= hour or hour < 6:
    greeting = "夜深了，该休息了，祝您好梦！"
else:
    greeting = "晚安！明天又是美好的一天！"

# 发送问候消息
send_message(greeting)

# 发送一些温馨的提醒
reminder1 = "记得整理一下今天的工作，为明天做准备！"
send_message(reminder1)

reminder2 = "睡前可以喝杯温水，有助于睡眠！"
send_message(reminder2)

# 发送晚安祝福
good_night = "🌙 晚安，明天见！"
send_message(good_night)

print("晚安问候脚本执行完成") 