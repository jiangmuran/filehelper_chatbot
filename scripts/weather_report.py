#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气报告脚本示例

这个脚本演示了如何发送天气信息（示例数据）
"""

import random

# 模拟天气数据（实际使用时可以调用真实的天气API）
weather_data = {
    "temperature": random.randint(15, 30),
    "weather": random.choice(["晴天", "多云", "小雨", "阴天"]),
    "humidity": random.randint(40, 80),
    "wind": random.choice(["微风", "轻风", "无风"])
}

# 构建天气报告
weather_report = f"""🌤️ 今日天气报告

温度: {weather_data['temperature']}°C
天气: {weather_data['weather']}
湿度: {weather_data['humidity']}%
风力: {weather_data['wind']}

💡 天气建议:"""

# 根据天气情况给出建议
if weather_data['weather'] == "晴天":
    weather_report += "\n• 天气晴朗，适合外出活动"
    weather_report += "\n• 注意防晒，多喝水"
elif weather_data['weather'] == "小雨":
    weather_report += "\n• 有小雨，记得带伞"
    weather_report += "\n• 注意路面湿滑"
elif weather_data['weather'] == "多云":
    weather_report += "\n• 天气多云，温度适宜"
    weather_report += "\n• 适合户外活动"
else:
    weather_report += "\n• 天气阴沉，注意保暖"
    weather_report += "\n• 可以室内活动"

# 发送天气报告
send_message(weather_report)

print("天气报告脚本执行完成") 