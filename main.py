import os
import logging
from configparser import ConfigParser
from imaplib import IMAP4_SSL
from logging import Logger
from typing import List, Any, Tuple

logging.basicConfig(filename='logfile.log',
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    filemode='w')
logger: Logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.debug('Test debug')
logger.info('Test info')
logger.warning('Test warning')
logger.error('Test error')
logger.critical('Test critical')

def get_unsubscriber_email(string: str) -> str:
    to_adress_template_1 = b'\r\nTo: '
    to_adress_template_2 = b'\r\n'
    finded_to_adress_template_1_pos = string.find(to_adress_template_1)
    if finded_to_adress_template_1_pos == -1:
        return ''
    else:
        logger.debug(finded_to_adress_template_1_pos)
        substring_pos = finded_to_adress_template_1_pos + len(to_adress_template_1)
        substring = string[substring_pos:]
        logger.debug(substring)
        deep_2_to_adress_template_1_pos = substring.find(to_adress_template_1)
        if deep_2_to_adress_template_1_pos == -1:
            return ''
        else:
            logger.debug(deep_2_to_adress_template_1_pos)
            to_adress_start_pos = deep_2_to_adress_template_1_pos + len(to_adress_template_1)
            substring = substring[to_adress_start_pos:]
            to_adress_end_pos = substring.find(to_adress_template_2)
            return substring[:to_adress_end_pos]

CONFIG_FILE = 'config.ini'
config: ConfigParser = ConfigParser(interpolation=None)

if not os.path.exists(CONFIG_FILE):
    config['Mail.ru'] = {'login': 'Please, type here your login of Mail.ru mailbox',
                         'password': 'Please, type here your password of Mail.ru mailbox'}
    config['Unisender.com'] = {'api_key': 'Please, type here your API key from Unisender.com'}
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)
    print('Please, write your config data in the', CONFIG_FILE+', after what run program again.')
else:
    config.read(CONFIG_FILE)
    login = config['Mail.ru']['login']
    password = config['Mail.ru']['password']
    api_key = config['Unisender.com']['api_key']

    with IMAP4_SSL('imap.mail.ru') as mail:
        logger.debug(mail.login(login, password))
        logger.debug(mail.list())
        logger.info(mail.select())
        status: str
        mailbox: list[Any]
        status, mailbox = mail.search(None, 'ALL')
        for num_letter in mailbox[0].split():
            content_letter: list[None] | list[bytes | tuple[bytes, bytes]]
            status, content_letter = mail.fetch(num_letter, '(RFC822)')
            unsubscriber_email: str = get_unsubscriber_email(content_letter[0][1])
            logger.debug('%s %s' % (num_letter, unsubscriber_email))
