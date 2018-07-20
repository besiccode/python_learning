import paramiko

# 将私钥导入
private_key = paramiko.RSAKey.from_private_key_file("/Users/mac/.ssh/id_rsa")

# 创建SSH对象
ssh = paramiko.SSHClient()

# 确保当前连接在kown_hosts中
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接远程用户
ssh.connect(hostname="118.89.32.173", port=22, username="ubuntu", pkey=private_key)

# 执行command命令，并返回结果
stdin, stdout, stderr = ssh.exec_command("cd ..;cd xiaohei;cd wrok;ls")

err = stderr.read()

out = stdout.read()

result = err if err else out

print(result.decode())