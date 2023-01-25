<script>
    import { onMount, onDestroy } from "svelte";
    import ViewDocument from "./ViewDocument.svelte";
    
    onMount(()=>{
        document.body.style.overflow = 'hidden'
    })
    onDestroy(()=>{
        document.body.style.overflow = 'scroll'
    })
    export let docs;
    export let accounts;
    
    let userDocs = docs.sort((a,b)=>{
        if (a.document.doc_date>b.document.doc_date){return 1}
        if (a.document.doc_date<b.document.doc_date){return -1}
        if (a.document.doc_date===b.document.doc_date){return 0}
    })

    let rowHeader;

    let docType;
    let startDate;
    let endDate;
    let docToView;
    let viewingDoc = false;
    
    let viewDoc = (docId)=>{
        docToView = docs.filter(doc=>{
            return doc.document.id === docId
        })[0]
        viewingDoc = true;
    }

    const filter = ()=>{
        userDocs = docs
        if (docType) {
            userDocs = docs.filter(doc=>{
                return (doc.document.doc_type === docType)
            })
        }
        if (startDate) {
            userDocs = docs.filter(doc=>{
                return (doc.document.doc_date >= startDate)
            })
        }
        if (endDate) {
            userDocs = docs.filter(doc=>{
                return (doc.document.doc_date <= endDate)
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

<main>
    {#if viewingDoc && docToView}
        <ViewDocument doc={docToView} {accounts} on:close={()=>{viewingDoc = false; docToView = undefined}}/>
    {/if}
    <div class="filters">
        <div class="filter-types">
            <div class="group title">
                <span>Filter Documents</span>
            </div>
            <div class="group">
                <label for="type">Document Type</label>
                <select name="type" id="type" bind:value={docType}>
                    <option value="" selected>All</option>
                    <option value="Journal">Journal</option>
                    <option value="Cash">Cash</option>
                    <option value="Bank">Bank</option>
                    <option value="Contra">Contra</option>
                    <option value="Depriciation">Depriciation</option>
                </select>
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
            <span>Document Type</span>
            <span>Document Amount (₹)</span>
            <span>Actions</span>
        </div>
        {#each userDocs as doc, i (i)}
            <div class="row">
                <span>{i+1}</span>
                <span>{doc.document.id}</span>
                <span>{doc.document.doc_date}</span>
                <span>{doc.document.doc_type}</span>
                <span>{parseFloat(doc.amount).toFixed(2)}</span>
                <button on:click={()=>{viewDoc(doc.document.id)}}>View Details</button>
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
        grid-template-columns: repeat(5, 1fr);
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
    .filters .filter-types .group input,
    .filters .filter-types .group select {
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
        grid-template-columns: 1fr 2fr 2fr 2fr 2fr 2fr;
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