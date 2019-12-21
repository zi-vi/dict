import hashlib
import getpass

# pwd = input(">>")
pwd = getpass.getpass()

# 生产hash对象
# hash = hashlib.md5()
hash = hashlib.md5("*#06#".encode())  # 加盐生产对象

# 对密码进行加密
hash.update(pwd.encode())

# 提取加密后的密码
pwd = hash.hexdigest()

print(pwd)