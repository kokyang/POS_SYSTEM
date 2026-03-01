import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='grocery_store.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')

        # Migrations: add columns if they don't exist yet
        try:
            cursor.execute('ALTER TABLE items ADD COLUMN image_url TEXT')
            conn.commit()
        except Exception:
            pass  # Column already exists

        try:
            cursor.execute('ALTER TABLE items ADD COLUMN barcode TEXT')
            conn.commit()
        except Exception:
            pass  # Column already exists
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT NOT NULL,
                total_amount REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        ''')
        
        conn.commit()
        conn.close()
