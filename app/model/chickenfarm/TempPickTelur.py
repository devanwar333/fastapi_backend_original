from sqlmodel import SQLModel, Field
class TempPickTelur(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, in)
    Tgl: str
    Dist: int
    Kandang: str
    Ikat: int
    Ppn: int
    Butir: int
    Tipe: str
    Jenisayam: str
    Input: int