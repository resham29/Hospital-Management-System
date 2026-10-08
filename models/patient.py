from sqlalchemy import Column, Integer, String
from database.database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    patName = Column(String)
    patAge = Column(Integer)
    patPhone = Column(String)
    patEmail = Column(String, unique=True)