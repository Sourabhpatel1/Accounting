from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from accounts.models import Accounts
from documents.models import EntryType, MasterAccount, Documents, DocumentBase, PurchaseInvoiceBase, PurchaseInvoices, SalesInvoiceBase, SalesInvoices, DebitEntry, CreditEntry, EntryBase
from vendors.models import Vendors
from customers.models import Customers
from inventory.models import LineItemBase, PurchaseLineItems, SaleLineItems, InventoryItem, Stock

import time


doc_route = APIRouter(prefix="/doc", tags=["Documents"])

@doc_route.post("/general")
def add_document(document:DocumentBase, master_account:MasterAccount, entries:List[EntryBase], session:Session=Depends(get_session)):
    new_document = Documents.from_orm(document)
    session.add(new_document)

    master_account_in_db = session.get(Accounts, master_account.id)

    if not master_account_in_db:
        raise HTTPException(
            status_code=404,
            detail=f"Account with account id {master_account.id} not found"
        )

    if master_account.entry_type == EntryType.debit:
        for entry in entries:
            account = session.get(Accounts, entry.account_id)
            if not account:
                raise HTTPException(status_code=404, detail=f"Account with account id {entry.account_id} not found")
            new_cr_entry = CreditEntry.from_orm(entry, update={
                'document_id' : new_document.id,
                'document' : new_document,
                'account_id' : account.id,
                'account' : account
            })
            new_dr_entry = DebitEntry(
                account_id=master_account_in_db.id,
                account=master_account_in_db,
                amount=entry.amount,
                document_id=new_document.id,
                document=new_document 
            )    
            new_cr_entry.dr_entries.append(new_dr_entry)
            session.add(new_dr_entry)
            session.add(new_cr_entry)
    else:
        for entry in entries:
            account = session.get(Accounts, entry.account_id)

            if not account:
                raise HTTPException(status_code=404, detail=f"Account with account id {entry.account_id} not found")
            
            new_dr_entry = DebitEntry.from_orm(entry, update={
                'document_id': new_document.id,
                'document' : new_document,
                'account_id' : account.id,
                'account' : account
            })

            new_cr_entry = CreditEntry(
                account_id=master_account_in_db.id,
                account=master_account_in_db,
                amount=entry.amount,
                document_id=new_document.id,
                document=new_document
            )
            new_dr_entry.cr_entries.append(new_cr_entry)

            session.add(new_dr_entry)
            session.add(new_cr_entry)
        
    session.commit()
    session.refresh(new_document)
    return (new_document, new_document.dr_entries, new_document.cr_entries)

