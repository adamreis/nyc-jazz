from sendgrid import SendGridClient
from sendgrid import Mail
from secret_keys import SENDGRID_USER, SENDGRID_PASSWORD

# make a secure connection to SendGrid
sg = SendGridClient(SENDGRID_USER, SENDGRID_PASSWORD, secure=True)

# make a message object
message = Mail()
message.set_subject('message subject')
message.set_html('<strong>HTML message body</strong>')
message.set_text('plaintext message body')
message.set_from('from@example.com')

# add a recipient
message.add_to('Adam Reis <adamhreis@gmail.com>')

# use the Web API to send your message
print(sg.send(message))

# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib

# msg = MIMEMultipart('alternative')
# msg['Subject'] = "Hi adamhreis"
# msg['From'] = "adamhreis@gmail.com"
# msg['To'] = "adamhreis@gmail.com"
# text = '<strong>HTML message body</strong>'
# html = 'plaintext message body'

# username = 'GeoCash'
# password = "pennappscolumbia1"

# # username = SENDGRID_USER
# # password = SENDGRID_PASSWORD

# part1 = MIMEText(text, 'plain')
# part2 = MIMEText(html, 'html')

# msg.attach(part1)
# msg.attach(part2)

# s = smtplib.SMTP('smtp.sendgrid.net', 587)
# s.login(username, password)


# print(s.sendmail(from_email, recipient_email, msg.as_string()))

# s.quit()