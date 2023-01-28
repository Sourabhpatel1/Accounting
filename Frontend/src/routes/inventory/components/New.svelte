<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    
    const dispatch = createEventDispatcher()

    export let data;

    let units =data.units;
    let itemTypes = data.types;

    let itemName;
    let itemUnitId;
    let itemTypeId;
    let itemAccountId;

    let nameError = false;
    let existingNameError = false;

    let message = '';
    let dialog;

    onMount(()=>{
        document.querySelector('input').focus()
    })

    export const saveItem = async () =>{
        nameError=false;
        existingNameError=false;
        if (!itemName) {
            nameError = true;
            return
        }
        if (data.items.filter(inventory=>inventory.item.name.toLowerCase() === itemName.toLowerCase()).length > 0) {
            existingNameError = true;
            message = `An item with name "${itemName}" already exist, please choose a diffrent name for new items.`
            document.getElementById('errorDialog').style.display='flex'
            return
        }
        if (nameError || existingNameError) {
            return
        }
        const itemRes = await fetch('http://127.0.0.1:8000/inv/', {
            method:'POST',
            mode:'cors',
            headers:{
                'Access-Control-Allow-Origin' : 'http://127.0.0.1:5173',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                "name" : itemName,
                "unit_id" : itemUnitId,
                "type_id" : itemTypeId,
                "account_id":itemAccountId
            })
        })
        if (itemRes.ok) {
            message = `Item "${itemName}" has been saved successfully.`
            dialog.style.display = 'flex'
        } else {
            message = "Something went Wrong, please try again later"
            dialog.style.display = 'flex'
        }
    }

</script>
<main>
    <div class="header">
        <span>Add Inventory Item</span>
    </div>
    <div class="item-info">
        <div class="labels">
            <label for="name" class="{nameError?'error':''}">Item Name</label>
            <label for="unit">Item Unit</label>
            <label for="type">Item Type</label>
            <label for="material">Material Type</label>
        </div>
        <div class="fields">
            <input type="text" name="name" id="name" placeholder="Enter Item Name" bind:value={itemName}>
            <select name="unit" id="unit" bind:value={itemUnitId}>
                {#each units as unit}
                    <option value="{unit.id}">{unit.name}</option>
                {/each}
            </select>
            <select name="type" id="type" bind:value={itemTypeId}>
                {#each itemTypes as type}
                    <option value="{type.id}">{type.name}</option>
                {/each}
            </select>
            <select name="material" id="material" bind:value={itemAccountId}>
                    <option value="5">Raw Materials</option>
                    <option value="6">Semi Finished Materials</option>
                    <option value="7">Finished Materials</option>
            </select>
        </div>
    </div>
    <div class="container" id="errorDialog" bind:this={dialog}>
        <div class="info">
            <span class="message">{message}</span>
            <button on:click={()=>{dialog.style.display='none'; existingNameError||nameError?'':dispatch('save')}}>Close</button>
        </div>
    </div>
</main>
<style>
    main {
        width: 100%;
        min-height: 100%;
    }
    .header {
        width: 100%;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header span {
        padding: 1rem 2rem;
        font-size: 2rem;
        font-weight: 700;
        background: var(--button-text);
        color: var(--button-background);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .item-info {
        width: 60%;
        margin-inline: auto;
        margin-top: 10px;
        padding: 3rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .item-info .labels,
    .item-info .fields {
        width: 100%;
        font-size: 1.5rem;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        gap: 1rem;
    }
    .item-info .labels label {
        width: 100%;
        height: 60px;
        padding: 0.5rem 0rem 0.5rem 8rem;
        color: var(--button-background);
        display: flex;
        align-items: center;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .item-info .fields input,
    .item-info .fields select {
        width: 100%;
        height: 60px;
        padding: 0.5rem 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border: 0;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .item-info .fields input:focus,
    .item-info .fields select:focus {
        outline: 1px solid var(--button-background);
    }
    .error {
        background: var(--color-danger);
    }
    .container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.5);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
        display: none;
        align-items: center;
        justify-content: center;
    }
    .info {
        height: 300px;
        margin-right: 300px;
        padding: 2rem;
        background: var(--button-text);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .info span {
        width: 100%;
        font-size: 2rem;
        font-weight: 500;
    }
    .info button {
        width: 200px;
        height: 60px;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--button-background);
        background: var(--color-danger);
    }
</style>