from imaplib import IMAP4, IMAP4_SSL

import os, email
from email.header import decode_header


server = IMAP4(host='testudo.tmdcloud.com')
server.login('vadym@testing.testudo.tmd.cloud', '35U_D0BwR6eW')
result, ids = server.select()
result, ids = server.search(None, 'ALL')
print("New emails with your email in TO is %d" % len(ids[0].split()))

for id_ in ids[0].decode("utf-8").split():
    try:
        print(id_)
        x = server.fetch(id_, '(RFC822)')
        # y = base64.b64decode(x)
        email_p = email.message_from_bytes(x[1][0][1])
        if email_p['Subject']:

            if decode_header(email_p['Subject'])[0][1]:
                subject = decode_header(email_p['Subject'])[0][0].decode()
            else:
                subject = decode_header(email_p['Subject'])[0][0]
        else:
            subject = 'none'
        print(subject)
        x_mail_list = email_p['X-Mailing-List']

        payload = email_p.get_payload(decode=True)
        bi = email_p.is_multipart()
        walk = email_p.walk()
        body = ''
        savedir = 'tmp'
        if email_p.is_multipart():
            for part in email_p.walk():

                if part.get_filename():
                    if not os.path.exists(savedir):
                        os.makedirs(savedir)
                    print(part.get_filename())
                    print(part.get_payload(decode=1))
                    fp = open(os.path.join(savedir, part.get_filename()), 'wb')
                    fp.write(part.get_payload(decode=1))
                    fp.close
                #print(part.get_content_type())
                if part.get_content_type() == "text/plain":

                    body = part.get_payload(decode=True)

                    # try:
                    #     print(body.decode('utf-8', 'ignore'))
                    # except TypeError:
                    #     print(body)


                elif part.get_content_type() == "text/html":
                    continue


        #print(payload)
    except IndexError:
        x = 'None'

# from imap_tools import MailBox
# mailbox = MailBox('testudo.tmdcloud.com')
# mailbox.login('vadym@testing.testudo.tmd.cloud', '35U_D0BwR6eW')
#
# r = mailbox.fetch()
#
# for message in mailbox.fetch():
#     print(message.id)
#     message.uid
#     message.subject
#     message.from_
#     message.to
#     message.date
#     message.text
#     message.html
#     message.flags
#     for filename, payload in message.get_attachments():
#         filename, payload
#

