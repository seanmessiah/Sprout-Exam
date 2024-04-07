from sqlalchemy import Boolean, Column, Integer, String

from core.config import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    class Config():
        orm_mode = True