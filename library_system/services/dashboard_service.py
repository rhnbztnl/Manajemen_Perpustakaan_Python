import sqlite3
from datetime import date, timedelta
from library_system.database.db import create_connection

class DashboardService:
    @staticmethod
    def get_kpi_stats():
        stats = {
            "books_available": 0,
            "books_borrowed": 0,
            "total_overdue": 0,
            "active_members": 0
        }
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Books Available (Sum of stock)
                cursor.execute("SELECT SUM(stock) FROM books")
                res = cursor.fetchone()[0]
                stats["books_available"] = res if res else 0
                
                # Books Borrowed
                cursor.execute("SELECT COUNT(*) FROM loans WHERE status = 'borrowed'")
                stats["books_borrowed"] = cursor.fetchone()[0]
                
                # Active Members
                cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = 1")
                stats["active_members"] = cursor.fetchone()[0]
                
                # Total Overdue (Status borrowed AND loan_date < 7 days ago)
                cursor.execute("""
                    SELECT COUNT(*) FROM loans 
                    WHERE status = 'borrowed' 
                    AND date(loan_date, '+7 days') < date('now')
                """)
                stats["total_overdue"] = cursor.fetchone()[0]
                
            except Exception as e:
                print(f"Error dashboard stats: {e}")
            finally:
                conn.close()
        return stats

    @staticmethod
    def get_urgent_tasks(limit=5):
        tasks = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Overdue items
                query = """
                    SELECT 
                        l.id, m.name as member_name, b.title as book_title, 
                        date(l.loan_date, '+7 days') as due_date
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    WHERE l.status = 'borrowed' 
                    AND date(l.loan_date, '+7 days') < date('now')
                    ORDER BY due_date ASC
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
                tasks = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error urgent tasks: {e}")
            finally:
                conn.close()
        return tasks

    @staticmethod
    def get_recent_activity(limit=10):
        activity = []
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Combine Loans and Returns
                # We select type, date, member, book
                query = """
                    SELECT 
                        'Pinjam' as type, 
                        l.loan_date as activity_date,
                        m.name as member_name,
                        b.title as book_title
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    
                    UNION ALL
                    
                    SELECT 
                        'Kembali' as type, 
                        l.return_date as activity_date,
                        m.name as member_name,
                        b.title as book_title
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    WHERE l.return_date IS NOT NULL
                    
                    ORDER BY activity_date DESC
                    LIMIT ?
                """
                cursor.execute(query, (limit,))
                activity = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error recent activity: {e}")
            finally:
                conn.close()
        return activity
