import matplotlib.pyplot as plt
import matplotlib

# 设置字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 数据准备
items = ['大文件写', '大文件读', '小文件写', '小文件读']
values = [20.42, 91.81, 49.8 * 128 / 1024, 1159.5 * 128 / 1024]  # 将小文件的性能转换为MiB/s

# 绘制性能对比图
plt.figure(figsize=(10, 6))
bars = plt.bar(items, values, color=['blue', 'green', 'red', 'purple'], alpha=0.6, width=0.4)

# 在数据条上添加具体数值
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

plt.xlabel('操作')
plt.ylabel('速率 (MiB/s)')
plt.title('JuiceFS 大文件与小文件读写性能对比图')
plt.tight_layout()

# 显示图像
plt.show()