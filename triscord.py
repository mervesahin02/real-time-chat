import os
import sys
import socket
import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon
from datetime import datetime
from user_manager import UserManager
from user_profiles import UserProfile
from message_logger import MessageLogger
from file_sharing import FileSharing


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# İkonu URL'den indirip bir dosyaya kaydetme
url = "https://assets-btkakademi-gov-tr.akamaized.net/api/gallery/51/bb2b1a79-8a7f-4c18-970c-6687a910b496/BTKAkademi-Normal.png?t=1739345573413"
icon_path = "icon.png"  # Kaydedilecek dosya adı
nickname = ""
emoji_list = ["😀", "😂", "😍", "😊", "😎", "😢", "😭", "😡", "👍", "👎", "💪", "🙏", "🔥", "🎉", "💯", "💔", "❤️", "🥳", "😅", "🤔", "🤷‍♂️",
          "🤷‍♀️", "🙌", "👏", "😴"]
target_user = None


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triscord'a Giriş Yap")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 300, 250)
        self.center()

        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # Kullanıcı adı input
        self.nickname_input = QtWidgets.QLineEdit(self)
        self.nickname_input.setPlaceholderText("Kullanıcı adınızı girin...")
        layout.addWidget(self.nickname_input)

        # Şifre input
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Şifrenizi girin...")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Email input (for registration)
        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setPlaceholderText("E-posta adresinizi girin (isteğe bağlı)...")
        layout.addWidget(self.email_input)

        # Buton layout
        button_layout = QtWidgets.QHBoxLayout()

        # Giriş butonu
        self.login_button = QtWidgets.QPushButton("Giriş", self)
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        # Kayıt butonu
        self.register_button = QtWidgets.QPushButton("Kayıt Ol", self)
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        global nickname
        nickname = self.nickname_input.text()
        password = self.password_input.text()

        user_manager = UserManager()
        if user_manager.validate_login(nickname, password):
            # Create user profile if not exists
            user_profile = UserProfile()
            if not user_profile.get_profile(nickname):
                user_profile.create_profile(nickname)

            self.close()
            self.chat_window = ChatWindow()
            receive_thread = threading.Thread(target=receive_messages, args=(self.chat_window,))
            receive_thread.start()
            self.chat_window.message_input.setFocus()
            self.chat_window.show()
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre")

    def register(self):
        nickname = self.nickname_input.text()
        password = self.password_input.text()
        email = self.email_input.text() or None

        if not nickname or not password:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre zorunludur")
            return

        user_manager = UserManager()
        if user_manager.register_user(nickname, password, email):
            # Automatically create a profile for the new user
            user_profile = UserProfile()
            user_profile.create_profile(nickname)

            QMessageBox.information(self, "Başarılı", "Kayıt işlemi başarıyla tamamlandı!")
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı kaydı başarısız oldu. Kullanıcı adı zaten mevcut olabilir.")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.login()

class ChatWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        global emoji_list
        global nickname
        screen = QDesktopWidget().screenGeometry()
        window_width = int(screen.width() / 2)
        window_height = int(screen.height() / 2)

        #Pencere ayarları
        self.setWindowTitle("Triscord")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100,100,window_width,window_height)
        self.center()

        #Sohbet başlığı etiketi
        self.chat_label = QtWidgets.QLabel("Sohbet",self)
        self.chat_label.setGeometry(QtCore.QRect(10,0,window_width-200,20))
        self.chat_label.setAlignment(QtCore.Qt.AlignCenter)

        #Sohbet Alanı
        self.chat_area = QtWidgets.QTextEdit(self)
        self.chat_area.setGeometry(QtCore.QRect(10,30,window_width-200,window_height-180))
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #F0F0F0; padding: 10px; font-size: 14px;")

        #Online kullanıcı başlığı etiketi
        self.user_label = QtWidgets.QLabel("Online Kullanıcılar",self)
        self.user_label.setGeometry(QtCore.QRect(window_width - 180, 0,160,20))
        self.user_label.setAlignment(QtCore.Qt.AlignCenter)
        #Kullanıcı Listesi
        self.user_list = QtWidgets.QListWidget(self)
        self.user_list.setGeometry(QtCore.QRect(window_width - 180,30,160,window_height-180))
        self.user_list.setStyleSheet("background-color: #E8E8E8; padding: 10px; font-size: 12px;")
        self.user_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.user_list.customContextMenuRequested.connect(self.show_context_menu)

        self.message_label = QtWidgets.QLabel("",self)
        self.message_label.setGeometry(QtCore.QRect(10,window_height-140,window_width-200,20))

        self.clear_target_button = QtWidgets.QPushButton("X",self)
        self.clear_target_button.hide()
        self.clear_target_button.setGeometry(QtCore.QRect(window_width-180, window_height-140 ,30,20))
        self.clear_target_button.clicked.connect(self.clear_target)
        #Mesaj yazma alanı
        self.message_input = QtWidgets.QLineEdit(self)
        self.message_input.setGeometry(QtCore.QRect(10,window_height - 110, window_width - 240, 30))
        self.message_input.setPlaceholderText("Mesajınızı yazın...")
        self.message_input.setStyleSheet("background-color: #FFFFFF; padding: 5px; font-size: 14px;")

        #Emoji butonu
        self.emoji_buton = QtWidgets.QPushButton("😁",self)
        self.emoji_buton.setGeometry(QtCore.QRect(window_width - 220, window_height - 110,40,30))
        self.emoji_buton.clicked.connect(self.open_emoji_picker)

        #Gönder butonu
        self.send_button = QtWidgets.QPushButton("Gönder",self)
        self.send_button.setGeometry(QtCore.QRect(window_width - 160, window_height- 110, 100,30))
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("background-color: #4CAF50; color: white;  font-weight: bold;")
        
    def show_context_menu(self,pos):
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("QMenu {background-color: #333; color: white;}")
        private_msg_action = menu.addAction("Özel Mesaj Gönder")
        view_profile_action = menu.addAction("Kullanıcı Profilini Görüntüle")
        action = menu.exec_(self.user_list.mapToGlobal(pos))
        if action==private_msg_action:
            self.set_private_message_target()
        elif action==view_profile_action:
            self.view_user_profile()
            
    def view_user_profile(self):
        selected_user = self.user_list.currentItem()
        if selected_user:
            user_profile = f'Kullanıcı: {selected_user.text()}\n'
            QtWidgets.QMessageBox.information(self,"Kullanıcı Profili",user_profile)
            
    def clear_target(self):
        global target_user
        target_user = None
        self.message_label.setText("")
        self.clear_target_button.hide()
        
    def set_private_message_target(self):
        global target_user
        selected_user = self.user_list.currentItem()
        if selected_user:
            target_user = selected_user.text()
            if target_user == nickname:
                QtWidgets.QMessageBox.warning(self,"Hata","Kendinize mesaj gönderemezsiniz.")
                target_user=None
                return
            else:
                self.message_label.setText(f"{target_user} adlı kişiye özel mesaj gönderiyorsunuz.")
                self.clear_target_button.show()
                
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def open_emoji_picker(self):
        emoji_dialog = QtWidgets.QDialog(self)
        emoji_dialog.setWindowTitle("Emoji Seçici")
        emoji_dialog.setGeometry(100,100,300,150,)
        self.center()
        grid_layout = QtWidgets.QGridLayout(emoji_dialog)

        row, col = 0,0
        for emoji in emoji_list:
            button = QtWidgets.QPushButton(emoji,emoji_dialog)
            button.setFixedSize(40,40)
            button.clicked.connect(lambda _, e=emoji: self.add_emoji(e,emoji_dialog))
            grid_layout.addWidget(button,row,col)
            col +=1
            if col>4:
                col = 0
                row +=1
        emoji_dialog.exec_()
        
    def add_emoji(self,emoji,dialog):
        self.message_input.setText(self.message_input.text()+emoji)
        dialog.accept()
        
    def update_user_list(self,message):
        users = message.split(":")[1].split(",")
        self.user_list.clear()
        self.user_list.addItems(users)
        
    def receive_message(self,message):
        if message.startswith('USER_LIST'):
            self.update_user_list(message)
        elif message.startswith('PRIVATE'):
            parts = message.split(":")
            target_user = parts[1]
            private_message = ":".join(parts[2:])
            if target_user == nickname:
                self.chat_area.append(f"Size özel olarak gönderilen mesaj: {private_message}")
        else:
            self.chat_area.append(message)
            
    def closeEvent(self, event):
        client.close()
        event.accept()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.send_message()
            
    def send_message(self):
        global target_user
        message = self.message_input.text()
        if message.strip():
            timestamp = datetime.now().strftime('%H:%M:%S')
            if target_user:
                full_message = f'[{timestamp}] [Özel] {nickname} -> {target_user}: {message}'
                client.send(f'PRIVATE:{target_user}:{full_message}'.encode('utf-8'))
                self.chat_area.append(f'Size özel olarak {target_user} adlı kişiye mesaj gönderildi: {message}')
            else:
                full_message = f'[{timestamp}] {nickname}: {message}'
                self.chat_area.append(full_message)
                client.send(full_message.encode('utf-8'))
            self.message_input.clear()
            
    def send_message(self):
        global target_user
        message = self.message_input.text()
        if message.strip():
            timestamp = datetime.now().strftime('%H:%M:%S')
            message_logger = MessageLogger()
        
            if target_user:
                full_message = f'[{timestamp}] [Özel] {nickname} -> {target_user}: {message}'
                client.send(f'PRIVATE:{target_user}:{full_message}'.encode('utf-8'))
                message_logger.log_message(nickname, message, recipient=target_user, is_private=True)
                self.chat_area.append(f'Size özel olarak {target_user} adlı kişiye mesaj gönderildi: {message}')
            else:
                full_message = f'[{timestamp}] {nickname}: {message}'
                self.chat_area.append(full_message)
                client.send(full_message.encode('utf-8'))
                message_logger.log_message(nickname, message)
        
            self.message_input.clear()
            
def receive_messages(chat_window):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message=='NICK':
                client.send(nickname.encode('utf-8'))
            else:
                messages = message.split("!")
                for msg in messages:
                    if msg:
                        chat_window.receive_message(msg)
        except:
            print("Sunucuyla bağlantı koptu!")
            client.close()
            break

def main():
    # Database initialization
    user_manager = UserManager()
    user_manager.create_users_table()
    
    user_profile = UserProfile()
    user_profile.create_profiles_table()
    
    message_logger = MessageLogger()
    message_logger.create_messages_table()
    
    file_sharing = FileSharing()
    file_sharing.create_file_table()

    try:
        client.connect(('localhost',54321))
    except:
        print("Sunucuya bağlanılmadı!")
        sys.exit()

    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

main()