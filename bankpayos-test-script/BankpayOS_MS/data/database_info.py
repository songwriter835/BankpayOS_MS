#!/user/bin/env python3
# -*- coding:UTF-8
# 2023/6/28 20:11
database_info = dict(host="54.199.166.162",
                       user="root",
                       port=3306,
                       password="qwe123qwe",
                       )



def wait():
    import time
    time.sleep(1)
    print("...", end=" ")
    time.sleep(1)
    print("...", end=" ")
    time.sleep(1)
    print("...")

def wait2():
    import time
    for x in range(2):
        time.sleep(0.5)
        print(".",end="  ")
    print(".")

