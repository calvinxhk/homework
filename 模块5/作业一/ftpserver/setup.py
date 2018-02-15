import os
import json

database_path = os.path.join(os.path.dirname(__file__),'db','userdatabase')
database = open(database_path,'r+')
if not database.read():
    dic = {'name':{'password':{'space':'2T','home':'root'}}}
    dic_json = json.dumps(dic)
    database.write(dic_json)
database.close()
