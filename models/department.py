from sqlalchemy import Column, Integer, String
from database.database import Base


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    deptName = Column(String)