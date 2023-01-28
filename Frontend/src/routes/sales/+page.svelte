<script>
    import New from "./components/New.svelte";
    import View from "./components/View.svelte";
    
    export let data;

    let current = 'new'
    let save;

    const refetchData = async ()=>{
        const salesRes = await fetch('http://127.0.0.1:8000/doc/sales')
        const inventoryRes = await fetch('http://127.0.0.1:8000/inv')
        const unitsRes = await fetch('http://127.0.0.1:8000/lookup/unit')
        const transactionRes = await fetch('http://127.0.0.1:8000/lookup/transaction')
        const inventoryTypeRes = await fetch('http://127.0.0.1:8000/lookup/inventory')
        const customersRes = await fetch('http://127.0.0.1:8000/cust/all')
        if (salesRes.ok && inventoryRes.ok && unitsRes.ok && transactionRes.ok && inventoryTypeRes.ok && customersRes.ok) {
            data = {
                invoices : await salesRes.json(),
                inventory : await inventoryRes.json(),
                units : await unitsRes.json(),
                transactionTypes : await transactionRes.json(),
                inventoryTypes : await inventoryTypeRes.json(),
                customers : await customersRes.json()
            }
        } 
    }

</script>

<main>
    <nav>
        <div class="tabs">
            <button class="{current==='new'?'active':''}" on:click={()=>{current='new'}}>New Sales Invoice</button>
            <button class="{current==='view'?'active':''}" on:click={()=>{current='view'}}>View Sales Invoices</button>
        </div>
        <div class="save">
            {#if current === 'new'}
                <button on:click={async ()=>{await save()}}>+ Save</button> 
            {/if}
        </div>
    </nav>
    <div class="content">
        {#key data}
            {#if current === 'new'}
                <New {data} bind:submitInvoice={save} on:save={()=>{refetchData()}}/>
            {:else}
                <View invoices={data.invoices} accounts={data.accounts} customers={data.customers}/>
            {/if}
        {/key}
    </div>
</main>

<style>
    main {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
    }
    nav {
        position: sticky;
        top: 0;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 1rem;
        background: var(--nav-background);
        box-shadow: var(--box-shadow-strong);
    }
    nav .tabs {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 2rem;
    }
    nav .save {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    nav .save button {
        width: 100px;
        height: 40px;
        font-weight: 500;
        color: var(--button-background);
        background: var(--color-success);
        box-shadow: var(--box-shadow-strong);
    }
    nav .tabs button {
        width: 230px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: var(--box-shadow-strong);
        transition: background 0.2s ease;
    }
    nav button.active {
        background: var(--button-text);
        color: var(--button-background);
    }
    nav button:active {
        transform: scale(0.98);
    }
    .content {
        width: 100%;
        height: 100%;
    }
</style>