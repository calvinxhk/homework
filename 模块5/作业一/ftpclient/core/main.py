import socket
import struct
import os
import json
from ftpclient.core.shellorder import ShellCmd
from ftpclient.core import lib
'''head_server:{0: login error, 1:login successfully ,2:cmd error,3:limited space,
                4: file exist!,5: file data error,6:file inconsistent
                7: file start upload 8 file upload successfully }'''
'''head_client {'file_dir':file_dir,'file_size':file_size,'cmd':cmd,'file_md5':file_md5,
                'user':user,'password':password}'''


class MyFtpClient:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_size = 8192
    coding = 'utf8'
    request_queue_size = 5
    database = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db')

    def __init__(self, server_address, connect=True):
        self.server_address = server_address
        self.socket = socket.socket(self.address_family, self.socket_type)
        if connect:
            try:
                self.__client_connect()
            except Exception:
                self.__client_close()
                raise

    def __client_connect(self):
        self.socket.connect(self.server_address)
        print('success')

    def __client_close(self):
        self.socket.close()

    def __log(self):
        while True:
            user = input('user:').strip()
            password = input('password').strip()
            head_log = {'user': user, 'password': password}
            self.__head_add(head_log)
            answer = self.__head_del()
            if '1' in answer:
                print('login successfully!')
                return 1
            print('error: 0   user or password is wrong!')

    def __head_del(self):
        data = self.socket.recv(4)
        data_len = struct.unpack('i', data)[0]
        head_json = self.socket.recv(data_len).decode(self.coding)
        head = json.loads(head_json)
        return head

    def __head_add(self, head):
        head_json = json.dumps(head)
        data_b = bytes(head_json, encoding=self.coding)
        data = struct.pack('i', len(data_b))
        self.socket.send(data)
        self.socket.send(data_b)

    def _run(self):
        self.__log()
        while True:
            order = input(':>>').strip().split()
            if not order:
                continue
            cmd = order[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                try:
                    func(order)
                except TypeError:
                    continue
            elif hasattr(ShellCmd, cmd):
                try:
                    filename = order[1]
                except IndexError:
                    filename = 0
                head = {'cmd': cmd, 'filename': filename}
                self.__head_add(head)
                answer = self.__head_del()
                print(answer)
            else:
                print('error: 2  wrong order!')

    def __put(self, file_dir, file_size, begin=0):
        with open(file_dir, 'rb') as f:
            send_size = 0
            f.seek(begin)
            # self.socket.send(f.read())
            for line in f:
                self.socket.send(line)
                send_size += len(line)
                percent = send_size / file_size * 100
                lib.myprocess(percent)
        head_answer = self.__head_del()
        if '8' in head_answer:
            print('upload successfully!')
            return 8
        else:
            print('error 5 file data error')
            return 5

    def upload(self, args):
        try:
            file_dir = args[1]
        except IndexError:
            print('please input filename')
            return
        if not os.path.isfile(file_dir):
            print('wrong file path!')
            return
        file_size = os.path.getsize(file_dir)
        filename = os.path.basename(file_dir)
        file_md5 = lib.file_md5(file_dir)
        head = {'filename': filename, 'file_size': file_size, 'file_md5': file_md5, 'cmd': 'upload'}
        self.__head_add(head)
        head_answer = self.__head_del()
        if '3' in head_answer:
            print('error:3  limited space')
            return 3
        if '4' in head_answer:
            print('file is exist.')
            return 4
        if '7' in head_answer:
            self.__put(file_dir, file_size)
        else:
            file_server_size = head_answer['file_size']
            file_server_md5 = head_answer['file_md5']
            with open(file_dir, 'rb') as f:
                file_server = f.read(file_server_size)
                file_client_md5 = lib.file_md5(file_server)
                if file_client_md5 == file_server_md5:
                    file_need_size = file_size - file_server_size
                    head_fin = {'file_size': file_need_size, 'file_md5': file_md5}
                    self.__head_add(head_fin)
                    self.__put(file_dir, file_need_size, begin=file_server_size)
                else:
                    head_fin = {6: 'file inconsistent'}
                    self.__head_add(head_fin)
                    print('error:6  file inconsistent')
                    return 6

    def download(self, args):
        try:
            filename = args[1]
        except IndexError:
            print('please input filename')
            return
        head = {'filename': filename, 'cmd': 'download'}
        self.__head_add(head)
        head_answer = self.__head_del()
        if '5' in head_answer:
            print('error wrong filename!')
            return 5
        file_size = head_answer['file_size']
        file_md5 = head_answer['file_md5']
        recv_size = 0
        file_dir = os.path.join(self.database, filename)
        if os.path.exists(file_dir):
            file_dir += '(1)'
        with open(file_dir, 'wb') as f:
            while recv_size < file_size:
                file_recv = self.socket.recv(self.max_size)
                f.write(file_recv)
                recv_size += len(file_recv)
                percent = recv_size / file_size * 100
                lib.myprocess(percent)
        md5 = lib.file_md5(file_dir)
        if md5 == file_md5:
            print('download successfully!')
            return 8
        else:
            print('error file data error,please download again!')
            os.remove(file_dir)
            return 5


