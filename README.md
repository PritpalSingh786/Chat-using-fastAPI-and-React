---
# Chat App Using FastAPI & React 🚀
A full-stack real-time chat application built with **FastAPI** (Python) for the backend and **React** for the frontend. This project demonstrates how to create a modern, full-stack web app with clear architecture, real-time communication, and a user-friendly interface.
---
## 🧠 Features
* 🔹 **Backend:** FastAPI server with REST APIs
* 🔹 **Frontend:** React client for interactive chat UI
* 🔹 **Real-Time Messaging:** Communicate instantly between users
* 🔹 **MVC-Style FastAPI Code Structure:** Clean backend architecture
* 🔹 **Modular React Client:** Built for scalability
---
## 📁 Project Structure
```
.
├── fastapi_mvc/          # FastAPI backend (MVC style)
│   ├── app/              # Application logic
│   ├── main.py           # FastAPI entrypoint
│   └── requirements.txt  # Backend dependencies
│
└── react_client/         # React frontend
    ├── public/           # Static assets
    ├── src/              # React code (components, pages)
    └── package.json      # Frontend dependencies
```

---

## 🛠️ Tech Stack

| Layer         | Technology                                |
| ------------- | ----------------------------------------- |
| Backend       | FastAPI (Python) ([Wikipedia][1])         |
| Frontend      | React (JavaScript)                        |
| Communication | HTTP / WebSockets                         |
| Architecture  | MVC (backend), Component-based (frontend) |

---

## 🚀 Getting Started

### **Backend (FastAPI)**

1. **Clone the project**

   ```bash
   git clone https://github.com/PritpalSingh786/Chat-using-fastAPI-and-React.git
   cd Chat-using-fastAPI-and-React/fastapi_mvc
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS / Linux
   # .\venv\Scripts\activate   # Windows
   ```

3. **Install requirements**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will be available at `http://localhost:8000`

---

### **Frontend (React)**

1. **Navigate to frontend folder**

   ```bash
   cd ../react_client
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Start the React app**

   ```bash
   npm start
   ```

   The frontend will run at `http://localhost:3000`

---

## 📦 Available Scripts

**Frontend**

| Command         | Description                      |
| --------------- | -------------------------------- |
| `npm start`     | Runs the app in development mode |
| `npm run build` | Builds the app for production    |

**Backend**

| Command                           | Description               |
| --------------------------------- | ------------------------- |
| `uvicorn main:app --reload`       | Starts FastAPI server     |
| `pip install -r requirements.txt` | Installs backend packages |

---

## 🧩 Folder Notes

### **fastapi_mvc**

* Follows MVC-like structure for clarity
* Contains API endpoints and business logic

### **react_client**

* Organized React components
* Clean chat UI and state management

---

## 💡 Tips & Next Improvements

* Add **WebSockets** for real-time chat
* Implement **authentication** (JWT)
* Store messages in a **database**
* Add support for **multiple chat rooms**

---

## 💬 Contributing

1. ⭐ Star the repo
2. Fork and create a new branch
3. Make your changes
4. Open a Pull Request

---

## 📄 License

This project is open source and available under the **MIT License**.

---
