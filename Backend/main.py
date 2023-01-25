from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import create_db_and_tables, engine

from lookups.models import PrimaryAccounts, TransactionType, EntryType, InventoryType, Unit
from accounts.models import Accounts
from documents.models import Documents
from inventory.models import InventoryItem
from customers.models import Customers
from vendors.models import Vendors

from lookups.utils import populate_lookup
from accounts.utils import initialize_accounts
from vendors.utils import make_test_vendor
from customers.utils import make_test_customer

from base_routes import base_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(base_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(PrimaryAccounts)).all():
            populate_lookup()
            initialize_accounts(session=session)
            make_test_vendor(session=session)
            make_test_customer(session=session)