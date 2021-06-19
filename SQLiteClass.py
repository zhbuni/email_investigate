import sqlite3

# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# Создание таблицы

# id, episode, suspect_id
episodes = [
    (1, 'АФТ001', 0),
    (2, 'АФТ002', 0),
    (3, 'АФТ003', 0),
    (4, 'АФТ004', 0),
    (5, 'АФТ005', 0),
    (6, 'АФТ006', 1),
]

# id, episode_id, first_name, last_name, evidence
suspects = [
    (1, 'МАКСИМ', 'ИВАНОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (2, 'ИГОРЬ', 'СМИРНОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (3, 'АЛЕКСЕЙ', 'СИДОРОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (4, 'АНДРЕЙ', 'ВОРОБЬЁВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (5, 'ЕВГЕНИЙ', 'ПЕТРОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (6, 'СЕРГЕЙ', 'КАБАЧКОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (7, 'ДЕНИС', 'ПЕТРУШКИН', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (8, 'ИВАН', 'МАКАРОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (9, 'МИХАИЛ', 'ПЕЛЬМЕШКИН', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (10, 'КОНСТАНТИН', 'СОСИСЬКИН', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
]

# id, episode_id, suspect_id
answers = [
    (1, 1, 1),
    (2, 1, 2),
    (3, 2, 3),
    (4, 2, 4),
    (5, 3, 5),
    (6, 3, 6),
    (7, 4, 7),
    (8, 5, 8),
    (9, 6, 9),
]

# player_id, email, answer_id
# players = []

# id, episode_id, item, hint, answer
hints = [
    (1, 1, 'ФОНАРИК', 'Подсказка Фонарик', 'Ответ Фонарик'),
    (2, 1, 'АЛЬБОМ', 'Подсказка АЛЬБОМ', 'Ответ АЛЬБОМ'),
    (3, 2, 'КОМПАС', 'Подсказка АЛЬБОМ', 'Ответ АЛЬБОМ'),
    (4, 2, 'РУЧКА', 'Подсказка РУЧКА', 'Ответ РУЧКА'),
    (5, 3, 'БЛОКНОТ', 'Подсказка БЛОКНОТ', 'Ответ БЛОКНОТ'),
    (6, 3, 'КАРАНДАШ', 'Подсказка КАРАНДАШ', 'Ответ КАРАНДАШ'),
    (7, 4, 'МЫШЬ', 'Подсказка МЫШЬ', 'Ответ МЫШЬ'),
    (8, 4, 'НАУШНИКИ', 'Подсказка НАУШНИКИ', 'Ответ НАУШНИКИ'),
    (9, 5, 'ФОТО', 'Подсказка ФОТО', 'Ответ ФОТО'),
    (10, 5, 'БУТЫЛКА', 'Подсказка БУТЫЛКА', 'Ответ БУТЫЛКА'),
    (11, 6, 'КРОВЬ', 'Подсказка КРОВЬ', 'Ответ КРОВЬ'),
    (12, 6, 'ШПРИЦ', 'Подсказка ШПРИЦ', 'Ответ ШПРИЦ'),
]


class DB:
    """Операции с БД"""

    def __init__(self, dbname):
        """Подключение к БД"""
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def fill_db(self):
        """Наполнить БД"""
        self.cursor.executemany("INSERT INTO Suspects VALUES (?, ?, ?, ?);", suspects)
        self.cursor.executemany("INSERT INTO Episodes VALUES (?, ?, ?);", episodes)
        self.cursor.executemany("INSERT INTO Hints VALUES (?, ?, ?, ?, ?);", hints)
        self.cursor.executemany("INSERT INTO Answers VALUES (?, ?, ?);", answers)
        self.conn.commit()

    def create_db(self):
        """Создать таблицу если её нет"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Suspects
                  (
                  id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  evidence TEXT
                  )
               """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Episodes
                  (
                  id INTEGER PRIMARY KEY,
                  box_name TEXT,
                  is_final INTEGER DEFAULT 0
                  )
               """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Hints
                  (
                  id INTEGER PRIMARY KEY,
                  episode_id INTEGER,
                  item TEXT,
                  hint TEXT,
                  answer TEXT,
                  FOREIGN KEY (episode_id) REFERENCES Episodes(id)
                  )
               """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Answers
                          (
                          id INTEGER PRIMARY KEY,
                          episode_id INTEGER,
                          suspect_id INTEGER,
                          FOREIGN KEY (episode_id) REFERENCES Episodes(id),
                          FOREIGN KEY (suspect_id) REFERENCES Suspects(id)
                          )
                       """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Players
                            (
                            email TEXT,
                            answer_id INTEGER,
                            try INTEGER default 0,
                            guessed INTEGER default 0,
                            FOREIGN KEY (answer_id) REFERENCES Answers(id)
                            )
        """)

    def drop_db(self):
        """Очестить БД"""
        self.cursor.execute('''DROP TABLE Answers''')
        self.cursor.execute('''DROP TABLE Episodes''')
        self.cursor.execute('''DROP TABLE Hints''')
        self.cursor.execute('''DROP TABLE Suspects''')
        self.cursor.execute('''DROP TABLE Players''')

    def get_all_names(self):
        """Получить массивы с уникальными именами фамилиями"""
        self.cursor.execute("""SELECT * from Suspects""")
        arr = self.cursor.fetchall()
        first_names = []
        last_names = []
        for i in range(len(arr)):
            first = arr[i][1]
            last = arr[i][2]
            if first not in first_names:
                first_names.append(first)
            if last not in last_names:
                last_names.append(last)

        return first_names, last_names

    def get_all_items(self):
        """Получить массивв с ключевыми словами для подсказок"""
        self.cursor.execute("""SELECT item FROM Hints""")
        arr = self.cursor.fetchall()
        items = []
        for i in range(len(arr)):
            items.append(arr[i][0])
        return items

    def get_box(self, box_name):
        sql = '''
                SELECT e.box_name, h.episode_id, s.first_name, s.last_name, h.item, h.hint, h.answer
                    from Episodes as e
                    JOIN Suspects as s on e.id = s.episode_id
                    JOIN Hints as h on e.id = h.episode_id
                    WHERE e.box_name LIKE "%{}%"
                '''.format(box_name)
        self.cursor.execute(sql)
        arr = self.cursor.fetchall()
        print(arr)

    def check_suspect(self, episode, first_name, last_name):
        """Проверить подозреваемого"""
        sql = '''
        SELECT s.evidence from Answers as a
        JOIN Episodes as e on a.episode_id = e.id
        JOIN Suspects as s on a.suspect_id = s.id
        WHERE s.first_name LIKE "{}" AND last_name LIKE "{}"
        AND e.box_name LIKE "{}"
        '''.format(first_name, last_name, episode)
        # print(sql)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        # print(boo)
        if boo:
            return boo[0]
        else:
            return False

    def get_hint(self, episode, action, item):
        if action == 'ПОДСКАЗКА':
            action = 'hint'
        else:
            action = 'answer'

        self.cursor.execute('''SELECT h.{}
                    from Episodes as e
                    JOIN Hints as h on e.id = h.episode_id
                    WHERE h.item LIKE "{}" AND e.box_name LIKE "{}"'''.format(action, item, episode))
        boo = self.cursor.fetchone()
        if boo:
            return boo[0]
        else:
            return False

    def right_answer(self, email, first_name, last_name):
        sql = '''UPDATE Players SET answer_id=(
            SELECT A.id FROM Answers A join Suspects S on S.id = A.suspect_id
            WHERE S.first_name LIKE "{}"
            AND S.last_name LIKE "{}"
        ), try=0, guessed=guessed+1
        WHERE email="{}"
        '''.format(first_name, last_name, email)
        # print(sql)
        self.cursor.execute(sql)
        if self.cursor.rowcount < 1:
            sql = '''INSERT INTO Players (email, answer_id, try, guessed) VALUES ("{}", (
            SELECT A.id FROM Answers A join Suspects S on S.id = A.suspect_id
            WHERE S.first_name LIKE "{}"
            AND S.last_name LIKE "{}"
        ), 0, 1)'''.format(email, first_name, last_name)
            # print(sql)
            self.cursor.execute(sql)
        self.conn.commit()

    def wrong_answer(self, email):
        sql = '''UPDATE Players SET try=try+1 WHERE email="{}"'''.format(email)
        print(sql)
        self.cursor.execute(sql)
        print(self.cursor.rowcount)
        if self.cursor.rowcount < 1:
            sql = '''INSERT INTO Players (email, answer_id, try, guessed) VALUES ("{}", 0, 1, 0)'''.format(email)
            # print(sql)
            self.cursor.execute(sql)
        self.conn.commit()


    def get_try(self, email):
        sql = '''SELECT try FROM Players
            WHERE email="{}"
            '''.format(email)
        # print(sql)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return True
        else:
            return False

    def get_guessed(self, email):
        sql = '''SELECT guessed FROM Players
            WHERE email="{}"
            '''.format(email)
        # print(sql)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return boo[0]
        else:
            return 0

    def get_suspect_count(self, episode):
        sql = '''
        SELECT count(*) FROM Answers WHERE episode_id = (SELECT id FROM Episodes WHERE box_name LIKE "{}")
        '''.format(episode)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return boo[0]
        else:
            return 0

    def if_final(self, episode):
        sql = '''
            SELECT is_final FROM Episodes WHERE box_name LIKE "{}"
        '''.format(episode)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            if boo[0] == 1:
                return True
            else:
                return False


    def check_suspect_repeat(self, first_name, last_name):
        sql = '''
            SELECT answer_id from Players P JOIN Answers A on P.answer_id = A.id JOIN Suspects S on S.id = A.suspect_id
            WHERE S.first_name LIKE "{}" AND S.last_name LIKE "{}"
        '''.format(first_name, last_name)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return True
        else:
            return False

    def get_evidence(self, episode):
        sql='''
            SELECT evidence FROM Suspects
            WHERE id = (
                SELECT suspect_id from Answers A JOIN Episodes E on E.id = A.episode_id
                WHERE E.box_name LIKE "{}"
                LIMIT 1
                )
        '''.format(episode)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return boo[0]
        else:
            return False

    def get_second_evidence(self, email):
        sql = '''
        SELECT evidence FROM Suspects S JOIN Answers A on S.id = A.suspect_id
        WHERE A.episode_id = (
            SElECT episode_id FROM Answers A JOIN Players P on A.id = P.answer_id
            WHERE P.email LIKE "{}"
        )
        AND A.id != (
            SELECT answer_id FROM Players WHERE email LIKE "{}"
        )
        '''.format(email, email)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        if boo:
            return boo[0]
        else:
            return False

    def rezoing(self, email):
        sql='''
            DELETE FROM Players WHERE email LIKE "{}"
        '''.format(email)
        # sql = '''
        # UPDATE Players SET try=0, guessed=0
        # WHERE email LIKE "{}"
        # '''.format(email)
        self.cursor.execute(sql)
        self.conn.commit()

