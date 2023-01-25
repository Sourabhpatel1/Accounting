<script>
    import { createEventDispatcher } from "svelte";
    
    const dispatch = createEventDispatcher()

    export let doc;
    export let accounts;
    
    let entries = []
    
    doc.dr_entries.forEach(entry=>{
        let newEntry = {
            account : accounts.filter(account=>{
                return account.id === entry.account_id
            })[0].name,
            amount : entry.amount,
            entryType : 'Debit'
        }
        entries = [...entries, newEntry]
    })
    
    doc.cr_entries.forEach(entry=>{
        let newEntry = {
            account : accounts.filter(account=>{
                return account.id === entry.account_id
            })[0].name,
            amount : entry.amount,
            entryType : 'Credit'
        }
        entries = [...entries, newEntry]
    })

</script>

<main>
    <div class="doc">
        <div class="doc-info">
            <div class="header">
                <span>Document #</span>
                <span>{doc.document.id}</span>
            </div>
            <div class="group">
                <span>Document Type :</span>
                <span class="value">{doc.document.doc_type}</span>
            </div>
            <div class="group">
                <span>Document Date :</span>
                <span class="value">{doc.document.doc_date}</span>
            </div>
            <div class="group">
                <span>Document Amount :</span>
                <span class="value">₹ {parseFloat(doc.amount).toFixed(2)}</span>
            </div>
        </div>
        <div class="entry-info">
            <span>Entries</span>
        </div>
        <div class="entries">
            <div class="head">
                <span>#</span>
                <span>Entry Type</span>
                <span>Account Name</span>
                <span>Dr. Amount (₹)</span>
                <span>Cr. Amount (₹)</span>
            </div>
            {#each entries as entry, i (i)}
                <div class="row">
                    <span>{i+1}</span>
                    <span>{entry.entryType}</span>
                    <span>{entry.account} A/c.</span>
                    <span>{entry.entryType==='Debit'?parseFloat(entry.amount).toFixed(2):''}</span>
                    <span>{entry.entryType==='Credit'?parseFloat(entry.amount).toFixed(2):''}</span>
                </div>
            {/each}
            <div class="footer">
                <span>Total</span>
                <span>{parseFloat(doc.amount).toFixed(2)}</span>
                <span>{parseFloat(doc.amount).toFixed(2)}</span>
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
        grid-template-columns: repeat(5, 1fr);
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
        grid-template-columns: 3fr 1fr 1fr;
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