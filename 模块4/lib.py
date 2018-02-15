import pickle


def login():
    f = open('database', 'rb')
    database = pickle.load(f)
    f.close()
    while True:
        user = input("user:").strip()
        password = input('password:').strip()
        if user == 'root' and password == '123456':
            information = [i for i in database if i.__class__.__name__ == 'Root'
                           and i.name == user and i.password == password]
        else:
            information = [i for i in database if i.__class__.__name__ == 'Student'
                           and i.name == user and i.password == password]
        if information:
            print('Successfully login!')
            return information[0]
        else:
            print('wrong user or password!')


def is_num(number):
    try:
        number = float(number)
        return number
    except ValueError:
        return 0


def database_search(name, cla):
    f = open('database', 'rb')
    database = pickle.load(f)
    target = [i for i in database if i.__class__.__name__ == '%s' % cla and i.name == name]
    if target:
        target = target[0]
    f.close()
    return target


def database_write(target):
    f = open('database', 'rb+')
    database = pickle.load(f)
    database.append(target)
    f.seek(0)
    f.truncate(0)
    pickle.dump(database, f)
    f.close()
    print('successfully!')


def database_del(name, cla):
    f = open('database', 'rb+')
    database = pickle.load(f)
    result = [i for i in database if i.__class__.__name__ == '%s' % cla and i.name == name]
    database.remove(result[0])
    f.seek(0)
    f.truncate(0)
    pickle.dump(database, f)
    print('successfully!')
    f.close()
    return True


def database_update(target):
    f = open('database', 'rb+')
    database = pickle.load(f)
    result = [i for i in database if i.__class__.__name__ == '%s' % target.__class__.__name__
              and i.name == target.name]
    database.remove(result[0])
    database.append(target)
    f.seek(0)
    f.truncate(0)
    pickle.dump(database, f)
    f.close()
    return True


