import schedule
import time
import psutil
import smtplib
from email.mime.text import MIMEText

# Monitoring items
app_name = "node name"

# Email configuration
mail_host = "smtp-relay.brevo.com"
mail_port = 587
mail_user = "mail" 
mail_pass = "password"
mail_receivers = ["incoming mail"]


def check_app():
  for p in psutil.process_iter():
    if p.name() == app_name:  
      return True
  return False


def send_mail(subject, content):

  msg = MIMEText(content) 
  msg['Subject'] = subject
  msg['From'] = mail_user
  
  server = smtplib.SMTP(mail_host, mail_port)
  server.ehlo()
  server.starttls()
  server.login(mail_user, mail_pass)

  for receiver in mail_receivers:  
    server.sendmail(mail_user, receiver, msg.as_string())

  server.quit()

# scheduled tasks  
def job():
  if not check_app():
    send_mail("node Down", f"App {app_name} is down!")

  else:
    print("App is running")

schedule.every(1).minutes.do(job)

while True:
  schedule.run_pending()
  time.sleep(1)
