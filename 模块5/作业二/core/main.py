import threading,paramiko

'''实现批量命令执行、文件分发'''


class Mytool:

    @staticmethod
    def ssh_cmd(hostname,user,password,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(hostname,22,user,password)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        for i in stdout.readlines():
            print(hostname,i)
        for i in stderr.readlines():
            print(i)
        ssh.close()

    @staticmethod
    def tran_put(hostname,user,password,local,remote):
        tran = paramiko.Transport((hostname,22))
        tran.connect(username=user,password=password)
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.put(local,remote)
        tran.close()

    @staticmethod
    def tran_get(hostname, user, password,remote,local):
        tran = paramiko.Transport((hostname, 22))
        tran.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.get(remote,local)
        tran.close()


    @staticmethod
    def get_ip():
        with open('database','r') as f:
            data = f.readlines()
        return data

    @staticmethod
    def mythreading(data,target,*args):
        func = []
        for i in data:
            info = tuple(i.split())
            argv = info+args
            t = threading.Thread(target=target, args=argv)
            func.append(t)
            t.start()
        for i in func:
            i.join()


    def run(self):
        while True:
            choose = input('1.ssh 2.put 3.get').strip()
            if choose == 'q':
                break
            if choose == '1':
                while True:
                    cmd = input('please input your commend:').strip()
                    if cmd == 'q':
                        break
                    data = self.get_ip()
                    self.mythreading(data,self.ssh_cmd,cmd)
            if choose == '2':
                while True:
                    local = input('input local file path:').strip()
                    remote = input('input remote file path:').strip()
                    choice = input('are you sure to go on ? q to quit:').strip()
                    if choice == 'q':
                        break
                    data = self.get_ip()
                    self.mythreading(data,self.tran_put,local,remote)
            if choose == '3':
                while True:
                    local = input('input local file path:').strip()
                    remote = input('input remote file path:').strip()
                    choice = input('are you sure to go on ? q to quit:').strip()
                    if choice == 'q':
                        break
                    data = self.get_ip()
                    self.mythreading(data, self.tran_get, remote, local)

mytool = Mytool()
mytool.run()


