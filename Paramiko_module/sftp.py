import paramiko

# 将私钥导入
private_key = paramiko.RSAKey.from_private_key_file("/Users/mac/.ssh/id_rsa")

transport = paramiko.Transport(('192.168.0.102', 22))

transport.connect(username="root", pkey=private_key)

sftp = paramiko.SFTPClient.from_transport(transport)

# 将本地文件上传至所连接的远程用户
sftp.put("/Users/mac/PycharmProjects/ssh/io_多路复用/server.py", "io_server.py")

# 从远程用户上下载文件
# sftp.get("/home/xiaohei/dos.c", "dos.c")

transport.close()