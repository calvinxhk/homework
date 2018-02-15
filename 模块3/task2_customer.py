import smtplib
import email.mime.multipart
import email.mime.text
import datetime


def is_num(self):
    try:
        float(self)
        return True
    except ValueError:
        pass


def deposit(data1, inf, user, amount, date):
    if is_num(amount):
        amount = float(amount)
        inf[2] = (float(inf[2]) + amount).__str__()
        data1[0] = ','.join(inf)
        record_d = '\n+,%s,%s' % (amount.__str__(), date)
        data1.append(record_d)
        data1 = ''.join(data1)
        with open("%s" % user, "w", encoding="utf8") as f_d:
            f_d.write(data1)
        print('successfully!')
    else:
        print("please input right number!")


def withdrawal(data1, inf, user, amount, date):
    if is_num(amount):
        amount = float(amount)
        if amount <= float(inf[2]) + float(inf[3]):
            if amount <= float(inf[2]):
                inf[2] = (float(inf[2]) - amount).__str__()
            else:
                answer = input("your don not have enough money,do you want to overdraft? y/n")
                if answer == 'y':
                    inf[3] = (float(inf[2]) + float(inf[3]) - amount).__str__()
                    inf[8] = (float(inf[8]) + amount - float(inf[2])).__str__()
                    inf[2] = '0'
            data1[0] = ','.join(inf)
            record_w = '\n-,%s,%s' % (amount.__str__(), date)
            data1.append(record_w)
            data1 = ''.join(data1)
            with open("%s" % user, "w", encoding="utf8") as f_with:
                f_with.write(data1)
                return True
        else:
            print("you don not have enough money!")
    else:
        print("please input right number!")


def overdraft_user(data1, inf, user, amount):
    if is_num(amount):
        amount = float(amount)
        if amount > float(inf[5]):
            print('you don not have enough quota!')
        else:
            if amount <= float(inf[3]):
                inf[3] = amount.__str__()
            inf[4] = amount.__str__()
            data1[0] = ','.join(inf)
            data1 = ''.join(data1)
            with open("%s" % user, "w", encoding="utf8") as f_o:
                f_o.write(data1)
                return True
    else:
        print("please input right number!")


def send_bill(bill):
    user = 'xinghuaikang2'
    pwd = 'xhk2623304075'
    server = 'smtp.163.com'
    port = '25'
    txt = email.mime.text.MIMEText(bill, _charset='utf-8')
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = 'bill'
    msg['From'] = 'xinghuaikang2@163.com'
    msg['To'] = 'xinghuaikang2@163.com'
    msg.attach(txt)
    smtp = smtplib.SMTP()
    smtp.connect(server, port)
    smtp.login(user, pwd)
    smtp.sendmail(msg['from'], msg['to'], msg.as_string())
    smtp.quit()
    print('email has send out !')
    return True


def regular_bill(data1, inf, user, day):
    if is_num(day):
        inf[6] = int(day).__str__()
        data1[0] = ','.join(inf)
        data1 = ''.join(data1)
        with open("%s" % user, "w", encoding="utf8") as f_rb:
            f_rb.write(data1)
        print('set successfully!')
        return True
    else:
        print("please input right number!")


def regular_pay(data1, inf, user, day):
    if is_num(day):
        inf[7] = int(day).__str__()
        data1[0] = ','.join(inf)
        data1 = ''.join(data1)

        with open("%s" % user, "w", encoding="utf8") as f_rp:
            f_rp.write(data1)
        print('set successfully!')
        return True
    else:
        print("please input right number!")


def transfer(user, amount, target, t_time):
    if is_num(amount):
        with open('database_transfer', 'r+', encoding='utf8') as f_t:
            data_t = [i for i in f_t]
            id_tr = (len(data_t)).__str__()
            inf = '\n%s,%s,%s,%s,%s,' % (id_tr, user, amount, target, t_time)
            f_t.write(inf)
    else:
        print('please input right number!')


def login():
    with open('database', 'r', encoding='utf8') as f_log:
        data_log = [i for i in f_log]

    while True:
        user = input("please input your name:")
        password = input("please input your password:") + '\n'
        for i in data_log:
            i = i.split(',')
            if i[1] == user and i[2] == password:
                if i[0] != 'locked':
                    print("login successful!")
                    return user
                if i[0] == 'locked':
                    print("your account is locked!")
                    break
        print("your name or password is wrong!")

name = login()
# information :
# 1.user                2.password              3.balance              4.Overdraft limit
# 5.max overdraft       6.bank max overdraft    7.The date of entry    8.Repayment date
# 9.Repayment amount    10.last bill month      11.last repayment month

while True:
    with open("%s" % name, "r+", encoding="utf8") as f:
        data = [i for i in f]
        information = data[0].split(",")
        time = datetime.datetime.now()
        if (int(information[9])) != time.month:
            if information[6] == time.day.__str__():
                count = 0
                data_mail = data
                mail = []
                for record in data_mail:
                    if count:
                        i = record.split(",")[2].split(' ')[0].split('-')[2]
                        if i == information[6]:
                            mail.append(record)
                    else:
                        mail.append('%s,%s' % (name, information[8]))
                    count += 1
                mail = ''.join(mail)
                print(mail)
                send_bill(mail)
                information[9] = time.month.__str__()
                data_mail = ','.join(information)
                data_mail = ''.join(data)
                f.seek(0)
                f.truncate(0)
                f.write(data_mail)
        if (int(information[10])) != time.month:
            if information[7] == time.day.__str__():
                data_mail = data
                bill_money = information[8]
                if withdrawal(data, information, name, bill_money, time):
                    information[3] = information[4]
                    information[8] = '0'
                information[10] = time.month.__str__() + '\n'
                data_mail[0] = ','.join(information)
                data_mail = ''.join(data_mail)
                f.seek(0)
                f.truncate(0)
                f.write(data_mail)
    print('''1.deposit  2.withdraw  3.time job  4.overdraft 5.transfer ''')
    choice = input("please choose service number:")
    if choice == "1":
        money = input('how much money do you want to deposit?:')
        deposit(data, information, name, money, time,)
    elif choice == "2":
        money = input('how much money do you want to withdraw?:')
        withdrawal(data, information, name, money, time)
    elif choice == '3':
        print(''' 1.regular pay  2.regular print bill ''')
        choice_1 = input("please choose time job:")
        if choice_1 == '1':
            choice_2 = input("please choose the day to pay the bill")
            regular_pay(data, information, name, choice_2)
        if choice_1 == '2':
            choice_2 = input("please choose the day to send the bill:")
            regular_bill(data, information, name, choice_2)
    elif choice == '4':
        money = input("how much quota do you want to set?:")
        overdraft_user(data, information, name, money)
    elif choice == '5':
        transfer_account = input('please input target account:')
        transfer_money = input('please input money you want to transfer:')
        transfer(name, transfer_money, transfer_account, time)
        withdrawal(data, information, name, transfer_money, time)
    elif choice == 'q':
        break
    else:
        continue




