from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from inventory.models import InventoryItem, InventoryItemBase

inv_route = APIRouter(prefix="/inv", tags=["Inventory"])

@inv_route.post("/")
def add_new_inventory_item(inv:InventoryItemBase, session:Session=Depends(get_session)):
    inventory_in_db = session.exec(select(InventoryItem).where(InventoryItem.name == inv.name)).first()
    if inventory_in_db:
        raise HTTPException(status_code=403, detail=f"Inventory Item with name {inv.name} already exists.")
    new_inventory = InventoryItem.from_orm(inv)
    session.add(new_inventory)
    session.commit()
    session.refresh(new_inventory)
    return new_inventory

@inv_route.get("/")
def read_all_inventory(session:Session=Depends(get_session)):
    inventories = session.exec(select(InventoryItem)).all()
    return [
        {
            'item' : inventory,
            'stock' : [{
                        'quantity' : item.stock.quantity,
                        'date_purchased' : item.stock.date
                       } for item in inventory.purchase_line_items]
        } for inventory in inventories
    ]

@inv_route.get("/sales_items")
def read_all_sales_inventory(session:Session=Depends(get_session)):
    inventory = session.exec(select(InventoryItem).where(InventoryItem.type_id == 1)).all()
    return inventory

@inv_route.get("/{id}")
def read_inventory_by_id(id:int, session:Session=Depends(get_session)):
    item = session.get(InventoryItem, id)
    if not item: 
        raise HTTPException(
            status_code=404,
            detail=f"Inventory Item with id {id} does not exist."
        )
    return item
