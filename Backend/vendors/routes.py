
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from vendors.models import Vendors, VendorRequest, VendorUpdate
from accounts.models import Accounts


vendor_route = APIRouter(prefix='/ven', tags=["Vendors"])

@vendor_route.post("/")
def add_new_vendor(vendor:VendorRequest, session:Session=Depends(get_session)):
    existing_vendor = session.exec(select(Vendors).where(Vendors.name == vendor.name)).first()
    if existing_vendor:
        raise HTTPException(
            status_code=403,
            detail=f"Vendor with name {vendor.name} already exists in the database, please try a diffrent name."
        )
    new_vendor_account = Accounts(name=vendor.name, group_account_id=3)
    session.add(new_vendor_account)
    new_vendor = Vendors(
        name=vendor.name,
        email=vendor.email,
        phone=vendor.phone,
        country_code=vendor.country_code,
        address=vendor.address,
        state=vendor.state,
        country=vendor.country,
        postal_code=vendor.postal_code,
        account_id=new_vendor_account.id,
        account=new_vendor_account,
        gst=vendor.gst
    )
    session.add(new_vendor)
    session.commit()
    session.refresh(new_vendor)
    return new_vendor

@vendor_route.get("/")
def read_all_vendors(session:Session=Depends(get_session)):
    return session.exec(select(Vendors)).all()

@vendor_route.get("/{id}")
def read_vendor_by_id(id:int, session:Session=Depends(get_session)):
    vendor = session.get(Vendors, id)
    if not vendor:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor with id {id} does not exist."
        )
    return vendor

@vendor_route.patch("/{id}")
def update_vendor(vendor:VendorUpdate, session:Session=Depends(get_session)):
    vendor = session.get(Vendors, id)
    if not vendor:
        raise HTTPException(
            status_code=404,
            detail=f"Vendor with id {id} does not exist."
        )
    vendor_update_data = vendor.dict(exclude_unset=True)
    for key, value in vendor_update_data.items():
        setattr(vendor, key, value)
    
    session.add(vendor)
    session.commit()
    session.refresh(vendor)
    return vendor

