from typing import Optional, List, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
if TYPE_CHECKING:
    from lookups.models import TransactionType
    from accounts.models import Accounts
    from inventory.models import SaleLineItems, PurchaseLineItems
    from customers.models import Customers
    from vendors.models import Vendors


class DocType(Enum):
    journal:str = "Journal"
    cash:str = "Cash"
    bank:str = "Bank"
    sales:str = "Sales"
    purchase:str = "Purchase"
    contra:str = "Contra"
    depriciation:str = "Depriciation"

class EntryType(Enum):
    debit:str = "dr"
    credit:str = "cr"

class EntryLink(SQLModel, table=True):
    dr_entry_id:Optional[int] = Field(default=None, foreign_key='debitentry.id', primary_key=True)
    cr_entry_id:Optional[int] = Field(default=None, foreign_key='creditentry.id', primary_key=True)

class EntryBase(SQLModel):
    account_id:int = Field(foreign_key='accounts.id')
    amount:float

class DebitEntry(EntryBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    document_id:Optional[int] = Field(foreign_key="documents.id")
    sales_invoice_id:Optional[int] = Field(foreign_key='salesinvoices.id')
    purchase_invoice_id:Optional[int] = Field(foreign_key='purchaseinvoices.id')
    account:"Accounts" = Relationship(back_populates='dr_entries')
    document:Optional["Documents"] = Relationship(back_populates='dr_entries')
    sales_invoice:Optional["SalesInvoices"] = Relationship(back_populates='dr_entries')
    purchase_invoice:Optional["PurchaseInvoices"] = Relationship(back_populates='dr_entries')
    cr_entries:List["CreditEntry"] = Relationship(back_populates='dr_entries', link_model=EntryLink)

class CreditEntry(EntryBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    document_id:Optional[int] = Field(foreign_key="documents.id")
    sales_invoice_id:Optional[int] = Field(foreign_key='salesinvoices.id')
    purchase_invoice_id:Optional[int] = Field(foreign_key='purchaseinvoices.id')
    document:Optional["Documents"] = Relationship(back_populates="cr_entries")
    sales_invoice:Optional["SalesInvoices"] = Relationship(back_populates='cr_entries')
    purchase_invoice:Optional["PurchaseInvoices"] = Relationship(back_populates='cr_entries')
    account:"Accounts" = Relationship(back_populates='cr_entries')
    dr_entries:List["DebitEntry"] = Relationship(back_populates='cr_entries', link_model=EntryLink)

class MasterAccount(SQLModel):
    id:int
    entry_type:EntryType

class DocumentBase(SQLModel):
    doc_type:DocType
    doc_date:date = date.today()
    is_cancelled:bool = False

class Documents(DocumentBase, table=True):
    id:Optional[int] = Field(unique=True, index=True, primary_key=True)
    dr_entries:Optional[List["DebitEntry"]] = Relationship(back_populates='document')
    cr_entries:Optional[List["CreditEntry"]] = Relationship(back_populates='document')

class PurchaseInvoiceBase(DocumentBase):
    transaction_type_id:int = Field(foreign_key='transactiontype.id')
    vendor_id:Optional[int] = Field(foreign_key='vendors.id')
    is_cancelled:bool = False

class SalesInvoiceBase(DocumentBase):
    transaction_type_id:int = Field(foreign_key='transactiontype.id')
    customer_id:Optional[int] = Field(foreign_key='customers.id')
    is_cancelled:bool = False

class PurchaseInvoices(PurchaseInvoiceBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    dr_entries:Optional[List["DebitEntry"]] = Relationship(back_populates='purchase_invoice')
    cr_entries:Optional[List["CreditEntry"]] = Relationship(back_populates='purchase_invoice')
    transaction_type:"TransactionType" = Relationship(back_populates='purchase_invoices')
    vendor:"Vendors" = Relationship(back_populates='purchase_invoices')
    line_items:Optional[List["PurchaseLineItems"]] = Relationship(back_populates='purchase_invoice')

class SalesInvoices(SalesInvoiceBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    dr_entries:Optional[List["DebitEntry"]] = Relationship(back_populates='sales_invoice')
    cr_entries:Optional[List["CreditEntry"]] = Relationship(back_populates='sales_invoice')
    transaction_type:"TransactionType" = Relationship(back_populates='sales_invoices')
    customer:"Customers" = Relationship(back_populates='sales_invoices')
    line_items:Optional[List["SaleLineItems"]] = Relationship(back_populates='sales_invoice')

