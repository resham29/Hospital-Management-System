from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.appointment import Appointment
from schemas.appointment import AppointmentCreate
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department
resolutionStatus = AppointmentCreate


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# CREATE APPOINTMENT
@router.post("/appointment")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(
        Patient.id == appointment.patId
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.docId
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    new_appointment = Appointment(
        patId=appointment.patId,
        docId=appointment.docId,
        problem=appointment.problem,
        fees=appointment.fees,
        resolutionStatus=appointment.resolutionStatus
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment

# GET ALL APPOINTMENTS
@router.get("/appointment")
def get_appointments(
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).all()

    return appointments

# GET APPOINTMENT BY ID
@router.get("/appointment/{appointmentId}")
def get_appointment(
    appointmentId: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointmentId
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment

# UPDATE APPOINTMENT STATUS
@router.put("/appointment/{appointmentId}")
def update_appointment(
    appointmentId: int,
    appointment: resolutionStatus,
    db: Session = Depends(get_db)
):
    existing_appointment = db.query(Appointment).filter(
        Appointment.id == appointmentId
    ).first()

    if not existing_appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    existing_appointment.resolutionStatus = appointment.resolutionStatus

    db.commit()
    db.refresh(existing_appointment)

    return existing_appointment


# DELETE APPOINTMENT
@router.delete("/appointment/{appointmentId}")
def delete_appointment(
    appointmentId: int,
    db: Session = Depends(get_db)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointmentId
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }

#Patient Appointment History API
@router.get("/patient/{patId}/appointments")
def get_patient_appointments(
    patId: int,
    db: Session = Depends(get_db)
):
    appointments = db.query(Appointment).filter(
        Appointment.patId == patId
    ).all()

    result = []

    for appointment in appointments:
        doctor = db.query(Doctor).filter(
            Doctor.id == appointment.docId
        ).first()

        department = db.query(Department).filter(
            Department.id == doctor.deptId
        ).first()

        result.append({
            "appointmentId": appointment.id,
            "doctorId": appointment.docId,
            "doctorName": doctor.docName,
            "departmentName": department.deptName,
            "problem": appointment.problem,
            "fees": appointment.fees,
            "resolutionStatus": appointment.resolutionStatus
        })

    return result