from fastapi import APIRouter
from app.database import SessionCafeDB
from sqlmodel import select, func, SQLModel
from app.model.cafe.JenisStok import JenisStok
router = APIRouter()

class JenisStokCreateRequest(SQLModel):
    Jenis: str
    Unit: str
    Aktif: bool


def get_latest_id(session: SessionCafeDB):
    query = select(func.max(JenisStok.ID))
    latest_id = session.exec(query).first()
    return latest_id if latest_id is not None else 0

def generate_new_id(session: SessionCafeDB):
    latest_id = get_latest_id(session)
    return latest_id + 1

@router.post("/")
def create(session: SessionCafeDB, data: JenisStokCreateRequest):
    new_id = generate_new_id(session)
    new_jenis_stok = JenisStok(
        ID=new_id,
        Jenis=data.Jenis,
        Unit=data.Unit,
        Aktif=data.Aktif,
    )
    session.add(new_jenis_stok)
    session.commit()
  
    return {
        "message": "Jenis Stok berhasil dibuat",
    }

@router.get("/")
def get(session: SessionCafeDB, limit: int = 10, offset: int = 0, search: str = None):
    ## select * from ayam  limit 10 offset 30 where nama like '%ayam%'
    query = select(JenisStok).limit(limit).offset(offset)
    if search:
        query = query.where(JenisStok.Jenis.like(f"%{search}%"))
    results = session.exec(query).all()
    
    ## select count(ayam.id) from ayam where nama like '%ayam%'
    query_total = select(func.count(JenisStok.ID))
    if search:
        query_total = query_total.where(JenisStok.Jenis.like(f"%{search}%"))
    total = session.exec(query_total).first()
    
    ## response
    return {
        "data" : results,
        "paging" : {
            "limit": limit, ## definisi untuk limit ambil data
            "offset": offset, ## definisi untuk offset data
            "total": total
        }
    }



