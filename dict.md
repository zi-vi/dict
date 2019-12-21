#在线词典

 ## 建立整体的结构 （软件怎么用）

 ## 研究技术方案和确定细节

 ###   确定并发方案？
       Process多进程

 ###   什么样套接字？
       tcp 套接字

 ##  二级界面结构？

 ##  数据库设计
 ### 存什么 --》 怎么建立表 --》 建表

     1.用户信息： 用户名  密码
     2.单词 ： 单词  解释
     3.历史记录： 用户名  单词  时间

    

     user: 
     ```
     create table user (id int primary key auto_increment,name char(20) not null,passwd char(64) not null);

     ```

     历史记录（关系表）：
     ```
     create table user_words (id int primary key auto_increment,uid int,wid int,time datetime default now(),constraint `user_fk` foreign key (uid) references user(id),constraint `words_fk` foreign key (wid) references words(id));

     ```

     words 建立索引：
     `create index word_index on words(word);`

 ## 结构设计： 如何封装，几个模块，每个模块功能

     1.客户端模块
     2.服务端逻辑功能模块
     3.服务端数据处理模块 （与数据库交互）

 ## 搭建通信 （通信协议）

 ## 具体功能分析，逐个实现模块

 ### 并发通信
        1.注册
        2.客户端： 发送请求  等待结果  （失败/成功）
               R name passwd

        3.服务端： 接收请求判定请求类型
                根据请求类型调用功能函数
                (数据请求)
                将结果发送给客户端

 ### 登录   L  name  passwd

 ### 查单词  Q
         
         1.客户端  输入单词 发送请求 接收结果
         2.服务端  接收请求 查询单词 给客户端发送结果
                插入历史记录


 ##历史记录

 #cookie:

   `hasattr(obj,attr)`
   功能: 判定一个对象是否有某个属性


 #cookie

    `import hashlib`

    ##生产hash对象
   ` hash = hashlib.md5()`

    ## 对密码进行加密
    `hash.update(pwd.encode())`

    ## 提取加密后的密码
   ` pwd = hash.hexdigest()`

 #cookie
    `import getpass`

    `passwd = getpass.getpass()`
    功能:隐藏输入




 #历史记录如果查询所有（包括不存在的单词）
   插入记录： uid   word


```
查询：
select word,time from history where user_id = (select id from user where name='%s') order by time desc limit 10;

````



