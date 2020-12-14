#!coding:utf-8
import smtplib
import email
from email.mime.text import MIMEText    #定义邮件内容
from email.header import Header         #定义邮件标题


def send(title,content):
    # 发送邮箱服务器
    smtpserver = 'smtp.163.com'

    # 发送邮箱用户名密码
    user = '' #你自己的邮箱
    password = ''#授权码

    # 发送和接收邮箱
    sender = '' #你自己的邮箱
    receive = '' #接受者，可以是你自己的邮箱

    # 发送邮件主题和内容
    subject = title
    content = content
    # HTML邮件正文
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receive

    # SSL协议端口号要使用465
    smtp = smtplib.SMTP_SSL(smtpserver, 465)

    # HELO 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 服务器返回结果确认
    smtp.ehlo(smtpserver)
    # 登录邮箱服务器用户名和密码
    smtp.login(user, password)

    print("开始发送邮件...")
    smtp.sendmail(sender, receive, msg.as_string())
    smtp.quit()
    print("邮件发送完成！")
