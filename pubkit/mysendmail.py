#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import yaml

def my_new_mail(from_address,to_address,subject,content):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    #添加邮件内容
    txt = MIMEText(content)
    msg.attach(txt)

    #添加二进制附件
    # fileName = r'e:/PyQt4.rar'
    # ctype, encoding = mimetypes.guess_type(fileName)
    # if ctype is None or encoding is not None:
    #     ctype = 'application/octet-stream'
    # maintype, subtype = ctype.split('/', 1)
    # att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)
    # att1.add_header('Content-Disposition', 'attachment', filename = fileName)
    # msg.attach(att1)

    return msg


def my_send_mail(msg):

    #发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('mail.ustc.edu.cn:25')
    smtp.login('lhrkkk@mail.ustc.edu.cn', 'starnada')
    smtp.sendmail('lhrkkk@mail.ustc.edu.cn', 'luhaorui@gmail.com', msg.as_string())
    smtp.quit()
    print '邮件发送成功'

def main():

    mail='''

from_address : 'lhrkkk@mail.ustc.edu.cn'
to_address : 'luhaorui@gmail.com'
subject : 'new subject'
content : 'new'

'''

    mail_config=yaml.load(mail)
    # mail_config['from_address'] = 'lhrkkk@mail.ustc.edu.cn'
    # mail_config['to_address'] = 'luhaorui@gmail.com'
    # mail_config['subject'] = 'new subject'
    # mail_config['content'] = 'new'

    msg=my_new_mail(mail_config['from_address'],mail_config['to_address'],mail_config['subject'],mail_config['content'])
    my_send_mail(msg)

if __name__ == '__main__':
    main()
