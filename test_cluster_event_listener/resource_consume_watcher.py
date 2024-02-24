from dotenv import load_dotenv

load_dotenv('ClusterEventListener.env')
import subprocess
import psutil
# import events

namespace = "bdap"
pod_name = "sleep-pod"

# # 删除所有事件
# events.delete_all_events(namespace)
#
# # 生成10000条与该Pod绑定的events
# events.create_multiple_events(namespace, pod_name, count=10000)

# 使用subprocess创建调用event_listener.py文件的子进程
process = subprocess.Popen(['python3', 'event_listener.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 获取进程ID
pid = process.pid

# 创建一个psutil进程对象
p = psutil.Process(pid)

while True:
    # 循环监控
    try:
        # CPU占用率
        cpu_percent = p.cpu_percent(interval=1)
        # 内存占用
        memory_info = p.memory_info()
        memory_percent = p.memory_percent()

        print(
            f"CPU占用率: {cpu_percent}%, 内存占用: {memory_info.rss / (1024 * 1024):.2f}MB, 内存占用率: {memory_percent}%\n")

        # 检查进程是否已结束
        if process.poll() is not None:
            print("程序执行完毕\n")
            # 将其标准输出和标准错误重定向到文件
            with open('stdout.txt', 'w') as stdout, open('stderr.txt', 'w') as stderr:
                for line in process.stdout:
                    stdout.write(line.decode())
                for line in process.stderr:
                    stderr.write(line.decode())
            break

    except psutil.NoSuchProcess:
        print("进程已结束")

    except KeyboardInterrupt:
        print("手动中断监控")
