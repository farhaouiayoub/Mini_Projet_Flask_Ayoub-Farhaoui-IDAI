# Flask Auth App

A complete user authentication system built with Flask, featuring secure registration, login, session management, and profile administration.

![Flask Auth App Banner](screenshots/banner.png)

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Future Improvements](#future-improvements)

## Features

- **User Authentication**
  - Secure registration with email validation
  - Login with password hashing
  - "Remember me" functionality
  - Session management
  - Logout capability

- **Profile Management**
  - View user profile details
  - Edit user information
  - Change password with validation

- **Security**
  - Password hashing using Werkzeug
  - Protected routes with login_required decorator
  - Session security

- **Performance Optimization**
  - Session management for user state
  - Caching system for frequently accessed data

## Screenshots

### Registration Page
![Registration Page](screenshots/register.png)
*Users can create a new account with email, username, and password*

### Login Page
![Login Page](screenshots/login.png)
*Secure login interface with "remember me" option*

### Profile Page
![Profile Page](screenshots/profile.png)
*User information displayed with auto-generated avatar*

### Edit Profile
![Edit Profile Page](screenshots/edit_profile.png)
*Interface for updating user information and changing password*

## Project Structure

The project follows a modular architecture for better maintainability:

```
Mini_Projet_Flask/
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── models/                 # Database models
│   ├── __init__.py
│   └── user.py             # User model definition
├── controllers/            # Business logic
│   ├── __init__.py
│   └── auth_controller.py  # Authentication controller
├── views/                  # Routes and views
│   ├── __init__.py
│   └── auth_views.py       # Authentication routes
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── register.html       # Registration form
│   ├── login.html          # Login form
│   ├── profile.html        # User profile page
│   └── edit_profile.html   # Profile editing page
├── static/                 # Static assets
│   ├── css/                # CSS stylesheets
│   │   └── style.css       # Main stylesheet
│   └── js/                 # JavaScript files
│       └── script.js       # Main scripts
└── utils/                  # Utility modules
    ├── __init__.py
    ├── decorators.py       # Custom decorators (e.g., login_required)
    └── cache.py            # Caching functionality
```

## Installation

Follow these steps to set up the application on your local machine:

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/flask-auth-app.git
# OR download and extract the ZIP file
cd flask-auth-app
```

### Step 2: Create and Activate a Virtual Environment (Optional but Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure the Application

The application is configured to use SQLite by default, which doesn't require additional setup. However, you can modify `config.py` if you need to change any settings:

- `SECRET_KEY`: For session security (change this in production)
- `DATABASE_URL`: Database connection string
- `SESSION_TYPE`: Session storage type
- `CACHE_TYPE`: Cache storage type

### Step 5: Initialize the Database

```bash
# Start Python interactive shell
python
```

In the Python shell:

```python
from app import create_app
from models.user import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
exit()
```

## Usage

### Running the Application

```bash
python app.py
```

By default, the application will be available at `http://127.0.0.1:5000/`

### Key Features Usage

1. **Registration**
   - Navigate to `/register` or click the "Register" link in the navigation bar
   - Fill in your email, username, and password
   - Click "Register" to create your account

   ![Registration Process](screenshots/register_process.png)

2. **Login**
   - Navigate to `/login` or click the "Login" link
   - Enter your email and password
   - Optionally check "Remember me"
   - Click "Login" to access your account

   ![Login Process](screenshots/login_process.png)

3. **Viewing Your Profile**
   - After logging in, click on "Profile" in the navigation bar
   - View your account details including email, username, and registration date

   ![Profile Details](screenshots/profile_details.png)

4. **Editing Your Profile**
   - From your profile page, click "Edit Profile"
   - Update your username or email
   - To change your password, enter your current password and then the new password twice
   - Click "Save Changes" to update your information

   ![Editing Profile](screenshots/edit_profile_process.png)

5. **Logging Out**
   - Click "Logout" in the navigation bar to end your session

## Technical Details

### Session Management

The application uses Flask-Session to maintain user state between HTTP requests:

- **Session Storage**: File-system based storage (configured in `config.py`)
- **Session Data**: User ID and username stored upon login
- **Session Lifetime**: 30 minutes of inactivity by default
- **Remember Me**: Extends session persistence when checked during login

Code example from `auth_controller.py`:
```python
# During login
session['user_id'] = user.id
session['username'] = user.username
session.permanent = remember  # Sets permanent session if "remember me" is checked
```

### Caching System

A caching system is implemented to improve performance by reducing database queries:

- **Cache Type**: Simple in-memory cache
- **Cache Timeout**: 5 minutes (300 seconds) by default
- **Cached Data**: User information stored with user ID as key

Code example from `auth_controller.py`:
```python
# Storing user data in cache
cache.set(f'user_{user.id}', user.to_dict(), timeout=300)

# Retrieving user data from cache
cached_user = cache.get(f'user_{user_id}')
if cached_user:
    return cached_user
```

### Security Features

- **Password Hashing**: Uses Werkzeug's security functions to hash passwords before storage
- **Protected Routes**: Uses a custom `login_required` decorator to protect private routes
- **Form Validation**: Client and server-side validation for all form submissions
- **Password Strength Meter**: Visual feedback on password strength during registration and password change

## Future Improvements

Potential enhancements for the project:

- **Advanced Session Storage**: Replace file-system sessions with Redis for better scalability
- **Distributed Caching**: Implement a distributed cache solution for improved performance
- **Additional Security**: Add CSRF protection and two-factor authentication
- **Password Recovery**: Implement a password reset feature with email confirmation
- **User Roles**: Add role-based access control for different user types
- **API Development**: Create RESTful APIs for mobile application integration

---

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
