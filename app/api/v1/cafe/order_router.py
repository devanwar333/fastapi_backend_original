from fastapi import APIRouter
from app.database import SessionCafeDB
from sqlmodel import select, func, delete
from app.model.cafe.BbOrder import BbOrder
from app.model.cafe.JenisStok import JenisStok
from app.model.cafe.Belanja import Belanja
from app.model.cafe.OrderStok import OrderStok
from app.request.create_order_request import CreateOrderRequest
from app.request.add_order_belanja_request import AddEditOrderBelanjaRequest
from app.request.add_edit_order_stock_request import AddEditOrderStockRequest
from datetime import datetime as Date
from fastapi import HTTPException
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/{type_order}")
def get(session: SessionCafeDB, type_order: str, limit: int = 10, offset: int = 0):

    if (type_order not in ["OB", "OS"]):
        return {
            "message": "type_order must be either 'OB' or 'OS'",
        }
    total_item_query = None
    if (type_order == "OB"):
        total_item_query = select(Belanja.ID.label("IDOrder"), func.count(Belanja.ID)).group_by(Belanja.ID).subquery()
    elif (type_order == "OS"):
        total_item_query = select(OrderStok.IDOrder, func.count(OrderStok.IDOrder)).group_by(OrderStok.IDOrder).subquery()
    query = select(
        BbOrder,
        func.coalesce(total_item_query.c.count, 0).label("total_items")
    ).outerjoin(total_item_query, BbOrder.IDOrder == total_item_query.c.IDOrder).limit(limit).offset(offset)
    query = query.order_by(BbOrder.IDOrder.desc())
    results = session.exec(query).all()

    query_total = select(func.count(BbOrder.IDOrder))
    total = session.exec(query_total).first()

    data = []

    # mapping
    for row in results:
        order = row[0]
        total_items = row[1]

        order_dict = order.model_dump()   # kalau error, ganti jadi order.dict()
        order_dict["Total_Items"] = total_items

        data.append(order_dict)

    return {
        "data" : data,
        "paging" : {
            "limit": limit, 
            "offset": offset, 
            "total": total
        }
    }


# @router.get("/{id_order}")
# def get_detail_by_id(session: SessionCafeDB, id_order: int):
#     query = select(BbOrder).where(BbOrder.IDOrder == id_order)
#     result = session.exec(query).first()
#     return {
#         "data": result
#     }

# @router.get("/{category}/{tanggal}")
# def get_order_by_date(session: SessionCafeDB, category: str, tanggal: str):
#     query = select(BbOrder).where(BbOrder.Tgl == tanggal, BbOrder.Category == category)
#     result = session.exec(query).first()

#     if (result is None):
#         lastest_id = select(func.max(BbOrder.IDOrder))
#         result_id = session.exec(lastest_id).first()
#         if (result_id is None):
#             result_id = 1
#         else : 
#             result_id = result_id + 1
#         query_add = BbOrder(IDOrder=result_id, Tgl=tanggal, Total=0, Aktif=True, Inputer=0, Category=category, Checked=False, ID_Check=0, Ket="")
#         session.add(query_add)
#         session.commit()
#         query_search = select(BbOrder).where(BbOrder.IDOrder == result_id)
#         result = session.exec(query_search).first()
#         return {
#             "data": result
#         }

#     return {
#         "data": result
#     }

def get_latest_id(session: SessionCafeDB):
    query = select(func.max(BbOrder.IDOrder))
    latest_id = session.exec(query).first()
    return latest_id if latest_id is not None else 0

def get_order_belanja_lastest_id(session: SessionCafeDB):
    query = select(func.max(Belanja.ID))
    latest_id = session.exec(query).first()
    return latest_id if latest_id is not None else 0

@router.post("")
def create_order(session: SessionCafeDB, new_order: CreateOrderRequest):
    try:
        new_id = get_latest_id(session) + 1
    
        date = Date.strptime(new_order.tanggal, "%Y-%m-%d")
        order = BbOrder(
            IDOrder=new_id,
            Tgl=date,
            Total=0,
            Aktif=True,
            Inputer=0,
            Category=new_order.category,
            Checked=False,
            ID_Check=0,
            Ket=new_order.ket
        )

        session.add(order)
        session.commit()
        session.refresh(order)

        return {
            "data" : order,
            "message": "Order created successfully",
        }
    except Exception as e:
        session.rollback()
        print(f"Error creating order: {e}")
        return {
            "message": "Failed to create order",
        }

