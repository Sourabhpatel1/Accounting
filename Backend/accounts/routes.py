import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from .models import AccountBase, Accounts, GroupAccountsBase, GroupAccounts
from .crud import create_new_account, create_new_group_account
from lookups.models import PrimaryAccounts

account_route = APIRouter(prefix="/acc", tags=["Accounts"])

@account_route.post("/group_account")
def add_new_group_account(acc:GroupAccountsBase, session:Session=Depends(get_session)):
    new_group_account = create_new_group_account(id=None, name=acc.name, primary_account_id=acc.primary_account_id, session=session)
    if not isinstance(new_group_account, GroupAccounts):
        raise HTTPException(
            status_code=500,
            detail=new_group_account
        )
    return new_group_account

@account_route.post("/account")
def add_new_account(account:AccountBase, session:Session = Depends(get_session)):
    new_account = create_new_account(name=account.name, group_account_id=account.group_account_id, session=session)
    if not isinstance(new_account, Accounts):
        raise HTTPException(
            status_code=500,
            detail=new_account
        )
    return new_account

@account_route.get("/all/primary")
def read_all_primary_accounts(session:Session=Depends(get_session)):
    return session.exec(select(PrimaryAccounts)).all()

@account_route.get("/all/group")
def read_all_group_accoounts(session:Session=Depends(get_session)):
    return session.exec(select(GroupAccounts)).all()

@account_route.get("/all")
def read_all_account(session:Session=Depends(get_session)):
    accounts = session.exec(select(Accounts)).all()
    return_accounts = []
    
    for account in accounts:
        dr_total = sum([entry.amount for entry in account.dr_entries])
        cr_total = sum([entry.amount for entry in account.cr_entries])
        balance_type:str
        balance:float
        
        if dr_total > cr_total:
            balance = dr_total - cr_total
            balance_type = "Debit"
        else:
            balance = cr_total - dr_total
            balance_type = "Credit"
        
        if balance == 0:
            balance_type = "-"
        
        a = {
            'id' : account.id,
            'group_account_id' : account.group_account_id,
            'name' : account.name,
            'balance' : balance,
            'balance_type' : balance_type
        }
        
        return_accounts.append(a)
    
    return return_accounts

@account_route.get("/{id}")
def get_account_by_id(id:int, session:Session=Depends(get_session)):
    account = session.get(Accounts, id)
    
    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with account id : {id} not found"
        )
    
    dr_total = sum([entry.amount for entry in account.dr_entries])
    cr_total = sum([entry.amount for entry in account.cr_entries])
    
    balance_type:str
    balance:float
    
    if dr_total > cr_total:
        balance = dr_total - cr_total
        balance_type = "Debit"
    else:
        balance = cr_total - dr_total
        balance_type = "Credit"
    
    if balance == 0:
        balance_type = "-"

    return {
        'id' : account.id,
        'primary_account_id' : account.primary_account_id,
        'name' : account.name,
        'balance' : balance,
        'balance_type' : balance_type
    }

@account_route.get("/entries/{id}")
def read_entries(id:int, session:Session=Depends(get_session)):
    account = session.get(Accounts, id)
    if not account:
        raise HTTPException(status_code=404,detail=f"Account with account id {id} not found")
    return {
        "dr_entries" : account.dr_entries,
        "cr_entries" : account.cr_entries
    }

@account_route.get("/ledger/{id}")
def read_ledger(id:int, session:Session=Depends(get_session)):
    account = session.get(Accounts, id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with account id {id} not found"
        )
    dr_entries = account.dr_entries
    cr_entries = account.cr_entries

    credited_accounts = [{'entry': entry.cr_entries[0], 'account' : entry.cr_entries[0].account, 'document' : entry.document or entry.sales_invoice or entry.purchase_invoice} for entry in dr_entries]
    debited_accounts = [{'entry' : entry.dr_entries[0], 'account' : entry.dr_entries[0].account, 'document' : entry.document or entry.sales_invoice or entry.purchase_invoice} for entry in cr_entries]

    return {
        'credited_accounts' : credited_accounts,
        'debited_accounts' : debited_accounts
    }

@account_route.delete("/{id}")
def delete_account(id:int, session:Session=Depends(get_session)):
    account = session.get(Accounts, id)
    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account with account id {id} not found"
        )
    if account.dr_entries or account.cr_entries:
        raise HTTPException(
            status_code=403,
            detail=f"{account.name} is not an empty or unused account and hance can not be deleted."
        )
    session.delete(account)
    session.commit()
    return True