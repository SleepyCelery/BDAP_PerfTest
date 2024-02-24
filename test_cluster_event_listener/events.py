from kubernetes import client, config
from datetime import datetime, timezone
from tqdm import tqdm

# 配置Kubernetes客户端
config.load_kube_config(config_file='kubernetes_admin_config')
# 使用EventsV1Api
api_instance = client.CoreV1Api()


# 创建事件的函数
def create_event(namespace, pod_name, event_name, event_message):
    # 准备事件对象
    event_time = datetime.now(timezone.utc).isoformat()
    # print(event_time)
    event = client.CoreV1Event(
        action="PERFTEST",
        involved_object=client.V1ObjectReference(
            api_version="v1",
            kind="Pod",
            name=pod_name,
            namespace=namespace,
            field_path="spec.containers{sleep-container}",
        ),
        metadata=client.V1ObjectMeta(name=event_name, namespace=namespace),
        message=event_message,
        type="Normal",
        reason="ForTest",
        event_time=event_time,
        reporting_component="bdap-perf-watcher",
        reporting_instance="bdap-perf-watcher-1",
    )
    # print(event)

    try:
        # 创建事件
        api_instance.create_namespaced_event(namespace, event, pretty="true")
    except client.rest.ApiException as e:
        print("Exception when calling EventsV1Api->create_namespaced_event: %s\n" % e)


# 在命名空间'namespace'的Pod 'pod_name'中创建10000个事件
def create_multiple_events(namespace, pod_name, count=10000):
    for i in tqdm(range(count)):
        event_name = f"test-event-{i}"
        event_message = f"This is test event {i} created by the Python script."
        create_event(namespace, pod_name, event_name, event_message)


def delete_all_events(namespace):
    # 获取命名空间中的所有事件
    events = api_instance.list_namespaced_event(namespace)
    # 删除所有事件
    for event in events.items:
        api_instance.delete_namespaced_event(event.metadata.name, namespace)
        print(f"Event {event.metadata.name} deleted.")


def get_events_count(namespace):
    # 获取命名空间中的所有事件
    events = api_instance.list_namespaced_event(namespace)
    return len(events.items)


if __name__ == '__main__':
    # 使用示例
    namespace = "bdap"
    pod_name = "sleep-pod"
    create_multiple_events(namespace, pod_name, count=10000)
    # delete_all_events(namespace)
    # print(get_events_count(namespace))
