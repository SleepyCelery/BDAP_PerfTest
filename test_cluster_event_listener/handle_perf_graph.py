import pandas as pd
import matplotlib.pyplot as plt
import re
import matplotlib

# 设置字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# File path
file_path = 'stdout.txt'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.readlines()

# Initialize lists to hold the extracted data
events_handled = []
cost_times = []
average_times = []

# Regular expressions to extract numbers
event_regex = re.compile(r'Handled (\d+) events')
cost_time_regex = re.compile(r'Cost time: ([\d.]+) seconds,')
average_time_regex = re.compile(r'average time: ([\d.]+) seconds per event')

# Extract data
for i in range(0, len(content), 5):
    event_line = content[i]
    cost_time_line = content[i + 2] if i + 2 < len(content) else None
    average_time_line = content[i + 3] if i + 3 < len(content) else None

    if event_line and cost_time_line and average_time_line:
        event_match = event_regex.search(event_line)
        cost_time_match = cost_time_regex.search(cost_time_line)
        average_time_match = average_time_regex.search(average_time_line)

        if event_match and cost_time_match and average_time_match:
            events_handled.append(int(event_match.group(1)))
            cost_times.append(float(cost_time_match.group(1)))
            average_times.append(float(average_time_match.group(1)))

# Create DataFrame
df = pd.DataFrame({
    'Events_Handled': events_handled,
    'Cost_Time_Seconds': cost_times,
    'Average_Time_Per_Event_Seconds': average_times
})

# Visualization

# Total Cost Time vs. Events Handled
plt.figure(figsize=(7, 6))
plt.plot(df['Events_Handled'], df['Cost_Time_Seconds'], marker='o', linestyle='-', color='blue')
plt.title('总耗时与处理事件数关系')
plt.xlabel('处理事件数')
plt.ylabel('总耗时 (秒)')
plt.show()

# Average Time Per Event vs. Events Handled
plt.figure(figsize=(7, 6))
plt.plot(df['Events_Handled'], df['Average_Time_Per_Event_Seconds'], marker='s', linestyle='-', color='red')
plt.title('每事件平均耗时与处理事件数关系')
plt.xlabel('处理事件数')
plt.ylabel('每事件平均耗时 (秒)')
plt.show()