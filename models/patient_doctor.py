from sqlalchemy import Column, Integer, ForeignKey
from database.database import Base


class PatientDoctor(Base):
    __tablename__ = "patientDoctor"

    id = Column(Integer, primary_key=True, index=True)
    patId = Column(Integer, ForeignKey("patient.id"))
    docId = Column(Integer, ForeignKey("doctor.id"))