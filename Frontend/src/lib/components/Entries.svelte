<script>
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
        grid-template-columns: repeat(5, 1fr);
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
        grid-template-columns: 3fr 1fr 1fr;
        background: var(--nav-background);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .entries .footer span {
        color: var(--button-background);
        font-weight: 500;
    }
</style>