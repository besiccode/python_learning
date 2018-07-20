import pika

# 建立socket通信
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

# 声明一个管道
channel = connection.channel()

# 声明一个queue(防止producer那边没有声明，如果那边声明了，就直接返回)
channel.queue_declare(queue="hello1", durable=True)


# 接受到消息时的处理函数
def callback(ch, method, properties, boby):
    print(boby.decode())
    # 代表执行完该函数的消息接受，主动向producer发送接受完数据的消息，以确保消息从queue中删除
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 当前机器的消息队列里面小于3条信息，producer将消息发到此机器处理
channel.basic_qos(prefetch_count=3)

# 配置相应的信息(处理函数，queue，no_ack(False:未执行完callback，不从producer的queue中删除
#                                    True:未执行完callback，从producer的queue中删除))
channel.basic_consume(callback,
                      queue="hello1",
                      no_ack=False)

print("start...")

# 循环堵塞接受消息
channel.start_consuming()
