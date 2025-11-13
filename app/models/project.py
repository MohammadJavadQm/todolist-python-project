from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"  # نام جدول در دیتابیس

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # ارتباط با تسک‌ها (One-to-Many)
    # cascade="all, delete-orphan" یعنی اگر پروژه حذف شد، تسک‌هاش هم حذف بشه (Cascade Delete)
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"