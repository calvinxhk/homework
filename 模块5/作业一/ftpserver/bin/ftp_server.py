import socketserver
import sys,os
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basedir)
from ftpserver.core import main
server_addr = ('127.0.0.1',8080)
ftp = socketserver.ThreadingTCPServer(server_addr, main.FtpServer)
ftp.serve_forever()