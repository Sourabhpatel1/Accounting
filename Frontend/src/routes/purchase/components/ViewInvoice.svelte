<script>
    import Items from "../../../lib/components/Items.svelte";
    import Entries from "../../../lib/components/Entries.svelte";
    import { createEventDispatcher } from "svelte";
    
    export let invoice;
    export let accounts;
    export let vendors;

    let viewing = 'items'

    const dispatch = createEventDispatcher()

</script>

<main>
    <div class="doc">
        <div class="doc-info">
            <div class="header">
                <span>Invoice #</span>
                <span>{invoice.invoice.id}</span>
            </div>
            <div class="groups">
                <div class="group">
                    <span>Invoice Type</span>
                    <hr>
                    <span class="value">{invoice.invoice.doc_type}</span>
                </div>
                <div class="group">
                    <span>Party Name</span>
                    <hr>
                    <span>{vendors.filter(ven=>ven.id === invoice.invoice.vendor_id)[0].name}</span>
                </div>
                <div class="group">
                    <span>Invoice Date</span>
                    <hr>
                    <span class="value">{invoice.invoice.doc_date}</span>
                </div>
                <div class="group">
                    <span>Invoice Amount</span>
                    <hr>
                    <span class="value">₹ {parseFloat(invoice.amount).toFixed(2)}</span>
                </div>
                <div class="group">
                    <span>Transaction Type </span>
                    <hr>
                    <span class="value">{invoice.transaction_type} Purchase</span>
                </div>
            </div>
        </div>
        <div class="entry-info">
            <button class="{viewing==='items'?'active':''}" on:click={()=>{viewing = 'items'}}>Items</button>
            <button class="{viewing==='entries'?'active':''}" on:click={()=>{viewing='entries'}}>Entries</button>
        </div>
        {#if viewing === 'items'}
            <Items {invoice}/>
        {:else if viewing === 'entries'}
            <Entries {accounts} doc={invoice}/>
        {/if}
        <div class="actions">
            <button>Cancel Document</button>
        </div>
        <button class="close" on:click={()=>{dispatch('close')}}>X</button>
    </div>
</main>

<style>
    main {
        position: fixed;
        top: 50%;
        left: 50%;
        width: 100vw;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.2);
        box-shadow: var(--box-shadow-strong);
        z-index: 10;
    }
    hr {
        width: 100%;
    }
    .doc {
        position: relative;
        width: 95%;
        height: 90%;
        background: var(--color-background);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        padding: 0.5rem;
    }
    .doc-info {
        width: 95%;
        margin: auto;
        padding: 1rem;
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.2rem;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .doc-info .header {
        width: 100%;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .doc-info .header span {
        padding: 0.5rem 1rem;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .groups {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 10px;
    }
    .doc-info .group {
        width: 25%;
        padding: 0.5rem 2rem;
        color: var(--button-background);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .doc .entry-info {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 10px 0px;
    }
    .doc .entry-info button {
        width: 20%;
        padding: 0.5rem 2rem;
        text-align: center;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--button-background);
        background: var(--button-text);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .doc .entry-info button.active {
        background: var(--color-success);
        color: var(--button-background);
    }
    .doc .doc-info .header span,
    .doc .doc-info .group span {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .close {
        position: absolute;
        top: -20px;
        right: -20px;
        width: 50px;
        height: 50px;
        font-size: 1.8rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--button-background);
        border-radius: 50%;
        background: var(--color-danger);
        box-shadow: var(--box-shadow-strong);
    }
    .close:active {
        transform: scale(0.98);
    }
    .actions {
        margin-top: 30px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .actions button {
        width: 20%;
        height: 50px;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--button-background);
        background-color: var(--color-danger);
        box-shadow: var(--box-shadow-strong);
    }
    .actions button:active {
        transform: scale(0.98);
    }
</style>