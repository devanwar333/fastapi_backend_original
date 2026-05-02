from sqlmodel import Field, SQLModel

class JenisStok(SQLModel, table=True):
    __tablename__ = "JnsStok"
    ID: int = Field(default=None, primary_key=True)
    Jenis: str = Field(default="")
    Unit: str  = Field(default="")
    Jmlh: int  = Field(default=0)
    Unit1: str  = Field(default="")
    Aktif: bool = Field(default=False)