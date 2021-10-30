# EmailDetective

##Установка и запуск
Необходим Python3 (Разработка велась на 3.8)

Переменные среды
```dotenv
IMAP_SERVER="imap.gmail.com"
SMTP_SERVER="smtp.gmail.com"
DETECTIVE_MAIL="username@gmail.com"
DETECTIVE_LOGIN="username@gmail.com"
DETECTIVE_PASSWORD="Password123"
```

Установка и запуск
```python
pip install -r req.txt
python3 fill_db.py
python3 main.py
```

###Примечание
gmail отбирает разрешение у "небезопасных" приложений время от времени.
[Выдать здесь](https://myaccount.google.com/lesssecureapps?pli=1)

так же необходимо разрешить в настройках IMAP. [Инструкция](https://support.google.com/mail/answer/7126229?hl=ru&visit_id=637711807522626069-3415149530&rd=2#zippy=%2C%D1%88%D0%B0%D0%B3-%D0%B2%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D0%B5-imap-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF)