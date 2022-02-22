import sqlite3
from excel_test import get_parsed_table

# Создание таблицы

table = get_parsed_table()

# id, episode, suspect_id
episodes = []
st = [el['theme'] for el in table[1:]]
count = 0
st_of_episodes = set()
for el in st:
    if el not in st_of_episodes:
        episodes.append((count, el, 0))
        count += 1
        st_of_episodes.add(el)
print(episodes)
# episodes = [
#     (1, 'АФТ001', 0),
#     (2, 'АФТ002', 0),
#     (3, 'АФТ003', 0),
#     (4, 'АФТ004', 0),
#     (5, 'АФТ005', 0),
#     (6, 'АФТ006', 1),
# ]

# id, episode_id, first_name, last_name, evidence
suspects = [
    (1, 'МАКСИМ', 'ИВАНОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (2, 'ИГОРЬ', 'СМИРНОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (3, 'АЛЕКСЕЙ', 'СИДОРОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (4, 'АНДРЕЙ', 'ВОРОБЬЁВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (5, 'ЕВГЕНИЙ', 'ПЕТРОВ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (6, 'СЕРГЕЙ', 'КАБАЧКОВЫЙ', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
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

# id, episode_id, item, hint, level, answer
hints = []
count = 0
for el in table[1:]:
    episode_id = [ep[0] for ep in episodes if ep[1] == el['theme']][0]
    item = el['keyword']
    hint = f'Подсказка {item}'
    level = 1
    answer = el['tip_1']
    hints.append((count, episode_id, item, hint, level, answer))
    if el['tip_2'] != 'None':
        count += 1
        level += 1
        answer = el['tip_2']
        hints.append((count, episode_id, item, hint, level, answer))
    if el['tip_3'] != 'None':
        count += 1
        level += 1
        answer = el['tip_3']
        hints.append((count, episode_id, item, hint, level, answer))
    count += 1
# print(hints)
# hints = [
#     (0, 1, 'ФОНАРИК1', 'Подсказка Фонарик1', 1, 'Ответ Фонарик1'),
#     (1, 1, 'ФОНАРИК1', 'Подсказка Фонарик2', 2, 'Ответ Фонарик2'),
#     (2, 1, 'АЛЬБОМ1', 'Подсказка АЛЬБОМ1', 1, 'Ответ АЛЬБОМ'),
#     (3, 2, 'КОМПАС', 'Подсказка АЛЬБОМ1', 1, 'Ответ АЛЬБОМ'),
#     (4, 2, 'РУЧКА', 'Подсказка РУЧКА', 1, 'Ответ РУЧКА'),
#     (5, 3, 'БЛОКНОТ', 'Подсказка БЛОКНОТ', 1, 'Ответ БЛОКНОТ'),
#     (6, 3, 'КАРАНДАШ', 'Подсказка КАРАНДАШ', 1, 'Ответ КАРАНДАШ'),
#     (7, 4, 'МЫШЬ', 'Подсказка МЫШЬ', 1, 'Ответ МЫШЬ'),
#     (8, 4, 'НАУШНИКИ', 'Подсказка НАУШНИКИ', 1, 'Ответ НАУШНИКИ'),
#     (9, 5, 'ФОТО', 'Подсказка ФОТО', 1, 'Ответ ФОТО'),
#     (10, 5, 'БУТЫЛКА', 'Подсказка БУТЫЛКА', 1, 'Ответ БУТЫЛКА'),
#     (11, 6, 'КРОВЬ', 'Подсказка КРОВЬ', 1, 'Ответ КРОВЬ'),
#     (12, 6, 'ШПРИЦ', 'Подсказка ШПРИЦ', 1, 'Ответ ШПРИЦ'),
# ]


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
        self.cursor.executemany("INSERT INTO Hints VALUES (?, ?, ?, ?, ?, ?);", hints)
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
                  level INTEGER,
                  answer TEXT,
                  FOREIGN KEY (episode_id) REFERENCES Episodes(id)
                  )
               """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Player_hints
                          (
                          id INTEGER PRIMARY KEY,
                          player_id INTEGER REFERENCES PLAYERS(id),
                          email TEXT,
                          item TEXT REFERENCES Hints(item),
                          hint_level INTEGER DEFAULT 1,
                          episode_id INTEGER
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
                            id INTEGER PRIMARY KEY,
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

    def get_hint(self, episode, action, item, email):
        if action == 'ПОДСКАЗКА':
            action = 'hint'
        else:
            action = 'answer'
        episode_from_db = self.cursor.execute(f'''
                                                          SELECT id FROM Episodes
                                                          WHERE box_name = "{episode}" 
                                                          ''').fetchone()[0]
        if action == 'hint':
            print(self.cursor.execute(f'''
                                    SELECT hint_level, item FROM Player_hints WHERE episode_id = {episode_from_db}
    ''').fetchall())
            hint_level = self.cursor.execute(f'''
                                                 SELECT hint_level FROM Player_hints
                                                 WHERE Player_hints.email = '{email}'
                                                 AND Player_hints.item = '{item}'
                                                 AND Player_hints.episode_id = {episode_from_db}
                                             ''').fetchone()[0]
            print(f'item is {item}', episode_from_db)
            max_hint_level = self.cursor.execute(f'''
                                                            SELECT MAX(level) FROM Hints
                                                            WHERE item = '{item}'
                                                            AND episode_id = {episode_from_db}
                                                             ''').fetchone()[0]
            print(max_hint_level)
            if hint_level >= max_hint_level:
                hint_level = 1
                query = self.cursor.execute(f'''
                                                                 UPDATE Player_hints SET hint_level = 1
                                                                 WHERE Player_hints.email = '{email}'
                                                                 AND Player_hints.item = '{item}'
                                                                 AND Player_hints.episode_id = {episode_from_db}
                                                             ''')
                self.conn.commit()

            else:
                if max_hint_level != hint_level:
                    query = self.cursor.execute(f'''
                                                                UPDATE Player_hints
                                                                SET hint_level = hint_level + 1
                                                                WHERE item = '{item}' and episode_id = {episode_from_db}
                                                                ''')
                    self.conn.commit()

            print(episode, hint_level, max_hint_level)

            hint = self.cursor.execute(f'''
                                SELECT answer FROM Hints
                                WHERE item = '{item}' AND level = {hint_level} AND episode_id = {episode_from_db}
                                ''').fetchone()[0]
            print(hint)
            return hint
        else:
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

    def add_player(self, email):
        self.cursor.execute(f'''
                            INSERT INTO Players (email) VALUES ('{email}')
                            ''')
        self.conn.commit()

    def get_player(self, email):
        person = self.cursor.execute(f'''
                            SELECT email FROM Players
                            WHERE email = '{email}'
                            ''').fetchone()
        return person

    def get_hint_level(self, email, item, episode):
        episode_id = self.cursor.execute(f'''
                                                                          SELECT id FROM Episodes
                                                                          WHERE box_name = "{episode}" 
                                                                          ''').fetchone()[0]
        hint_level = self.cursor.execute(f'''SELECT hint_level FROM Player_hints
                                             WHERE Player_hints.email = '{email}'
                                             AND Player_hints.item = '{item}'
                                             AND Player_hints.episode_id = {episode_id}
                                                     ''').fetchone()
        return hint_level

    def add_player_item(self, email, item, episode):
        # self.cursor.execute("""CREATE TABLE IF NOT EXISTS Player_hints
        #                           (
        #                           id INTEGER PRIMARY KEY,
        #                           player_id INTEGER REFERENCES PLAYERS(id),
        #                           email TEXT,
        #                           item TEXT REFERENCES Hints(item),
        #                           hint_level INTEGER DEFAULT = 1,
        #                           )
        #                        """)
        player_id = self.cursor.execute(f'''
                                    SELECT id FROM Players
                                    WHERE email = '{email}'
                                    ''').fetchone()[0]
        episode_id = self.cursor.execute(f'''
                                                                  SELECT id FROM Episodes
                                                                  WHERE box_name = "{episode}" 
                                                                  ''').fetchone()[0]
        self.cursor.execute(f'''
                            INSERT INTO Player_hints (player_id, email, item, hint_level, episode_id)
                             VALUES ({player_id}, '{email}', '{item}', 1, {episode_id})
                            
                            ''')
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

