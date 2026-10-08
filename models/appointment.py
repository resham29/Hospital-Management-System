from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base


class Appointment(Base):
    __tablename__ = "patientAppointment"

    id = Column(Integer, primary_key=True, index=True)
    patId = Column(Integer, ForeignKey("patient.id"))
    docId = Column(Integer, ForeignKey("doctor.id"))
    problem = Column(String)
    fees = Column(Integer)
    resolutionStatus = Column(String)