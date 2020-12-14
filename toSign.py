#!coding:utf-8
import requests
import datetime

def tosign(lectureId,communicationAddress):
    url = 'http://jwxk.ucas.ac.cn/subject/toSign'
    header = {
    'Host': 'jwxk.ucas.ac.cn',
    'Connection': 'keep-alive',
    'Content-Length': '62',
    'Accept': '*/*',
    'Origin': 'http://jwxk.ucas.ac.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://jwxk.ucas.ac.cn/subject/humanityLecture',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': ''
    }

    with open('/root/web/profile/cookie.txt', 'r') as f:
        header['Cookie'] = f.read()
    data = {"lectureId": lectureId, "communicationAddress": communicationAddress}
    #s = requests.Session()

    content = requests.post(url, data=data, headers=header)
    data = content.content
    if data == "success":
        return("报名成功！")
    elif data == "exits":
        return("该讲座已经报名！")
    elif data == "conflict":
        return("该讲座与已选课程时间有冲突，无法报名！")
    elif (data == "fail"):
        return("有爽约记录，两周内无法报名！")
    elif (data == "countFail"):
        return("讲座地点容纳人数已满，无法预约！")
    else:
        return data

def autosign(lecture):
    item = lecture.split("///")
    if item[1] != "":
        itemright = item[1]
        itemright = itemright.replace("'", "").split(',')
        if "预约" in itemright[1]:
            return(itemright[1])
        daytime = itemright[1]
        daytime = daytime[0:16] + ":00"
        whatday = datetime.datetime.strptime(daytime, '%Y-%m-%d %H:%M:%S').strftime("%w")  # 星期几，0(日)到6
        if whatday == '1' or whatday == '3' or whatday == '5' or whatday == '2':
            return tosign(itemright[0], itemright[1])
        else:
            return("不是周一、周三、周二、周五的课，自动抢课关闭")