@doc_route.post("/purchase")
def add_purchase_invoice(invoice:PurchaseInvoiceBase, items:List[LineItemBase], session:Session=Depends(get_session)):
    new_purchase_invoice = PurchaseInvoices.from_orm(invoice)
    session.add(new_purchase_invoice)

    for item in items:
        # Inventory
        inventory = session.get(InventoryItem, item.inventory_id)
        
        if not inventory:
            raise HTTPException(
                status_code=404,
                detail=f"Inventory with inventory id {item.inventory_id} not found"
            )
        
        # Accounts
        purchase_cr_account:Accounts
        vendor = session.get(Vendors, invoice.vendor_id)
        if not vendor:
            raise HTTPException(status_code=404,detail=f"Vendor with id {invoice.vendor_id} not found.")

        if invoice.transaction_type_id == 1:
            purchase_cr_account = session.exec(select(Accounts).where(Accounts.name=="Cash in Hand")).first()
        elif invoice.transaction_type_id == 2:
            purchase_cr_account = session.exec(select(Accounts).where(Accounts.name=="Bank Account")).first()
        else:
            purchase_cr_account = vendor.account
        
        gst_account = session.exec(select(Accounts).where(Accounts.name == "GST-input")).first()
        discount_account = session.exec(select(Accounts).where(Accounts.name=="Discount Received")).first()
        
        #Amounts
        gross_total = item.price * item.quantity
        discount_amount = gross_total * (item.discount_rate/100)
        total_after_discount = gross_total - discount_amount
        gst_amount = total_after_discount * (item.gst_rate/100)
        
        #Purcahse Enrty
        dr_purchase_entry = DebitEntry(
            account_id=inventory.account_id,
            account=inventory.account,
            amount=gross_total-discount_amount,
            purchase_invoice_id=new_purchase_invoice.id,
            purchase_invoice=new_purchase_invoice
        )
        cr_purchase_entry = CreditEntry(
            account_id=purchase_cr_account.id,
            account=purchase_cr_account,
            amount=gross_total-discount_amount,
            purchase_invoice_id=new_purchase_invoice.id,
            purchase_invoice=new_purchase_invoice
        )
        session.add(dr_purchase_entry)
        session.add(cr_purchase_entry)
        dr_purchase_entry.cr_entries.append(cr_purchase_entry)
        #Discount Entry
        if not discount_amount == 0:
            dr_discount_entry = DebitEntry(
                account_id=inventory.account_id,
                account=inventory.account,
                amount=discount_amount,
                purchase_invoice_id=new_purchase_invoice.id,
                purchase_invoice=new_purchase_invoice
            )
            cr_discount_entry = CreditEntry(
                account_id=discount_account.id,
                account=discount_account,
                amount=discount_amount,
                purchase_invoice_id=new_purchase_invoice.id,
                purchase_invoice=new_purchase_invoice
            )
            session.add(dr_discount_entry)
            session.add(cr_discount_entry)
            dr_discount_entry.cr_entries.append(cr_discount_entry)
        #GST Entry
        if not gst_amount == 0:
            dr_gst_entry = DebitEntry(
                account_id=gst_account.id,
                account=gst_account,
                amount=gst_amount,
                purchase_invoice_id=new_purchase_invoice.id,
                purchase_invoice=new_purchase_invoice
            )
            cr_gst_entry = CreditEntry(
                account_id=purchase_cr_account.id,
                account=purchase_cr_account,
                amount=gst_amount,
                purchase_invoice_id=new_purchase_invoice.id,
                purchase_invoice=new_purchase_invoice
            )
            session.add(dr_gst_entry)
            session.add(cr_gst_entry)
            dr_gst_entry.cr_entries.append(cr_gst_entry)

        #Items
        new_stock = Stock.from_orm(item, update={
            'discount_amount' : discount_amount,
            'gst_amount' : gst_amount,
            'total' : gross_total-discount_amount+gst_amount
        })

        new_line_item = PurchaseLineItems(
            quantity=item.quantity,
            price=item.price,
            inventory_id=inventory.id,
            inventory=inventory,
            purchase_invoice_id=new_purchase_invoice.id,
            purchase_invoice=new_purchase_invoice,
            stock_id=new_stock.id,
            stock=new_stock,
            discount_rate=item.discount_rate,
            discount_amount=discount_amount,
            gst_rate=item.gst_rate,
            gst_amount=gst_amount,
            total=total_after_discount
        )
        session.add(new_stock)
        session.add(new_line_item)

    # Updates
    session.add(new_purchase_invoice)
    session.add(inventory)
    session.add(purchase_cr_account)
    session.add(vendor)
    session.add(gst_account)
    session.add(gst_account)
    
    # Commit
    session.commit()

    return new_purchase_invoice, new_purchase_invoice.dr_entries, new_purchase_invoice.cr_entries, new_purchase_invoice.line_items

