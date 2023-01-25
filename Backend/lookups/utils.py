import os
import json
from sqlmodel import Session, select
from database import engine
from .crud import create_new_primary_account, create_new_transction_type, create_new_entry_type, create_new_inventory_type, create_new_unit

lookup_file_path = os.getcwd()

def populate_lookup():
    with open(lookup_file_path + "/lookups/lookup.json", 'r') as f:
        lookups = json.loads(f.read())
        with Session(engine) as session:

            for accounts in lookups["primary_accounts"]:
                create_new_primary_account(id=accounts["id"],name=accounts["name"], session=session)
            
            for transction_type in lookups["transaction_type"]:
                create_new_transction_type(id=transction_type["id"], name=transction_type["name"], session=session)
            
            for entry_type in lookups["entry_type"]:
                create_new_entry_type(id=entry_type["id"], name=entry_type["name"], session=session)
            
            for inventory_type in lookups["inventory_type"]:
                create_new_inventory_type(id=inventory_type["id"], name=inventory_type["name"], session=session)
            
            for unit_type in lookups["unit"]:
                create_new_unit(id=unit_type["id"], name=unit_type["name"], session=session)
