# 📚 Library System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/database-MongoDB-brightgreen.svg)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, streamlined web application for managing library catalogs and book borrowings. Built with **Flask** and **MongoDB**, this system provides a robust solution for both library administrators and patrons.

[Slovenská verzia nižšie / Slovak version below]

---

## ✨ Features

- **🔐 Secure Authentication**: User registration and login with encrypted passwords using Bcrypt.
- **👥 Role-Based Access (RBAC)**: Differentiated interfaces and permissions for regular **Users** and **Administrators**.
- **📖 Catalog Management**:
  - Browse available books with dynamic filtering.
  - Search books by title, author, or publisher using MongoDB text indexing.
- **🔄 Borrowing Workflow**: One-click borrowing and returning system.
- **👤 Profile Management**: Users can update their personal information and upload profile pictures.
- **🛠️ Admin Dashboard**:
  - Add, edit, or remove books from the system.
  - Manage user accounts and monitor active borrowings.

---

## 🛠️ Tech Stack

- **Backend:** [Flask](https://flask.palletsprojects.com/) (Python)
- **Database:** [MongoDB](https://www.mongodb.com/) with [MongoEngine](http://mongoengine.org/) ODM
- **Authentication:** [Flask-Login](https://flask-login.readthedocs.io/)
- **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templates
- **Security:** Password hashing with [Bcrypt](https://pypi.org/project/bcrypt/)
- **Image Handling:** [Pillow](https://python-pillow.org/)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MongoDB instance (Local or Atlas)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/library-system.git
   cd library-system
   ```

2. **Create and activate a virtual environment:**

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**
   - Copy `sample_config.ini` to a new file named `config.ini`.
   - Update the `MONGO_DATABASE_URI` and `FLASK_SECRET_KEY` with your settings.

   ```bash
   cp sample_config.ini config.ini  # On Linux/macOS
   copy sample_config.ini config.ini # On Windows
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.

---

## 📂 Project Structure

```text
├── admin/          # Admin-specific logic and templates
├── auth/           # Authentication blueprints
├── general/        # Core business logic and shared templates
├── profile/        # User profile management
├── static/         # CSS, JS, and image assets
├── app.py          # Application entry point
├── models.py       # MongoDB schemas (User, Book, Borrowing)
└── config.ini      # Local configuration (Database & Flask)
```

---

## 🇸🇰 Slovenský Jazyk

Tento projekt je semestrálnou prácou zameranou na demonštráciu tvorby webových aplikácií v Pythone.

**Kľúčové funkcie:**

- Prehľadávanie katalógu knižnice.
- Správa výpožičiek (priraďovanie/odoberanie).
- Administrátorské rozhranie pre správu kníh.
- Nastavenie používateľského profilu a nahratie fotky.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
