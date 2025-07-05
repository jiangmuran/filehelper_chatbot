#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提醒脚本示例

这个脚本演示了如何发送各种提醒消息
"""

# 获取当前时间
current_time = get_time()
weekday = current_time.strftime("%A")
hour = current_time.hour

# 根据星期几发送不同的提醒
weekday_reminders = {
    "Monday": "周一了，新的一周开始，加油！",
    "Tuesday": "周二，工作顺利！",
    "Wednesday": "周三，一周过半，继续努力！",
    "Thursday": "周四，周末快到了！",
    "Friday": "周五，明天就是周末了！",
    "Saturday": "周六，好好休息！",
    "Sunday": "周日，明天又要上班了，做好准备！"
}

# 发送星期提醒
weekday_msg = weekday_reminders.get(weekday, "今天也要加油哦！")
send_message(weekday_msg)

# 根据时间发送不同的提醒
if 9 <= hour < 12:
    time_reminder = "上午工作时间，专注工作，提高效率！"
elif 12 <= hour < 14:
    time_reminder = "午休时间，记得吃饭休息！"
elif 14 <= hour < 18:
    time_reminder = "下午工作时间，保持精力充沛！"
elif 18 <= hour < 20:
    time_reminder = "下班时间，记得整理工作，准备回家！"
else:
    time_reminder = "晚上时间，注意休息，不要熬夜！"

send_message(time_reminder)

# 发送健康提醒
health_reminders = [
    "记得多喝水，保持身体水分！",
    "工作久了记得站起来活动一下！",
    "注意用眼卫生，适当休息眼睛！",
    "保持良好坐姿，预防颈椎病！"
]

# 随机选择一个健康提醒
import random
health_reminder = random.choice(health_reminders)
send_message(health_reminder)

print("提醒脚本执行完成") 