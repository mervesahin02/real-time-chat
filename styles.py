# styles.py
from PyQt5.QtCore import Qt

def get_login_window_style():
    return """
    QWidget {
        background-color: #3674B5;
        color: #FFFFFF;
        font-family: Arial;
    }
    QLineEdit {
        padding: 10px;
        border: 2px solid #578FCA;
        border-radius: 10px;
        background-color: #D1F8EF;
        color: #3674B5;
        margin-bottom: 10px;
    }
    QPushButton {
        background-color: #D1F8EF;
        color: #578FCA;
        border: none;
        padding: 10px;
        border-radius: 10px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #A1E3F9;
    }
    """

def get_chat_window_style():
    return """
    QWidget {
        background-color: #3673674B54B5;
        color: #FFFFFF;
        font-family: Arial;
    }
    QTextEdit {
        background-color: #3674B5;
        color: #FFFFFF;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }
    QListWidget {
        background-color: #3674B5;
        color: #FFFFFF;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }
    QLineEdit {
        background-color: #3674B5;
        color: #FFFFFF;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }
    QPushButton {
        background-color: #D1F8EF;
        color: #578FCA;
        border: none;
        padding: 10px;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #A1E3F9;
    }
    """