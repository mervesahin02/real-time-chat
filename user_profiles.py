import psycopg2
from psycopg2 import pool
from datetime import datetime

class UserProfile:
    
    def __init__(self, 
                 dbname="triscord_db", 
                 user="postgres", 
                 password="HappyCat", 
                 host="localhost", 
                 port="5432"):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
        except (Exception, psycopg2.Error) as error:
            print("PostgreSQL bağlantısı hatası:", error)
            raise

    def create_profiles_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_profiles (
            username TEXT PRIMARY KEY,
            full_name TEXT,
            avatar_path TEXT,
            status TEXT DEFAULT 'Çevrimiçi',
            bio TEXT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP
        )
        """
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(create_table_query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Tablo oluşturma hatası:", error)
        finally:
            self.connection_pool.putconn(conn)

    def create_profile(self, username, full_name=None, avatar_path=None, bio=None):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO user_profiles 
                    (username, full_name, avatar_path, bio) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE 
                    SET full_name = %s, avatar_path = %s, bio = %s
                ''', (
                    username, full_name, avatar_path, bio,
                    full_name, avatar_path, bio
                ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Profil oluşturma hatası: {e}")
            return False
        finally:
            self.connection_pool.putconn(conn)

    def update_status(self, username, status):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    UPDATE user_profiles 
                    SET status = %s, last_active = CURRENT_TIMESTAMP 
                    WHERE username = %s
                ''', (status, username))
            conn.commit()
        except Exception as e:
            print(f"Durum güncelleme hatası: {e}")
        finally:
            self.connection_pool.putconn(conn)

    def get_profile(self, username):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM user_profiles WHERE username = %s', (username,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Profil alma hatası: {e}")
            return None
        finally:
            self.connection_pool.putconn(conn)

    def close_connection(self):
        if hasattr(self, 'connection_pool'):
            self.connection_pool.closeall()