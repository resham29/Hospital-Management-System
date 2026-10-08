from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    resolutionStatus: str
