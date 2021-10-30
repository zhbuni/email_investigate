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
first_names, last_names = db.get_all_names()
items = db.get_all_items()


def send_mail(to, answer, subject):
    smtp = SMTP(smtp_server, detective_login, detective_password, detective_mail)
    smtp.send_mail(to, 'RE:{}'.format(subject), answer)
    smtp.close()


def suspect(episode, sus_f_name, sus_l_name, to, subject):
    # print(episode, sus_l_name, sus_f_name)
    answer = db.check_suspect(episode, sus_f_name, sus_l_name)
    if db.check_suspect_repeat(sus_f_name, sus_l_name):
        email = 'Мы уже все выяснили про этого подозреваемого'
        send_mail(to, email, subject)
    else:
        if answer:
            email = 'Молодец! {} {} действительно невиновен.\n'.format(sus_f_name.capitalize(), sus_l_name.capitalize())
            if not db.get_try(to):
                email += 'Вот материалы которые подтверждают твою догадку: {}\n'.format(answer)
            db.right_answer(to, sus_f_name, sus_l_name)
            if db.get_guessed(to) >= db.get_suspect_count(episode):
                db.rezoing(to)
                email += 'Жди новую коробку!'
            else:
                evidence = db.get_second_evidence(to)
                email += 'Кажется из имеющихся улик можно вычеркнуть еще одного. Взгляни на эти материалы {}'.format(evidence)
            if db.if_final(episode):
                email = 'Убийца найден! Спасибо за помощь!'
            send_mail(to, email, subject)
        elif not answer:
            email = 'Нельзя однозначно вычеркнуть подозреваемого {} {} из списка подозреваемых.\n'.format(
                sus_f_name.capitalize(), sus_l_name.capitalize())

            if db.if_final(episode):
                email = 'Ты уверен в этом?'

            if not db.get_try(to):
                evidence = db.get_evidence(episode)
                email += 'Вот материалы которые могут помочь: {}\n'.format(evidence)

            db.wrong_answer(to)

            send_mail(to, email, subject)


def hint(episode, action, item, to, subject):
    answer = db.get_hint(episode, action, item)
    if not answer:
        answer = 'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?'
    send_mail(to, answer, subject)


def main():
    imap = IMAP(imap_server, detective_login, detective_password)

    emails = imap.get_messages()
    if len(emails) > 0:
        for email in emails:
            parsed_message = email[3].strip()
            subject = email[2]
            FROM = email[1]
            idm = email[0]
            # print(parsed_message, subject, FROM)
            words = re.split('\.|-| |; |,|:|\n|\r', parsed_message)
            normal_words = []

            for word in words:
                p = morph.parse(word)[0]
                normal_words.append(p.normal_form.upper())

            del words

            print(normal_words)

            try:
                episode = re.search(r'АФТ\d+', subject.upper()).group(0)
            except:
                episode = ''
            # print(episode)
            sus_f_name = []
            sus_l_name = []
            action = ''
            item = ''
            for n_word in normal_words:
                if n_word.startswith('АФТ'):
                    episode = n_word
                if n_word in first_names:
                    sus_f_name.append(n_word)
                if n_word in last_names:
                    sus_l_name.append(n_word)
                if n_word in items:
                    item = n_word
                if n_word == 'ПОДСКАЗКА' or n_word == "ОТВЕТ":
                    action = n_word

            if len(sus_f_name) > 1 or len(sus_l_name) > 1:
                answer = 'Кажется вам сложно определиться. Кто-то из них точно виноват, а кто-то нет. ' \
                         'Я думаю вам нужно еще раз пройтись по уликам.'
                send_mail(FROM, answer, subject)

            elif episode and sus_f_name and sus_l_name or episode and item and action:
                # print(FROM[1])
                # print(episode)
                if sus_f_name and sus_l_name:
                    # print(sus_f_name[0], sus_l_name[0])
                    suspect(episode, sus_f_name[0], sus_l_name[0], FROM, subject)
                if item and action:
                    hint(episode, action, item, FROM, subject)
                    # print(action, item)
            else:
                answer = 'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?'
                send_mail(FROM, answer, subject)

            imap.delete(idm)

        else:
            print('null')

    imap.close()


while True:
    main()
    time.sleep(20)
