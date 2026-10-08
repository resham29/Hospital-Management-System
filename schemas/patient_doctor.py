from pydantic import BaseModel


class PatientDoctorCreate(BaseModel):
    patId: int
    docId: int