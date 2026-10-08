from pydantic import BaseModel


class PatientCreate(BaseModel):
    patName: str
    patAge: int
    patPhone: str
    patEmail: str