from pydantic import BaseModel

# Create StuDent Schema (Pydantic Model)
class StuDent(BaseModel):
    sname: str
    section: str
    grp: str
