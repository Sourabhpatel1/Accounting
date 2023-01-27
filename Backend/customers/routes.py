from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from customers.models import Customers, CustomerRequest, CustomerUpdate
from accounts.models import Accounts

customer_route = APIRouter(prefix='/cust', tags=["Customers"])

@customer_route.post("/")
def add_new_customer(customer:CustomerRequest, session:Session=Depends(get_session)):
    existing_customer = session.exec(select(Customers).where(Customers.name == customer.name)).first()
    if existing_customer:
        raise HTTPException(
            status_code=403,
            detail = f"Customer with name '{customer.name}' already exists."
        )
    new_customer_account = Accounts(name=customer.name, group_account_id=5)
    session.add(new_customer_account)
    new_customer = Customers(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        country_code=customer.country_code,
        country=customer.country,
        state=customer.state,
        address=customer.address,
        postal_code=customer.postal_code,
        gst=customer.gst,
        account_id=new_customer_account.id,
        account=new_customer_account
    )
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer

@customer_route.get("/all")
def read_all_customers(session:Session=Depends(get_session)):
    return session.exec(select(Customers)).all()

@customer_route.get("/{id}")
def read_customer_by_id(id:int, session:Session=Depends(get_session)):
    customer = session.get(Customers, id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer id {id} not found"
        )
    return customer

@customer_route.patch("/{id}")
def update_customer_details(customer_details:CustomerUpdate, id:int, session:Session=Depends(get_session)):
    customer = session.get(Customers, id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer with customer id {id} not found"
        )
    customer_update_data = customer_details.dict(exclude_unset=True)
    for key, value in customer_update_data.items():
        setattr(customer, key, value)
    
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer