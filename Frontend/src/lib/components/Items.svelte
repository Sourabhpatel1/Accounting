<script>
    export let invoice;
</script>
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

<style>
    .entries {
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
    .entries .head,
    .entries .row {
        width: 90%;
        padding: 0.2rem 1rem;
        margin: auto;
        color: var(--button-background);
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .entries .head {
        position: sticky;
        top: 0px;
        background: var(--nav-background);
    }
    .entries .row {
        background: var(--button-text);
    }
    .entries .footer {
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
    .entries .footer span {
        color: var(--button-background);
        font-weight: 500;
    }
</style>