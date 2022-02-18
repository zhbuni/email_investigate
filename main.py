#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
from random import choice
import time

import pymorphy2
from dotenv import load_dotenv

morph = pymorphy2.MorphAnalyzer()

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
# items = ['папка выпускника']
print(sorted(items))
print('код на открытие ящика' in items)
list_of_ids = []

list_of_answers = [
    'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?',
    'Извините, куча дел... Можете более конкретно задать ваш вопрос?',
    'К сожалению не могу разобрать ваш вопрос',
    'Пожалуйста, задавайте вопросы по делу, ничего не понятно...z']


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
    hint_level = db.get_hint_level(to, item)
    if not hint_level:
        db.add_player_item(to, item)
    answer = db.get_hint(episode, action, item, to)
    if answer == 'OVERLOAD':
        answer = choice(list_of_answers)
    if not answer:
        answer = choice(list_of_answers)
    send_mail(to, answer, subject)


def main():
    print('In main')
    imap = IMAP(imap_server, detective_login, detective_password)

    emails = imap.get_messages()
    print(emails)
    if len(emails) > 0:
        for email in emails:
            if email[0] in list_of_ids:
                continue
            list_of_ids.append(email[0])
            print(email)
            subject = email[2]
            FROM = email[1]
            if FROM.split('@')[1] in ('yandex.ru', 'ya.ru'):
                message = email[4][email[4].find('>') + 1:]
                message = message[:message.find('<')]
            else:
                message = email[3]
            parsed_message = message.strip()
            print(FROM.strip())
            player = db.get_player(FROM.strip())
            if not player:
                db.add_player(FROM)
            idm = email[0]
            # print(parsed_message, subject, FROM)
            words = re.split('\.|-| |; |,|:|\n|\r', parsed_message)
            print(words)
            normal_words = []

            for word in words:
                p = morph.parse(word)[0]
                normal_words.append(p.normal_form.upper())
            print(normal_words)
            del words
            episode = subject
            # try:
            #     episode = re.search(r'АФ\d+', subject.upper()).group(0)
            # except:
            #     episode = ''
            # print(episode)
            sus_f_name = []
            sus_l_name = []
            action = ''
            item = ''
            flag = False
            flag_to_photos = False
            if 'ПРОТОКОЛ' in normal_words:
                item = 'Протокол опроса Кукушкиной Алины'
                flag = True
            elif 'ФОТОГРАФИЯ' in normal_words:
                flag_to_photos = True
                items_with_photos = [el for el in items if 'фотография' in el.lower()]
            for n_word in normal_words:
                items_to_iterate = items_with_photos if flag_to_photos else items
                for el in items_to_iterate:
                    if not flag and 'протокол' in str(el).lower()\
                            or not flag_to_photos and 'фотография' in str(el).lower():
                        continue
                    if item:
                        break
                    test_word = ''
                    splitted_item = []
                    for el1 in el.split():
                        p = morph.parse(el1)[0]
                        splitted_item.append(p.normal_form.upper())
                    for word in splitted_item:
                        if n_word == word:
                            test_word = n_word
                    if not test_word:
                        continue
                    is_break = False
                    if len(message.split()) == 1:
                        item = el
                        is_break = True
                        break
                    else:
                        for word in normal_words:
                            if word in splitted_item and word != test_word and not item:
                                item = el
                                is_break = True
                                break
                    if is_break:
                        break
                    if n_word.startswith('АФ'):
                        episode = n_word
                    if n_word in first_names:
                        sus_f_name.append(n_word)
                    if n_word in last_names:
                        sus_l_name.append(n_word)
                    # if n_word in items:
                    #     item = n_word
                if n_word == 'ПОДСКАЗКА' or n_word == "ОТВЕТ":
                    action = n_word
            if not action:
                action = 'ПОДСКАЗКА'
            if len(sus_f_name) > 1 or len(sus_l_name) > 1:
                answer = 'Кажется вам сложно определиться. Кто-то из них точно виноват, а кто-то нет. ' \
                         'Я думаю вам нужно еще раз пройтись по уликам.'
                send_mail(FROM, answer, subject)
            elif episode and len(episode.split()) > 1 and episode.split()[1] == 'КОД':
                digits = list(filter(lambda x: x.isdigit(), normal_words))
                if len(digits) == 1:
                    digit = digits[0]
                    if str(digit) == '420':
                        string_ans = '''Браво! Все получилось! Тут внутри Блокнот с записями и флешка (фото по ссылкам - https://clck.ru/bUU2Y, https://clck.ru/bUUNB ). 
Пришлю вам все это в следующей посылке. 

С уважением,
Кира Райнис'''
                        send_mail(FROM, string_ans, subject)
                    else:
                        string_ans = '''Не подходит. 
Подумайте еще.
Жду вашу версию.
                                    
С уважением,
Кира Райнис'''
                        send_mail(FROM, string_ans, subject)
            elif episode and item and action:
                if item and action:
                    print(episode, action, item, FROM, subject)
                    hint(episode, action, item, FROM, subject)

            imap.delete(idm)
        else:
            print('null')
    imap.close()


if __name__ == '__main__':
    print('started')
    while True:
        main()
        time.sleep(5)
