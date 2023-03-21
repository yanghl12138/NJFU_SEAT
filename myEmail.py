import smtplib
from email.mime.text import MIMEText

'''
管理发送邮件
'''
class myEmail:
    def __init__(self, addr:str, code:str, smtp_url:str, smtp_port:int):
        self.addr = addr
        self.code = code
        self.smtp_url = smtp_url
        self.smtp_port = smtp_port
    def sendMail(self, subject, content, To_addr, sendername=None):
        msg = MIMEText(content)
        if not sendername:
            msg["From"] = self.addr
        else:
            msg["From"] = sendername
        msg["To"] = To_addr
        msg["Subject"] = subject
        try:
            s = smtplib.SMTP_SSL(self.smtp_url, self.smtp_port)
            s.login(self.addr, self.code)
            s.sendmail(self.addr, To_addr, msg.as_string())
        except s.SMTPException as e:
            raise e
        finally:
            s.quit()

'''
InfoSender类输入填写邮件的内容、目的地，转交myEmail类处理
'''
class InfoSender:
    def __init__(self, email:myEmail, sendername:str):
        self.email = email
        self.sendername = sendername
        with open("./mailprompt/succ.txt", encoding="utf8") as f:
            self.obj_succ = f.read()
        with open("./mailprompt/fail.txt", encoding="utf8") as f:
            self.obj_fail = f.read()
    
    def seadOKmail(self, seat:str, start:str, end:str, To_addr:str):
        msg = self.obj_succ.format(seat=seat, start=start, end=end)
        self.email.sendMail("抢座成功！", msg, To_addr=To_addr, sendername=self.sendername)
    
    def seadFailmail(self, To_addr:str):
        self.email.sendMail("抢座失败！", self.obj_fail, To_addr=To_addr, sendername=self.sendername)