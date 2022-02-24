#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import smtplib
from email.message import EmailMessage
from email.headerregistry import Address


class SMTP:
    """Операции с SMTP сервером"""
    def __init__(self, uri, login, password, from_mail):
        """Подключение к серверу, начальные настройки"""
        self.uri = uri
        self.login = login
        self.password = password
        self.server = smtplib.SMTP_SSL(uri)
        self.server.login(self.login, self.password)
        self.FROM = from_mail

    def send_mail(self, TO, SUBJECT, TEXT):
        """Отправить сообщение"""
        BODY = "\r\n".join((
            "From: %s" % self.FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT,
            "",
            TEXT
        ))
        self.server.sendmail(self.FROM, TO, BODY.encode('utf-8'))

    def close(self):
        """Отклюситься от сервера"""
        self.server.quit()