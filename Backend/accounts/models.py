import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from lookups.models import PrimaryAccounts
    from documents.models import DebitEntry, CreditEntry
    from inventory.models import InventoryItem
    from customers.models import Customers
    from vendors.models import Vendors

class GroupAccountsBase(SQLModel):
    name:str = Field(unique=True, index=True)
    primary_account_id:int = Field(foreign_key='primaryaccounts.id')

class GroupAccounts(GroupAccountsBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    primary_account:"PrimaryAccounts" = Relationship(back_populates='group_accounts')
    accounts:Optional[List["Accounts"]] = Relationship(back_populates='group_account')

class AccountBase(SQLModel):
    name:str = Field(unique=True, index=True)
    group_account_id:int = Field(foreign_key="groupaccounts.id")

class Accounts(AccountBase, table=True):
    id:Optional[int] = Field(primary_key=True, index=True)
    group_account:"GroupAccounts" = Relationship(back_populates='accounts')
    dr_entries:Optional[List["DebitEntry"]] = Relationship(back_populates="account")
    cr_entries:Optional[List["CreditEntry"]] = Relationship(back_populates="account")
    items:Optional[List["InventoryItem"]] = Relationship(back_populates='account')
    customer:Optional["Customers"] = Relationship(back_populates='account')
    vendor:Optional["Vendors"] = Relationship(back_populates='account')