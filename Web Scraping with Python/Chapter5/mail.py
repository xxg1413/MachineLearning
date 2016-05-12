import  smtplib

from email.mime.text import  MIMEText

msg = MIMEText("This is a mail test")

msg['Subject'] = "An Email ALERT"
msg['From']="xxxxx@gmail.com"
msg['To']="xxxxx@qq.com"

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

