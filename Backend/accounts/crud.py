from sqlmodel import Session
from .models import Accounts, GroupAccounts

def create_new_group_account(id:int, name:str, primary_account_id:int, session:Session)->GroupAccounts or str:
    new_group_account = GroupAccounts(
        name=name,
        id=id,
        primary_account_id=primary_account_id
    )
    try:
        session.add(new_group_account)
        session.commit()
        session.refresh(new_group_account)
        return new_group_account
    except Exception as e:
        return str(e)

def create_new_account(name:str, group_account_id:int, session:Session)->Accounts or str:
    new_account = Accounts(
        name=name,
        group_account_id=group_account_id
    )
    try:
        session.add(new_account)
        session.commit()
        session.refresh(new_account)
        return new_account
    except Exception as e:
        return str(e)