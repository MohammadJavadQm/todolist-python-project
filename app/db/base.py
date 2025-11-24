from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy Base class.
    All database models (tables) should inherit from this class.
    """
    pass