<script>
    export let data;

    let vendorId;
    let today = new Date().toJSON().slice(0,10);
    let fistRow = {
        sr : 1,
        name : '',
        unit : '',
        unitId : '',
        price : '',
        quantity : '',
        total : ''
    }
    let rows = [{...fistRow}]

    const setUnit = (e, row)=>{
        let unitId = data.inventory.filter(item=>item.name === e.target.value)[0].unit_id
        let unitName = data.units.filter(unit=> unit.id === unitId)[0].name
        row.name = e.target.value
        row.unitId = unitId
        row.unit = unitName
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
            return
        }
        let newRow = rows.filter(row=>row.sr !== rowId)
        newRow.forEach((row, i)=>row.sr = i+1)
        rows = newRow
    }
</script>

<main>
    <div class="invoice">
        <div class="header">
            <span>Purchase Invoice #</span>
            <span>{data.invoices.length + 1}</span>
        </div>
        <div class="purchase-info">
            <div class="group">
                <label for="date">Date</label>
                <input type="date" name="date" id="date" bind:value={today}>
            </div>
            <div class="group">
                <label for="type">Transaction Type</label>
                <select name="type" id="type">
                    {#each data.transactionTypes as type}
                        <option value="{type.id}">{type.name}</option>
                    {/each}
                </select>
            </div>
            <div class="group">
                <label for="vendor">Vendor Name</label>
                <input id="vendor" name="vendor" list="vendors" autocomplete="off" placeholder="Vendor Name"/>
                <datalist id="vendors">
                    {#each data.vendors as vendor}
                        <option value="{vendor.name}">{vendor.name}</option>
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
                <span>Total (₹)</span>
            </div>
            {#each rows as row (row.sr)}
                {#key rows}    
                <div class="row">
                    <button on:click={()=>{removeRow(row.sr)}}>{row.sr}</button>
                    <input type="text" name="item-name" id="item-name" placeholder="Item Name" value="{row.name}" list="items" on:change={(e)=>{setUnit(e, row)}}>
                    <datalist id="items">
                        {#each data.inventory as item}
                            <option value="{item.name}">{item.name}</option>
                        {/each}
                    </datalist>
                    <span>{row.unit}</span>
                    <input type="text" name="price" id="price" placeholder="₹ 0.00" value="{row.price}" on:change={(e)=>{row.price=e.target.value}}>
                    <input type="text" name="quantity" id="quantity" placeholder="0" value="{row.quantity}" on:change={(e)=>{row.quantity=e.target.value}}>
                    <input type="text" name="total" id="total-{row.sr}" placeholder="0" value="{row.quantity*row.price}">
                </div>
                {/key}
            {/each}
            <button on:click={addRow} class="add">+ Add Item</button>
        </div>
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
    .invoice .purchase-info {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
    }
    .invoice .purchase-info .group {
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
    .invoice .purchase-info .group label {
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
        grid-template-columns: repeat(6, 1fr);
        gap: 0.5rem;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        text-align: center;
    }
    .items .head span,
    .items .row span {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .row button {
        position: relative;
        width: 50%;
        justify-self: center;
        align-self: center;
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
</style>