import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
def send_mail(patient_name, date, time, name):
    sender = 'fakeperson211@gmail.com'
    receivers = 'vegeta.pasari@gmail.com'

    code = name
    message = MIMEMultipart()
    message['Subject'] = 'Report code ' + code
    message['From'] = sender
    message['To'] = receivers
    html = 'Report for the patient ' + patient_name + ", generated on " + date + " at " + time
    body = MIMEText(html, 'html')
    message.attach(body)
    file = MIMEApplication(open('./Reports/' + code, "rb").read())
    file.add_header('Content-Disposition', 'attachment', filename=code)
    message.attach(file)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender, 'fakeperson')
    server.sendmail(sender, receivers, message.as_string().encode('utf-8'))
    server.quit()

