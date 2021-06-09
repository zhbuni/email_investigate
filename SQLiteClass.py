import sqlite3

# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# Создание таблицы

# id, episode_id, first_name, last_name
suspects = [
    (1, 'МАКСИМ', 'ИВАНОВ'),
    (2, 'ИГОРЬ', 'СМИРНОВ'),
    (3, 'АЛЕКСЕЙ', 'СИДОРОВ'),
    (4, 'АНДРЕЙ', 'ВОРОБЬЁВ'),
    (5, 'ЕВГЕНИЙ', 'ПЕТРОВ'),
    (6, 'СЕРГЕЙ', 'КАБАЧКОВ'),
    (7, 'ДЕНИС', 'ПЕТРУШКИН'),
    (8, 'ИВАН', 'МАКАРОВ'),
    (9, 'МИХАИЛ', 'ПЕЛЬМЕШКИН'),
    (10, 'КОНСТАНТИН', 'СОСИСЬКИН'),
]

# id, episode, suspect_id
episodes = [
    (1, 'АФТ001'),
    (2, 'АФТ002'),
    (3, 'АФТ003'),
    (4, 'АФТ004'),
    (5, 'АФТ005'),
    (6, 'АФТ006'),
    (7, 'АФТ000'),
]

answers = [
    #id, episode_id, suspect_id, answer
    (1, 1, 1, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (2, 1, 2, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (3, 2, 3, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (4, 2, 4, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (5, 3, 5, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (6, 3, 6, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (7, 4, 7, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (8, 5, 8, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    (9, 6, 9, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
]

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
        self.cursor.executemany("INSERT INTO Suspects VALUES (?, ?, ?);", suspects)
        self.cursor.executemany("INSERT INTO Episodes VALUES (?, ?);", episodes)
        self.cursor.executemany("INSERT INTO Hints VALUES (?, ?, ?, ?, ?);", hints)
        self.cursor.executemany("INSERT INTO Answers VALUES (?, ?, ?, ?);", answers)
        self.conn.commit()

    def create_db(self):
        """Создать таблицу если её нет"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Suspects
                  (
                  id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT
                  )
               """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Episodes
                  (
                  id INTEGER PRIMARY KEY,
                  box_name TEXT
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
                          answer TEXT,
                          FOREIGN KEY (episode_id) REFERENCES Episodes(id),
                          FOREIGN KEY (suspect_id) REFERENCES Suspects(id)
                          )
                       """)

    def drop_db(self):
        self.cursor.execute('''DROP TABLE Answers''')
        self.cursor.execute('''DROP TABLE Episodes''')
        self.cursor.execute('''DROP TABLE Hints''')
        self.cursor.execute('''DROP TABLE Suspects''')

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
        query = '''
                SELECT e.box_name, h.episode_id, s.first_name, s.last_name, h.item, h.hint, h.answer
                    from Episodes as e
                    JOIN Suspects as s on e.id = s.episode_id
                    JOIN Hints as h on e.id = h.episode_id
                    WHERE e.box_name LIKE "%{}%"
                '''.format(box_name)
        self.cursor.execute(query)
        arr = self.cursor.fetchall()
        print(arr)

    def check_suspect(self, episode, first_name, last_name):
        """Проверить подозреваемого"""
        sql = '''
        SELECT answer from Answers as a
        JOIN Episodes as e on a.episode_id = e.id
        JOIN Suspects as s on a.suspect_id = s.id
        WHERE s.first_name LIKE "{}" AND last_name LIKE "{}"
        AND e.box_name LIKE "{}"
        '''.format(first_name, last_name, episode)
        # print(sql)
        self.cursor.execute(sql)
        boo = self.cursor.fetchone()
        print(boo)
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

