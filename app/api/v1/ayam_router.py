import select

from fastapi import APIRouter
from app.database import SessionDB1
from app.model.chickenfarm.Ayam import Ayam
from sqlmodel import select, func

router = APIRouter()


@router.post("/")
def create(ayam: Ayam, session: SessionDB1):
    return {"message": "Ayam created successfully"}


## untuk menampilkan semua data ayam
@router.get("/")
def get(session: SessionDB1, limit: int = 10, offset: int = 0):
    ## select * from ayam  limit 10 offset 30;
    query = select(Ayam).limit(limit).offset(offset)
    results = session.exec(query).all()


    ## select count(ayam.id) from ayam 
    query_total = select(func.count(Ayam.ID))
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

@router.get("/{id}")
def getById(session: SessionDB1, id: int):
    query = select(Ayam).where(Ayam.ID == id)
    result = session.exec(query).first()
    if result is None:
        return {"message": "Ayam not found"}
    else: 
        return {
            "data": result
        }


@router.put("/")
def update(ayam: Ayam, session: SessionDB1):
    return {"message": "Ayam updated successfully"}

@router.delete("/")
def delete(ayam: Ayam, session: SessionDB1):
    return {"message": "Ayam deleted successfully"}