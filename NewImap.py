from imap_tools import MailBox, AND, A


class IMAP:
    """Все что касается получения, парсинга и управления сообщениями"""
    def __init__(self, uri, login, password):
        """Подключение к IMAP серверу"""
        self.mailbox = MailBox(uri)
        self.mailbox.login(login, password, initial_folder='INBOX')

    def get_messages(self):
        """Получение массива UID сообщений из папки входящее если есть"""
        uids = [[msg.uid, msg.from_, msg.subject, msg.text] for msg in self.mailbox.fetch(AND(all=True))]
        if len(uids) > 0:
            return uids
        else:
            return []

    def close(self):
        self.mailbox.logout()