@router.get("/{id_order}/belanja")
def get_belanja_by_id(session: SessionCafeDB, id_order: int):

    query = select(Belanja).where(Belanja.ID == id_order).join(JenisStok, Belanja.Jenis == JenisStok.Jenis)
    result = session.exec(query).all()
    return {
        "data": result,
        
    }

@router.post("/{id_order}/belanja")
def add_belanja(session: SessionCafeDB, id_order: int, add_belanja: AddEditOrderBelanjaRequest):
    try:
       
        order = session.get(BbOrder, id_order)
        if order is None:
            return {
                "message": "Order not found",
            }
    

        delete_all_belanja = delete(Belanja).where(
            Belanja.ID == id_order
        )
        session.exec(delete_all_belanja)

        new_added_belanja = {}
        for item in add_belanja.data:
            if item.jenis_stock in new_added_belanja:
                return {
                    "message": f"Duplicate jenis_stock: {item.jenis_stock}",
                }
            jenis_stock_query = select(JenisStok).where(JenisStok.Jenis == item.jenis_stock, JenisStok.Aktif == True)
            jenis_stock = session.exec(jenis_stock_query).first()
            if jenis_stock is None:
                return {
                    "message": "Jenis stock not found or not active",
                }
            belanja = Belanja(
                ID=order.IDOrder,
                Jenis=item.jenis_stock,
                Jmlh=item.qty,
                ket=item.ket,
                Unit=jenis_stock.Unit,
                Price=0,
                Divisi="",
                Checked=False
            )
            new_added_belanja[item.jenis_stock] = belanja
            session.add(belanja)
            
        session.commit()
        return {
            "message": "Belanja added successfully",
        }
    except Exception as e:
        session.rollback()
        return {
            "message": "something went wrong",
        }
    
@router.post("/{id_order}/stok")
def add_order_stock(session: SessionCafeDB, id_order: int, add_order_stock: AddEditOrderStockRequest):
    try:
        order = session.get(BbOrder, id_order)
        if order is None:
            return JSONResponse(status_code=404, content={"message": "Order not found"})
        
        delete_all_order_stok = delete(OrderStok).where(
            OrderStok.IDOrder == id_order
        )
        session.exec(delete_all_order_stok)

        new_added_order_stok = {}
        for item in add_order_stock.data:
            if item.jenis_stock in new_added_order_stok:
                return {
                    "message": f"Duplicate jenis_stock: {item.jenis_stock}",
                }
            jenis_stock_query = select(JenisStok).where(JenisStok.Jenis == item.jenis_stock, JenisStok.Aktif == True)
            jenis_stock_result = session.exec(jenis_stock_query).first()
            if jenis_stock_result is None:
                return {
                    "message": "Jenis stock not found or not active",
                }
            order_stok = OrderStok(
                IDOrder=id_order,
                Jenis=item.jenis_stock,
                Jmlh=item.qty,
                Tgl=Date.now().strftime("%Y-%m-%d"),
                JmlhInp=0,
                unit=jenis_stock_result.Unit,
                Divisi="",
                Inputer=0,
                Ket=item.ket
            )
            new_added_order_stok[item.jenis_stock] = order_stok
            session.add(order_stok)
        session.commit()
        return {
            "message": "Order stock added successfully",
        }
    except Exception as e:
        session.rollback()
        print(f"Error adding order stock: {e}")
        return {
            "message": "Failed to add order stock",
        }
    


@router.get("/{id_order}/order_stok")
def get_order_stok_by_id(session: SessionCafeDB, id_order: int): 
    query = select(OrderStok).where(OrderStok.IDOrder == id_order)
    result = session.exec(query).all()
    return {
        "data": result
    }

@router.delete("/{id_order}")
def delete_order_by_id(session: SessionCafeDB, id_order: int):
    try:
        order = session.get(BbOrder, id_order)
        if order is None:
            return {
                "message": "Order not found",
            }
        session.delete(order)
        session.commit()
        return {
            "message": "Order deleted successfully",
        }
    except Exception as e:
        session.rollback()
        print(f"Error deleting order: {e}")
        return {
            "message": "Failed to delete order",
        }

