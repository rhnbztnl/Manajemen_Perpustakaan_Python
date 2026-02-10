import sqlite3
import os
from datetime import datetime
from library_system.utils.paths import AppPaths

def get_db_path():
    # Use cross-platform path
    return str(AppPaths.get_db_path())

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        db_file = get_db_path()
        # [DEBUG] Print exact DB path being used
        # print(f"[DEBUG] Connecting to DB: {db_file}") 
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] Error connecting to database at {db_file}: {e}")
    return conn

def initialize_db():
    """Initialize the database tables and default data."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Categories Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """)

            # Books Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                year INTEGER,
                stock INTEGER DEFAULT 0,
                category_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
            """)

            # Members Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Loans Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                loan_date DATE,
                return_date DATE,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (book_id) REFERENCES books (id),
                FOREIGN KEY (member_id) REFERENCES members (id)
            );
            """)

            # Seed Categories if empty
            cursor.execute("SELECT count(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                categories = [('Pemrograman',), ('Desain',), ('Jaringan',), ('Sains',), ('Bisnis',)]
                cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories)

            # Seed Books if empty (Dummy Data)
            cursor.execute("SELECT count(*) FROM books")
            if cursor.fetchone()[0] == 0:
                books = [
                    ("Belajar Python Dasar", "Budi Santoso", "Informatika", 2023, 10, 1),
                    ("Mastering UI/UX", "Doni Pratama", "Elex Media", 2024, 5, 2),
                    ("Jaringan Komputer Modern", "Eko Salim", "Andi Offset", 2022, 8, 3),
                ]
                cursor.executemany("""
                    INSERT INTO books (title, author, publisher, year, stock, category_id) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, books)
                print("Dummy data inserted.")

            conn.commit()
            print("Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    initialize_db()
