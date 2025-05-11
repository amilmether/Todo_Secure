# 📝 FastAPI Todo App with JWT Authentication

A simple and powerful Todo app backend built using **FastAPI** and **PostgreSQL**, with **JWT-based authentication** and full CRUD features for managing todos.

---

## 🚀 Features

- ✅ User Signup and Login with JWT
- 📝 Create, Update, Delete, and View Todos
- 🗂️ Group Todos by:
  - Completed
  - To Be Done
  - Time Elapsed
- 🔐 All Todo routes protected using JWT
- 🐘 PostgreSQL as the database

---

## 🛠️ Tech Stack

- **FastAPI** - Backend framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **python-jose** - JWT tokens
- **Pydantic** - Data validation

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/amilmether/Todo_Secure.git
cd Todo_Secure
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
```env
DATABASE_URL=postgresql://postgres:password@localhost/tododb
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Setup your PostgreSQL database manually
Create a new database in PostgreSQL named `tododb` (or as per your `.env`)

### 6. Run the app
```bash
uvicorn app.main:app --reload
```

Visit Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📂 Project Structure

```
app/
├── main.py           # FastAPI app entry
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── database.py       # DB session setup
├── auth.py           # JWT handling
├── routes/
│   ├── auth.py       # Login/Signup endpoints
│   └── todo.py       # Todo APIs
.env                   # Environment variables
```

---

## 📬 API Endpoints

| Method | Endpoint         | Description                      |
|--------|------------------|----------------------------------|
| POST   | `/auth/signup`   | Register a new user              |
| POST   | `/auth/login`    | Login and get a JWT token        |
| POST   | `/todos/`        | Create a todo                    |
| GET    | `/todos/`        | Get all todos                    |
| GET    | `/todos/grouped` | Group todos by status            |
| PUT    | `/todos/{id}`    | Edit a specific todo             |
| DELETE | `/todos/{id}`    | Delete a specific todo           |

---

## ✅ Todo

- [ ] Add testing using `pytest`
- [ ] Add Docker support
- [ ] Connect a frontend (HTML or React)
- [ ] Deploy to Railway/Render

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Developed by [Amil Mether](https://github.com/amilmether)