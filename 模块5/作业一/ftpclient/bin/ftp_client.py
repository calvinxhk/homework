import sys,os
basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(basedir)
from ftpclient.core import main
server_address = ('127.0.0.1',8080)
client = main.MyFtpClient(server_address)
client._run()