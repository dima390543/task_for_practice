#модуль для работы с бд
import sqlite3
from config import db_file, db_name_table

class DB:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.name_table = db_name_table
        self.cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.name_table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            status TEXT,
            edo_status TEXT,
            inn TEXT,
            ogrnip TEXT,
            ogrnip_date TEXT,
            code_okvd TEXT,
            activity TEXT
        )
        ''')
        self.conn.commit()

    def insert(self, data):
        if len(data) == 11:
            full_name, status, edo_status, _, inn, _, ogrnip, _, ogrnip_date, code_okvd, activity = data# распакоука чеек
            query = 'SELECT * from InformationIp WHERE ogrnip=?'
            self.cursor.execute(query, (ogrnip,))
            if self.cursor.fetchall():
                self.cursor.execute(f"UPDATE {self.name_table} SET full_name=?, status=?, edo_status=?, inn=?, ogrnip=?, ogrnip_date=?, code_okvd=?, activity=? WHERE ogrnip=?",
                                    (full_name, status, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity, ogrnip))
            else:
                # формируем запрос с добавлением новой записи в БД
                self.cursor.execute(f"INSERT INTO {self.name_table} (full_name, status, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                    (full_name, status, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity))
                # сохраняем изменения
            self.conn.commit()
        else:
            full_name, edo_status, _, inn, _, ogrnip, _, ogrnip_date, code_okvd, activity = data
            status = None
            query = 'SELECT * from InformationIp WHERE ogrnip=?'
            self.cursor.execute(query, (ogrnip,))
            if self.cursor.fetchall():
                self.cursor.execute(
                    f"UPDATE {self.name_table} SET full_name=?, status=?, edo_status=?, inn=?, ogrnip=?, ogrnip_date=?, code_okvd=?, activity=? WHERE ogrnip=?",
                    (full_name, status, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity, ogrnip))
            else:
                # формируем запрос с добавлением новой записи в БД
                self.cursor.execute(
                    f"INSERT INTO {self.name_table} (full_name, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (full_name, edo_status, inn, ogrnip, ogrnip_date, code_okvd, activity))
            # сохраняем изменения
            self.conn.commit()
