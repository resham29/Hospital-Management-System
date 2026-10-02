from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base

app = FastAPI()

DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

# Create a base class for all SQLAlchemy database models
Base = declarative_base()


# -------------------- PATIENT --------------------

class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    patName = Column(String)
    patAge = Column(Integer)
    patPhone = Column(String)
    patEmail = Column(String, unique=True)


# -------------------- APPOINTMENT --------------------

class Appointment(Base):
    __tablename__ = "patientAppointment"

    id = Column(Integer, primary_key=True, index=True)
    patId = Column(Integer, ForeignKey("patient.id"))
    docId = Column(Integer, ForeignKey("doctor.id"))
    problem = Column(String)
    fees = Column(Integer)
    resolutionStatus = Column(String)


# -------------------- DOCTOR --------------------

class Doctor(Base):
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, index=True)
    docName = Column(String)
    docStatus = Column(String)
    deptId = Column(Integer, ForeignKey("department.id"))


# -------------------- PATIENT DOCTOR --------------------

class PatientDoctor(Base):
    __tablename__ = "patientDoctor"

    id = Column(Integer, primary_key=True, index=True)
    patId = Column(Integer, ForeignKey("patient.id"))
    docId = Column(Integer, ForeignKey("doctor.id"))


# -------------------- DEPARTMENT --------------------

class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    deptName = Column(String)


# -------------------- DATABASE SESSION --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all database tables
Base.metadata.create_all(bind=engine)


# -------------------- ADD DEPARTMENTS --------------------

def add_departments():

    db = SessionLocal()

    if db.query(Department).count() == 0:

        departments = [
            Department(deptName="Cardiology"),
            Department(deptName="Neurology"),
            Department(deptName="Orthopedics"),
            Department(deptName="Dermatology"),
            Department(deptName="Gynecology"),
            Department(deptName="Ophthalmology"),
        ]

        db.add_all(departments)
        db.commit()

    db.close()


add_departments()


# -------------------- ADD DOCTORS --------------------

def add_doctors():

    db = SessionLocal()

    if db.query(Doctor).count() == 0:

        doctors = [
            Doctor(
                docName="Dr. Amit Sharma",
                docStatus="Available",
                deptId=1
            ),
            Doctor(
                docName="Dr. Priya Patil",
                docStatus="Available",
                deptId=2
            ),
            Doctor(
                docName="Dr. Rahul Joshi",
                docStatus="On Leave",
                deptId=3
            ),
            Doctor(
                docName="Dr. Sneha Kulkarni",
                docStatus="Available",
                deptId=4
            ),
            Doctor(
                docName="Dr. Rohan Deshmukh",
                docStatus="Available",
                deptId=5
            ),
            Doctor(
                docName="Dr. Neha Shah",
                docStatus="Busy",
                deptId=6
            ),
            Doctor(
                docName="Dr. Akshay More",
                docStatus="Available",
                deptId=5
            ),
            Doctor(
                docName="Dr. Pooja Jadhav",
                docStatus="Available",
                deptId=4
            ),
            Doctor(
                docName="Dr. Kunal Mehta",
                docStatus="On Leave",
                deptId=3
            ),
            Doctor(
                docName="Dr. Anjali Deshpande",
                docStatus="Available",
                deptId=2
            ),
            Doctor(
                docName="Dr. Swati Dharia",
                docStatus="Busy",
                deptId=1
            )
        ]

        db.add_all(doctors)
        db.commit()

    db.close()


add_doctors()


# -------------------- API --------------------

@app.get("/")
def home(db: Session = Depends(get_db)):
    return {
        "message": "DB connected successfully"
    }

@app.post("/patient")
def create_patient(id: int, patName: str, patAge: int,patPhone :str, patEmail: str, db: Session = Depends(get_db)):
    patient =  Patient(
        id=id,
        patName=patName,
        patAge = patAge,
        patPhone = patPhone,
        patEmail = patEmail
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return{
        "message":"Patient added succesfully",
        "data" : patient
    }