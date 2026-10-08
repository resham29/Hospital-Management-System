from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    deptName: str