#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import re
from random import choice
import time
import pymorphy2
from dotenv import load_dotenv
from excel_test import get_parsed_table

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
try:
    db.create_db()
    db.fill_db()
except:
    print(0)
items = [(str(el['keyword']).strip(), el['theme']) for el in get_parsed_table()]

list_of_ids = []

list_of_answers = [
    'Не совсем понимаю о чем речь, можете сформулировать свой вопрос иначе?',
    'Извините, куча дел... Можете более конкретно задать ваш вопрос?',
    'К сожалению не могу разобрать ваш вопрос',
    'Пожалуйста, задавайте вопросы по делу, ничего не понятно...']


suspects = ['Алина Кукушкина', 'Ирина Фокина', 'Светлана Комарова', 'Павел Старков',
            'Глеб Горбунов', 'Сергей Фролов', 'Марлен Кветенадзе', 'Наталья Ткачева', 'Мария Мухина']


def send_mail(to, answer, subject):
    smtp = SMTP(smtp_server, detective_login, detective_password, detective_mail)
    smtp.send_mail(to, 'RE:{}'.format(subject), answer)
    smtp.close()


def hint(episode, action, item, to, subject):
    hint_level = db.get_hint_level(to, item, episode)
    if not hint_level:
        db.add_player_item(to, item, episode)
    answer = db.get_hint(episode, action, item, to)
    if answer != 'OVERLOAD':
        send_mail(to, answer, subject)


def main(imap):
    # with IMAP(imap_server, detective_login, detective_password) as imap:
    # imap = IMAP(imap_server, detective_login, detective_password)

    emails = imap.get_messages()
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
                if len(message.split(detective_mail)) != 1:
                    message = message.split(detective_mail)[0]
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
                if p.normal_form.upper():
                    normal_words.append(p.normal_form.upper())

            # if 'КУКУШКИН' in normal_words:
            #     normal_words.append('КУКУШКИНА')
            del words
            episode = ' '.join(subject.split()[-2:])
            print(episode)
            sus_f_name = []
            sus_l_name = []
            action = ''
            item = ''
            flag = False
            hard_words = ['фотография', "фото", "протокол", "стенограмма", "пост", 'тоже', "жалоба"]
            hard_words = [el.upper() for el in hard_words]
            item_of_norm = None
            items_with_flag = []
            print(set(hard_words), set(normal_words))
            new_suspects = set()
            normal_suspects = []
            for word in suspects:
                w1, w2 = word.split()
                p1 = morph.parse(w1)[0].normal_form.upper()
                p2 = morph.parse(w2)[0].normal_form.upper()
                new_suspects.add(f'{p1} {p2}')
                normal_suspects.append(f'{p1} {p2}')
            current_suspects = []
            for word in normal_words:
                for el in normal_suspects:
                    lst = [_.upper() for _ in el.split()]
                    susp = ' '.join(lst)
                    if word in lst and susp in new_suspects:
                        new_suspects.remove(susp)
                        current_suspects.append(susp)
            if len(current_suspects) == 2:
                for el in items:
                    low = el[0].lower()
                    if current_suspects[0].lower() in low and current_suspects[1].lower() in low and el[1] == episode:
                        item = el[0]
                        break
            else:
                if len(set(hard_words).intersection(set(normal_words))) == 1:
                    item_of_norm = set(hard_words).intersection(set(normal_words)).pop()
                    flag = True if item_of_norm in normal_words else False
                    print(episode == 'АФ032020 БАКУ')
                    lst = [el for el in items if el[1] == episode]
                    items_with_flag = [el for el in items if item_of_norm.lower()
                                       in str(el[0]).lower() and el[1] == episode]
                for n_word in normal_words:
                    items_to_iterate = items_with_flag if flag else [el for el in items if el[1] == episode]
                    print(items_to_iterate)
                    break_normal = False
                    if break_normal:
                        break
                    for el in items_to_iterate:
                        if not flag:
                            inter = len(set(hard_words).intersection(set([el1.upper() for el1 in str(el[0]).split()])))
                            if inter:
                                continue
                        if item:
                            break_normal = True
                            break
                        test_word = ''
                        splitted_item = []
                        for el1 in str(el[0]).split():
                            p = morph.parse(el1)[0]
                            splitted_item.append(p.normal_form.upper())
                        for word in splitted_item:
                            if n_word == word:
                                test_word = n_word
                        if not test_word:
                            continue
                        is_break = False
                        if len(splitted_item) == 1:
                            item = el[0]
                            is_break = True
                            break
                        else:
                            if not flag:
                                item = el[0]
                            else:
                                for word in normal_words:
                                    if word in splitted_item and word != test_word and not item:
                                        item = el[0]
                                        is_break = True
                                        break
                        if is_break:
                            break
            print(f'item is {item}')
            if not action:
                action = 'ПОДСКАЗКА'
            if episode and len(episode.split()) > 1 and episode.split()[1] == 'КОД':
                digits = list(filter(lambda x: x.isdigit(), normal_words))
                if '420' in digits:
                    digit = digits[0]
                    if str(digit) == '420':
                        string_ans = '''Браво! Все получилось! Тут внутри Блокнот с записями и флешка (фото по ссылкам - https://clck.ru/bUU2Y, https://clck.ru/bUUNB ). 
Пришлю вам все это в следующей посылке. 

С уважением,
Кира Райнис'''
                        send_mail(FROM, string_ans, subject)
                elif len(digits) > 0:
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
            else:
                answer = choice(list_of_answers)
                send_mail(FROM, answer, subject)
            imap.delete(idm)
        else:
            print('null')


if __name__ == '__main__':
    print('started')
    mailbox = IMAP(imap_server, detective_login, detective_password)
    with mailbox.get_mail_box() as imap:
        while True:
            main(mailbox)
            time.sleep(60)
