import pika, sys

# 建立socket通信
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

# 声明一个管道
channel = connection.channel()

# 声明一个中间转化器exchange，防止producer那边没声明报错
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# 声明一个随机且唯一的queue，(exclusive:唯一的，排他的)
result = channel.queue_declare(exclusive=True)

# 得到queue的name
queue_name = result.method.queue

# 绑定中间转发器exchange，和刚才产生的queue
channel.queue_bind(exchange='logs', queue=queue_name)

# 从命令行获得参数，该参数作用是：queue能够接受消息类型的
severities = sys.argv[1:]

# 如果没有参数，直接报错，退出
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# 循环所有参数，绑定所有参数所示有类型，使该queue能够接受相应类型的消息
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

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
                      queue=queue_name,
                      no_ack=False)

print("start...")

# 循环堵塞接受消息
channel.start_consuming()