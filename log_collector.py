import sqlite3
from datetime import datetime, timedelta

class LogCollector:
    def __init__(self, db_name='logs.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()
        self.create_archive_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_level TEXT,
                message TEXT
            )
        ''')
        self.conn.commit()

    def create_archive_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS archived_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_level TEXT,
                message TEXT
            )
        ''')
        self.conn.commit()

    def add_log(self, log_level, message):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO logs (timestamp, log_level, message)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), log_level, message))
        self.conn.commit()

    def get_logs(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC')
        return cursor.fetchall()

    def delete_log(self, log_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM logs WHERE id = ?', (log_id,))
        self.conn.commit()

    def filter_logs(self, log_level, start_date, end_date):
        query = 'SELECT * FROM logs WHERE 1=1'
        params = []
        if log_level:
            query += ' AND log_level = ?'
            params.append(log_level)
        if start_date:
            query += ' AND timestamp >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND timestamp <= ?'
            params.append(end_date)
        query += ' ORDER BY timestamp DESC'
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def archive_logs(self, days_old=30):
        threshold_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO archived_logs (timestamp, log_level, message)
            SELECT timestamp, log_level, message FROM logs
            WHERE timestamp < ?
        ''', (threshold_date,))
        cursor.execute('DELETE FROM logs WHERE timestamp < ?', (threshold_date,))
        self.conn.commit()
log_collector = LogCollector()