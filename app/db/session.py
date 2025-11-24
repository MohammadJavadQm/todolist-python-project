import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

# بارگذاری متغیرها از فایل .env
load_dotenv()

# خواندن اطلاعات اتصال با مقادیر پیش‌فرض ایمن
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "todolist_db")

# ساخت آدرس اتصال (Connection String)
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ایجاد موتور اتصال به دیتابیس
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ساخت کارخانه سشن‌ها (برای ساخت ارتباط در هر درخواست)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Dependency function for FastAPI to handle database sessions.
    Creates a new session for each request and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()