@doc_route.post("/cash_sale")
def add_cash_sales_invoice(invoice:SalesInvoiceBase, items:List[LineItemBase], session:Session=Depends(get_session)):
    new_sales_invoice = SalesInvoices.from_orm(invoice)
    session.add(new_sales_invoice)

    item_total = 0

    for item in items:
        inventory = session.get(InventoryItem, item.inventory_id)
        
        if not inventory:
            raise HTTPException(status_code=404, detail=f"Inventory with inventory id {item.inventory_id} not found")

        new_sale_line_item = SaleLineItems(
            quantity=item.quantity,
            price=item.price,
            inventory_id=inventory.id,
            inventory=inventory,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice
        )

        session.add(new_sale_line_item)
        new_sales_invoice.line_items.append(new_sale_line_item)
        
        inventory_stock = session.exec(select(Stock).where(Stock.inventory_id == item.inventory_id)).all()
        cost_account = session.exec(select(Accounts).where(Accounts.name == "COGS")).first()
        
        inventory_account = inventory.account
        sale_quantity = item.quantity

        if len(inventory_stock) == 0:
            raise HTTPException(
                status_code=403,
                detail=f"There is no stock of item {inventory.name}"
            )

        if sum(stock.quantity for stock in inventory_stock) < item.quantity:
            raise HTTPException(
                status_code=403,
                detail=f"Not enough inventory of item {inventory.name} for the specified sale quantity"
            )

        for stock in inventory_stock:
            if sale_quantity == 0:
                break
            if not stock.quantity == 0:
                if sale_quantity <= stock.quantity:
                    stock.sale_line_items.append(new_sale_line_item)
                    stock.quantity -= sale_quantity
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    
                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)

                    item_total += sale_quantity * item.price
                    sale_quantity = 0
                else:
                    stock.sale_line_items.append(new_sale_line_item)
                    sale_quantity -= stock.quantity
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount= stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )

                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)

                    item_total += stock.quantity * item.price
                    stock.quantity = 0

    cash_account = session.exec(select(Accounts).where(Accounts.name=="Cash")).first()
    sales_account = session.exec(select(Accounts).where(Accounts.name=="Sales")).first()

    cash_entry = DebitEntry(
        account_id=cash_account.id,
        account=cash_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )


    sales_entry = CreditEntry(
        account_id=sales_account.id,
        account=sales_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )

    cash_entry.cr_entries.append(sales_entry)
    cash_account.dr_entries.append(cash_entry)
    sales_account.cr_entries.append(sales_entry)
    new_sales_invoice.dr_entries.append(cash_entry)
    new_sales_invoice.cr_entries.append(sales_entry)
    session.add(cash_entry)
    session.add(cash_account)
    session.add(sales_entry)
    session.add(sales_account)
    session.add(new_sales_invoice)
    session.commit()
    session.refresh(new_sales_invoice)
    
    return new_sales_invoice
    
@doc_route.post("/bank_sale")
def add_bank_sales_invoice(invoice:SalesInvoiceBase, items:List[LineItemBase], session:Session=Depends(get_session)):
    new_sales_invoice = SalesInvoices.from_orm(invoice)
    session.add(new_sales_invoice)

    item_total = 0

    for item in items:
        inventory = session.get(InventoryItem, item.inventory_id)
        
        if not inventory:
            raise HTTPException(status_code=404, detail=f"Inventory with inventory id {item.inventory_id} not found")

        new_sale_line_item = SaleLineItems(
            quantity=item.quantity,
            price=item.price,
            inventory_id=inventory.id,
            inventory=inventory,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice
        )
        
        session.add(new_sale_line_item)
        new_sales_invoice.line_items.append(new_sale_line_item)
        
        inventory_stock = session.exec(select(Stock).where(Stock.inventory_id == item.inventory_id)).all()
        cost_account = session.exec(select(Accounts).where(Accounts.name == "COGS")).first()
        
        inventory_account = inventory.account
        sale_quantity = item.quantity
        
        if len(inventory_stock) == 0:
            raise HTTPException(
                status_code=403,
                detail=f"There is no stock of item {inventory.name}"
            )

        if sum(stock.quantity for stock in inventory_stock) < item.quantity:
            raise HTTPException(
                status_code=403,
                detail=f"Not enough inventory of item {inventory.name} for the specified sale quantity"
            )


        for stock in inventory_stock:
            if sale_quantity == 0:
                break
            
            if not stock.quantity == 0:
                if sale_quantity <= stock.quantity:
                    stock.sale_line_items.append(new_sale_line_item)
                    stock.quantity -= sale_quantity
                    
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    
                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)
                    
                    item_total += sale_quantity * item.price
                    sale_quantity = 0
                else:
                    stock.sale_line_items.append(new_sale_line_item)
                    sale_quantity -= stock.quantity
                    
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount= stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    
                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)

                    item_total += stock.quantity * item.price
                    stock.quantity = 0

    bank_account = session.exec(select(Accounts).where(Accounts.name=="Bank")).first()
    sales_account = session.exec(select(Accounts).where(Accounts.name=="Sales")).first()

    bank_entry = DebitEntry(
        account_id=bank_account.id,
        account=bank_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )


    sales_entry = CreditEntry(
        account_id=sales_account.id,
        account=sales_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )

    bank_entry.cr_entries.append(sales_entry)
    bank_account.dr_entries.append(bank_entry)
    sales_account.cr_entries.append(sales_entry)
    new_sales_invoice.dr_entries.append(bank_entry)
    new_sales_invoice.cr_entries.append(sales_entry)
    
    session.add(bank_entry)
    session.add(bank_account)
    session.add(sales_entry)
    session.add(sales_account)
    session.add(new_sales_invoice)
    session.commit()
    session.refresh(new_sales_invoice)
    
    return new_sales_invoice

