import psycopg2
from psycopg2 import pool
from datetime import datetime

class MessageLogger:
    def __init__(self, 
                 dbname="triscord_db", 
                 user="postgres", 
                 password="your_password", 
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

    def create_messages_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            sender TEXT NOT NULL,
            recipient TEXT,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_private BOOLEAN DEFAULT FALSE
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

    def log_message(self, sender, message, recipient=None, is_private=False):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO messages (sender, recipient, message, is_private) 
                    VALUES (%s, %s, %s, %s)
                ''', (sender, recipient, message, is_private))
                conn.commit()
        except Exception as e:
            print(f"Mesaj kaydetme hatası: {e}")
        finally:
            self.connection_pool.putconn(conn)

    def get_message_history(self, username, limit=50):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT sender, recipient, message, timestamp, is_private
                    FROM messages 
                    WHERE sender = %s OR recipient = %s OR recipient IS NULL
                    ORDER BY timestamp DESC
                    LIMIT %s
                ''', (username, username, limit))
                return cursor.fetchall()
        except Exception as e:
            print(f"Mesaj geçmişi alma hatası: {e}")
            return []
        finally:
            self.connection_pool.putconn(conn)

    def close_connection(self):
        if hasattr(self, 'connection_pool'):
            self.connection_pool.closeall()