from imaplib import IMAP4, IMAP4_SSL
import poplib
import email
import humanfriendly
import os
import time
from email.header import decode_header
import datetime
from send_email import send_mail
from os import listdir
from os.path import isfile, join, isdir
from send_email import send_mail


class EmailLib:
    def __init__(self, hostname='some.hostname.com', ssl=True, port=None, email_='some_email@some.hostname.com',
                 password='some_password'):
        self.server = self.server_connect(host=hostname, port=None, ssl=None)

        self.email_ = email_
        self.password = password
        self.server.login(self.email_, self.password)
        self.server.select()

    def server_connect(self, host='localhost', port=None, ssl=None):
        if ssl and port:
            server = IMAP4_SSL(host=host, port=port)
        elif ssl and port is None:
            server = IMAP4_SSL(host=host)
        elif ssl is None and port is None:
            server = IMAP4(host=host)

        else:
            server = IMAP4(host=host, port=port)
        return server

    def checksize(self):
        result, ids = self.server.search(None, 'ALL')
        #print('New emails with your email in TO is %d' % len(ids[0].split()))
        size = 0
        for id_ in ids[0].decode('utf-8').split():
            x = self.server.fetch(id_, '(RFC822.SIZE)')
            size += int(x[1][0].split()[2].decode().split(')')[0])
        return humanfriendly.format_size(size)

# ___ download mails   _________

    def downloadmails(self, dir_='/home/user/dl_dir'):
        # ___ download mails   _________
        result, ids = self.server.search(None, 'ALL')
        print('New emails with your email in TO is %d' % len(ids[0].split()))

        for id_ in ids[0].decode('utf-8').split():
            x = self.server.fetch(id_, '(RFC822)')
            try:
                email_p = email.message_from_bytes(x[1][0][1])
            except IndexError:
                x = 'None'

            if email_p['Date'] is not None:
                timestamp = str(time.mktime(email.utils.parsedate(email_p['Date']))).replace('.', '')
            else:
                timestamp = str(datetime.datetime.now().timestamp()).replace('.', '')

            if email_p['Subject']:
                if decode_header(email_p['Subject'])[0][1]:
                    subject = decode_header(email_p['Subject'])[0][0].decode()
                else:
                    subject = decode_header(email_p['Subject'])[0][0]
            else:
                subject = 'none'
            email_from = email_p['Return-Path'].replace('<', '').replace('>', '')

            # create local dir
            dir_l = os.path.join(dir_, timestamp)
            if not os.path.exists(dir_l):
                os.makedirs(dir_l)
            # save subject
            print('Save subject:', subject)
            fp = open(os.path.join(dir_l, 'subject'), 'w')
            fp.write(subject)
            fp.close
            print('Save email from:', email_from)
            fp = open(os.path.join(dir_l, 'email_from'), 'w')
            fp.write(email_from)
            fp.close
            # save atach files
            if email_p.is_multipart():
                atach_files = ''
                for part in email_p.walk():

                    # body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                    if part.get_filename():
                        print('Save atach file: ', part.get_filename(), 'in ', dir_l)
                        fp = open(os.path.join(dir_l, part.get_filename()), 'wb')
                        fp.write(part.get_payload(decode=1))
                        fp.close
                        # save file attach
                        atach_files += '{file}\n'.format(file=part.get_filename())
                        fp = open(os.path.join(dir_l, 'attach'), 'w')
                        fp.write('')
                        fp.close

                    else:
                        fp = open(os.path.join(dir_l, 'body'), 'wb')
                        body = part.get_payload(decode=1)
                        if body:
                            fp.write(body)
                        fp.close

                    fp = open(os.path.join(dir_l, 'attach'), 'a')
                    fp.write(atach_files)
                    fp.close
            else:
                print('none_multi')
                # body = email_p.get_payload()
                # fp = open(os.path.join(dir_l, 'body'), 'w')
                # fp.write(body)
                # fp.close

    # upload email

    def uploadmails(self, from_dir='/home/', port_send=587, email_to='other_email@other.hostname.com',
                    password_to='some_other_password', user_to='user', host='other.hostname.com'):
        # get lisd dirs
        dirs = [f for f in listdir(from_dir) if isdir(join(from_dir, f))]
        for dir_ in dirs:
            path = join(from_dir, dir_)
            # get files in dir
            files = [f for f in listdir(path) if isfile(join(path, f))]
            if 'subject' and 'body' and 'email_from' in files:
                attach_files = []
                # open and read subject file
                with open(join(path, 'subject'), 'r') as myfile:
                    subject = myfile.readlines()
                # open and read body file
                with open(join(path, 'body'), 'r') as myfile:
                    body = myfile.readlines()
                # open and read email_from file
                with open(join(path, 'email_from'), 'r') as myfile:
                    email_from = myfile.readlines()
                # open and read attach file
                if isfile(join(path, 'attach')):
                    with open(join(path, 'attach'), 'r') as myfile:
                        attach = myfile.readlines()
                    for file_attach in attach:
                        attach_files.append(join(path, file_attach.replace('\n', '')))
                else:
                    attach_files = []
            send_mail(send_from=email_from[0], send_to=[email_to], subject=subject[0], text=body[0],
                      files=attach_files, server=host, username=user_to, password=password_to, istls=True, port=port_send)
            print(subject[0])

    def transfermails(self, dir_='/home/user/dl_dir', hostname='other.hostname.com', ssl=True, port_upload=993,
                      port_send=587, email_to='other_email@other.hostname.com', password='some_other_password'):
        self.downloadmails(dir_=dir_)
        self.uploadmails(from_dir=dir_, port_send=port_send, email_to=email_to, password_to=password, user_to=email_to,
                         host=hostname)




