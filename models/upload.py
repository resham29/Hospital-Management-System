from sqlalchemy import Column, Integer, String, ForeignKey
from database.database import Base

class PatientReport(Base):
    __tablename__ = "patient_report"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    report_type = Column(String, nullable=False)
