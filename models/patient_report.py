from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base

class PatientReport(Base):
    __tablename__ = "patient_report"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patient.id"))
    appointment_id = Column(Integer, ForeignKey("patientAppointment.id"))
    filename = Column(String)
    file_path = Column(String)
    report_type = Column(String)