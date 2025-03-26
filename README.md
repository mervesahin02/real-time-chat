# Triscord: A Real-Time Chat Application

## Project Overview

Triscord is a feature-rich, real-time chat application built with Python, utilizing PyQt5 for the graphical user interface and PostgreSQL for data management. The application provides secure user authentication, private messaging, emoji support, and robust file-sharing capabilities.

## Features

### User Management
- Secure user registration and login
- Password hashing for enhanced security
- User profile creation and management

### Messaging
- Real-time group chat
- Private messaging
- Message logging with timestamps
- Emoji picker

### User Experience
- Dynamic online user list
- Context menu for user interactions
- Responsive UI design

### Database Integration
- PostgreSQL database for:
  - User management
  - Message history
  - User profiles
  - File sharing metadata

## Prerequisites

### Software Requirements
- Python 3.8+
- PostgreSQL 12+
- Required Python Libraries:
  - PyQt5
  - psycopg2
  - socket
  - threading
  - uuid
  - hashlib

### Database Setup
1. Create a PostgreSQL database named `triscord_db`
2. Ensure PostgreSQL is running on localhost:5432
3. Default credentials:
   - Username: postgres
   - Password: HappyCat

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/triscord.git
cd triscord
```

2. Install dependencies
```bash
pip install PyQt5 psycopg2 
```

3. Configure Database
- Modify connection parameters in each class constructor if needed
- Ensure PostgreSQL is running

## Running the Application

```bash
python triscord.py
```

## Project Structure

- `triscord.py`: Main application entry point
- `server.py`: Socket server for real-time communication
- `user_manager.py`: User authentication and registration
- `user_profiles.py`: User profile management
- `message_logger.py`: Message history logging
- `file_sharing.py`: File upload and metadata tracking
- `styles.py`: UI styling configurations

## Security Features

- Password hashing with SHA-256
- Secure database connection pooling
- Unique user identification
- Private message encryption

## Customization

- Modify `styles.py` to change UI appearance
- Adjust database connection parameters in respective class constructors

## Planned Improvements

- End-to-end message encryption
- File transfer functionality
- Advanced user profile features
- Enhanced error handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Seyyide Merve Şahin - sydmervesihin@gmail.com

Project Link: [https://github.com/yourusername/triscord](https://github.com/yourusername/triscord)
