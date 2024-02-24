import matplotlib.pyplot as plt
import matplotlib

# 设置字体为支持中文的字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 操作及其对应的平均成本（ms）
operations = ['Stat file', 'FUSE operation', 'Update meta', 'Put object', 'Get object', 'Write into cache',
              'Read from cache']
# 创建一个字典来存储操作的英文名称和对应的中文翻译
operation_translation = {
    'Stat file': '文件状态',
    'FUSE operation': 'FUSE操作',
    'Update meta': '更新元数据',
    'Put object': '放置对象',
    'Get object': '获取对象',
    'Write into cache': '写入缓存',
    'Read from cache': '从缓存读取'
}

# 使用字典来翻译操作的名称
operations_cn = [operation_translation[op] for op in operations]
costs = [
    1.79, 114.28,  # 文件状态和FUSE操作
    26.47, 180.79, 609.73,  # 元数据和对象操作
    5.37, 266.10  # 缓存操作
]

# 绘制操作成本图
plt.figure(figsize=(12, 8))
plt.barh(operations_cn, costs, color='skyblue')
plt.xlabel('平均耗时 (ms)')
plt.ylabel('操作')
plt.title('JuiceFS 各操作平均耗时对比图')
plt.tight_layout()

# 显示图像
plt.show()