@doc_route.post("/credit_sale")
def add_credit_sales_invoice(invoice:SalesInvoiceBase, items:List[LineItemBase], session:Session=Depends(get_session)):
    if not invoice.customer_id:
        raise HTTPException(status_code=403, detail="Customer Id is reuired for a credit sale")
    new_sales_invoice = SalesInvoices.from_orm(invoice)
    session.add(new_sales_invoice)

    item_total = 0

    for item in items:
        inventory = session.get(InventoryItem, item.inventory_id)
        
        if not inventory:
            raise HTTPException(status_code=404, detail=f"Inventory with inventory id {item.inventory_id} not found")

        new_sale_line_item = SaleLineItems(
            quantity=item.quantity,
            price=item.price,
            inventory_id=inventory.id,
            inventory=inventory,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice
        )
        
        session.add(new_sale_line_item)
        new_sales_invoice.line_items.append(new_sale_line_item)
        
        inventory_stock = session.exec(select(Stock).where(Stock.inventory_id == item.inventory_id)).all()
        cost_account = session.exec(select(Accounts).where(Accounts.name == "COGS")).first()
        inventory_account = inventory.account
        sale_quantity = item.quantity
        
        if len(inventory_stock) == 0:
            raise HTTPException(
                status_code=403,
                detail=f"There is no stock of item {inventory.name}"
            )

        if sum(stock.quantity for stock in inventory_stock) < item.quantity:
            raise HTTPException(
                status_code=403,
                detail=f"Not enough inventory of item {inventory.name} for the specified sale quantity"
            )


        for stock in inventory_stock:
            if sale_quantity == 0:
                break
            
            if not stock.quantity == 0:
                if sale_quantity <= stock.quantity:
                    stock.sale_line_items.append(new_sale_line_item)
                    stock.quantity -= sale_quantity
                    
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=sale_quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    
                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)
                    
                    item_total += sale_quantity * item.price
                    sale_quantity = 0
                else:
                    stock.sale_line_items.append(new_sale_line_item)
                    sale_quantity -= stock.quantity
                    new_debit_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount= stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    new_credit_entry = CreditEntry(
                        account_id=inventory_account.id,
                        account=inventory_account,
                        amount=stock.quantity * stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    
                    new_debit_entry.cr_entries.append(new_credit_entry)
                    
                    session.add(new_debit_entry)
                    session.add(new_credit_entry)
                    
                    cost_account.dr_entries.append(new_debit_entry)
                    inventory_account.cr_entries.append(new_credit_entry)
                    new_sales_invoice.dr_entries.append(new_debit_entry)
                    new_sales_invoice.cr_entries.append(new_credit_entry)
                    
                    session.add(cost_account)
                    session.add(inventory_account)
                    session.add(new_sales_invoice)
                    session.add(stock)

                    item_total += stock.quantity * item.price
                    stock.quantity = 0
            
    customer =  session.get(Customers, invoice.customer_id)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer Account with id {invoice.customer_id} not found"
        )
    customer_account = customer.account
    sales_account = session.exec(select(Accounts).where(Accounts.name=="Sales")).first()

    customer_entry = DebitEntry(
        account_id=customer_account.id,
        account=customer_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )

    sales_entry = CreditEntry(
        account_id=sales_account.id,
        account=sales_account,
        sales_invoice_id=new_sales_invoice.id,
        sales_invoice=new_sales_invoice,
        amount=item_total
    )
    
    customer_entry.cr_entries.append(sales_entry)
    customer_account.dr_entries.append(customer_entry)
    sales_account.cr_entries.append(sales_entry)
    new_sales_invoice.dr_entries.append(customer_entry)
    new_sales_invoice.cr_entries.append(sales_entry)
    session.add(customer_entry)
    session.add(customer_account)
    session.add(sales_entry)
    session.add(sales_account)
    session.add(new_sales_invoice)
    session.commit()
    session.refresh(new_sales_invoice)
    
    return new_sales_invoice

@doc_route.get("/doc")
def read_all_documents(session:Session=Depends(get_session)):
    documents = session.exec(select(Documents)).all()
    return [
        {
            'document' : doc,
            'dr_entries' : doc.dr_entries,
            'cr_entries' : doc.cr_entries,
            'amount' : sum([entry.amount for entry in doc.dr_entries])
        } for doc in documents
    ]
    
@doc_route.get("/doc/{id}")
def read_document_by_id(id:int, session:Session=Depends(get_session)):
    document = session.get(Documents, id)
    if not document:
        raise HTTPException(status_code=404, detail=f"Document with document id {id} not found.")
    return document, document.dr_entries, document.cr_entries

@doc_route.get("/purchase")
def read_all_purchase_invoices(session:Session=Depends(get_session)):
    purchase_invoices = session.exec(select(PurchaseInvoices)).all()
    invoices = []
    for invoice in purchase_invoices:
        new_invoice = {
            'invoice' : invoice,
            'items' : [
                {
                    'item_name' :item.inventory.name, 
                    'price' : item.price, 
                    'quantity' : item.quantity, 
                    'unit': item.inventory.unit.name,
                    'discount_rate' : item.discount_rate,
                    'discount_amount' : item.discount_amount,
                    'gst_rate' : item.gst_rate,
                    'gst_amount' : item.gst_amount,
                    'total' : item.total
                    } for item in invoice.line_items],
            'dr_entries' : invoice.dr_entries,
            'cr_entries' : invoice.cr_entries,
            'amount' : sum([((item.price*item.quantity)-item.discount_amount+item.gst_amount) for item in invoice.line_items]),
            'transaction_type' : invoice.transaction_type.name
        }
        invoices.append(new_invoice)
    return invoices

@doc_route.get("/purchase/{id}")
def read_purchase_invoice_by_id(id:int, session:Session=Depends(get_session)):
    purchase_invoice = session.get(PurchaseInvoices, id)
    if not purchase_invoice:
        raise HTTPException(status_code=404, detail=f"Purchase Invoice with id {id} not found.")
    return purchase_invoice

@doc_route.get("/sales")
def read_all_sales_invoices(session:Session=Depends(get_session)):
    sales_invoices =  session.exec(select(SalesInvoices)).all()
    invoices = []
    for invoice in sales_invoices:
        new_invoice = {
            'invoice' : invoice,
            'items' : [
                {
                    'item_name' :item.inventory.name, 
                    'price' : item.price, 
                    'quantity' : item.quantity, 
                    'unit': item.inventory.unit.name,
                    'discount_rate' : item.discount_rate,
                    'discount_amount' : item.discount_amount,
                    'gst_rate' : item.gst_rate,
                    'gst_amount' : item.gst_amount,
                    'total' : item.total
                    } for item in invoice.line_items],
            'dr_entries' : invoice.dr_entries,
            'cr_entries' : invoice.cr_entries,
            'amount' : sum([((item.price*item.quantity)-item.discount_amount+item.gst_amount) for item in invoice.line_items]),
            'transaction_type' : invoice.transaction_type.name
        }
        invoices.append(new_invoice)
    return invoices

@doc_route.get("/sales/{id}")
def read_sales_invoice_by_id(id:int, session:Session=Depends(get_session)):
    sales_invoice = session.get(SalesInvoices, id)
    if not sales_invoice:
        raise HTTPException(status_code=404, detail=f"Sales Invoice with id {id} not found")
    return sales_invoice, sales_invoice.dr_entries, sales_invoice.cr_entries, sales_invoice.line_items

@doc_route.patch("/documents/{id}")
def cancel_document(id:int, session:Session=Depends(get_session)):
    document = session.get(Documents, id)
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document with document id {id} does not exist"
        )

    if document.is_cancelled:
        raise HTTPException(status_code=403, detail=f"Document with document id {id} is already cancelled")

    doc_entries = document.dr_entries.copy()

    for entry in doc_entries:
        cr_contra_entry = CreditEntry(
            account_id=entry.account_id,
            account=entry.account,
            amount=entry.amount,
            document=entry.document,
            document_id=entry.document_id,
        )
        dr_contra_entry = DebitEntry(
            account_id=entry.cr_entries[0].account_id,
            account=entry.cr_entries[0].account,
            amount=entry.cr_entries[0].amount,
            document=entry.cr_entries[0].document,
            document_id=entry.cr_entries[0].document
        )
        
        cr_contra_entry.dr_entries.append(dr_contra_entry)

        document.dr_entries.append(dr_contra_entry)
        document.cr_entries.append(cr_contra_entry)
        session.add(dr_contra_entry)
        session.add(cr_contra_entry)
    
    document.is_cancelled = True

    session.commit()
    session.refresh(document)

    return document, document.cr_entries, document.dr_entries

@doc_route.patch("/purchase/{id}")
def cancel_purchase_invoice(id:int, session:Session=Depends(get_session)):
    purchase_invoice = session.get(PurchaseInvoices, id)

    if not purchase_invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Purchase Invoice with purchase invoice id {id} not found"
        )
    
    if purchase_invoice.is_cancelled:
        raise HTTPException(
            status_code = 403,
            detail = f"Purchase Invoice with id {purchase_invoice.id} is already cancelled." 
        )
    
    items = purchase_invoice.line_items.copy()

    for item in items:
        item.stock.quantity -= item.quantity
        if item.stock.quantity == 0:
            session.delete(item.stock)
        session.add(item)
        session.add(item.stock)

    purchase_entries = purchase_invoice.cr_entries.copy()

    for entry in purchase_entries:
        contra_dr_entry = DebitEntry(
            account_id=entry.account_id,
            account=entry.account,
            purchase_invoice_id=entry.purchase_invoice_id,
            purchase_invoice=entry.purchase_invoice,
            amount=entry.amount
        )
        contra_cr_entry = CreditEntry(
            account_id=entry.dr_entries[0].account_id,
            account=entry.dr_entries[0].account,
            purchase_invoice_id=entry.dr_entries[0].purchase_invoice_id,
            purchase_invoice=entry.dr_entries[0].purchase_invoice,
            amount=entry.dr_entries[0].amount
        )
        
        contra_dr_entry.cr_entries.append(contra_cr_entry)
        
        session.add(contra_dr_entry)
        session.add(contra_cr_entry)
    
    purchase_invoice.is_cancelled = True

    session.add(purchase_invoice)

    session.commit()
    session.refresh(purchase_invoice)

    return purchase_invoice, purchase_invoice.dr_entries, purchase_invoice.cr_entries, purchase_invoice.line_items


