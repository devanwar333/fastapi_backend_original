from sqlmodel import Field, SQLModel
class Kandang(SQLModel, table=True):
    __tablename__ = "datakandang"
    ID: int = Field(default=None, primary_key=True)
    Kandang: str | None = Field(default=None)
    Kapasitas: int | None = Field(default=None)