

def select(self):
    with open("%s" % self[3], "r", encoding="utf8") as f:
        content = [i for i in f]
    number = int(kind.index(self[5]))
    count = 0
    if self[6] == ">":
        for i in content:
            i = i.split(",")
            if int(i[number]) > int(self[7]):
                select_print(self, i)
                count += 1
    elif self[6] == "<":
        for i in content:
            i = i.split(",")
            if int(i[number]) < int(self[7]):
                select_print(self, i)
                count += 1
    elif self[6] == "=":
        for i in content:
            i = i.split(",")
            if i[number] == self[7]:
                select_print(self, i)
                count += 1
    elif self[6] == "like":
        print(self[7])
        for i in content:
            i = i.split(",")
            if self[7] in i[number]:
                select_print(self, i)
                count += 1
    print("There are %s records." % count)


def select_print(self, i):
    if self[1] == "*":
        print(','.join(i))
    else:
        order_content = self[1].split(',')
        for m in order_content:
            if m in kind:
                print_index = kind.index(m)
                print(i[print_index])


def staff_create():
    with open("staff_table", "r+", encoding='utf8') as f:
        content = [i for i in f]
        staff_id = int(content[-1].split(',')[0])+1
        name = input("please input name:")
        age = input("please input age:")
        phone = input("please input phone number:")
        dapt = input("please input department:")
        enroll_date = input("please input enroll_date(year-month-day):")
        record = "%s,%s,%s,%s,%s,%s" % (staff_id, name, age, phone, dapt, enroll_date)
        make_sure = input("%s,enter y to go on :" % record)
        if make_sure == "y":
            f.write(record+"\n")
            print("create successfully!")
            return True


def staff_del(self):
    with open("staff_table", "r+", encoding="utf8") as f:
        content = [i for i in f]
        content_new = []
        for line in content:
            line = line.split(",")
            if self == line[0]:
                line = ','.join(line)
                answer = input("%s are you sure to delete?y/n" % line)
                if answer == "y":
                    print('delete successfully!')
                    continue
            line = ','.join(line)
            content_new.append(line)
        content_new = ''.join(content_new)
        f.seek(0)
        f.truncate(0)
        f.write(content_new)
        return True


def staff_update(self):
    with open("%s" % self[1], "r+", encoding="utf8") as f:
        content = [i for i in f]
    number_a = int(kind.index(self[8]))
    f.seek(0)
    for i in content:
        i = i.split(",")
        if i[number_a] == self[10]:
            i[number_a] = self[5]
        i = ','.join(i)
        f.write(i)
    print("update successfully!")
    return True

kind = ("id", "name", "age", "phone", 'dept', 'enroll_date')
while True:
    order = input('''please input your order: 1.search   2.create  3.delete  4.update  5.help ''')
    if order == "1":
        order = input("please input your search order:").split()
        if order[0] == "select" and order[2] == "from" and order[4] == "where" and order.__len__() == 8:
            select(order)
    elif order == "2":
        staff_create()
    elif order == "3":
        id_d = input("please input id:")
        staff_del(id_d)
    elif order == "4":
        order = input("please input your  update order:").split()
        if order[0] == "UPDATE" and order[2] == "SET" and order[6] == "WHERE" and order.__len__() == 11:
            staff_update(order)
    elif order == "q":
        break
    elif order == "5":
        print('''
        search grammar:  1.select name,age from staff_table where age > 22
　　                     2.select * from staff_table where dept = IT
                         3.select  * from staff_table where enroll_date like 2013
        update grammar: UPDATE staff_table SET dept = Market WHERE where dept = IT
        ''')
    else:
        print("wrong order!")