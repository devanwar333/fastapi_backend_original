from app.request.pick_up_telur_request import PickUpTelurRequest
from pydantic import BaseModel, field_validator
class CreatePickUpTelurRequest(BaseModel):
    data: list[PickUpTelurRequest]


    @field_validator("data")
    def data_must_not_empty(self, v):
        if not v:
            raise ValueError("data must not be empty")
        return v        