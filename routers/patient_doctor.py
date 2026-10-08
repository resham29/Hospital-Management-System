from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from main2 import Appointment
from models.patient_doctor import PatientDoctor
from schemas.patient_doctor import PatientDoctorCreate
from models.patient import Patient
from models.doctor import Doctor


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# CREATE PATIENT-DOCTOR RELATIONSHIP
@router.post("/patient-doctor")
def create_patient_doctor(
    data: PatientDoctorCreate,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == data.patId
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == data.docId
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_record = PatientDoctor(
        patId=data.patId,
        docId=data.docId
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
    "id": new_record.id,
    "patId": new_record.patId,
    "patientName": patient.patName,
    "docId": new_record.docId,
    "doctorName": doctor.docName
}

# GET PATIENT-DOCTOR RELATIONSHIP BY ID
@router.get("/patient-doctor/{recordId}")
def get_patient_doctor(
    recordId: int,
    db: Session = Depends(get_db)
):
    record = db.query(PatientDoctor).filter(
        PatientDoctor.id == recordId
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Patient-doctor record not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == record.patId
    ).first()

    doctor = db.query(Doctor).filter(
        Doctor.id == record.docId
    ).first()

    return {
        "id": record.id,
        "patId": record.patId,
        "patientName": patient.patName,
        "docId": record.docId,
        "doctorName": doctor.docName
    }

# UPDATE PATIENT-DOCTOR RELATIONSHIP
@router.put("/patient-doctor/{recordId}")
def update_patient_doctor(
    recordId: int,
    data: PatientDoctorCreate,
    db: Session = Depends(get_db)
):
    record = db.query(PatientDoctor).filter(
        PatientDoctor.id == recordId
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Patient-doctor record not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == data.patId
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == data.docId
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    record.patId = data.patId
    record.docId = data.docId

    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "patId": record.patId,
        "patientName": patient.patName,
        "docId": record.docId,
        "doctorName": doctor.docName
    }

# DELETE PATIENT-DOCTOR RELATIONSHIP
@router.delete("/patient-doctor/{recordId}")
def delete_patient_doctor(
    recordId: int,
    db: Session = Depends(get_db)
):
    record = db.query(PatientDoctor).filter(
        PatientDoctor.id == recordId
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Patient-doctor record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Patient-doctor record deleted successfully"
    }

