import sqlite3
from datetime import date
from library_system.database.db import create_connection

class LoanService:
    @staticmethod
    def get_all_loans():
        conn = create_connection()
        loans = []
        if conn:
            try:
                cursor = conn.cursor()
                # Join with books and members to get names instead of IDs
                query = """
                    SELECT 
                        l.id, 
                        l.loan_date, 
                        l.return_date, 
                        l.status,
                        b.title as book_title,
                        m.name as member_name,
                        m.member_code
                    FROM loans l
                    JOIN books b ON l.book_id = b.id
                    JOIN members m ON l.member_id = m.id
                    ORDER BY l.loan_date DESC
                """
                cursor.execute(query)
                loans = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error fetching loans: {e}")
            finally:
                conn.close()
        return loans

    @staticmethod
    def borrow_book(member_id, book_id):
        conn = create_connection()
        if not conn:
            return False, "Database connection failed"
            
        try:
            cursor = conn.cursor()
            
            # 1. Validate Member (Must be active)
            cursor.execute("SELECT is_active, name FROM members WHERE id = ?", (member_id,))
            member = cursor.fetchone()
            if not member:
                return False, "Member not found"
            if member['is_active'] != 1:
                return False, f"Member '{member['name']}' is not active"

            # 2. Validate Book (Stock > 0)
            cursor.execute("SELECT stock, title FROM books WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if not book:
                return False, "Book not found"
            if book['stock'] <= 0:
                return False, f"Book '{book['title']}' is out of stock"

            # 3. Check for existing active loan of SAME book
            cursor.execute("""
                SELECT id FROM loans 
                WHERE member_id = ? AND book_id = ? AND status = 'borrowed'
            """, (member_id, book_id))
            if cursor.fetchone():
                return False, "Member is already borrowing this book"

            # 3b. Check MAX BOOKS limit
            from library_system.managers.settings_manager import SettingsManager
            settings = SettingsManager()
            max_books = int(settings.get("loans/max_books", 3))
            
            cursor.execute("""
                SELECT COUNT(*) FROM loans 
                WHERE member_id = ? AND status = 'borrowed'
            """, (member_id,))
            current_loans = cursor.fetchone()[0]
            
            if current_loans >= max_books:
                return False, f"Member has reached the limit of {max_books} books"

            # 4. Transaction: Insert Loan + Update Stock
            today = date.today().isoformat()
            
            cursor.execute("""
                INSERT INTO loans (book_id, member_id, loan_date, status)
                VALUES (?, ?, ?, 'borrowed')
            """, (book_id, member_id, today))
            
            cursor.execute("""
                UPDATE books SET stock = stock - 1 WHERE id = ?
            """, (book_id,))
            
            conn.commit()
            return True, "Book borrowed successfully"

        except Exception as e:
            conn.rollback()
            print(f"Error borrowing book: {e}")
            return False, str(e)
        finally:
            conn.close()

    @staticmethod
    def return_book(loan_id):
        conn = create_connection()
        if not conn:
            return False, "Database connection failed"
            
        try:
            cursor = conn.cursor()
            
            # 1. Get Loan Details
            cursor.execute("SELECT book_id, loan_date, status FROM loans WHERE id = ?", (loan_id,))
            loan = cursor.fetchone()
            
            if not loan:
                return False, "Loan not found"
            
            if loan['status'] != 'borrowed':
                return False, "Book is not currently borrowed"

            book_id = loan['book_id']
            loan_date_str = loan['loan_date']
            
            # 2. Determine Status (Overdue or Returned)
            today = date.today()
            loan_date = date.fromisoformat(loan_date_str)
            
            # Use Settings for Duration
            from library_system.managers.settings_manager import SettingsManager
            settings = SettingsManager()
            duration = int(settings.get("loans/duration_days", 7))
            
            delta = (today - loan_date).days
            new_status = 'overdue' if delta > duration else 'returned'
            
            # 3. Transaction
            today_str = today.isoformat()
            
            cursor.execute("""
                UPDATE loans 
                SET return_date = ?, status = ? 
                WHERE id = ?
            """, (today_str, new_status, loan_id))
            
            cursor.execute("""
                UPDATE books SET stock = stock + 1 WHERE id = ?
            """, (book_id,))
            
            conn.commit()
            return True, f"Book returned ({new_status})"

        except Exception as e:
            conn.rollback()
            print(f"Error returning book: {e}")
            return False, str(e)
        finally:
            conn.close()
