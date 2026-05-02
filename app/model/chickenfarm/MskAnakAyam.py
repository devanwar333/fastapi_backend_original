from sqlmodel import Field, SQLModel
class MskAnakAyam(SQLModel, table=True):
    __tablename__ = "mskanakayam"
    ID: int = Field(default=None, primary_key=True)
    TglMsk: str | None = Field(default=None)