from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.doctor import Doctor
from schemas.doctor import DoctorCreate


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# CREATE DOCTOR
@router.post("/doctor")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    new_doctor = Doctor(
        docName=doctor.docName,
        docStatus=doctor.docStatus,
        deptId=doctor.deptId
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

# GET DOCTORS
@router.get("/doctors")
def get_doctors(
    db: Session = Depends(get_db)
):
    doctors = db.query(Doctor).all()
    return doctors

# GET DOCTOR BY ID
@router.get("/doctor/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor