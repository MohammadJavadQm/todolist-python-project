from fastapi import FastAPI
from app.api.controllers import project_controller, task_controller
from app.db.base import Base
from app.db.session import engine

# ایجاد جداول در دیتابیس (اگر وجود نداشته باشند)
# نکته: در محیط پروداکشن معمولاً از Alembic استفاده می‌شود، اما اینجا برای اطمینان اجرا می‌کنیم
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo List API",
    description="A simple ToDo List API developed for Software Engineering Course",
    version="1.0.0",
    docs_url="/docs",  # آدرس Swagger UI
    redoc_url="/redoc"
)

# اتصال کنترلرها (Routers) به برنامه اصلی
app.include_router(project_controller.router)
app.include_router(task_controller.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to ToDo List API! Go to /docs to see the API documentation."}