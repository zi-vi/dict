def er():
    while True:
        print("二级界面")
        cmd = input(">>")
        if cmd == '1':
            print('lalal')
        elif cmd == '2':
            break

while True:
    print("一级界面")
    cmd = input(">>")
    if cmd == '1':
        er()
    elif cmd == '2':
        er()
    elif cmd == '3':
        break

