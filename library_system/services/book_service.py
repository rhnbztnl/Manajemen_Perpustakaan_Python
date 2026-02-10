from library_system.database.db import create_connection

class BookService:
    @staticmethod
    def get_all_books():
        conn = create_connection()
        books = []
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT b.id, b.title, b.author, b.publisher, b.year, b.stock, c.name as category
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                    ORDER BY b.created_at DESC
                """
                cursor.execute(query)
                books = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error fetching books: {e}")
            finally:
                conn.close()
        return books

    @staticmethod
    def search_books(keyword):
        conn = create_connection()
        books = []
        if conn:
            try:
                cursor = conn.cursor()
                search_term = f"%{keyword}%"
                query = """
                    SELECT b.id, b.title, b.author, b.publisher, b.year, b.stock, c.name as category
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                    WHERE b.title LIKE ? OR b.author LIKE ?
                    ORDER BY b.created_at DESC
                """
                cursor.execute(query, (search_term, search_term))
                books = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error searching books: {e}")
            finally:
                conn.close()
        return books

    @staticmethod
    def add_book(title, author, publisher, year, stock, category_id):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO books (title, author, publisher, year, stock, category_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query, (title, author, publisher, int(year), int(stock), int(category_id)))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error adding book: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def update_book(book_id, title, author, publisher, year, stock, category_id):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE books 
                    SET title=?, author=?, publisher=?, year=?, stock=?, category_id=?
                    WHERE id=?
                """
                cursor.execute(query, (title, author, publisher, int(year), int(stock), int(category_id), book_id))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error updating book: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def delete_book(book_id):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "DELETE FROM books WHERE id=?"
                cursor.execute(query, (book_id,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error deleting book: {e}")
                return False
            finally:
                conn.close()
        return False
    
    @staticmethod
    def get_categories():
        conn = create_connection()
        categories = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM categories")
                categories = [dict(row) for row in cursor.fetchall()]
            finally:
                conn.close()
        return categories
