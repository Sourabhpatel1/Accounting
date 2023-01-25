from fastapi import APIRouter
from lookups.routes import lookup_route
from accounts.routes import account_route
from customers.routes import customer_route
from vendors.routes import vendor_route
from documents.routes import doc_route
from inventory.routes import inv_route

base_router = APIRouter()

base_router.include_router(account_route)
base_router.include_router(lookup_route)
base_router.include_router(customer_route)
base_router.include_router(vendor_route)
base_router.include_router(doc_route)
base_router.include_router(inv_route)