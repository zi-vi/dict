"""
dict 客户端
功能： 根据用户输入，发送请求，得到结果，展示结果
"""
from socket import *
import sys
from getpass import getpass

# 服务器地址
ADDR = ('127.0.0.1',8888)

# 几乎所有函数都要使用s --》全局变量
s = socket()
try:
    s.connect(ADDR)
except:
    sys.exit()

# 查单词
def do_query(name):
    while True:
        word = input("单词:")
        if word == '##':
            break
        msg = "Q %s %s"%(name,word)
        s.send(msg.encode())
        # 接收结果
        data = s.recv(2048).decode()
        print(data)

# 历史记录 （最近10条）
def do_history(name):
    msg = "H "+name
    s.send(msg.encode())
    data = s.recv(128).decode() # 反馈
    if data == 'OK':
        # 不确定接收次数
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("您还没有查询记录")


def login(name):
    while True:
        print("""
        ==============Query==============
         1. 查单词   2. 历史记录    3. 注销
        =================================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确选项")

# 处理注册
def do_register():
    while True:
        name = input("User:")
        passwd = getpass()
        passwd_ = getpass("Again:")
        if passwd != passwd_:
            print("两次密码不一致!")
            continue
        if (' ' in name) or (' ' in passwd):
            print("用户名密码请不要加入空格")
            continue

        msg = "R %s %s"%(name,passwd)
        s.send(msg.encode()) # 发送请求
        data = s.recv(128).decode() # 收到结果
        if data == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return

# 处理登录
def do_login():
    name = input("User:")
    passwd = getpass()
    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())  # 发送请求
    data = s.recv(128).decode()  # 收到结果
    if data == 'OK':
        print("登录成功")
        login(name)
    else:
        print("登录失败")

# 程序启动函数
def main():
    while True:
        print("""
        ============Welcome============
         1. 注册    2. 登录     3. 退出
        ===============================
        """)
        cmd = input("输入选项：")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")

if __name__ == '__main__':
    main()