import pika

# 建立一个socket通信
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

# 声明一个管道
channel = connection.channel()

# 声明一个中间转发器exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

while True:
    message = input(">>:").strip()
    if message == "stop":
        break
    # 向相应的queue里面发消息
    channel.basic_publish(exchange='logs', #转发器的名字
                          routing_key='', # queue名字
                          body=message, # 发送的内容
                          )
    print("send ", message)

# 关闭socket
connection.close()
