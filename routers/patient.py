from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.patient import Patient
from schemas.patient import PatientCreate


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# CREATE PATIENT
@router.post("/patient")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    new_patient = Patient(
        patName=patient.patName,
        patAge=patient.patAge,
        patPhone=patient.patPhone,
        patEmail=patient.patEmail
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

# GET PATIENT
@router.get("/patient")
def get_patients(
    db: Session = Depends(get_db)
):
    patients = db.query(Patient).all()

    return patients

# GET PATIENT BY ID
@router.get("/patient/{patId}")
def get_patient(
    patId: int,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patId).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient

#UPDATE PATIENT
@router.put("/patient/{patId}")
def update_patient(
    patId: int,
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    existing_patient = db.query(Patient).filter(Patient.id == patId).first()

    if not existing_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing_patient.patName = patient.patName
    existing_patient.patAge = patient.patAge
    existing_patient.patPhone = patient.patPhone
    existing_patient.patEmail = patient.patEmail

    db.commit()
    db.refresh(existing_patient)

    return existing_patient

# DELETE PATIENT
@router.delete("/patient/{patId}")
def delete_patient(
    patId: int,
    db: Session = Depends(get_db)
):
    existing_patient = db.query(Patient).filter(Patient.id == patId).first()

    if not existing_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(existing_patient)
    db.commit()

    return {"message": "Patient deleted successfully"}