from fastapi import FastAPI
from app.api.controllers import project_controller, task_controller

app = FastAPI(
    title="ToDo List API",
    description="A simple ToDo List API developed for Software Engineering Course (Phase 3)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(
    project_controller.router,
    prefix="/api/projects",  # تمام مسیرهای پروژه با /api/projects شروع می‌شوند
    tags=["Projects"]        # در سواگر زیر دسته Projects قرار می‌گیرند
)

app.include_router(
    task_controller.router,
    prefix="/api/tasks",     # تمام مسیرهای تسک با /api/tasks شروع می‌شوند
    tags=["Tasks"]           # در سواگر زیر دسته Tasks قرار می‌گیرند
)

@app.get("/")
def read_root():
    return {"message": "Welcome to ToDo List API! Go to /docs to see the API documentation."}