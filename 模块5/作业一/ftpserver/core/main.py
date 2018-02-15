import socketserver
import os
import struct
import json
from ftpserver.core.cmd_method import ShellCmd
from ftpserver.core import lib
'''head_server:{0: login error, 1:login successfully ,2:cmd error,3:limited space,
                4: file exist!,5: file data error,6:file inconsistent
                7: file start upload 8 file upload successfully }'''
'''head_client {'filename':filename,'file_size':file_size,'cmd':cmd,'file_md5':file_md5,
                'user':user,'password':password}'''
'''database:   {user:{password:{'home':home,'space':space}'''


class FtpServer(socketserver.BaseRequestHandler):
    code = 'utf8'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, 'db', 'userdatabase')
    max_recv_size = 8092

    def handle(self):
        print(self.request)
        login_result = self.__login()
        os.chdir(login_result['home'])
        while True:
            head = self.__head_del()
            cmd = head['cmd']
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                try:
                    func(head, login_result)
                except TypeError:
                    continue
            elif hasattr(ShellCmd, cmd):
                func = getattr(ShellCmd, cmd)
                try:
                    answer = func(self, head)
                    self.__head_add(answer)
                except TypeError:
                    continue

    def __login(self):
        with open(self.db_dir, 'r') as database_json:
            database = json.load(database_json)
        while True:
            head = self.__head_del()
            user = head['user']
            password = head['password']
            try:
                result = database[user][password]
                head_server = {1: 'login successfully!'}
                self.__head_add(head_server)
                return result
            except KeyError:
                head_server = {0: 'login error!'}
                self.__head_add(head_server)

    def __head_del(self):
        data = self.request.recv(4)
        data_len = struct.unpack('i', data)[0]
        head_json = self.request.recv(data_len).decode(self.code)
        head = json.loads(head_json)
        return head

    def __head_add(self, head):
        head_json = json.dumps(head)
        head_b = bytes(head_json, encoding=self.code)
        data = struct.pack('i', len(head_b))
        self.request.send(data)
        self.request.send(head_b)

    def __put(self,file_dir,file_size,file_md5):
        recv_size = 0
        with open(file_dir, 'ab+') as f:
            while recv_size < file_size:
                recv_data = self.request.recv(self.max_recv_size)
                f.write(recv_data)
                recv_size += len(recv_data)
        up_md5 = lib.file_md5(file_dir)
        if up_md5 == file_md5:
            head_server = {8: 'file upload successfully!'}
            self.__head_add(head_server)
            return 8
        else:
            head_server = {5: 'file data error!'}
            self.__head_add(head_server)
            os.remove(file_dir)
            return 5

    def upload(self, *argv):
        head, login_result = argv
        space = login_result['space']
        space_used = os.path.getsize(login_result['home'])
        space_spare = float(space) - float(space_used)
        filename = head['filename']
        file_size = head['file_size']
        file_md5 = head['file_md5']
        file_dir = os.path.join(os.getcwd(), filename)
        if file_size >= space_spare:
            head_server = {3: 'limited space!'}
            self.__head_add(head_server)
            return 3
        if os.path.exists(file_dir):
            file_server_md5 = lib.file_md5(file_dir)
            if file_server_md5 == file_md5:
                head_server = { 4: 'file exist'}
                self.__head_add(head_server)
                return 4
            file_server_size = os.path.getsize(file_dir)
            head_server = {'filename': filename, "file_size": file_server_size, 'file_md5': file_server_md5}
            self.__head_add(head_server)
            head_client = self.__head_del()
            file_size = head_client['file_size']
            file_md5 = head_client['file_md5']
            if '6' in head_client:
                return 6
        else:
            head_server = {7: 'file start upload'}
            self.__head_add(head_server)
        self.__put(file_dir, file_size, file_md5)

    def download(self, *argv):
        head, login_result = argv
        filename = head['filename']
        if not os.path.isfile(filename):
            head_answer = {5: 'filedata error'}
            self.__head_add(head_answer)
            return 5
        file_md5 = lib.file_md5(filename)
        file_size = os.path.getsize(filename)
        head_new = {'filename': filename, 'file_md5': file_md5, 'file_size': file_size}
        self.__head_add(head_new)
        with open(filename, 'rb') as f:
            # for line in f:
            #     self.request.send(line)
                self.request.send(f.read())


