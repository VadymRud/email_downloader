from os import listdir
from os.path import isfile, join, isdir
from send_email import send_mail

main_dir = '/home/vadymrud/~~~temp/emails/'


def uploadmails(from_dir, hostname='other.hostname.com', port=587, email='other_email@other.hostname.com',
                password='some_other_password', user='user'):
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
        send_mail(send_from=email_from[0], send_to=[email], subject=subject[0], text=body[0],
                  files=attach_files, server=hostname, username=user, password=password, istls=True, port=port)
        print(attach_files)
        print(subject[0])

#