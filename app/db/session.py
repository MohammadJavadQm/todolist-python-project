import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# بارگذاری متغیرها از فایل .env
load_dotenv()

# خواندن اطلاعات اتصال
DB_USER = os.getenv("DB_USER", "parsa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb")

# ساخت آدرس اتصال (Connection String)
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ایجاد موتور اتصال به دیتابیس
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ساخت کارخانه سشن‌ها (برای ساخت ارتباط در هر درخواست)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)