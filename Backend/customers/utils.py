from sqlmodel import Session
from accounts.models import Accounts
from .models import Customers

def make_test_customer(session:Session) -> None:
    new_customer_account = Accounts(name='Test Customer', group_account_id=12)
    
    session.add(new_customer_account)
    
    new_customer = Customers(
        name='Test Customer',
        email='test@customer.com',
        country_code='+91',
        phone=9876543210,
        address='Customer Test Address',
        state='Test State',
        country='Test Country',
        postal_code='496001',
        gst='Test GST No.',
        account_id=new_customer_account.id,
        account=new_customer_account
    )

    session.add(new_customer)
    session.commit()