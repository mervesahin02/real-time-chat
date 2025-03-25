import os
import psycopg2
from psycopg2 import pool
import uuid

class FileSharing:
    def __init__(self, 
                 dbname="triscord_db", 
                 user="postgres", 
                 password="your_password", 
                 host="localhost", 
                 port="5432",
                 upload_directory="uploads"):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.upload_directory = upload_directory
            os.makedirs(upload_directory, exist_ok=True)
        except (Exception, psycopg2.Error) as error:
            print("PostgreSQL bağlantısı hatası:", error)
            raise

    def create_file_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS shared_files (
            id SERIAL PRIMARY KEY,
            file_uuid UUID UNIQUE NOT NULL,
            sender TEXT NOT NULL,
            recipient TEXT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    def save_file_metadata(self, sender, recipient, file_name, file_path, file_size):
        file_uuid = uuid.uuid4()
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO shared_files 
                    (file_uuid, sender, recipient, file_name, file_path, file_size) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (file_uuid, sender, recipient, file_name, file_path, file_size))
                conn.commit()
            return file_uuid
        except Exception as e:
            print(f"Dosya meta bilgisi kaydetme hatası: {e}")
            return None
        finally:
            self.connection_pool.putconn(conn)

    def handle_file_upload(self, client_socket, sender, recipient=None):
        try:
            file_name = client_socket.recv(1024).decode()
            file_size = int(client_socket.recv(1024).decode())
            
            file_uuid = str(uuid.uuid4())
            file_path = os.path.join(self.upload_directory, f"{file_uuid}_{file_name}")
            
            with open(file_path, 'wb') as file:
                bytes_received = 0
                while bytes_received < file_size:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    bytes_received += len(data)
            
            self.save_file_metadata(sender, recipient, file_name, file_path, file_size)
            return True
        except Exception as e:
            print(f"Dosya yükleme hatası: {e}")
            return False

    def get_file_metadata(self, file_uuid):
        conn = self.connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM shared_files WHERE file_uuid = %s', (file_uuid,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Dosya meta bilgisi alma hatası: {e}")
            return None
        finally:
            self.connection_pool.putconn(conn)

    def close_connection(self):
        if hasattr(self, 'connection_pool'):
            self.connection_pool.closeall()