import os
from configparser import ConfigParser
from imaplib import IMAP4_SSL
from typing import List, Any, Tuple

CONFIG_FILE = 'config.ini'
config: ConfigParser = ConfigParser(interpolation=None)

if not os.path.exists(CONFIG_FILE):
    config['Mail.ru'] = {'login': 'Please, type here your login of Mail.ru mailbox',
                         'password': 'Please, type here your password of Mail.ru mailbox'}
    config['Unisender.com'] = {'api_Key': 'Please, type here your API key from Unisender.com'}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
    print('Please, write your config data in the', CONFIG_FILE+', after what run program again.')
else:
    config.read(CONFIG_FILE)
    login = config['Mail.ru']['login']
    password = config['Mail.ru']['password']
    api_key = config['Unisender.com']['api_key']

    with IMAP4_SSL('imap.mail.ru') as Mail:
        Mail.login(login, password)
        print(Mail.select())
        status: str
        mailbox: list[Any]
        status, mailbox = Mail.search(None, 'ALL')
        for numLetter in mailbox[0].split():
            contentLetter: list[None] | list[bytes | tuple[bytes, bytes]]
            status, contentLetter = Mail.fetch(numLetter, '(RFC822)')
            print('Message %s\n%s\n' % (numLetter, contentLetter[0][1]))
        print(Mail.list())
        # print(Mail.readline()) - it freeze
        Mail.noop()
