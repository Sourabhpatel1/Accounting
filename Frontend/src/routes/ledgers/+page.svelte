<script>
    import { onMount, onDestroy } from "svelte";
    
    onMount(()=>{
        document.body.style.overflow = 'hidden'
    })
    onDestroy(()=>{
        document.body.style.overflow = 'scroll'
    })

    export let data;

    let loaded = false;
    let accounts = data.accounts;
    let ledgerEntries = [];
    let accountName;
    let selectedAccount;
    let startDate;
    let endDate;
    let ledger;
    let balance;
    let balanceType;
    let accountdesc;

    const setAccountId = ()=>{
        let acc = accounts.filter(acc=>{
            return acc.name === accountName
        })
        selectedAccount = acc[0].id
        accountdesc = acc[0].name
    }
    const getLedger = async ()=>{
        const ledgerRes = await fetch('http://127.0.0.1:8000/acc/ledger/' + selectedAccount)
        if (ledgerRes.ok) {
            ledger = await ledgerRes.json()
            loaded = true;
        } else {
            alert("Failed to fetch ledger")
        }
    }
    $: if (loaded) {
        
        ledgerEntries = []
        
        let debitTotal = 0;
        let creditTotal = 0;

        ledger.debited_accounts.forEach(entry=>{
            if (startDate && endDate) {
                if (entry.document.doc_date >= startDate && entry.document.doc_date <= endDate) {
                    let newEntry = {
                        'date' : entry.document.doc_date,
                        'accountName' : 'By ' + entry.account.name,
                        'documentNo' : entry.document.id,
                        'documentType' : entry.document.doc_type,
                        'crAmount' : entry.entry.amount,
                        'drAmount' : ''
                    }
                    ledgerEntries = [...ledgerEntries, newEntry]
                    creditTotal += entry.entry.amount   
                }
            } else {
                let newEntry = {
                    'date' : entry.document.doc_date,
                    'accountName' : 'By ' + entry.account.name,
                    'documentNo' : entry.document.id,
                    'documentType' : entry.document.doc_type,
                    'crAmount' : entry.entry.amount,
                    'drAmount' : ''
                }
                ledgerEntries = [...ledgerEntries, newEntry]
                creditTotal += entry.entry.amount   
            }
        })
        ledger.credited_accounts.forEach(entry=>{
            if (startDate && endDate) {
                if (entry.document.doc_date >= startDate && entry.document.doc_date <= endDate) {
                    let newEntry = {
                        'date' : entry.document.doc_date,
                        'accountName' :'To ' + entry.account.name,
                        'documentNo' : entry.document.id,
                        'documentType' : entry.document.doc_type,
                        'crAmount' : '',
                        'drAmount' : entry.entry.amount
                    }
                    ledgerEntries = [...ledgerEntries, newEntry]
                    debitTotal += entry.entry.amount   
                } 
            } else {
                let newEntry = {
                    'date' : entry.document.doc_date,
                    'accountName' : 'To ' + entry.account.name,
                    'documentNo' : entry.document.id,
                    'documentType' : entry.document.doc_type,
                    'crAmount' : '',
                    'drAmount' : entry.entry.amount
                }
                ledgerEntries = [...ledgerEntries, newEntry]
                debitTotal += entry.entry.amount  
            }
        })
        if (debitTotal > creditTotal) {
            balance = debitTotal - creditTotal
            balanceType = "Debit"
        } else if (creditTotal > debitTotal) {
            balance = creditTotal - debitTotal
            balanceType = "Credit"
        } else {
            balance = 0
            balanceType = '-'
        }
        ledgerEntries.sort((a, b) => {
            if (a.date < b.date) {
                return -1
            }
            if (a.date > b.date) {
                return 1
            }
            if (a.date === b.date) {
                return 0
            }
        })
    }
</script>

