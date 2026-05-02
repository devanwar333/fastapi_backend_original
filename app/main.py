from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import ayam_router
from app.api.v1 import report_router
from app.api.v1.cafe import jenis_stock_router
from app.api.v1.cafe import order_router
from app.database import test_database_connection
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
def startup_event():
    logging.info("Aplikasi dimulai...")
    test_database_connection()
    for route in app.routes:
        logging.info(f"Route terdaftar: {route.path}")
    
base_url = "/api/v1"

app.include_router(ayam_router.router, prefix=base_url+"/ayam", tags=["Ayam"]) ## http://127.0.0.1:8000/api/v1/ayam 
app.include_router(report_router.router, prefix=base_url+"/report", tags=["Report"]) 


cafe_url = base_url + "/cafe"
app.include_router(jenis_stock_router.router, prefix=cafe_url+"/jenis_stock", tags=["Jenis Stok"]) ## http://127.0.0.1:8000/api/v1/cafe/jenis_stock
app.include_router(order_router.router, prefix=cafe_url+"/order", tags=["Order"]) ## http://127.0.0.1:8000/api/v1/cafe/order

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logging.error(f"Terjadi kesalahan: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Terjadi kesalahan pada server. Silakan coba lagi nanti."},
    )

@app.get("/")
def root():
    return {"message": "API is running"}