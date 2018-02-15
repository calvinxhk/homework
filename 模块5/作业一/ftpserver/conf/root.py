import os,json,shutil

database_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'userdatabase')

while True:
    choice = input('1.useradd 2.userdel 3.user search 4.user change')
    if choice == '1':
        user = input('user')
        password = input('password')
        space = input('space')
        space = float(space) * 1024 * 1024
        with open(database_path, 'r+') as f:
            database = json.load(f)
            home = os.path.join(os.path.dirname(database_path), user)
            os.makedirs(home)
            info = {'space': space, 'home': home}
            info1 = {password: info}
            database[user] = info1
            f.seek(0)
            f.truncate(0)
            json.dump(database, f)
    if choice == '2':
        user = input('user')
        with open(database_path, 'r+') as f:
            database = json.load(f)
            try:
                del database[user]
                database = json.dumps(database)
                shutil.rmtree(os.path.join(os.path.dirname(database_path), user))
                f.seek(0)
                f.truncate(0)
                f.write(database)
            except KeyError:
                print('no user!')
    if choice == '3':
        with open(database_path, 'r') as f:
            database = json.load(f)
            user = input('user:')
            try:
                information = database[user]
                print(information)
            except KeyError:
                print('no user!')
    if choice == '4':
        with open(database_path, 'r+') as f:
            database = json.load(f)
            user = input('user:')
            try:
                information = database[user]
                print(information)
            except KeyError:
                print('no user!')
            database[user]['123456']['space'] = 1024*1024*1024
            f.seek(0)
            f.truncate(0)
            json.dump(database,f)

    if choice == 'q':
        break