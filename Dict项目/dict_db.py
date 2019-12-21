"""
dict 数据库处理功能
给server提供所有数据支持
"""
import pymysql
import hashlib

# 加密函数
def change_passwd(passwd):
    # 生产hash对象
    hash = hashlib.md5("*#06#".encode())  # 加盐生产对象
    # 对密码进行加密
    hash.update(passwd.encode())
    # 提取加密后的密码
    return hash.hexdigest()

class Database:
    def __init__(self,host='localhost',
                 port = 3306,
                 user=None,
                 passwd=None,
                 database=None,
                 charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db() # 链接数据库

    def connect_db(self):
        self.db=pymysql.connect(host=self.host,
                              port=self.port,
                              user=self.user,
                              passwd=self.passwd,
                              database=self.database,
                              charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        # 如果有 cur这个属性则执行关闭
        if hasattr(self,'cur'):
            self.cur.close()
        if hasattr(self,'db'):
            self.db.close()

    # 处理注册
    def register(self,name,passwd):
        # 判断名是否重复
        sql = "select name from user where name='%s'" % name
        self.cur.execute(sql)
        result = self.cur.fetchone()  # 查不到返回None
        if result:
            return False
        try:
            # 密码转换
            passwd = change_passwd(passwd)
            sql = "insert into user (name,passwd) values (%s,%s);"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 处理登录
    def login(self,name,passwd):
        passwd = change_passwd(passwd)
        sql = "select name from user " \
              "where name=%s and passwd=%s;"
        self.cur.execute(sql, [name, passwd])
        result = self.cur.fetchone()  # 如果查到说明用户存在
        if result:
            return True
        else:
            return False

    # 查询单词
    def query(self,word):
        sql = "select mean from words where word='%s'"%word
        self.cur.execute(sql)
        r = self.cur.fetchone() # (xxxxx) / None
        if r:
            return r[0]

    # 插入历史
    def insert_history(self,name,word):
        sql = "select id from user where name='%s'"%name
        self.cur.execute(sql)
        uid = self.cur.fetchone()[0]

        sql = "select id from words where word='%s'"%word
        self.cur.execute(sql)
        wid = self.cur.fetchone()[0]

        sql = "insert into user_words (uid,wid) values (%s,%s)"
        try:
            self.cur.execute(sql,[uid,wid])
            self.db.commit()
        except:
            self.db.rollback()

    # 查询历史记录
    def history(self,name):
        sql = "select word,h.time from words inner join (select wid,time from user_words where uid=(select id from user where name=%s) order by time desc limit 10) as h on words.id=h.wid;"
        self.cur.execute(sql,[name])
        # ((word,time),())
        return self.cur.fetchall()




if __name__ == '__main__':
    my_db = Database(user='root',passwd='123456',database='stu')
    my_db.close()













