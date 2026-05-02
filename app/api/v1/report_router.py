from fastapi import APIRouter, Depends # Import Depends
from app.database import SessionDB1
from app.model.chickenfarm.Kandang import Kandang
from app.model.chickenfarm.Ayam import Ayam
from app.model.chickenfarm.AyamMini import AyamMini
from app.model.chickenfarm.TempJmlhAyam import TempJmlhAyam
from app.model.chickenfarm.TelurPro import TelurPro
from app.model.chickenfarm.MskAnakAyam import MskAnakAyam
from sqlmodel import select


router = APIRouter()

@router.get("/{tanggal}")
# Use Depends to inject the database session
def get(tanggal: str, session: SessionDB1): 
    
    ayam_subquery = select(
        Ayam.Kandang,
        MskAnakAyam.TglMsk.label("Tgl"),
        TelurPro.Jmlh,
    ).join(
        AyamMini, AyamMini.ID == Ayam.ID_Mini
    ).join(
        MskAnakAyam, MskAnakAyam.ID == AyamMini.ID_kcl
    ).join(
        TelurPro, TelurPro.ID == Ayam.ID
    ).where(
        TelurPro.Tgl == tanggal
    ).subquery()

    jmlh_ayam_subquery = select(
        TempJmlhAyam.Kandang,
        TempJmlhAyam.Jmlh
    ).where(
        TempJmlhAyam.Tgl == tanggal
    ).subquery()

    query = select(
        ayam_subquery.c.Tgl.label("tgl_lahir"),
        ayam_subquery.c.Kandang,
        jmlh_ayam_subquery.c.Jmlh,
        ayam_subquery.c.Jmlh.label("jmlh_telur")
    ).join(
        jmlh_ayam_subquery,
        ayam_subquery.c.Kandang == jmlh_ayam_subquery.c.Kandang
    )
    
    results = session.exec(query).all()

    
    
    return {
        "data": [
            {
                "TglLahir": row[0],
                "Kandang": row[1],
                "Jmlh": row[2],
                "JmlhTelur": row[3]
            }
            for row in results
        ]
    }

