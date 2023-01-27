<script>
    import { createEventDispatcher } from "svelte";   
    
    const dispatch = createEventDispatcher()

    export let data;

    let customerId;
    let transactionType;
    let itemId
    let today = new Date().toJSON().slice(0,10);

    let dateError;
    let customerError;
    let transactionTypeError;
    let rowErrorList = []
    let items = data.inventory.filter(inv=>{
        return inv.type_id == 1
    })
    let fistRow = {
        sr : 1,
        name : '',
        unit : '',
        inventory_id : '',
        price : '',
        quantity : '',
        discount_rate: '',
        discount_amount : '',
        gst_rate : '',
        gst_amount: '',
        total : ''
    }
    let rows = [{...fistRow}]

    const setCustomerId = (e)=>{
        customerId = ''
        let customer = data.customers.filter(c=>c.name === e.target.value)[0] || ''
        customer?customerId=customer.id:''
    }

    const setUnit = (e, row)=>{
        itemId = items.filter(item=>item.name === e.target.value)[0].id
        let unitId = data.inventory.filter(item=>item.name === e.target.value)[0].unit_id
        let unitName = data.units.filter(unit=> unit.id === unitId)[0].name
        row.name = e.target.value
        row.unit = unitName
        row.inventory_id = itemId
        rows = rows
    }
    const addRow = ()=>{
        if (rows.length>=10) {
            return
        }
        let newRow = {...fistRow}
        newRow.sr = rows.length + 1
        rows = [...rows, newRow]
    }
    const removeRow = (rowId)=>{
        if (rows.length <= 1) {
            rows = [{...fistRow}]
            rowErrorList = []
            return
        }
        let newRow = rows.filter(row=>row.sr !== rowId)
        newRow.forEach((row, i)=>row.sr = i+1)
        rows = newRow
    }
    export const submitInvoice = async () => {
        console.log(customerId)
        dateError = false;
        customerError = false;
        transactionTypeError = false;
        rowErrorList = []
        if (!today) {
            dateError = true;
        }
        if (!customerId) {
            customerError = true;
        }
        if (!transactionType) {
            transactionTypeError = true;
        }
        if (dateError || customerError || transactionTypeError) {
            return
        }
        let invoice = {
            'doc_type' : 'Sales',
            'doc_date' : today,
            'transaction_type_id' : transactionType,
            'customer_id' : customerId
        }
        let items = []
        rows.forEach(row=>{
            if (!row.quantity || !row.price || !row.inventory_id) {
                rowErrorList = [...rowErrorList, row.sr]
                return
            }
            let newItem = {
                quantity : row.quantity,
                price : row.price,
                inventory_id : row.inventory_id,
                gst_rate : row.gst_rate || 0,
                discount_rate : row.discount_rate || 0
            }
            items = [...items, newItem]
        })
        if (rowErrorList.length > 0) {
            return
        }
        const invoiceRes = await fetch('http://127.0.0.1:8000/doc/sale', {
            method : 'POST',
            mode : 'cors',
            headers : {
                'Access-Control-Allow-Origin' : 'http://localhost:5173',
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({
                'invoice' : invoice,
                'items' : items
            })
        })
        if (invoiceRes.ok) {
            alert("Invoice saved successfully")
            dispatch('save')
            rows = [{...fistRow}]
            
        } else alert('Something went wrong')
    }
</script>

<main>
    <div class="invoice">
        <div class="header">
            <span>Sales Invoice #</span>
            <span>{data.invoices.length + 1}</span>
        </div>
        {#key data}
        <div class="sales-info">
            <div class="group {dateError?'error':''}">
                <label for="date">Date</label>
                <input type="date" name="date" id="date" bind:value={today}>
            </div>
            <div class="group {transactionTypeError?'error':''}">
                <label for="type">Transaction Type</label>
                <select name="type" id="type" bind:value={transactionType}>
                    {#each data.transactionTypes as type}
                        <option value="{type.id}">{type.name}</option>
                    {/each}
                </select>
            </div>
            <div class="group {customerError?'error':''}">
                <label for="customer">Customer Name</label>
                <input type="text" name="customer" id="customer" list="customers" placeholder="Customer Name" on:change={(e)=>{setCustomerId(e)}}>
                <datalist id="customers">
                    {#each data.customers as customer (customer.id)}
                        <option value="{customer.name}">{customer.name}</option>
                    {/each}
                </datalist>
            </div>
        </div>
        <div class="items">
            <div class="head">
                <span>#</span>
                <span>Name</span>
                <span>Unit</span>
                <span>Price (₹)</span>
                <span>Quantity</span>
                <span>Disc(%)</span>
                <span>Disc(₹)</span>
                <span>GST(%)</span>
                <span>GST(₹)</span>
                <span>Total (₹)</span>
            </div>
            {#each rows as row (row.sr)}
            {#key rows && data}    
            <div class="row {rowErrorList.includes(row.sr)?'error':''}">
                <button on:click={()=>{removeRow(row.sr)}}>{row.sr}</button>
                <input type="text" name="item-name" id="item-name" placeholder="Item Name" value="{row.name}" list="items" on:change={(e)=>{setUnit(e, row)}}>
                <datalist id="items">
                    {#each items as item}
                        <option value="{item.name}">{item.name}</option>
                    {/each}
                </datalist>
                <span>{row.unit}</span>
                    <input type="text" name="price" id="price" placeholder="₹ 0.00" value="{row.price}" on:change={
                        (e)=>{
                                row.price = parseFloat(e.target.value).toFixed(2)
                                row.discount_amount=((Number(row.quantity) * Number(row.price)) * (Number(row.discount_rate/100))).toFixed(2)
                                row.gst_amount=(((Number(row.quantity) * Number(row.price))-Number(row.discount_amount)) * (Number(row.gst_rate/100))).toFixed(2)
                            }
                        }>
                    <input type="text" name="quantity" id="quantity" placeholder="0" value="{row.quantity}" on:change={
                        (e)=>{
                                row.quantity = parseFloat(e.target.value).toFixed(2)
                                row.discount_amount=((Number(row.quantity) * Number(row.price)) * (Number(row.discount_rate/100))).toFixed(2)
                                row.gst_amount=(((Number(row.quantity) * Number(row.price))-Number(row.discount_amount)) * (Number(row.gst_rate/100))).toFixed(2)
                            }
                        }>
                    <input type="text" name="discount" id="discount" placeholder="0" value="{row.discount_rate}" on:change={
                        (e)=>{
                                row.discount_rate=+e.target.value;
                                row.discount_amount=((Number(row.quantity) * Number(row.price)) * (Number(row.discount_rate/100))).toFixed(2)
                                row.gst_amount=(((Number(row.quantity) * Number(row.price))-Number(row.discount_amount)) * (Number(row.gst_rate/100))).toFixed(2)
                            }
                        }>
                    <input type="text" name="discountAmount" id="discountAmount" placeholder="0" value="{row.discount_amount}" disabled>
                    <input type="text" name="gst-rate" id="gst-rate" placeholder="0" value="{row.gst_rate}" on:change={
                        (e)=>{
                                row.gst_rate=e.target.value;
                                row.discount_amount=((Number(row.quantity) * Number(row.price)) * (Number(row.discount_rate/100))).toFixed(2)
                                row.gst_amount=(((Number(row.quantity) * Number(row.price))-Number(row.discount_amount)) * (Number(row.gst_rate/100))).toFixed(2)
                            }
                        }>
                    <input type="text" name="gst-amount" id="gst-amount" placeholder="0" value="{row.gst_amount}" disabled>
                    <input type="text" name="total" id="total-{row.sr}" placeholder="0" value="{
                        ((Number(row.price)*Number(row.quantity)) + Number(row.gst_amount) - Number(row.discount_amount)).toFixed(2)   
                    }" disabled>
                </div>
                {/key}
                {/each}
                <button on:click={addRow} class="add">+ Add Item</button>
            </div>
            {/key}
        </div>
</main>

<style>
    select,
    input {
        width: 100%;
        height: 35px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        color: var(--button-background);
        background: var(--button-text);
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    main {
        min-width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }
    .invoice {
        width: 99%;
        height: 90%;
        margin-inline: auto;
        background: var(--nav-background);
        padding: 1rem 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .invoice .header {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    .invoice .header span {
        padding: 0.5rem 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        background-color: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .invoice .sales-info {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
    }
    .invoice .sales-info .group {
        position: relative;
        width: 100%;
        height: 100%;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: center;
        justify-content: center;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .invoice .sales-info .group label {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--button-background);
    }
    .items {
        width: 100%;
        margin-top: 10px;
        margin-inline: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
    .items .head,
    .items .row {
        width: 100%;
        height: 45px;
        padding: 0.3rem 1rem;
        color: var(--button-background);
        display: grid;
        grid-template-columns: 1fr 3fr 2fr 2fr 2fr 1.2fr 2fr 1.2fr 2fr 3fr;
        align-items: center;
        gap: 0.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        text-align: center;
    }
    .items .row input,
    .items .row span {
        padding: 0 1rem;
        font-size: 0.9rem;
    }
    .items .head span,
    .items .row span {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .row {
        position: relative;
    }
    .row button {
        position: relative;
        width: 50%;
        justify-self: center;
        align-self: center;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--button-text);
        color: var(--button-background);
        box-shadow: var(--box-shadow-strong);
        overflow: hidden;
    }
    .row button:active {
        transform: scale(0.98);
    }
    .row button::after {
        content: 'X';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--color-danger);
        opacity: 0;
    }
    .row button:hover::after {
        opacity: 1;
    }
    .add {
        width: 200px;
        height: 40px;
        margin-top: 5px;
        font-weight: 600;
        color: var(--button-background);
        background: var(--color-success);
        box-shadow: var(--box-shadow-strong);
    }
    .add:active {
        transform: scale(0.98);
    }
    .error {
        background: var(--color-danger);
    }
</style>