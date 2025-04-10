# 🚀 FastAPI Backend with Docker & PostgreSQL

 This is a **FastAPI backend** for Spark! Bytes that provides **user authentication (signup & login)** and **PostgreSQL** as the database (hosted on Railway).

---

## 🛠️ **Setup & Installation**
### **1️. Clone the Repository**
```bash
git clone https://github.com/Project-BU-SparkBytes/hungerhub-backend.git
cd fastapi-backend
```

### **2. Configure Environmental Variables**

Navigate to the project folder where requirements.txt is located:
```bash
cd ~/fastapi-backend  # macOS/Linux
cd C:\Users\YourName\fastapi-backend  # Windows
```

Activate the virtual environment (optional, but recommended):
```bash
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
```

Install the dependencies using pip:
```bash
pip install -r requirements.txt
```

Rename .env.example to .env and update the contents.


## 📌 **Running the Application**

### **Using Docker**

Run the application using Docker Compose:
```bash
docker-compose up 
```

Rebuild the container (after modifying requirements.txt or Dockerfile):
```bash
docker-compose up --build
```
Stop running the container:
```bash
docker-compose down
```

## **API Endpoints Testing**

FastAPI's documentation is available at: http://127.0.0.1:8000/docs  (allows us to test the endpoint requests and responses)
- /signup will return the user's registered email and ID key on success.
- /login will return an authentication token for that specific user.
- /create-event will create a new event in the events database table with the specified credentials.
- /profile will return the current logged-in, authenticated user's credentials (this is a protected route)
- Other error messages are provided for testing.






 

