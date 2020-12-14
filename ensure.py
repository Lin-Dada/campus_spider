#coding:utf-8
from SendEmail import send
import time

memorytimeStamp = 0
while True:
    with open('/root/web/profile/statrecord', 'r') as f:
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        readtime = f.read().replace("正常:", "").replace("错误:", "")
        nowtimeArray = time.strptime(nowtime, "%Y-%m-%d %H:%M:%S")
        readtimeArray = time.strptime(readtime, "%Y-%m-%d %H:%M:%S")
        nowtimeStamp = int(time.mktime(nowtimeArray))
        readtimeStamp = int(time.mktime(readtimeArray))
        if readtimeStamp != memorytimeStamp and nowtimeStamp-readtimeStamp>120:
            print nowtimeStamp, readtimeStamp  # 1381419600
            memorytimeStamp = readtimeStamp
            send("【脚本已经停止运行】", "脚本已经停止运行，可能有课程更新，请登录查看！")
    time.sleep(60)