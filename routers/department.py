from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.department import Department
from schemas.department import DepartmentCreate


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# CREATE DEPARTMENT
@router.post("/department")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    new_department = Department(
        deptName=department.deptName
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department

# GET DEPARTMENTS
@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db)
):
    departments = db.query(Department).all()
    return departments

# GET DEPARTMENT BY ID
@router.get("/department/{deptId}")
def get_department(
    deptId: int,
    db: Session = Depends(get_db)
):
    department = db.query(Department).filter(Department.id == deptId).first()

    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return department

# UPDATE DEPARTMENT
@router.put("/department/{deptId}")
def update_department(
    deptId: int,
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):
    existing_department = db.query(Department).filter(Department.id == deptId).first()

    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")

    existing_department.deptName = department.deptName

    db.commit()
    db.refresh(existing_department)

    return existing_department

# DELETE DEPARTMENT
@router.delete("/department/{deptId}")
def delete_department(
    deptId: int,
    db: Session = Depends(get_db)
):
    existing_department = db.query(Department).filter(Department.id == deptId).first()

    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(existing_department)
    db.commit()

    return {"message": "Department deleted successfully"}