from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patId: int
    docId: int
    problem: str
    resolutionStatus: str
    fees: int
