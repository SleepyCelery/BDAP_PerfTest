import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# 设置字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# Data
data = {
    'Record Count': [10000, 20000, 50000, 100000],
    'Average TPS': [1802.369833, 1806.287400, 1827.359667, 1803.019133],
    'Average QPS': [36180.934600, 36193.274867, 36575.604667, 36074.938900]
}

df = pd.DataFrame(data)

# TPS Bar Chart
plt.figure(figsize=(7, 5))
tps_min, tps_max = df['Average TPS'].min(), df['Average TPS'].max()
tps_buffer = (tps_max - tps_min) * 0.1
plt.ylim([tps_min - tps_buffer, tps_max + tps_buffer])
plt.bar(df['Record Count'].astype(str), df['Average TPS'],
        color='skyblue')  # Convert Record Count to string for plotting
plt.title('不同记录数下的平均 TPS 对比图')
plt.xlabel('记录数')
plt.ylabel('平均 TPS')
plt.grid(axis='y', linestyle='--')
plt.show()

# QPS Bar Chart
plt.figure(figsize=(7, 5))
qps_min, qps_max = df['Average QPS'].min(), df['Average QPS'].max()
qps_buffer = (qps_max - qps_min) * 0.1
plt.ylim([qps_min - qps_buffer, qps_max + qps_buffer])
plt.bar(df['Record Count'].astype(str), df['Average QPS'],
        color='lightgreen')  # Convert Record Count to string for plotting
plt.title('不同记录数下的平均 QPS 对比图')
plt.xlabel('记录数')
plt.ylabel('平均 QPS')
plt.grid(axis='y', linestyle='--')
plt.show()
