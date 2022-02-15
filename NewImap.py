from imap_tools import MailBox, AND, A


class IMAP:
    """Все что касается получения, парсинга и управления сообщениями"""
    def __init__(self, uri, login, password):
        """Подключение к IMAP серверу"""
        self.mailbox = MailBox(uri)
        self.mailbox.login(login, password, initial_folder='INBOX')

    def get_messages(self):
        """Получение массива UID сообщений из папки входящее если есть"""
        uids = []
        for msg in self.mailbox.fetch(reverse=True, limit=10,
                                      mark_seen=False):
            lst = [msg.uid, msg.from_, msg.subject, msg.text, msg.html]
            uids.append(lst)
        # uids = [[msg.uid, msg.from_, msg.subject, msg.text] for msg in self.mailbox.fetch(reverse=True, limit=1,
        #                                                                                   mark_seen=False)]

        if len(uids) > 0:
            return uids
        else:
            return []

    def delete(self, uid):
        self.mailbox.delete(uid)

    def close(self):
        self.mailbox.logout()
