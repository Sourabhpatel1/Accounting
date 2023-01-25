from sqlmodel import Session
from .models import Accounts
from .crud import create_new_account, create_new_group_account
import json
import os

cwd = os.getcwd()

def initialize_accounts(session:Session) -> None:
    with open(cwd + "/accounts/init.json", 'r') as f:
        accounts = json.loads(f.read())
        for account in accounts["Group Accounts"]:
            create_new_group_account(id=account["id"], name=account["name"], primary_account_id=account["primary_account_id"], session=session)
        for account in accounts["Accounts"]:
            create_new_account(name=account["name"], group_account_id=account["group_account_id"], session=session)
