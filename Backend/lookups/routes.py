import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from .models import TransactionType, InventoryType, Unit
from .crud import create_new_transction_type, create_new_inventory_type, create_new_unit

lookup_route = APIRouter(prefix="/lookup", tags=["Lookups"])

@lookup_route.post("/transaction")
def add_new_transaction(name:str, session:Session=Depends(get_session)):
    new_transaction = create_new_transction_type(id=None, name=name, session=session)
    if not isinstance(new_transaction, TransactionType):
        raise HTTPException(
            status_code=500,
            detail=new_transaction
        )
    else:
        return new_transaction

@lookup_route.post("inventory")
def add_new_inventory(name:str, session:Session=Depends(get_session)):
    new_inventory_type = create_new_inventory_type(id=None, name=name, session=session)
    if not isinstance(new_inventory_type, InventoryType):
        raise HTTPException(
            status_code=500,
            detail=new_inventory_type
        )
    return new_inventory_type

@lookup_route.post("/unit")
def add_new_unit(name:str, session:Session=Depends(get_session)):
    new_unit = create_new_unit(id=None, name=name, session=session)
    if not isinstance(new_unit, Unit):
        raise HTTPException(
            status_code=500,
            detail=new_unit
        )
    return new_unit

@lookup_route.get("/transaction")
def read_transaction_types(session:Session=Depends(get_session)):
    return session.exec(select(TransactionType)).all()

@lookup_route.get("/transaction/{id}")
def read_transaction_type_by_id(id:int, session:Session=Depends(get_session)):
    transaction_type = session.get(TransactionType, id)
    if not transaction_type:
        raise HTTPException(status_code=404, detail=f"Transaction Type with id {id} does not exist.")
    return transaction_type

@lookup_route.get("/inventory")
def read_all_inventory_type(session:Session=Depends(get_session)):
    return session.exec(select(InventoryType)).all()

@lookup_route.get("/inventory/{id}")
def read_inventory_type_by_id(id:int, session:Session=Depends(get_session)):
    inventory_type = session.get(InventoryType, id)
    if not inventory_type: 
        raise HTTPException(
            status_code=404, 
            detail=f"Inventory Type with id {id} does not exist."
        )
    return inventory_type

@lookup_route.get("/unit")
def read_all_units(session:Session=Depends(get_session)):
    return session.exec(select(Unit)).all()

@lookup_route.get("/unit/{id}")
def read_unit_by_id(id:int, session:Session=Depends(get_session)):
    unit = session.get(Unit, id)
    if not unit:
        raise HTTPException(
            status_code=404,
            detail=f"Unit with id {id} does not exist."
        )
    return unit