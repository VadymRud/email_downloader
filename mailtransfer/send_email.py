import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, make_msgid
from email import encoders


def send_mail(send_from, send_to, subject, text, files_=[], server='localhost', port=587, username='', password='',
              istls=True, content_id=[]):
    msg = MIMEMultipart('related')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text, 'html'))

    for f in files_:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(f, 'rb').read())
        encoders.encode_base64(part)
        # add cid def msg.add_related()
        # msg.add_related()
        if content_id:
            for cid in content_id:
                if cid.split(' 9=========9 ')[0] in f:
                    part.add_header('Content-ID', cid.split(' 9=========9 ')[1])
        part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if istls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
