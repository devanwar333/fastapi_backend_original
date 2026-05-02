from pydantic import BaseModel, field_validator


class BelanjaItemRequest(BaseModel):
    id: int | None = None
    jenis_stock: str
    qty: int

    @field_validator("qty")
    def qty_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("qty must be > 0")
        return v

    @field_validator("jenis_stock")
    def jenis_stock_must_not_empty(cls, v):
        if not v:
            raise ValueError("jenis_stock must not be empty")
        return v