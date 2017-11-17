from imaplib import IMAP4, IMAP4_SSL
import email
import datetime
import os
import time
from email.header import decode_header

def downloadmails(dir_=None):
    server = IMAP4(host='testudo.tmdcloud.com')
    server.login('vadym@testing.testudo.tmd.cloud', '35U_D0BwR6eW')
    server.select()
    result, ids = server.search(None, 'ALL')
    print("New emails with your email in TO is %d" % len(ids[0].split()))

    for id_ in ids[0].decode("utf-8").split():
        x = server.fetch(id_, '(RFC822)')
        try:
            email_p = email.message_from_bytes(x[1][0][1])
        except IndexError:
            x = 'None'

        if email_p['Date'] is not None:
            timestamp = str(time.mktime(email.utils.parsedate(email_p['Date']))).replace('.', '')
        else:
            timestamp = str(datetime.datetime.now().timestamp()).replace('.', '')

        print(email_p['Return-Path'].replace('<', '').replace('>', ''))

        # if email_p['Subject']:
        #     if decode_header(email_p['Subject'])[0][1]:
        #         subject = decode_header(email_p['Subject'])[0][0].decode()
        #     else:
        #         subject = decode_header(email_p['Subject'])[0][0]
        # else:
        #     subject = 'none'


        # # create local dir
        # dir_l = os.path.join(dir_, timestamp)
        # if not os.path.exists(dir_l):
        #     os.makedirs(dir_l)
        # # save subject
        # print('Save subject:', subject)
        # fp = open(os.path.join(dir_l, 'subject'), 'w')
        # fp.write(subject)
        # fp.close
        #
        # #           save atach files  0951036314
        # if email_p.is_multipart():
        #     atach_files = ''
        #     for part in email_p.walk():
        #
        #         # body = part.get_payload(decode=True).decode('utf-8', 'ignore')
        #         if part.get_filename():
        #             print('Save atach file: ', part.get_filename(), 'in ', dir_l)
        #             fp = open(os.path.join(dir_l, part.get_filename()), 'wb')
        #             fp.write(part.get_payload(decode=1))
        #             fp.close
        #             # save file attach
        #             atach_files += '{file}\n'.format(file=part.get_filename())
        #             fp = open(os.path.join(dir_l, 'attach'), 'w')
        #             fp.write('')
        #             fp.close
        #
        #         else:
        #             fp = open(os.path.join(dir_l, 'body'), 'wb')
        #             body = part.get_payload(decode=1)
        #             if body:
        #                 fp.write(body)
        #             fp.close
        #
        #         fp = open(os.path.join(dir_l, 'attach'), 'a')
        #         fp.write(atach_files)
        #         fp.close


        # else:
        #     print('none_multi')
        # body = email_p.get_payload()
        # fp = open(os.path.join(dir_l, 'body'), 'w')
        # fp.write(body)
        # fp.close






downloadmails(dir_='/home/vadymrud/~~~temp/emails/')
