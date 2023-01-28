<script>
    import New from "./components/New.svelte";

    export let data;

    let current = 'customers';
    let editing = [];
    let adding = false;
    let addingTo = ''
    let parties;
    let searchfield;
    let searchterm;

    $: if (current === 'customers') {
        parties = data.customers
    } else if(current === 'vendors') {
        parties = data.vendors
    }
    const edit = (rowNum)=>{
        const row = document.querySelector('#row-'+rowNum)
        const inputs = row.querySelectorAll('input')
        if (!editing.includes(rowNum)) {
            editing = [...editing, rowNum];
            inputs.forEach((inp,i)=>{
                inp.style.outline = 'solid 2px var(--button-background)';
                inp.disabled = false;
                i===0?inp.disabled=true:''
                i===0?inp.style.outline='none':''
                i===1?inp.focus():''
            })
        } else {
            if (current === 'customers') {
                parties = data.customers
            } else if (current === 'vendors') {
                parties=data.vendors
            }
            editing=editing.filter(num=>rowNum!==num);
            inputs[0].parentNode.querySelectorAll('input').forEach(inp=>{
                inp.style.disabled=true;
                inp.style.outline=0
            })
        }
    }
    $: filterParty = (e, searchterm)=>{
        let field = searchfield.toLowerCase()
        parties = data[current].filter(party=>{
            let fieldValue = party[field].toString().toLowerCase()
            return fieldValue.includes(searchterm.toLowerCase())
        })
    }
    const updateParty = async (e, party, rowNum)=>{
        const row = e.target.parentNode.parentNode
        const inputs = row.querySelectorAll('input')
        let updatedValues = {}
        inputs.forEach(input=>{
            switch(input.name) {
                case 'name':
                    updatedValues.name = input.value
                    break
                case 'email':
                    updatedValues.email = input.value
                    break
                case 'country_code':
                    updatedValues.country_code = input.value.split("-")[0]
                    updatedValues.phone = Number(input.value.split("-")[1])
                    break
                case 'address':
                    updatedValues.address = input.value
                    break
                case 'state':
                    updatedValues.state = input.value
                    break
                case 'country':
                    updatedValues.country = input.value
                    break
                case 'postal_code':
                    updatedValues.postal_code = Number(input.value)
                    break
                case 'gst':
                    updatedValues.gst = input.value
                    break
            }
        })
        let urlSuffix = current==="customers"?'/cust/'+party.id:current==='vendors'?'/ven/'+party.id:null
        const partyRes = await fetch('http://127.0.0.1:8000'+urlSuffix, {
            method:'PATCH',
            mode:'cors',
            headers:{
                'Access-Control-Allow-Origin':'http://localhost:5173',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({...updatedValues})
        })
        if (partyRes.ok) {
            alert(`${party.name} has been updated successfully.`)
            editing = []
            refetchData()
        } else {
            let messageObj = await partyRes.json()
            messageObj.detail.forEach(item=>{
                alert(`${item.loc[1]} : ${item.msg}, Error : ${item.type}`)
            })
        }
    }
    const refetchData = async ()=>{
        const customerRes = await fetch('http://127.0.0.1:8000/cust/all')
        const vendorRes = await fetch('http://127.0.0.1:8000/ven')
        if (customerRes.ok && vendorRes.ok) {
            data = {
                customers : await customerRes.json(),
                vendors : await vendorRes.json()
            }
        }
    }
</script>
{#key data}
{#if addingTo == 'customers' && adding}
    <New tab={current} on:close={()=>{addingTo='';adding=false}} on:save={()=>{refetchData()}}/>
{:else if addingTo === 'vendors' && adding}
    <New tab={current} on:close={()=>{addingTo='';adding=false}} on:save={()=>{refetchData()}}/>         
{/if}
<main>
    <nav>
        <div class="tabs">
            <button class="{current==='customers'?'active':''}" on:click={()=>{current='customers'; editing = [];}}>Customers</button>
            <button class="{current==='vendors'?'active':''}" on:click={()=>{current='vendors'; editing = [];}}>Vendors</button>
        </div>
        <div class="save">
            {#if current === 'customers'}
            <button on:click={()=>{addingTo = 'customers'; adding=true;}}>+ Add Customer</button>
            {:else}
                <button on:click={()=>{addingTo = 'vendors'; adding=true;}}>+ Add Vendor</button> 
            {/if}
        </div>
    </nav>
    <div class="content">
        <div class="title">
            <div class="filter">
                <div class="filter-title">
                    <span>Search {current}</span>
                </div>
                <div class="group">
                    <select name="filter-by" id="filter-by" bind:value={searchfield}>
                        <option value="Name">Name</option>
                        <option value="Email">Email</option>
                        <option value="Phone">Phone</option>
                        <option value="State">State</option>
                        <option value="Country">Country</option>
                        <option value="GST">GST</option>
                    </select>
                </div>
                <div class="group">
                    <label for="searchfield">Enter {searchfield}</label>
                    <input type="text" bind:value={searchterm} on:keyup={(e)=>{filterParty(e, searchterm)}}>
                </div>
            </div>
        </div>
        <div class="wrapper">
            <div class="head">
                <span>#</span>
                <span>Name</span>
                <span>Email</span>
                <span>Phone</span>
                <span>Address</span>
                <span>GST No.</span>
                <span>Balance</span>
            </div>
            {#key current}
            {#each parties as party, i (i)}
            <div class="row" id="row-{i+1}">
                <div class="actions">
                    {#if !editing.includes(i+1)}    
                    <button on:click={()=>{edit(i+1)}} class="edit">{i+1}</button>
                    {:else}
                    <button class="save" on:click={(e)=>{updateParty(e, party, (i+1))}}>Save</button>
                    <button class="cancel" on:click={()=>{edit(i+1);}}>X</button>
                    {/if}
                </div>
                <input name="name" value="{party.name}" disabled>
                <input name="email" value="{party.email}" disabled>
                <input name="country_code" value="{party.country_code}-{party.phone}" disabled>
                <div class="address">
                    <input name="address" type="text" value="{party.address}" disabled>
                    <input name="state" type="text" value="{party.state}" disabled>
                    <input name="country" type="text" value="{party.country}" disabled>
                    <input name="postal_code" type="text" value="{party.postal_code}" disabled>
                </div>
                <input name="gst" value="{party.gst}" disabled>
                <span>0.00</span>
            </div>
            {/each}
            {/key}
        </div>
    </div>
</main>
{/key}

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
        width: 180px;
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
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .title {
        width: 100%;
        height: 100%;
        padding: 0 2.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .title span {
        width: 250px;
        font-size: 1.5rem;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        color: var(--button-background);
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .title .filter {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        height: 100%;
    }
    .title .filter .filter-title {
        width: 350px;
    }
    .title .filter .filter-title span {
        width: 100%;
    }
    .title .filter .group {
        width: auto;
        height: 100%;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 1rem;
    }
    .title .filter .group input,
    .title .filter .group select {
        width: 250px;
        height: 40px;
        padding: 0.5rem 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .title .filter .group label {
        padding: 0.3rem 1rem;
        font-size: 1.2rem;
        font-weight: 500;
        color: var(--button-background);
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .wrapper {
        width: 95%;
        height: 750px;
        padding: 1rem;
        margin-inline: auto;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        overflow: scroll !important;
    }
    .wrapper .head {
        position: sticky;
        top: -18px;
        margin-bottom: 15px;
        background: var(--nav-background);
        z-index: 9;
    }
    .wrapper .head,
    .wrapper .row {
        width: 100%;
        padding: 0.5rem 1rem;
        color: var(--button-background);
        display: grid;
        grid-template-columns: 1fr repeat(3, 3fr) 5fr 3fr 3fr;
        place-items: center;
        gap: 0.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .wrapper .row{
        height: 130px;
        width: 100%;
    }
    .wrapper .row > span,
    .wrapper .row > input {
        word-wrap: normal;
        width: 100%;
        height: 100% !important;
        padding: 0.5rem 1rem;
        color: var(--button-background);
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--button-text);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        overflow: hidden;
        resize: none;
        border: 0;
        outline: 0;
    }
    .wrapper .row .address {
        width: 100%;
        height: 100%;
        padding: 0.5rem 1rem;
        background: var(--button-text);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .wrapper .row .address input {
        padding: 0.2rem 1rem;
        font-size: 0.85rem;
        box-shadow: none;
        width: 100%;
        background: var(--button-text);
        color: var(--button-background);
        border: 0;
        outline: 0;
    }
    .actions {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .actions .edit {
        height: 50%;
    }
    .actions .save,
    .actions .cancel {
        height: 40%;
        width: 80%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .actions .cancel {
        font-weight: 600;
        background: var(--color-danger);
    }
    .wrapper button {
        position: relative;
        width: 100%;
        height: 50%;
        overflow: hidden;
        background: var(--color-success);
        color: var(--button-background);
    }
    .wrapper .row button:active {
        transform: scale(0.98);
    }
    .wrapper .row .edit::after {
        content: 'Edit';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        font-weight: 600;
        color: var(--button-text);
        background: var(--color-warning);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
    }
    .wrapper .row .edit:hover::after {
        opacity: 1;
    }
</style>