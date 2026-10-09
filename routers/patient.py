from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.patient import Patient
from schemas.patient import PatientCreate
from models.appointment import Appointment
from models.doctor import Doctor
from models.department import Department


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
def get_patient(patId: int, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(
        Patient.id == patId
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    appointments = db.query(Appointment).filter(
        Appointment.patId == patId
    ).all()

    appointment_history = []

    for appointment in appointments:

        doctor = db.query(Doctor).filter(
            Doctor.id == appointment.docId
        ).first()

        department = db.query(Department).filter(
            Department.id == doctor.deptId
        ).first()

        appointment_history.append({
            "appointmentId": appointment.id,
            "doctorId": appointment.docId,
            "doctorName": doctor.docName,
            "departmentName": department.deptName,
            "problem": appointment.problem,
            "fees": appointment.fees,
            "resolutionStatus": appointment.resolutionStatus
        })

    return {
        "id": patient.id,
        "patName": patient.patName,
        "patAge": patient.patAge,
        "patPhone": patient.patPhone,
        "patEmail": patient.patEmail,
        "appointments": appointment_history
    }

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