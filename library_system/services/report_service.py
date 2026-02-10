import sqlite3
from datetime import date
from library_system.database.db import create_connection

class ReportService:
    @staticmethod
    def get_summary_stats(fine_per_day=0):
        stats = {
            "total_books": 0,
            "active_members": 0,
            "active_loans": 0,
            "overdue_count": 0,
            "total_fines": 0
        }
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Total Books
                cursor.execute("SELECT COUNT(*) FROM books")
                stats["total_books"] = cursor.fetchone()[0]
                
                # Active Members
                cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = 1")
                stats["active_members"] = cursor.fetchone()[0]
                
                # Active Loans
                cursor.execute("SELECT COUNT(*) FROM loans WHERE status = 'borrowed'")
                stats["active_loans"] = cursor.fetchone()[0]
                
                # Overdue & Fines
                # We need to calculate this manually since we don't have a fines table
                # Get all borrowed loans that are overdue
                cursor.execute("""
                    SELECT loan_date FROM loans 
                    WHERE status = 'borrowed' 
                    AND date(loan_date, '+7 days') < date('now')
                """)
                overdue_loans = cursor.fetchall()
                stats["overdue_count"] = len(overdue_loans)
                
                if fine_per_day > 0:
                    total_fines = 0
                    today = date.today()
                    for row in overdue_loans:
                        loan_date = date.fromisoformat(row['loan_date'])
                        delta = (today - loan_date).days
                        overdue_days = delta - 7
                        if overdue_days > 0:
                            total_fines += (overdue_days * fine_per_day)
                    stats["total_fines"] = total_fines
                
            except Exception as e:
                print(f"Error stats: {e}")
            finally:
                conn.close()
        return stats

    @staticmethod
    def get_loans_by_period(start_date, end_date):
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT l.id, b.title, m.name, l.loan_date, l.return_date, l.status
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    WHERE l.loan_date BETWEEN ? AND ?
                    ORDER BY l.loan_date DESC
                """
                cursor.execute(query, (start_date, end_date))
                data = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error loans period: {e}")
            finally:
                conn.close()
        return data

    @staticmethod
    def get_popular_books(limit=10):
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT b.title, b.author, COUNT(l.id) as borrow_count 
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    GROUP BY l.book_id
                    ORDER BY borrow_count DESC
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
                data = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error popular books: {e}")
            finally:
                conn.close()
        return data
        
    @staticmethod
    def get_never_borrowed_books():
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT b.title, b.author, c.name as category, b.stock
                    FROM books b
                    LEFT JOIN categories c ON b.category_id = c.id
                    LEFT JOIN loans l ON b.id = l.book_id
                    WHERE l.id IS NULL
                    ORDER BY b.title ASC
                """
                cursor.execute(query)
                data = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error never borrowed: {e}")
            finally:
                conn.close()
        return data

    @staticmethod
    def get_active_members(limit=10):
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT m.name, m.member_code, COUNT(l.id) as borrow_count 
                    FROM loans l
                    JOIN members m ON l.member_id = m.id
                    GROUP BY l.member_id
                    ORDER BY borrow_count DESC
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
                data = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error active members: {e}")
            finally:
                conn.close()
        return data

    @staticmethod
    def get_overdue_loans():
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Status 'borrowed' AND loan_date < 7 days ago
                query = """
                    SELECT 
                        l.id, m.name as member_name, b.title as book_title, l.loan_date
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    WHERE l.status = 'borrowed' 
                    AND date(l.loan_date, '+7 days') < date('now')
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                
                # Calculate days overdue
                today = date.today()
                result = []
                for row in rows:
                    r = dict(row)
                    loan_date = date.fromisoformat(r['loan_date'])
                    delta = (today - loan_date).days
                    days_overdue = delta - 7
                    r['days_overdue'] = days_overdue
                    result.append(r)
                
                # Sort by days overdue descending
                result.sort(key=lambda x: x['days_overdue'], reverse=True)
                data = result
                
            except Exception as e:
                print(f"Error overdue: {e}")
            finally:
                conn.close()
        return data
    
    @staticmethod
    def get_low_stock_books(limit=20):
        data = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    SELECT title, author, stock
                    FROM books
                    WHERE stock < 3
                    ORDER BY stock ASC
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
                data = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error low stock: {e}")
            finally:
                conn.close()
        return data
