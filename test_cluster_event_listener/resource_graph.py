import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 设置字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 读取数据文件
file_path = 'cpu_memory_usage.txt'  # 请替换为实际文件路径
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 初始化列表存储提取的数据
cpu_usage_percentages = []
memory_usage_mb = []
memory_usage_percentages = []

# 提取CPU占用率和内存占用数据
for line in lines:
    if line.strip():  # 跳过空行
        parts = line.strip().split(', ')
        try:
            cpu_usage = float(parts[0].split(': ')[1].strip('%'))
            memory_usage = float(parts[1].split(': ')[1].strip('MB'))
            memory_percentage = float(parts[2].split(': ')[1].strip('%'))

            cpu_usage_percentages.append(cpu_usage)
            memory_usage_mb.append(memory_usage)
            memory_usage_percentages.append(memory_percentage)
        except IndexError as e:
            # 处理非数据行或错误
            print(f"Error processing line: {line}. Error: {e}")

# 将数据转换为DataFrame
df = pd.DataFrame({
    "CPU Usage (%)": cpu_usage_percentages,
    "Memory Usage (MB)": memory_usage_mb,
    "Memory Usage (%)": memory_usage_percentages
})

# 绘制CPU占用率图表
fig, ax_cpu = plt.subplots(figsize=(10, 4))
ax_cpu.plot(df.index, df["CPU Usage (%)"], label='CPU占用率(%)', color='blue')
ax_cpu.fill_between(df.index, df["CPU Usage (%)"], 0, alpha=0.3, color='blue')
ax_cpu.set_title('单测试实例CPU占用率')
ax_cpu.set_xlabel('时间（秒）')
ax_cpu.set_ylabel('CPU占用率(%)')
ax_cpu.set_ylim(bottom=0, top=100)
ax_cpu.grid(True)
ax_cpu.legend()

# 调整坐标轴
ax_cpu.spines['left'].set_position(('data', 0))
ax_cpu.spines['bottom'].set_position(('data', 0))
ax_cpu.spines['right'].set_visible(False)
ax_cpu.spines['top'].set_visible(False)

# 绘制内存占用图表
fig, ax_memory = plt.subplots(figsize=(10, 4))
ax_memory.plot(df.index, df["Memory Usage (MB)"], label='内存占用量（MB）', color='red')
ax_memory.fill_between(df.index, df["Memory Usage (MB)"], 0, alpha=0.3, color='red')
ax_memory.set_title('单测试实例内存占用量')
ax_memory.set_xlabel('时间（秒）')
ax_memory.set_ylabel('内存用量（MB）')
ax_memory.set_ylim(bottom=0, top=max(df["Memory Usage (MB)"]) * 1.1)
ax_memory.grid(True)
ax_memory.legend()

# 调整坐标轴
ax_memory.spines['left'].set_position(('data', 0))
ax_memory.spines['bottom'].set_position(('data', 0))
ax_memory.spines['right'].set_visible(False)
ax_memory.spines['top'].set_visible(False)

plt.tight_layout()
plt.show()
