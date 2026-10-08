from fastapi import FastAPI

from database.database import Base, engine
from routers import patient, doctor, department, appointment, patient_doctor, auth
from models import patient as patient_model
from models import doctor as doctor_model
from models import department as department_model
from models import appointment as appointment_model
from models import patient_doctor as patient_doctor_model
from auth.middleware import verify_token
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

app = FastAPI()

security = HTTPBearer()

app.include_router(patient.router)
app.include_router(doctor.router)   
app.include_router(department.router)
app.include_router(appointment.router)
app.include_router(patient_doctor.router)
app.include_router(auth.router)
app.middleware("http")(verify_token)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Hospital Management API",
        version="1.0.0",
        routes=app.routes
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["security"] = [
        {
            "BearerAuth": []
        }
    ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi