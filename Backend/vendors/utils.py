from sqlmodel import Session
from accounts.models import Accounts
from .models import Vendors

def make_test_vendor(session:Session) -> None:
    new_vendor_account = Accounts(name='Test Vendor', group_account_id=5)
    
    session.add(new_vendor_account)
    
    new_vendor = Vendors(
        name='Test Vendor',
        email='test@vendor.com',
        country_code='+91',
        phone=9876543210,
        address='Vendor Test Address',
        state='Test State',
        country='Test Country',
        postal_code='496001',
        gst='Test GST No.',
        account_id=new_vendor_account.id,
        account=new_vendor_account
    )

    session.add(new_vendor)
    session.commit()