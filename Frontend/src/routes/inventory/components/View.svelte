<script>
    export let data;

    let inventoryItems = data.items;
    
    const filterByName = (e)=>{
        let searchTerm = e.target.value.toLowerCase();
        inventoryItems = data.items.filter(inventory=>inventory.item.name.toLowerCase().includes(searchTerm));
    }
    const filterByType = (e)=>{
        let type_id = e.target.value;
        if (type_id == '') {
            inventoryItems = data.items;
            return;
        }
        inventoryItems = data.items.filter(inventory=>inventory.item.type_id==type_id);
    }
    const filterByUnit = (e)=>{
        let unit_id = e.target.value;
        if (unit_id === '') {
            inventoryItems = data.items;
            return
        }
        inventoryItems = data.items.filter(inventory=>inventory.item.unit_id==unit_id)
    }
</script>

<main>
    <div class="filters">
        <div class="group">
            <span>Filter Items</span>
        </div>
        <div class="group">
            <label for="name">Search by Name</label>
            <input type="text" name="name" id="name" list="items" placeholder="Enter Item Name" on:keyup={(e)=>{filterByName(e)}}>
            <datalist id="items">
                {#each data.items as inventory}
                    <option value="{inventory.item.name}">{inventory.item.name}</option>
                {/each}
            </datalist>
        </div>
        <div class="group">
            <label for="type">Filter by Item Type</label>
            <select name="type" id="type" on:change={(e)=>{filterByType(e)}}>
                <option value="">All Items</option>
                {#each data.types as type}
                    <option value="{type.id}">{type.name} Items</option>
                {/each}
            </select>
        </div>
        <div class="group">
            <label for="unit">Filter by Unit</label>
            <select name="unit" id="unit" on:change={(e)=>{filterByUnit(e)}}>
                <option value="">All Units</option>
                {#each data.units as unit}
                    <option value="{unit.id}">{unit.name}</option>
                {/each}
            </select>
        </div>
    </div>
    <div class="items">
        <div class="head">
            <span>#</span>
            <span>Name</span>
            <span>Unit</span>
            <span>Type</span>
            <span>Material Type</span>
            <span>Actions</span>
        </div>
        {#each inventoryItems as inventory, i (i)}
            <div class="row">
                <span>{i+1}</span>
                <span>{inventory.item.name}</span>
                <span>{data.units.filter(unit=>unit.id === inventory.item.unit_id)[0].name}</span>
                <span>{data.types.filter(type=>type.id===inventory.item.type_id)[0].name} Item</span>
                <span>{inventory.item.account_id === 7?'Finished Materials':inventory.item.account_id === 6?'Semi Finished Materials' : 'Raw Materials'}</span>
                <button on:click={()=>{document.getElementById('stock-'+(i+1)).style.display='flex'}}>
                    View Stock
                </button>
                <div class="stock" id="stock-{i+1}">
                    <div class="wrapper">
                        <div class="stock-head">
                            <span>#</span>
                            <span>Name</span>
                            <span>Date Purchased</span>
                            <span>Unit</span>
                            <span>Quantity Purchsed</span>
                            <span>Quantity in Stock</span>
                            <span>Price (₹)</span>
                        </div>
                        {#each inventory.stock as stock, i (i)}
                            <div class="stock-row">
                                <span>{i+1}</span>
                                <span>{inventory.item.name}</span>
                                <span>{new Date(stock.date_purchased).toDateString()}</span>
                                <span>{data.units.filter(unit=>unit.id === inventory.item.unit_id)[0].name}</span>
                                <span>{stock.quantity_purchased}</span>
                                <span>{stock.quantity_stock}</span>
                                <span>{stock.price}</span>
                            </div>
                        {/each}
                        <button class="close-stock" on:click={()=>{document.getElementById('stock-'+(i+1)).style.display='none'}}>X</button>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</main>
<style>
    main {
        position: relative;
        width: 100%;
        height: 100%;
    }
    .filters {
        width: 100%;
        padding: 1rem;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        align-items: center;
        justify-content: flex-start;
    }
    .filters .group {
        width: 100%;
        height: 100%;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        background: var(--nav-background);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .filters .group label,
    .filters .group span {
        width: 100%;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--button-background);
        text-align: center;
    }
    .filters .group input,
    .filters .group select {
        width: 100%;
        height: 40px;
        padding: 0.2rem 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .items {
        width: 90%;
        height: 680px;
        margin-inline: auto;
        padding: 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        overflow: scroll;
    }
    .items .head,
    .items .row {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1rem;
        padding: 0.5rem 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        margin-bottom: 10px;
        height: 40px;
    }
    .items .head {
        position: sticky;
        top: -1rem;
        background: var(--nav-background);
    }
    .row > button {
        color: var(--button-background);
        background: var(--color-success);
    }
    .row .stock {
        position: absolute;
        top: 0px;
        right: 0;
        width: 100%;
        height: 100%;
        padding: 1rem;
        display: none;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.5);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        z-index: 9;
    }
    .stock .wrapper {
        position: relative;
        width: 90%;
        height: 70%;
        background: var(--button-text);
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .row .stock .stock-row,
    .row .stock .stock-head {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 1rem;
        padding: 0.5rem 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        margin-bottom: 10px;
        height: 40px;
    }
    .row .stock .stock-head {
        background: var(--nav-background);
    }
    .close-stock {
        position: absolute;
        top: -20px;
        right: -20px;
        width: 40px;
        height: 40px;
        font-size: 1.25rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--button-background);
        background: var(--color-danger);
        box-shadow: var(--box-shadow-strong);
        border-radius: 50%;
    }
    button:active {
        transform: scale(0.98);
    }
</style>