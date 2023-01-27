<script>
    import { createEventDispatcher } from "svelte";
    
    export let invoice;

    const dispatch = createEventDispatcher()

</script>

<main>
    <div class="doc">
        <div class="doc-info">
            <div class="header">
                <span>Invoice #</span>
                <hr>
                <span>{invoice.invoice.id}</span>
            </div>
            <div class="group">
                <span>Invoice Type</span>
                <hr>
                <span class="value">{invoice.invoice.doc_type}</span>
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
                <span class="value">{invoice.transaction_type} Sale</span>
            </div>
        </div>
        <div class="entry-info">
            <span>Items</span>
        </div>
        <div class="entries">
            <div class="head">
                <span>#</span>
                <span>Name</span>
                <span>Unit</span>
                <span>Price</span>
                <span>Quantity</span>
                <span>Disc(%)</span>
                <span>Disc(₹)</span>
                <span>GST(%)</span>
                <span>GST(₹)</span>
                <span>Total</span>
            </div>
            {#each invoice.items as item, i (i)}
                <div class="row">
                    <span>{i+1}</span>
                    <span>{item.item_name}</span>
                    <span>{item.unit}</span>
                    <span>{item.price}</span>
                    <span>{item.quantity}</span>
                    <span>{item.discount_rate}</span>
                    <span>{item.discount_amount}</span>
                    <span>{item.gst_rate}</span>
                    <span>{item.gst_amount}</span>
                    <span>{+invoice.amount}</span>
                </div>
            {/each}
            <div class="footer">
                <span>Total</span>
                <span>{parseFloat(invoice.amount).toFixed(2)}</span>
            </div>
        </div>
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
        width: 90%;
        height: 90%;
        background: var(--color-background);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        padding: 1rem;
    }
    .doc-info {
        width: 80%;
        margin: auto;
        padding: 1rem;
        margin-top: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .doc .doc-info .header,
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
        margin: 10px 0px;
    }
    .doc .entry-info span {
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
    .doc .doc-info .header span,
    .doc .doc-info .group span {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .doc .entries {
        position: relative;
        width: 85%;
        max-height: 480px;
        min-height: 180px;
        margin-inline: auto;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        gap: 10px;
        overflow: scroll;
    }
    .doc .entries .head,
    .doc .entries .row {
        width: 90%;
        padding: 0.2rem 1rem;
        margin: auto;
        color: var(--button-background);
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .doc .entries .head {
        position: sticky;
        top: 0px;
        background: var(--nav-background);
    }
    .doc .entries .row {
        background: var(--button-text);
    }
    .doc .entries .footer {
        position: sticky;
        bottom: 0;
        width: 90%;
        padding: 0.3rem 1rem;
        margin: auto;
        margin-top: 0px;
        display: grid;
        grid-template-columns: 9fr 1fr;
        background: var(--nav-background);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .doc .entries .footer span {
        color: var(--button-background);
        font-weight: 500;
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