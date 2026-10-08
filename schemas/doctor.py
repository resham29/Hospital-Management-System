from pydantic import BaseModel


class DoctorCreate(BaseModel):
    docName: str
    docStatus: str
    deptId: int