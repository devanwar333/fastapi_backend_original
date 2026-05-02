from sqlmodel import Field, SQLModel

class Belanja (SQLModel, table=True):
    __tablename__ = "Belanja"
    ID: int = Field(default=None, primary_key=True)
    Jenis: str = Field(default=None, primary_key=True)
    Jmlh: float = Field(default=None)
    Unit: str = Field(default=None)
    Price: int = Field(default=None)
    Divisi: str = Field(default=None)
    ket: str = Field(default=None)
    Checked: bool = Field(default=None)