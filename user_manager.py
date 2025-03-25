import psycopg2
from psycopg2 import pool
import hashlib

class UserManager:
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

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_users_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            email VARCHAR(100),
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    def register_user(self, username, password, email=None):
        hashed_password = self.hash_password(password)
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', 
                    (username, hashed_password, email)
                )
                conn.commit()
                return True
        except psycopg2.IntegrityError:
            print("Kullanıcı adı zaten mevcut")
            return False
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return False
        finally:
            self.connection_pool.putconn(conn)

    def validate_login(self, username, password):
        hashed_password = self.hash_password(password)
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM users WHERE username = %s AND password = %s', 
                    (username, hashed_password)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Giriş doğrulama hatası: {e}")
            return False
        finally:
            self.connection_pool.putconn(conn)

    def close_connection(self):
        if hasattr(self, 'connection_pool'):
            self.connection_pool.closeall()