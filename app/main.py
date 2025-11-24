from fastapi import FastAPI

# ایجاد نمونه اصلی برنامه FastAPI
app = FastAPI(
    title="ToDoList API",
    description="A RESTful API for managing projects and tasks.",
    version="1.0.0"
)

# یک روت ساده برای تست (Health Check)
@app.get("/")
async def root():
    return {"message": "Welcome to ToDoList API! The server is running."}