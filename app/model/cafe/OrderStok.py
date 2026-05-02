from sqlmodel import SQLModel, Field
from datetime import date

class OrderStok(SQLModel, table=True):
    __tablename__ = "OrderStok"
    
    IDOrder: int = Field(default=None, primary_key=True)
    Tgl: str
    Jenis: str
    Jmlh: float
    JmlhInp: float
    unit: str
    Divisi: str
    Inputer: int
    Ket: str