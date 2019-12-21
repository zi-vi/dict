"""
dict  服务端
功能 ： 业务逻辑
模型 ： 多进程tcp并发
"""
from socket import *
from multiprocessing import Process
import sys,signal,time
from dict_db import Database

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
# 数据库链接对象
db = Database(user='root',passwd='123456',database='dict')

# 处理注册
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')

# 处理登录
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')


# 查询单词
def do_query(connfd,name,word):
    mean = db.query(word) # 负责查询单词
    # 查不到返回一个空
    if mean:
        msg = "%s : %s"%(word,mean)
        connfd.send(msg.encode())
        db.insert_history(name, word)  # 插入历史记录
    else:
        connfd.send("没有找到该单词".encode())


# 历史记录
def do_history(connfd,name):
    r = db.history(name) # ((word,time),())
    if not r:
        connfd.send(b"FAIL")
        return
    connfd.send(b'OK')
    for word,tm in r:
        msg = "%s   %-16s   %s"%(name,word,tm)
        time.sleep(0.1)
        connfd.send(msg.encode())
    time.sleep(0.1)
    connfd.send(b'##')


# 接收请求，调用具体功能函数处理
def request(connfd):
    db.create_cursor()
    while True:
        data = connfd.recv(1024).decode()
        tmp = data.split(' ')
        if not data or tmp[0] == 'E':
            return
        elif tmp[0] == 'R':
            # R name passwd
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # L name passwd
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            # Q name word
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # H name
            do_history(connfd,tmp[1])


def main():
    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print("Listen the port 8888...")
    # 循环接收客户端链接
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            db.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #  创建进程处理
        p = Process(target=request, args=(c,))
        p.daemon = True  # 父程退出其他线程也退出
        p.start()

if __name__ == '__main__':
    main()