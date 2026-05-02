
from datetime import datetime
from pydantic import BaseModel, field_validator
from app.request.belanja_item_request import BelanjaItemRequest

class CreateOrderRequest(BaseModel):

    tanggal: str
    # qty: int
    # jenis_stock: str
    ket: str
    category: str
      

    # @field_validator("qty")
    # def qty_must_be_positive(cls,v):
    #     if v <= 0:
    #         raise ValueError("qty must be > 0")
    #     return v

    # @field_validator("jenis_stock")
    # def jenis_stock_must_not_empty(cls,v):
    #     if not v:
    #         raise ValueError("jenis_stock must not be empty")
    #     return v
    
    @field_validator("ket")
    def ket_must_not_empty(cls,v):
        if not v:
            raise ValueError("ket must not be empty")
        return v
    
    @field_validator("category")
    def category_must_be_exact(cls,v):
        if v not in ["OB", "OS"]:
            raise ValueError("category must be either 'OB' or 'OS'")
        return v

    @field_validator("tanggal")
    def tanggal_format_valid(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("tanggal must be in the format YYYY-MM-DD")
        return v
    
