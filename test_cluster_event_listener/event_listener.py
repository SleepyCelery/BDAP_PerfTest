from dotenv import load_dotenv

import mq

load_dotenv('ClusterEventListener.env')
import time
from kubernetes import client, config, watch
from mq import send_message_to_queue

# 配置 kubernetes 客户端
config.load_kube_config("kubernetes_admin_config")

# 定义一个字典，用于查询事件
event_dict = {
    "Scheduled": "changeTaskStatusToScheduled",
    "Started": "changeTaskStatusToRunning",
    "Succeeded": "changeTaskStatusToSucceeded",
    "Failed": "changeTaskStatusToFailed",
    "Killing": "changeTaskStatusToKilling"
}


# 定义一个函数，该函数将接收一个事件，查询字典，然后将查询结果发送到消息队列中
def handle_event(event):
    event_type = event['type']
    event_data = event['object']
    event_reason = event_data.reason

    # 查询字典
    dict_result = event_dict.get(event_reason, "Unknown event")

    # 将查询结果发送到消息队列中
    send_message_to_queue(dict_result)


# 创建一个 watch 对象
w = watch.Watch()

# 获取特定命名空间的事件
namespace = "bdap"  # 更改为你的命名空间

# 计算并打印整个过程的时间
start_time = time.time()
handled_count = 0
for event in w.stream(client.CoreV1Api().list_namespaced_event, namespace):
    handle_event(event)
    handled_count += 1
    if handled_count % 100 == 0:
        print(f"Handled {handled_count} events")
        end_time = time.time()
        print(f"""
                Cost time: {end_time - start_time} seconds,
                average time: {round((end_time - start_time) / handled_count, 4)} seconds per event
                """)
    if handled_count == 10000:
        end_time = time.time()
        print(f"""
        All events handled.
        Total time: {end_time - start_time} seconds,
        handled {handled_count} events,
        average time: {round((end_time - start_time) / handled_count, 4)} seconds per event,
        handle speed: {round(handled_count / (end_time - start_time), 4)} events per second
        """)
        mq.clear_queue()
        break
