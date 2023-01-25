import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from typing import Optional
from sqlmodel import Session
from database import engine
from .models import PrimaryAccounts, TransactionType, EntryType, InventoryType, Unit

def create_new_primary_account(id:Optional[int], name:str, session:Session) -> PrimaryAccounts or str:
    primary_account = PrimaryAccounts(id=id, name=name)
    try:
        session.add(primary_account)
        session.commit()
        session.refresh(primary_account)
        return primary_account
    except Exception as e:
        return str(e)

def create_new_transction_type(id:Optional[int], name:str, session:Session) -> TransactionType or str:
    transaction_type = TransactionType(id=id, name=name)
    try:
        session.add(transaction_type)
        session.commit()
        session.refresh(transaction_type)
        return transaction_type
    except Exception as e:
        return str(e)

def create_new_entry_type(id:Optional[int], name:str, session:Session) -> EntryType or str:
    entry_type = EntryType(id=id, name=name)
    try:
        session.add(entry_type)
        session.commit()
        session.refresh(entry_type)
        return entry_type
    except Exception as e:
        return str(e)

def create_new_inventory_type(id:Optional[int], name:str, session:Session) -> InventoryType or str:
    inventory_type = InventoryType(id=id, name=name)
    try:
        session.add(inventory_type)
        session.commit()
        session.refresh(inventory_type)
        return inventory_type
    except Exception as e:
        return str(e)

def create_new_unit(id:Optional[int], name:str, session:Session) -> Unit or str:
    unit = Unit(id=Optional[int], name=name)
    try:
        session.add(unit)
        session.commit()
        session.refresh(unit)
        return unit
    except Exception as e:
        return str(e)

