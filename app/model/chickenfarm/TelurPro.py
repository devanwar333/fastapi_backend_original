from sqlmodel import Field, SQLModel
class TelurPro(SQLModel, table=True):
    __tablename__ = "telurpro"
    ID: int = Field(default=None, primary_key=True)
    Bulan: str | None = Field(default=None)
    Tgl: str | None = Field(default=None)
    Jmlh: int | None = Field(default=None)
    Persen: float | None = Field(default=None)