@doc_route.patch("/sales/{id}")
def cancel_sales_invoice(id:int, session:Session=Depends(get_session)):
    sales_invoice = session.get(SalesInvoices, id)
    
    if not sales_invoice:
        raise HTTPException(status_code=404, detail=f"Sales Invoice with id {id} does not exist.")
    
    if sales_invoice.is_cancelled:
        raise HTTPException(status_code=403, detail=f"Sales Invoice with id {id} is already cancelled.")

    invoice_entries = sales_invoice.cr_entries.copy()

    for entry in invoice_entries:
        contra_dr_entry = DebitEntry(
            account_id=entry.account_id,
            account=entry.account,
            sales_invoice_id=sales_invoice.id,
            sales_invoice=sales_invoice,
            amount=entry.amount
        )
        contra_cr_entry = CreditEntry(
            account_id=entry.dr_entries[0].account_id,
            account=entry.dr_entries[0].account,
            sales_invoice_id=entry.dr_entries[0].sales_invoice_id,
            sales_invoice=entry.dr_entries[0].sales_invoice,
            amount=entry.dr_entries[0].amount
        )

        entry.account.dr_entries.append(contra_dr_entry)
        entry.dr_entries[0].account.cr_entries.append(contra_cr_entry)

        contra_dr_entry.cr_entries.append(contra_cr_entry)
        
        sales_invoice.cr_entries.append(contra_cr_entry)
        sales_invoice.dr_entries.append(contra_dr_entry)

        session.add(entry)
        session.add(contra_dr_entry)
        session.add(contra_cr_entry)

    for item in sales_invoice.line_items:
        for stock in item.stocks:
            stock.quantity += item.quantity
            session.add(stock)

    sales_invoice.is_cancelled = True

    session.add(sales_invoice)
    session.commit()
    session.refresh(sales_invoice)

    return sales_invoice, sales_invoice.dr_entries, sales_invoice.cr_entries

