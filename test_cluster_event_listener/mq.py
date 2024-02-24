import os
import pika

# Get RabbitMQ connection parameters from environment variables
rabbitmq_host = os.getenv('rabbitmq_host')
rabbitmq_port = int(os.getenv('rabbitmq_port'))
rabbitmq_user = os.getenv('rabbitmq_user')
rabbitmq_password = os.getenv('rabbitmq_password')
rabbitmq_vhost = os.getenv('rabbitmq_vhost')
rabbitmq_queue = os.getenv('rabbitmq_queue')
rabbitmq_exchange = os.getenv('rabbitmq_exchange')
rabbitmq_routing_key = os.getenv('rabbitmq_routing_key')

# Create a global channel variable to hold our channel object
global channel


def connect_to_rabbitmq():
    # Define our connection parameters
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host,
                                           port=rabbitmq_port,
                                           virtual_host=rabbitmq_vhost,
                                           credentials=credentials)

    # Create a new connection with the parameters
    connection = pika.BlockingConnection(parameters)

    # Create a new channel with the connection
    global channel
    channel = connection.channel()
    channel.confirm_delivery()
    # 创建队列
    result = channel.queue_declare(rabbitmq_queue, exclusive=False, durable=False)
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange=rabbitmq_exchange, durable=False, exchange_type='direct')
    # 绑定exchange和队列  exchange 使我们能够确切地指定消息应该到哪个队列去
    channel.queue_bind(exchange=rabbitmq_exchange, queue=result.method.queue, routing_key='Event')


# Connect to RabbitMQ
connect_to_rabbitmq()

publish_properties = pika.BasicProperties(
    delivery_mode=2,  # make message persistent
)


def send_message_to_queue(message):
    # Send the message to the queue
    channel.basic_publish(exchange=rabbitmq_exchange,
                          routing_key="Event",
                          body=message,
                          properties=publish_properties)


def clear_queue():
    channel.queue_purge(rabbitmq_queue)
