import pika

# 建立一个socket通信
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

# 声明一个管道
channel = connection.channel()

# 声明一个queue，durable=True是将队列设置为持久化
channel.queue_declare(queue="hello1", durable=True)
# channel.queue_declare(queue="hello")

while True:
    message = input(">>:").strip()
    if message == "stop":
        break
    # 向相应的queue里面发消息
    channel.basic_publish(exchange='',
                          routing_key="hello1", # queue名字
                          body=message, # 发送的内容
                          properties=pika.BasicProperties(
                              delivery_mode=2 # 将消息设置为持久化
                          ))
    print("send ", message)

# 关闭socket
connection.close()
