from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, ForeignKey, Relationship

if TYPE_CHECKING:
    from accounts.models import Accounts, GroupAccounts
    from documents.models import PurchaseInvoices, SalesInvoices
    from inventory.models import InventoryItem

class PrimaryAccounts(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(unique=True, index=True)
    group_accounts:Optional[List["GroupAccounts"]] = Relationship(back_populates='primary_account') 

class TransactionType(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(unique=True, index=True)
    purchase_invoices:Optional[List["PurchaseInvoices"]] = Relationship(back_populates='transaction_type')
    sales_invoices:Optional[List["SalesInvoices"]] = Relationship(back_populates='transaction_type')

class EntryType(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(unique=True, index=True)

class InventoryType(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(unique=True, index=True)
    items:Optional[List["InventoryItem"]] = Relationship(back_populates='type')

class Unit(SQLModel, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    name:str = Field(unique=True, index=True)
    items:Optional[List["InventoryItem"]] = Relationship(back_populates='unit')

