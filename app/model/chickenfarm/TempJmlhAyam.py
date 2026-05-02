

from sqlmodel import Field, SQLModel
class TempJmlhAyam(SQLModel, table=True):
    __tablename__ = "TempJmlhAyam"
    ID: int = Field( primary_key=True)
    Kandang: str 
    Indexing: int
    Jmlh: int
    Tgl: str