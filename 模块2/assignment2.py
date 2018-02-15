
# 作业二
# 三级菜单：
#     1. 运行程序输出第一级菜单
#     2. 选择一级菜单某项，输出二级菜单，同理输出三级菜单
#     3. 返回上一级菜单和顶部菜单
#     4. 菜单数据保存在文件中
with open("date2",encoding="utf8") as f:
    menu=eval(f.read())
    last_layer=[menu]
    current_layer=menu

    while True:
        for key in current_layer:
            print(key)
        choice=input(">>:")
        if len(choice) == 0:continue
        if choice== "q":break
        if choice in current_layer:
            last_layer.append(current_layer)
            current_layer=current_layer[choice]
        if choice=="b":
            if last_layer:
                current_layer=last_layer[-1]
                last_layer.pop()
            continue







