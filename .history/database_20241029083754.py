# database.py
import sqlite3
from datetime import datetime

def connect():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY, 
            isbn TEXT, 
            title TEXT, 
            author TEXT, 
            year INTEGER, 
            borrowed BOOLEAN DEFAULT 0,
            borrow_time TEXT,
            return_time TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_book(isbn, title, author, year):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    
    try:
        # Attempt to insert the book
        cur.execute("INSERT INTO books (isbn, title, author, year, borrowed) VALUES (?, ?, ?, ?, 0)", 
                    (isbn, title, author, year))
        conn.commit()
        print("Book added successfully.")
    except sqlite3.IntegrityError:
        print("Error: A book with this ISBN already exists in the database.")
    finally:
        conn.close()


def borrow_book(isbn):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    borrow_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update borrowed status, set borrow_time, and clear return_time
    cur.execute("UPDATE books SET borrowed = 1, borrow_time = ?, return_time = NULL WHERE isbn = ?", (borrow_time, isbn))
    
    conn.commit()
    conn.close()

def return_book(isbn):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    return_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE books SET borrowed = 0, return_time = ? WHERE isbn = ?", (return_time, isbn))
    conn.commit()
    conn.close()

def search_book_by_isbn(isbn):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    book = cur.fetchone()
    conn.close()
    return book

def fetch_all_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return books

def search_books_by_title(title):
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("SELECT isbn, title, author, year, borrowed FROM books WHERE title LIKE ?", ('%' + title + '%',))
    results = cur.fetchall()
    conn.close()
    return results