import sqlite3
from datetime import datetime

class TaskModel:
    def __init__(self, db_path='tasks.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT,
            tags TEXT,
            subtasks TEXT,
            repeating TEXT,
            reminder TEXT,
            completed_at TEXT
        )''')
        conn.commit()
        conn.close()

    def add_task(self, title, desc, priority, due_date, tags, subtasks='', repeating='', reminder=''):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO tasks (title, description, priority, due_date, tags, subtasks, repeating, reminder, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (title, desc, priority, due_date, tags, subtasks, repeating, reminder, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        last_id = c.lastrowid
        conn.close()
        return last_id

    def get_all_tasks(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = c.fetchall()
        conn.close()
        return tasks

    def complete_task(self, task_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?', ('Completed', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), task_id))
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        
    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        total = c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
        pending = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Pending'").fetchone()[0]
        completed = c.execute("SELECT COUNT(*) FROM tasks WHERE status='Completed'").fetchone()[0]
        conn.close()
        return {'total': total, 'pending': pending, 'completed': completed}