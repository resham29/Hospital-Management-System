from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base

app = FastAPI()

DATABASE_URL = "sqlite:///./hospital.db"

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

security = HTTPBearer()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

# Create a base class for all SQLAlchemy database models
Base = declarative_base()

# -------------------- CREATE ACCESS TOKEN --------------------
#1. Create a function to generate a JWT token.
#2. The function should take a dictionary as input and return a JWT token.
#3. The token should have an expiry time of 30 minutes.
#4. Use the jwt.encode() method to generate the token.
#5. Use the SECRET_KEY and ALGORITHM to encode the token.
#6. Return the token to the user.
def create_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    payload = ({
        "sub": username,
        "exp": expire
        })
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token
    
# -------------------- LOGIN API --------------------
#1. Create a /login API.
#2. Take username and password from the user.
#3. Check if the username is admin and password is 12345.
#4. If both are correct, set the token expiry time to 30 minutes.
#5. Generate a JWT token using the jose library.
#6. Return the token to the user.
#7. If the username or password is wrong, show a 401 Unauthorized error.
#8. Display the message "Invalid username or password" if the login details are incorrect.
@app.post("/login")
def login(username:str, password:str):
    if username == "admin" and password == "12345":
        token = create_token(username)
        payload = {
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer"
        }
        return(payload)
        
    raise HTTPException(
        status_code=401, 
        detail="Invalid username or password"
    )
    
# -------------------------
# JWT Middleware
# -------------------------
@app.middleware("http")
async def verify_token(request: Request, call_next):
    
    public_paths = [
        "/login",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]

    if request.url.path in public_paths:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    print(f"auth_header: {auth_header}")  
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    # Expected:
    # Authorization: Bearer <token>

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header"
        )
    
    token = parts[1]
    print(f"parts: {parts}")
    print(f"token: {token}")
    
    try:

        # Verify JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        username = payload.get("sub")
        print(f"payload: {payload}")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        # Store username in request
        request.state.username = username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return await call_next(request)

# ------------------------- Protected API -------------------------
@app.get("/users")
def users(request: Request):

    username = request.state.username

    return {
        "message": "Authorized",
        "username": username
    }

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
def create_patient(patName: str, patAge: int,patPhone :str, patEmail: str, db: Session = Depends(get_db)):
    patient =  Patient(
        patName = patName,
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

@app.get("/patient")
async def get_patient(request: Request, db: Session = Depends(get_db),token: str = Depends(security)):

    patient = db.query(Patient).all()
    
    username = request.state.username
    print(f"token: {token}")
    return {
        "data": patient
    }

@app.get("/patient/{patId}")
def get_patient(patId: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patId).first()

    return {
        "data": patient
    }
    

@app.get("/doctor")
def get_doctor(db: Session = Depends(get_db)):
    doctor = db.query(Doctor).all()

    return {
        "data": doctor
    }

@app.get("/doctor/{docId}")
def get_doctor(docId: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == docId).first()

    return {
        "data": doctor
    }

@app.post("/appointment")
def create_appointment(patId: int, docId: int, problem: str, fees: int, resolutionStatus: str, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.id == patId).first()
    if patient is None:
        return {
            "message" : "Patient not found"
        }

    doctor = db.query(Doctor).filter(Doctor.id == docId).first()
    if doctor is None:
        return {
            "message" : "Doctor not found"
        }

    if doctor.docStatus != "Available":
        return{
            "message" : "Appointment can't be booked",
            "reason" : f"{doctor.docName} is currently {doctor.docStatus}"
        }

    appointment = Appointment(
        patId = patId,
        docId = docId,
        problem = problem,
        fees = fees,
       resolutionStatus = resolutionStatus
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return {
        "message" : "Appointment booked succesfully",
        "data" : appointment
    }

@app.put("/doctor")
def update_docStatus(docId: int, docStatus = str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == docId).first() 
    if doctor is None: 
        return { 
            "message": "Doctor not found"
        } 
    
    doctor.docStatus = docStatus 
    
    db.commit() 
    db.refresh(doctor) 
    
    return { 
        "message": "Status updated successfully", 
        "data": doctor 
    }