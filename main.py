#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
import time
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from NewImap import IMAP
from SmtpClass import SMTP
from SQLiteClass import DB

imap_server = os.environ['IMAP_SERVER']
smtp_server = os.environ['SMTP_SERVER']
detective_mail = os.environ['DETECTIVE_MAIL']
detective_login = os.environ['DETECTIVE_LOGIN']
detective_password = os.environ['DETECTIVE_PASSWORD']

db = DB("database.db")
# db.create_db()
# db.fill_db()
# db.get_box('01203')
first_names, last_names = db.get_all_names()
items = db.get_all_items()


# print(items)
# print(first_names, last_names)


def send_mail(to, answer, subject):
    smtp = SMTP(smtp_server, detective_login, detective_password, detective_mail)
    smtp.send_mail(to, 'RE:{}'.format(subject), answer)
    smtp.close()


def suspect(episode, sus_f_name, sus_l_name, to, subject):
    answer = db.check_suspect(episode, sus_f_name, sus_l_name)
    if answer:
       send_mail(to, answer, subject)
    elif not answer:
        answer = 'Нельзя однозначно вычеркнуть подозреваемого {} {} из списка подозреваемых.'.format(sus_f_name.capitalize(), sus_l_name.capitalize())
        send_mail(to, answer, subject)


def hint(episode, action, item, to, subject):
    answer = db.get_hint(episode, action, item)
    if not answer:
        answer = 'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?'
    send_mail(to, answer, subject)


def main():
    imap = IMAP(imap_server, detective_login, detective_password)

    emails = imap.get_messages()
    if len(emails) > 0:
        for idm in emails:
            parsed_message = idm[3].strip()
            subject = idm[2]
            FROM = idm[1]
            print(parsed_message, subject, FROM)
            words = re.split('-| |; |,|:|\n|\r', parsed_message)
            normal_words = []

            for word in words:
                p = morph.parse(word)[0]
                normal_words.append(p.normal_form.upper())

            del words

            print(normal_words)

            episode = re.match(r'АФТ\d+', subject)
            print(episode)
            sus_f_name = ''
            sus_l_name = ''
            action = ''
            item = ''
            for n_word in normal_words:
                if n_word.startswith('АФТ'):
                    episode = n_word
                if n_word in first_names:
                    sus_f_name = n_word
                if n_word in last_names:
                    sus_l_name = n_word
                if n_word in items:
                    item = n_word
                if n_word == 'ПОДСКАЗКА' or n_word == "ОТВЕТ":
                    action = n_word

            if episode and sus_f_name and sus_l_name or episode and item and action:
                print(FROM[1])
                print(episode)
                if sus_f_name and sus_l_name:
                    print(sus_f_name, sus_l_name)
                    suspect(episode, sus_f_name, sus_l_name, FROM, subject)
                if item and action:
                    hint(episode, action, item, FROM, subject)
                    print(action, item)
            else:
                answer = 'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?'
                send_mail(FROM, answer, subject)

            # imap.delete(idm)
            #

            #
            # else:
            #     print('null')

    imap.close()


while True:
    main()
    time.sleep(60)
