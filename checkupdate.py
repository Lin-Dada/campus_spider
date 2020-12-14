#!coding:utf-8
import requests
import re
import time
import datetime
import toSign
from SendEmail import send
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def check():
    url = 'http://jwxk.ucas.ac.cn/subject/humanityLecture#'
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'max-age=0',
              'Connection': 'keep-alive',
              'Host': 'jwxk.ucas.ac.cn',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
              'Cookie' : ''
              }
    old_lect = []
    new_lect = []
    start = True
    while(True):
        #header['Host'] = 'lindada.com.cn'
        #url = 'http://lindada.com.cn/test'
        with open('/root/web/profile/cookie.txt', 'r') as f:
            header['Cookie'] = f.read()
        texts = requests.get(url, headers=header).text
        list=re.findall(r'<tbody>(.*?)</tbody>',texts,re.I|re.M|re.S)
        try:
            item = list[0].replace("<td>", "").replace("</td>", "").replace("<br/>", "")
            with open('/root/web/profile/statrecord', 'w+') as f:
            #with open('statrecord', 'w+') as f:
                nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                f.write('正常:'+nowtime)
            if start == True:
                start = False
                send("【代码运行提醒】正常", "稳得一批！")
                #print("【代码运行提醒】正常")
        except IndexError:
            with open('/root/web/profile/statrecord', 'w+') as f:
            #with open('statrecord', 'w+') as f:
                nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                f.write('错误:' + nowtime)
                send("【代码运行提醒】错误","Cookie可能已失效！")
            break
        res = r'<tr>(.*?)</tr>'
        texts = re.findall(res, item, re.S|re.M)
        for i in range(len(texts)):
            toSignMsg = re.findall(r'toSign\((.*?)\)">', texts[i])
            if len(toSignMsg) == 0:
                toSignMsg = [""]
                whatday = ""
            else:
                dayTime = toSignMsg[0].split(",")[-1].replace("'","")[0:16]+":00"
                whatday = datetime.datetime.strptime(dayTime, '%Y-%m-%d %H:%M:%S').strftime("%w") #星期几，0(日)到6
                whatday = whatday.replace("0"," 星期日").replace("1"," 星期一 ").replace("2"," 星期二 ").replace("3"," 星期三") \
                    .replace("4", " 星期四").replace("5"," 星期五").replace("6"," 星期六")
            toSignMsg="///"+toSignMsg[0]
            texts[i] = re.sub(r'<a(.*?)</a>',"",texts[i])
            texts[i] = re.sub(r'\r\n\t\t\t\t\t', "", texts[i])
            texts[i] = texts[i].replace("&nbsp;", "")
            texts[i] = texts[i].strip()
            texts[i] = texts[i].split()
            str = whatday
            for item in texts[i]:
                str += ", "+item
            str += toSignMsg
            texts[i] = str[1:]
            #print texts[i]
        old_lect = new_lect
        #if len(old_lect) == 0:
        new_lect = texts
        # else:
        #     temp = []
        #     temp.append(old_lect[3])
        #     temp.append(old_lect[4])
        #     temp += old_lect
        #     new_lect = temp

        if len(old_lect)>=1:#不是第一次運行
            if old_lect[0] != new_lect[0] or old_lect[1] != new_lect[1] or old_lect[2] != new_lect[2]:
                new = "新的人文讲座课程 "

                for item in new_lect:
                    if item in old_lect:
                        continue
                    else:
                        stat = toSign.autosign(item)
                        stat = "\n<br>" + "自动抢课结果：" + stat + "<br>\n"
                        new += "<br>\n" + item + stat
                if new == "新的人文讲座课程 ":
                    new = "服务器删除了部分课程，但没有课程更新"
                send("【人文讲座课程】有新的课程可选",new)
                with open('/root/web/profile/lectrecord', 'a+') as f:
                #with open('lectrecord', 'a+') as f:
                    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    f.write(nowtime+"<br>\n"+new)
            else:
                print "暂无课程更新"

        lasttime = ""
        for item in new_lect:
            item = item.split("///")
            if item[1]!="":
                itemright = item[1]
                itemright = itemright.replace("'","").split(',')
                str = '&nbsp;&nbsp;<a href = "/toSign?lectureId=%s&communicationAddress=%s\">报名</a>'%(itemright[0],itemright[1])
            else:
                str = ""
            lasttime += "<br>" + item[0]+ str
        nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        with open('/root/web/profile/lasttime', 'w+') as f:
            f.write(nowtime+"<br>\n"+lasttime)


        time.sleep(60)


if __name__ == '__main__':
    check()



