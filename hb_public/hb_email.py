from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def formatHtmlMsg(msg, title=""):
    htmlHead = "<html><head><title>" + title + "</title></head><body>"
    htmlEnd = "</body></html>"
    html_msg = htmlHead + msg + htmlEnd
    return html_msg


def sendHtmlEmail(email_title, email_msg, to_addr,
                  from_name="python_server", from_addr="hbpythonserver@163.com",
                  password="hb0424", smtp_server="smtp.163.com", smtp_port=25):
    html_email_msg = formatHtmlMsg(email_msg, email_title)
    msg = MIMEText(html_email_msg, 'html', 'utf-8')

    msg['From'] = format_addr(from_name + "<" + from_addr + ">")
    msg['To'] = format_addr(to_addr)
    msg['Subject'] = Header(email_title, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


sendHtmlEmail("testPythonEmail", "testPythonEmail", "540050860@qq.com")
