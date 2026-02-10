import sqlite3
from library_system.database.db import create_connection

class MemberService:
    @staticmethod
    def get_all_members(active_only=True):
        conn = create_connection()
        members = []
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM members"
                if active_only:
                    query += " WHERE is_active = 1"
                query += " ORDER BY created_at DESC"
                
                cursor.execute(query)
                members = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error fetching members: {e}")
            finally:
                conn.close()
        return members

    @staticmethod
    def search_members(keyword, active_only=True):
        conn = create_connection()
        members = []
        if conn:
            try:
                cursor = conn.cursor()
                search_term = f"%{keyword}%"
                query = """
                    SELECT * FROM members 
                    WHERE (name LIKE ? OR member_code LIKE ? OR email LIKE ?)
                """
                if active_only:
                    query += " AND is_active = 1"
                query += " ORDER BY created_at DESC"

                cursor.execute(query, (search_term, search_term, search_term))
                members = [dict(row) for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error searching members: {e}")
            finally:
                conn.close()
        return members

    @staticmethod
    def add_member(member_code, name, email, phone, address):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO members (member_code, name, email, phone, address, is_active)
                    VALUES (?, ?, ?, ?, ?, 1)
                """
                cursor.execute(query, (member_code, name, email, phone, address))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                print("Error: Member code must be unique.")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def update_member(member_id, member_code, name, email, phone, address):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    UPDATE members 
                    SET member_code=?, name=?, email=?, phone=?, address=?
                    WHERE id=?
                """
                cursor.execute(query, (member_code, name, email, phone, address, member_id))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error updating member: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def delete_member(member_id):
        """Soft delete member by setting is_active to 0."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE members SET is_active=0 WHERE id=?"
                cursor.execute(query, (member_id,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error deleting member: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def activate_member(member_id):
        """Re-activate member by setting is_active to 1."""
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE members SET is_active=1 WHERE id=?"
                cursor.execute(query, (member_id,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error activating member: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def generate_member_code():
        """Auto-generate a simple unique code."""
        # This is a simplistic approach. Better to check max ID + 1
        conn = create_connection()
        code = "MEM001"
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(id) FROM members")
                max_id = cursor.fetchone()[0]
                next_id = (max_id or 0) + 1
                code = f"MEM{next_id:03d}"
            except Exception:
                pass
            finally:
                conn.close()
        return code