<main>
    <div class="filters">
        <div class="group">
            <label for="account">Account</label>
            <input type="text" name="account" id="account" list="accounts" autocomplete="true" bind:value={accountName} on:change={setAccountId}>
            <datalist id="accounts">
                {#each accounts as acc (acc.id)}
                    <option value="{acc.name}">{acc.name}</option>
                {/each}
            </datalist>
        </div>
        <div class="group">
            <label for="start">Start Date</label>
            <input type="date" name="start" id="start" bind:value={startDate}>
        </div>
        <div class="group">
            <label for="end">End Date</label>
            <input type="date" name="end" id="end" bind:value={endDate}>
        </div>
        <div class="actions">
            <button on:click={getLedger}><i class='bx bx-search-alt'></i> Search by Account Name</button>
        </div>
    </div>
    <div class="account-description">
        <span id='accountName'>
            {#if ledgerEntries.length > 0}
                {accountdesc} A/c.
            {/if}
        </span>
    </div>
    <div class="ledger">
        <div class="header">
            <span>#</span>
            <span>Entry Date</span>
            <span>Account Name</span>
            <span>Document Type</span>
            <span>Document No</span>
            <span>Dr. Amount</span>
            <span>Cr. Amount</span>
        </div>
        {#each ledgerEntries as entry, i (i)}        
            <div class="rows">
                <span>{i+1}</span>
                <span>{entry.date}</span>
                <span>{entry.accountName}</span>
                <span>{entry.documentType}</span>
                <span>{entry.documentNo}</span>
                <span>{parseFloat(entry.drAmount).toFixed(2)==='NaN'?'-':parseFloat(entry.drAmount).toFixed(2)}</span>
                <span>{parseFloat(entry.crAmount).toFixed(2)==='NaN'?'-':parseFloat(entry.crAmount).toFixed(2)}</span>
            </div>
        {/each}
        {#if ledgerEntries.length > 0}
            <div class="footer">
                <span class="bal">Balance</span>
                <span>{balance.toFixed(2)}</span>
                <span>{balanceType}</span>
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        padding: 0rem 1rem 3rem 1rem;
    }
    .filters {
        width: 100%;
        padding: 1rem; 
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        background: var(--nav-background);
        border-radius: var(--border-radius);
    }
    .filters .group {
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        box-shadow: var(--box-shadow-strong);
        padding: 1rem;
        border-radius: var(--border-radius);
    }
    .filters .group input {
        width: 100%;
        padding: 0.5rem 1rem;
        border: 0;
        outline: 0;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        background: var(--button-text);
        color: var(--button-background);
    }
    .filters .actions {
        width: 100%;
        height: 100px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .filters .actions button {
        width: 80%;
        font-size: 1rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 1rem;
        box-shadow: var(--box-shadow-strong);
    }
    .filters .actions button:active {
        transform: scale(0.98);
    }
    .ledger {
        position: relative;
        margin-top: 15px;
        width: 100%;
        max-height: calc(100vh - 210px);
        padding: 0rem;
        overflow: scroll;
    }
    .account-description {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .account-description span {
        padding: 0.5rem 1rem;
        margin-top: 10px;
        margin-bottom: -5px;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--button-background);
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .ledger .header {
        position: sticky;
        top: 0;
        width: 100%;
        padding: 0.5rem 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color:  var(--text-color);
        display: grid;
        grid-template-columns: 1fr 2fr 3fr 2fr 2fr 3fr 3fr;
        place-items: center;
        background: var(--nav-background);
        border-radius: var(--border-radius);
    }
    .ledger .header span {
        width: 100%;
        padding: 0.1rem 0.5rem;
        text-align: left;
    }
    .ledger .rows {
        width: 100%;
        margin-top: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        display: grid;
        grid-template-columns: 1fr 2fr 3fr 2fr 2fr 3fr 3fr;
        place-items: center;
        background: var(--button-text);
    }
    .ledger .rows span {
        width: 100%;
        padding: 0.1rem 0.5rem;
        text-align: left;
    }
    .ledger .footer {
        position: sticky;
        bottom: 0;
        width: 100%;
        padding: 0.5rem 1rem;
        margin-top: 5px;
        background: var(--nav-background);
        color: var(--text-color);
        display: grid;
        grid-template-columns: 9fr 1fr 1fr;
        border-radius: var(--border-radius);
    }
    .ledger .footer span {
        width: 100%;
        font-size: 1.2rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
</style>