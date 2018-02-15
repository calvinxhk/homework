# 购物车
#     1. 商品信息- 数量、单价、名称
#     2. 用户信息- 帐号、密码、余额
#     3. 用户可充值
#     4. 购物历史信息
#     5. 允许用户多次购买，每次可购买多件
#     6. 余额不足时进行提醒
#     7. 用户退出时 ，输出本次购物信息
#     8. 用户下次登陆时可查看购物历史
#     9. 商品列表分级显示

with open("date3customer", encoding="utf8") as c:
    customer = eval(c.read())
    count = 0
    while count <= 2:
        user = input("user:")
        password = input("password:")
        if user in customer and password == customer[user]:
            print("Successful login!")
            break
        count += 1
        print("user name or password is wrong!")
    while count == 3:
        print("\ryour account is locked!"),
with open("date3money", "r+", encoding="utf8") as m:
    with open("date3history", "r+", encoding="utf8") as h:
        with open("date3goods", "r", encoding="utf8") as g:
            money = eval(m.read())
            history = eval(h.read())
            goods = eval(g.read())
            while True:
                print("1.show balance\n2.show history\n3.shopping!\n4.recharge")
                choice1 = input("choose the number to move on or enter 'q' to quit:")
                if len(choice1) == 0:
                    continue
                if choice1 == "q":
                    break
                if choice1 == "1":
                    print(money[user])
                if choice1 == "2":
                    print(history[user])
                if choice1 == "3":
                    basket_cost = 0
                    basket = []
                    last_layer = [goods]
                    current_layer = goods
                    while basket_cost <= float(money[user]):
                        for key in current_layer:
                            print(key)
                        choice2 = input("please choose your commodity(enter b to back,q to pay):")
                        if len(choice2) == 0:
                            continue
                        if choice2 in current_layer:
                            if str(current_layer[choice2]).isdigit():
                                quality = input("how much?:")
                                if str(quality).isdigit():
                                    basket_cost += float(current_layer[choice2])*float(quality)
                                    basket.append(choice2)
                                    basket.append(quality)
                                else:
                                    print("please enter the true number!")
                            else:
                                last_layer.append(current_layer)
                                current_layer = current_layer[choice2]
                        if choice2 == "b":
                            if last_layer:
                                current_layer = last_layer[-1]
                                last_layer.pop()
                            continue
                        if choice2 == "q":
                            money[user] = float(money[user])-float(basket_cost)
                            m.truncate(0)
                            m.seek(0)
                            m.write(str(money))
                            print("shopping list:\r\n")
                            list1 = ""
                            for i in basket:
                                list1 += str(i)+"\r\n"
                                print(i)
                            history[user] = history[user]+list1
                            h.truncate(0)
                            h.seek(0)
                            h.write(str(history))
                            break
                        else:
                            print("please choose the given commodity! ")

                    print('you do not have enough money,please charge!')
                if choice1 == "4":
                    recharge = input("how much money do you want to recharge?:")
                    if str(recharge).isdigit():
                        money[user] = float(recharge)+float(money[user])
                        m.truncate(0)
                        m.seek(0)
                        m.write(str(money))
                        m.flush()
                    print("please enter right nuber!")
                else:
                    print("please choose the given number!")