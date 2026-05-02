from fastapi import APIRouter, Depends # Import Depends
from app.request.pick_up_telur_request import PickUpTelurRequest
from app.request.create_pick_up_telur_request import CreatePickUpTelurRequest
from app.database import SessionFarmDB as SessionDB
from app.model.chickenfarm.TempPickTelur import TempPickTelur
from datetime import date
router = APIRouter()

@router.post("/")
def create(request: CreatePickUpTelurRequest, session: SessionDB):
    now = date.today().strftime("yyyy-mm-dd")
    for item in request.data:
        pick_up_telur = TempPickTelur(
            Tgl= now,
            Kandang=item.kandang,
            Ikat=item.ikat,
            Ppn=item.papan,
            Butir=item.butir,
            Tipe=item.tipe,
            Jenisayam=item.jenis_ayam,
            Input=0

        )
        session.add(pick_up_telur)
    session.commit()
    return {"message": "Pick up telur created successfully"}