@doc_route.post("/sale")
def test_sale(invoice:SalesInvoiceBase, items:List[LineItemBase], session:Session=Depends(get_session)):
    new_sales_invoice = SalesInvoices.from_orm(invoice)
    session.add(new_sales_invoice)

    item_total = 0
    for item in items:
        # Amounts
        gross_total = item.price * item.quantity
        discount_amount = gross_total * (item.discount_rate/100)
        total_after_discount = gross_total - discount_amount
        gst_amount = total_after_discount * (item.gst_rate/100)
        total = gross_total - discount_amount + gst_amount
        
        print('gross', gross_total)
        print('total_after_discount', total_after_discount)
        print('discount', discount_amount)
        print('gst', gst_amount)
        #Inventory
        inventory = session.get(InventoryItem, item.inventory_id)      
        if not inventory:
            raise HTTPException(status_code=404, detail=f"Inventory with inventory id {item.inventory_id} not found")

        new_sale_line_item = SaleLineItems(
            quantity=item.quantity,
            price=item.price,
            inventory_id=inventory.id,
            inventory=inventory,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice,
            discount_rate=item.discount_rate,
            discount_amount=discount_amount,
            gst_rate=item.gst_rate,
            gst_amount=gst_amount,
            total=total
        )
        session.add(new_sale_line_item)
        # Accounts
        customer = session.get(Customers, invoice.customer_id)
    
        cost_account = session.exec(select(Accounts).where(Accounts.name == "Cost of Goods Sold")).first()
        discount_account = session.exec(select(Accounts).where(Accounts.name == "Discount Given")).first()
        gst_account = session.exec(select(Accounts).where(Accounts.name == "GST-output")).first()
        sales_revenue_account = session.exec(select(Accounts).where(Accounts.name == "Sales Revenue")).first()

        dr_sale_account:Accounts
        if invoice.transaction_type_id == 1:
            dr_sale_account = session.exec(select(Accounts).where(Accounts.name == "Cash in Hand")).first()
        elif invoice.transaction_type_id == 2:
            dr_sale_account = session.exec(select(Accounts).where(Accounts.name=="Bank Account")).first()
        else:
            if not customer:
                raise HTTPException(
                    status_code=404,
                    detail=f"Customer with id {invoice.customer_id} does not exist"
                )
            dr_sale_account = customer.account
        
        # Inventory Errors
        inventory_stock = session.exec(select(Stock).where(Stock.inventory_id == item.inventory_id)).all()
        if len(inventory_stock) == 0:
            raise HTTPException(
                status_code=403,
                detail=f"There is no stock of item {inventory.name}"
            )
        if sum(stock.quantity for stock in inventory_stock) < item.quantity:
            raise HTTPException(
                status_code=403,
                detail=f"Not enough inventory of item {inventory.name} for the specified sale quantity"
            )

        #Sale Entry
        dr_sale_entry = DebitEntry(
            account_id=dr_sale_account.id,
            account=dr_sale_account,
            amount=total_after_discount,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice
        )
        cr_sale_entry = CreditEntry(
            account_id=sales_revenue_account.id,
            account=sales_revenue_account,
            amount=total_after_discount,
            sales_invoice_id=new_sales_invoice.id,
            sales_invoice=new_sales_invoice
        )
        dr_sale_entry.cr_entries.append(cr_sale_entry)
        session.add(dr_sale_entry)
        session.add(cr_sale_entry)
        
        #Discount Entry
        if not item.discount_amount == 0:
            dr_discount_entry = DebitEntry(
                account_id=discount_account.id,
                account=discount_account,
                amount=discount_amount,
                sales_invoice_id=new_sales_invoice.id,
                sales_invoice=new_sales_invoice
            )
            cr_discount_entry = CreditEntry(
                account_id=sales_revenue_account.id,
                account=sales_revenue_account,
                amount=discount_amount,
                sales_invoice_id=new_sales_invoice.id,
                sales_invoice=new_sales_invoice
            )
            dr_discount_entry.cr_entries.append(cr_discount_entry)
            session.add(dr_discount_entry)
            session.add(cr_discount_entry)
        
        #GST Entry
        if not gst_amount == 0:
            dr_gst_entry = DebitEntry(
                account_id=dr_sale_account.id,
                account=dr_sale_account,
                amount=gst_amount,
                sales_invoice_id=new_sales_invoice.id,
                sales_invoice=new_sales_invoice
            )
            cr_gst_entry = CreditEntry(
                account_id=gst_account.id,
                account=gst_account,
                amount=gst_amount,
                sales_invoice_id=new_sales_invoice.id,
                sales_invoice=new_sales_invoice
            )
            dr_gst_entry.cr_entries.append(cr_gst_entry)
            session.add(dr_gst_entry)
            session.add(cr_gst_entry)
            
        # Inventory Management
        sale_quantity = item.quantity

        for stock in inventory_stock:
            if sale_quantity == 0:
                break
            if not stock.quantity == 0:
                if sale_quantity <= stock.quantity:
                    stock.sale_line_items.append(new_sale_line_item)
                    stock.quantity -= sale_quantity
                    
                    #COST ENTRY
                    dr_cost_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount=sale_quantity*stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    cr_cost_entry = CreditEntry(
                        account_id=inventory.account_id,
                        account=inventory.account,
                        amount=sale_quantity*stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    dr_cost_entry.cr_entries.append(cr_cost_entry)
                    session.add(dr_cost_entry)
                    session.add(cr_cost_entry)
                    sale_quantity = 0
                    session.add(stock)
                else:
                    stock.sale_line_items.append(new_sale_line_item)
                    sale_quantity -= stock.quantity
                    #Sale Entry
                    dr_cost_entry = DebitEntry(
                        account_id=cost_account.id,
                        account=cost_account,
                        amount=stock.quantity*stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    cr_cost_entry = CreditEntry(
                        account_id=inventory.account_id,
                        account=inventory.account,
                        amount=stock.quantity*stock.price,
                        sales_invoice_id=new_sales_invoice.id,
                        sales_invoice=new_sales_invoice
                    )
                    dr_cost_entry.cr_entries.append(cr_cost_entry)
                    session.add(dr_cost_entry)
                    session.add(cr_cost_entry)

                    stock.quantity = 0
                    session.add(stock)
        
        # Updates
        session.add(new_sales_invoice)
        session.add(inventory)
        session.add(customer)
        session.add(cost_account)
        session.add(discount_account)
        session.add(gst_account)
        session.add(sales_revenue_account)
        session.add(dr_sale_account)
        
        #Commit
        session.commit()

    return new_sales_invoice, new_sales_invoice.dr_entries, new_sales_invoice.cr_entries, new_sales_invoice.line_items