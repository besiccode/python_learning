import socket
import selectors


# 得到一个selectors对象
sel = selectors.DefaultSelector()


# 当来一个链接时，触发的回调函数。
def accept(sock, mark):
    conn, addr = sock.accept()
    conn.setblocking(False)
    # 将新来的链接，注册到selectors中进行等待,当该链接活跃时，触发read函数进行处理
    sel.register(conn, selectors.EVENT_READ, read)


# 每个链接的活跃时，触发的回调函数，进行相应的处理
def read(conn, mark):
    data = conn.recv(1024)
    if data:
        conn.send(data)
    else:
        # print("close", conn)
        sel.unregister(conn)
        conn.close()


if __name__ == '__main__':
    # 得到一个socket对象
    sock = socket.socket()

    # 绑定本地端口
    sock.bind(("", 7339))

    # 进行监听事件
    sock.listen(1000)

    # 将该socket对象，设为非堵塞
    sock.setblocking(False)

    # 将socket对象注册到selectors对象中，当有新的链接时，触发accept函数，进行处理
    sel.register(sock, selectors.EVENT_READ, accept)

    # 循环进行消息处理
    while True:
        # selectors对象进行消息等待，当有消息时，返回该消息事件
        events = sel.select()
        # 循环事件列表。
        # 新链接建立事件，触发accept函数，进行处理；
        # 每个已注册链接的活跃事件，触发read函数进行处理；
        for key, mark in events:
            callable = key.data
            callable(key.fileobj, mark)




