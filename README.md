# 🎭 TicketEase — A Smart Theatre Ticket Booking System

Welcome to **TicketEase**, your seamless digital solution for managing shows, venues, and ticket bookings! Built with 💖 using **Flask**, **SQLAlchemy**, and **Flask-RESTful**, this project serves as a backend system for an event/theatre booking platform.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)


---

## 🚀 Features

* ✨ Robust RESTful API using `Flask-RESTful`
* 🛠️ Full CRUD support for Users, Theatres, Shows, Tickets, and Bookings
* 🔐 Secure user registration and login support (JWT-compatible design)
* 🗕️ Track upcoming shows with datetime support
* 📍 Theatre location, capacity, and venue images
* 🎫 Book and rate shows with flexible ticket handling
* 📦 Modular, scalable, and ready for frontend integration

---

## 🧠 Tech Stack

| Tech                 | Description             |
| -------------------- | ----------------------- |
| 🐍 Python            | Programming language    |
| 🔥 Flask             | Web framework           |
| 🧱 SQLAlchemy        | ORM for DB interactions |
| 🧪 Flask-RESTful     | REST API framework      |
| 🐘 SQLite/PostgreSQL | Database                |

---

## 📁 Project Structure

```
/ticket-ease/
│
├── backend/
│   ├── __init__.py
│   ├── app.py                  # Flask app creation
│   ├── models.py               # SQLAlchemy models
│   ├── api_controllers.py      # API resources
│   └── config.py               # DB and app config
│
├── migrations/                 # Alembic migrations
├── README.md
└── requirements.txt
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ticketease.git
cd ticketease
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Run the app

```bash
python backend/app.py
```

---

## 📬 API Endpoints Overview

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/api/shows`      | Get all shows     |
| GET    | `/api/shows/<id>` | Get specific show |
| POST   | `/api/shows`      | Create a new show |
| PUT    | `/api/shows/<id>` | Update a show     |
| DELETE | `/api/shows/<id>` | Delete a show     |

Additional endpoints for `Users`, `Theatres`, `Bookings`, and `Tickets` are also available.

---


## ✅ Future Improvements

* 🧑‍🤝‍🧑 Admin vs User role separation with auth
* 🌍 Integration with Google Maps for theatre locations
* 📱 Frontend with React/Flutter
* 💳 Online payment gateway

---

## 🧑‍💼 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---


## 💙 Acknowledgements

* Flask & SQLAlchemy Docs
* Freepik / Unsplash for venue image placeholders
* All open-source contributors 



