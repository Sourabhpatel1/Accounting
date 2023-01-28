from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from accounts.models import Accounts
    from documents.models import PurchaseInvoices

class Vendors(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(index=True, unique=True)
    email:str = Field(unique=True)
    country_code:str = Field(max_length=5)
    phone:int
    address:str
    state:str
    country:str
    postal_code:int
    gst:str = Field(max_length=16)
    purchase_invoices:Optional[List["PurchaseInvoices"]] = Relationship(back_populates='vendor')
    account_id:int = Field(foreign_key='accounts.id')
    account:"Accounts" = Relationship(back_populates='vendor')

class VendorRequest(SQLModel):
    name:str = Field(index=True, unique=True)
    email:str = Field(unique=True)
    country_code:str = Field(max_length=5)
    phone:int
    address:str
    state:str
    country:str
    postal_code:int
    gst:Optional[str] = Field(max_length=16)

class VendorUpdate(SQLModel):
    email:Optional[str] = Field(unique=True)
    country_code:Optional[str] = Field(max_length=5)
    phone:Optional[int]
    address:Optional[str]
    state:Optional[str]
    country:Optional[str]
    postal_code:Optional[int]
    gst:Optional[str] = Field(max_length=16)