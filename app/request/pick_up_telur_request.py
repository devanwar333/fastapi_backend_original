from pydantic import BaseModel, field_validator

class PickUpTelurRequest(BaseModel):
    kandang: str
    ikat: int
    papan: int
    butir: int
    tipe : str
    jenis_ayam: str

    @field_validator("kandang")
    def kandang_must_not_empty(cls, v):
        if not v:
            raise ValueError("kandang must not be empty")
        return v
    
    @field_validator("ikat")
    def ikat_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("ikat must be >= 0")
        return v
    
    @field_validator("papan")
    def papan_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("papan must be >= 0")
        return v
    
    @field_validator("butir")
    def butir_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("butir must be >= 0")
        return v
    
    @field_validator("tipe")
    def tipe_must_not_empty(cls, v):
        if v not in ["B", "P"]:
            raise ValueError("tipe must be 'B' or 'P'")
        return v

    @field_validator("jenis_ayam")
    def jenis_ayam_must_not_empty(cls, v):
        if v not in ["Layer", "Arab"]:
            raise ValueError("jenis_ayam must be 'Layer' or 'Arab'")
        return v




