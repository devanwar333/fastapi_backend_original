from sqlmodel import SQLModel, Field

class AyamMini(SQLModel, table=True):
    __tablename__ = "ayammini"
    ID_kcl: int = Field( nullable=True, )
    ID: int = Field( primary_key=True, )
    Tgl: str = Field( nullable=True, )
    Jenis: str = Field( nullable=True, )
    Jmlh: int = Field( nullable=True, )
    Ket: str = Field( nullable=True, )
    
    JenisAyam: str = Field( nullable=True, )
    Kelas: str = Field( nullable=True, )
    PosAyamMini: str = Field( nullable=True, )