import pika
import sys

# 建立一个socket通信
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

# 声明一个管道
channel = connection.channel()

# 声明一个中间转发器exchange
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 从命令行获得参数，该参数作用是：让exchange转发器，能够向，具有参数所示类型，的queue发送消息
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'

while True:
    message = input(">>:").strip()
    if message == "stop":
        break
    # 向相应的queue里面发消息
    channel.basic_publish(exchange='direct_logs', #转发器的名字
                          routing_key='', # queue名字
                          body=message, # 发送的内容
                          )
    print("send ", message)

# 关闭socket
connection.close()
