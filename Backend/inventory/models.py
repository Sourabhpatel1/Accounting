from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime

if TYPE_CHECKING:
    from accounts.models import Accounts
    from documents.models import SalesInvoices, PurchaseInvoices
    from lookups.models import InventoryType, Unit

class InventoryItemBase(SQLModel):
    name:str = Field(unique=True, index=True)
    unit_id:int = Field(foreign_key='unit.id')
    type_id:int = Field(foreign_key='inventorytype.id')
    account_id:int = Field(foreign_key="accounts.id")

class InventoryItem(InventoryItemBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    date_created:date = date.today()
    type:"InventoryType" = Relationship(back_populates='items')
    unit:"Unit" = Relationship(back_populates='items')
    account:"Accounts" = Relationship(back_populates='items')
    sale_line_items:"SaleLineItems" = Relationship(back_populates='inventory')
    purchase_line_items:"PurchaseLineItems" = Relationship(back_populates='inventory')
    

class LineItemBase(SQLModel):
    quantity:float
    price:float
    inventory_id:int = Field(foreign_key='inventoryitem.id')

class SaleStockLink(SQLModel, table=True):
    stock_id:Optional[int] = Field(default=None, foreign_key='stock.id', primary_key=True)
    sale_line_item_id:Optional[int] = Field(default=None, foreign_key='salelineitems.id', primary_key=True)

class SaleLineItems(LineItemBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    inventory:InventoryItem = Relationship(back_populates='sale_line_items')
    sales_invoice_id:int = Field(foreign_key='salesinvoices.id')
    sales_invoice:"SalesInvoices" = Relationship(back_populates='line_items')
    stocks:Optional[List["Stock"]] = Relationship(back_populates='sale_line_items', link_model=SaleStockLink)

class PurchaseLineItems(LineItemBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    inventory:InventoryItem = Relationship(back_populates='purchase_line_items')
    purchase_invoice_id:int = Field(foreign_key='purchaseinvoices.id')
    purchase_invoice:"PurchaseInvoices" = Relationship(back_populates='line_items')
    stock_id:Optional[int] = Field(foreign_key='stock.id')
    stock:Optional["Stock"] = Relationship(back_populates='purchase_line_items')

class Stock(LineItemBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    date:datetime = datetime.utcnow()
    purchase_line_items:Optional[List["PurchaseLineItems"]] = Relationship(back_populates='stock')
    sale_line_items:Optional[List["SaleLineItems"]] = Relationship(back_populates='stocks', link_model=SaleStockLink)
