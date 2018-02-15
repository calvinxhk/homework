#  1、使用while循环输入 1 2 3 4 5 6     8 9 10
i = 1
while i <= 10:
    if i !=7:
        print (i)
        i+=1
    else:
        i+=1#     2、求1-100的所有数的和#     2、求1-100的所有数的和

#     2、求1-100的所有数的和
sum =0
for i in range(100):
     sum+=i
print (sum)

#     3、输出 1-100 内的所有奇数
for i in range (1,101):
    if i%2==1:
        print (i)

#     4、输出 1-100 内的所有偶数
for i in range (1,101):
    if i%2==0:
        print (i)

#     5、求1-2+3-4+5 ... 99的所有数的和
sum = 0
for i in range(99):
    sum+=(-1)**(i+1) * i
print(sum)
# 模拟登陆
#     1. 用户输入帐号密码进行登陆
#     2. 用户信息保存在文件内
#     3. 用户密码输入错误三次后锁定用户
with open("date1",encoding="utf8") as f:
    book=eval(f.read())
    count = 0
    while count <=2:
        user=input("user:")
        password=input("password:")
        if user in book and password == book[user]:
            print("Successful login!")
            exit()
        else:
            count+=1
            print("user name or password is wrong!")
    while True:
        print("\ryour account is locked!"),