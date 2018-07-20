import socket


message = "哈哈哈哈哈哈哈哈"


def handle(IP):
    client = socket.socket()
    client.connect(IP)
    client.send(message.encode())
    data = client.recv(1024).decode()
    print(data)
    # while True:
    #     data = input(">>:").strip().encode()
    #     client.send(data)
    #     data = client.recv(1024).decode()
    #     print(data)


if __name__ == '__main__':
    IP = ("192.168.0.102", 7339)
    for i in range(15000):
        handle(IP)