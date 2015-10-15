#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders



def my_new_mail(from_address,to_address,subject,content,file=None,filename=None):
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    #添加邮件内容
    txt = MIMEText(content)
    msg.attach(txt)

    if file:
        part=MIMEApplication(
            file.read(),
            # Content_Disposition='attachment; filename="%s"' % filename
        )
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
        msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect('mail.ustc.edu.cn:25')
    smtp.login('lhrkkk@mail.ustc.edu.cn', 'starnada')
    smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.quit()
    print '邮件发送成功'



# def my_send_mail(msg):
#
#     #发送邮件
#     # smtp = smtplib.SMTP("127.0.0.1")
#     smtp = smtplib.SMTP()
#     smtp.connect('mail.ustc.edu.cn:25')
#     smtp.login('lhrkkk@mail.ustc.edu.cn', 'starnada')
#     smtp.sendmail('lhrkkk@mail.ustc.edu.cn', 'luhaorui@gmail.com', msg.as_string())
#     smtp.quit()
#     print '邮件发送成功'

def main():

    mail='''

from_address : 'lhrkkk@mail.ustc.edu.cn'
to_address : 'luhaorui@gmail.com'
subject : 'new subject'
content : 'new'

'''

    mail_config=yaml.loads(mail)
    # mail_config['from_address'] = 'lhrkkk@mail.ustc.edu.cn'
    # mail_config['to_address'] = 'luhaorui@gmail.com'
    # mail_config['subject'] = 'new subject'
    # mail_config['content'] = 'new'

    msg=my_new_mail(mail_config['from_address'],mail_config['to_address'],mail_config['subject'],mail_config['content'])
    my_send_mail(msg)

if __name__ == '__main__':
    main()
