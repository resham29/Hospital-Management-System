from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base


class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, index=True)
    docName = Column(String)
    docStatus = Column(String)
    deptId = Column(Integer, ForeignKey("department.id"))