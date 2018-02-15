# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# ssh.connect('192.168.1.81',22,'root','123')
# while True:
#     stdin, stdout, stderr = ssh.exec_command(input())
#     for i in stdout.readlines():
#         print(i)
#
# ssh.close()
import threading
# def a(name=456):
#     # name = input('name')
#     print(name)
#
# def b(name=123):
#     # name = input('test')
#     print(name +466)
#
# t1 = threading.Thread(target=a, )
# t2 = threading.Thread(target=b ,)
# t1.start()
# t2.start()

def a()