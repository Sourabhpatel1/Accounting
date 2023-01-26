<script>
    import { onMount, onDestroy } from "svelte";
    import ViewInvoice from "./ViewInvoice.svelte";

    onMount(()=>{
        document.body.style.overflow = 'hidden'
    })
    onDestroy(()=>{
        document.body.style.overflow = 'scroll'
    })

    export let invoices;

    let userInvoices = invoices.sort((a,b)=>{
        if (a.invoice.doc_date>b.invoice.doc_date){return 1}
        if (a.invoice.doc_date<b.invoice.doc_date){return -1}
        if (a.invoice.doc_date===b.invoice.doc_date){return 0}
    })

    let rowHeader;

    let invoiceType;
    let startDate;
    let endDate;
    let invoiceToView;
    let viewinginvoice = false;

    let viewInvoice = (invoiceId)=>{
        invoiceToView = invoices.filter(inv=>{
            return inv.invoice.id === invoiceId
        })[0]
        viewinginvoice = true;
        console.log(invoiceToView)
    }
    const filter = ()=>{
        userInvoices = invoices
        if (startDate) {
            userInvoices = invoices.filter(inv=>{
                return (inv.invoice.doc_date >= startDate)
            })
        }
        if (endDate) {
            userInvoices = invoices.filter(inv=>{
                return (inv.invoice.doc_date <= endDate)
            })
        }
    }
    const hideRow = ()=>{
        document.querySelectorAll('.row').forEach(row=>{
            if (rowHeader.getBoundingClientRect().bottom >= row.getBoundingClientRect().top) {
                row.style.zIndex = -1
             } else {
                row.style.zIndex = 1
            }
        })
    }
</script>
{#if viewinginvoice}
    <ViewInvoice invoice={invoiceToView} on:close={()=>{viewinginvoice=false; invoiceToView=null}}/>
{/if}
<main>
    <div class="filters">
        <div class="filter-types">
            <div class="group title">
                <span>Filter Invoices</span>
            </div>
            <div class="group">
                <label for="start">Start Date</label>
                <input type="date" name="start" id="start" bind:value={startDate}>
            </div>
            <div class="group">
                <label for="end">End Date</label>
                <input type="date" name="end" id="end" bind:value={endDate}>
            </div>
            <div class="group">
                <i class='bx bx-filter' ></i>
                <button on:click={filter}>Apply</button>
            </div>
        </div>
    </div>
    <div class="cards" on:scroll={hideRow}>
        <div class="head" bind:this={rowHeader}>
            <span>#</span>
            <span>Document No</span>
            <span>Document Date</span>
            <span>Document Amount (₹)</span>
            <span>Actions</span>
        </div>
        {#each userInvoices as inv, i (i)}
            <div class="row">
                <span>{i+1}</span>
                <span>{inv.invoice.id}</span>
                <span>{inv.invoice.doc_date}</span>
                <span>{parseFloat(inv.amount).toFixed(2)}</span>
                <button on:click={()=>{viewInvoice(inv.invoice.id)}}>View Details</button>
            </div>
        {/each}
    </div>
</main>

<style>
    main {
        left: 0;
        width: 100%;
        height: 100%;
        padding: 0.2rem 0.5rem;
    }
    .filters {
        width: 100%;
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .filters .title {
        width: 100%;
        height: 100%;
        text-align: center;
    }
    .filters .title span {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--button-background);
    }
    .filters .filter-types {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        place-items: center;
        gap: 2rem;
    }
    .filters .filter-types .group {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: var(--box-shadow-strong);
        padding: 1rem 1rem;
        border-radius: var(--border-radius);
    }
    .filters .filter-types .group label {
        font-size: 1.2rem;
        font-weight: 600;
    }
    .filters .filter-types .group input {
        width: 100%;
        height: 40px;
        padding: 0.2rem 1.8rem;
        background: var(--button-text);
        color: var(--button-background);
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .filters .filter-types .group button {
        width: 100%;
        height: 40px;
        box-shadow: var(--box-shadow-strong);
    }
    .filters .filter-types .group button:active {
        transform: scale(0.98);
    }
    .cards {
        width: 90%;
        height: 700px;
        margin: auto;
        display: flex;
        flex-direction: column;
        margin-top: 10px;
        background: var(--button-text);
        padding: 1rem 1rem;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        overflow: scroll;
    }
    .cards .head,
    .cards .row {
        padding: 0.5rem 1rem;
        display: grid;
        grid-template-columns: 1fr 2fr 2fr 2fr 2fr;
        border-radius: var(--border-radius);
        place-items: start;
    }
    .cards .head {
        width: 100%;
        color: var(--button-background);
        background: var(--button-text);
        margin-bottom: 5px;
        box-shadow: var(--box-shadow-strong);
        position: sticky;
        top: 0px;
        z-index: 9;
    }
    .cards .row {
        position: relative;
        width: 100%;
        margin-inline: auto;
        color: var(--button-background);
        background: var(--nav-background);
        margin: 2px 0;
        box-shadow: var(--box-shadow-medium);
        transition: opacity 0.5 ease;
    }
    .cards .row span,
    .cards .row button {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    .cards .row button {
        width: 60%;
        color: white;
        background: var(--color-success);
        box-shadow: var(--box-shadow-strong);
    }
    .cards .row button:active {
        transform: scale(0.98);
    }
    :global(body) {
        overflow: hidden;
    }
</style>