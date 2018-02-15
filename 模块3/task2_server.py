import datetime
# ATM
#     1. 指定最大透支额度


#     6. 支持多用户登陆，用户间转帐


#     8. 管理员可添加账户、指定用户额度、冻结用户等


def is_num(self):
    try:
        float(self)
        return True
    except ValueError:
        pass


def user_search(name):
    with open('database', 'r', encoding='utf8') as f:
        data = [i for i in f]
        for i in data:
            i = i.split(',')
            if i[1] == name:
                return True
        print("no target user!")


def overdraft_root(user_o, amount):
    if user_search(user_o):
        if is_num(amount):
            with open("%s" % user_o, "r", encoding="utf8") as f:
                amount = float(amount)
                data = [i for i in f]
                inf = data[0].split(",")
                inf[5] = amount.__str__()
                if amount <= float(inf[4]):
                    if amount <= float(inf[3]):
                        inf[3] = amount.__str__()
                    inf[4] = amount.__str__()
                data[0] = ','.join(inf)
                data = ''.join(data)
            with open("%s" % user_o, "w", encoding="utf8") as f_w:
                f_w.write(data)
                print("successfully!")
        else:
            print('please input right number!')


def user_add(name, password="123456", level="customer"):
    with open("database", "r", encoding="utf8") as f_1:
        data = [i for i in f_1]
        information = '\n%s,%s,%s' % (level, name, password)
        data.append(information)
    with open("database", "w", encoding="utf8") as f:
        data = ''.join(data)
        f.write(data)
        information = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (name, password, 0, 0, 0, 0, 1, 1, 0, 1, 1)
    with open("%s" % name, "w+", encoding="utf8") as f:
        f.write(information)
    print("successfully!")


def user_lock(name):
    if user_search(name):
        with open("database", "r", encoding="utf8") as f:
            data = [i for i in f]
            for i in data:
                m = i.split(',')
                if m[1] == name:
                    m[0] = 'locked'
                m = ','.join(m)
                data[data.index(i)] = m
            data = ''.join(data)
        with open("database", "w", encoding="utf8") as f_w:
            f_w.write(data)
        print("successfully!")


def deposit(user, amount, date):
    if is_num(amount):
        amount = float(amount)
        with open("%s" % user, "r", encoding="utf8") as f:
            data1 = [i for i in f]
            inf = data1[0].split(',')
            inf[2] = (float(inf[2]) + amount).__str__()
            data1[0] = ','.join(inf)
            record_d = '\n+,%s,%s' % (amount.__str__(), date)
            data1.append(record_d)
            data1 = ''.join(data1)
        with open("%s" % user, "w", encoding="utf8") as f_d:
            f_d.write(data1)
    else:
        print("please input right number!")


def login():
    with open('database', 'r', encoding='utf8') as f_log:
        data_log = [i for i in f_log]
    while True:
        name = input("please input your name:")
        password = input("please input your password:") + '\n'
        i = data_log[0].split(',')
        if name == i[1] and password == i[2]:
            print("login successful!")
            break
        print("your name or password is wrong!")


login()
while True:
    time = datetime.datetime.now()
    with open('database_transfer', 'r', encoding='utf8') as f_t:
        data_t = [i for i in f_t]
    if int(data_t[0]) != len(data_t):
        count = 0
        for info in data_t:
            if count:
                info = info.split(',')
                if int(data_t[0]) <= int(info[0]):
                    target = info[3]
                    money = info[2]
                    if user_search(target):
                        deposit(target, money, time)
                    else:
                        deposit(info[1], money, time)
            count += 1
        data_t[0] = len(data_t).__str__()+'\n'
        data_t = ''.join(data_t)
        with open('database_transfer', 'w', encoding='utf8') as f_tt:
            f_tt.write(data_t)
    print('1.user_add  2.user_lock  3.user_quota  ')
    choice = input('please choose service:')
    user = input('please input account name:')
    if choice == "1":
        user_add(user)
    elif choice == '2':
        user_lock(user)
    elif choice == '3':
        quota = input('please input account quota:')
        overdraft_root(user, quota)
    elif choice == 'q':
        break
    else:
        continue
