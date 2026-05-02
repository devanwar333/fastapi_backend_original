from sqlmodel import Field, SQLModel
class BbOrder (SQLModel, table=True):
    __tablename__ = "BBOrder"
    IDOrder: int = Field(default=None, primary_key=True)
    Tgl: str | None = Field(default=None)
    Total: str | None = Field(default=None)
    Aktif: bool | None = Field(default=None)    
    Inputer: int | None = Field(default=None)
    Category: str | None = Field(default=None)
    Checked: bool | None = Field(default=None)
    ID_Check: int | None = Field(default=None)
    Ket: str | None = Field(default=None)