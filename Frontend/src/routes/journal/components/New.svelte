<script>
    import { createEventDispatcher } from "svelte";
    
    const dispatch = createEventDispatcher()

    export let docNumber;
    export let accounts;

    let documentTypes = [
        '',
        'Journal',
        'Cash',
        'Bank',
        'Depriciation',
        'Contra'
    ]
    let rows = [
        {
            'sr' : 1,
            'accountName' : '',
            'accountId' : '',
            'entryType' : '',
            'amount' : ''
        }
    ]
    let journal = {
        'document' : {
            'doc_type' : '',
            'doc_date' : '',
        },
        'master_account' : {
            'id' : '',
            'entry_type' : ''
        },
        'entries' : []
    }
    let savePrompt;
    let saveSuccess;
    let docType;
    let docDate = new Date().toJSON().slice(0,10)
    let masterAccount;
    let entryType = '';
    
    let typeError;
    let dateError;
    let masterAccountError;
    let entryTypeError;
    let rowErrorList = [];

    let message;
    let messageError = false;

    const setEntryType = () => {
        rows.forEach(row=>{
            if (entryType === 'cr') {
                row.entryType = 'Debit'
            } else {
                row.entryType = 'Credit'
            }
        })
        rows = rows
    }
    const addRow = ()=>{

        if (rows.length >= 10) {
            return
        }
        let newEntry = {
            'sr' : rows.length + 1,
            'accountName' : '',
            'accountId' : '',
            'entryType' : entryType === 'dr'?'Credit':'Debit',
            'amount' : ''
        }
        rows = [...rows, newEntry]
    }
    const removeRow = (rowNum)=>{
        if (rows.length < 2) {
            return
        }
        let newRows = rows.filter(row=>{
            return row.sr !== rowNum
        })
        newRows.forEach((row, i)=>{
            row.sr = i+1
        })
        console.log(newRows)
        rows = newRows
    }
    const setAccount = (e, rowNum)=>{
        rows.forEach(row=>{
            if (row.sr === rowNum) {
                row.accountName = e.target.value
                try {
                    row.accountId = accounts.filter(account=>{
                        return account.name === row.accountName
                    })[0].id
                } catch (err) {
                    
                }
            }
        })
    }
    const setAmount = (e, rowNum)=>{
        rows.forEach(row=>{
            if (row.sr === rowNum) {
                if (parseFloat(e.target.value).toFixed(2) == 'NaN') {
                    e.target.value = ''
                    row.amount = ''
                } else {
                    e.target.value = parseFloat(e.target.value)
                    row.amount = parseFloat(e.target.value).toFixed(2)
                }
            }
        })
    }
    const formatAmount = (e)=>{
        e.target.value = parseFloat(e.target.value).toFixed(2) === 'NaN'?'':parseFloat(e.target.value).toFixed(2)
    }
    export const startSave = ()=>{
        if (typeError || dateError || masterAccountError || entryTypeError || (rowErrorList.length > 0)) {
            saveDocument()
        } else {
            savePrompt.showModal()
        }
    }
    const saveDocument = async ()=>{
        typeError = false;
        dateError = false;
        masterAccountError = false;
        entryTypeError = false;
        rowErrorList = [];

        if(!docType) {
            typeError = true;
        }
        if (!docDate) {
            dateError = true;
        }
        if (!masterAccount) {
            masterAccountError = true;
        }
        if (!entryType) {
            entryTypeError = true;
        }
        rows.forEach(row=>{
            if (!row.accountId || !row.amount) {
                rowErrorList = [...rowErrorList, row.sr]
            }
        })
        if (typeError || dateError || masterAccountError || entryTypeError || (rowErrorList.length > 0)) {
            savePrompt.close()
            return false
        }
        journal.document.doc_type = docType
        journal.document.doc_date = docDate
        journal.master_account.id = accounts.filter(account=>{return account.name === masterAccount})[0].id
        journal.master_account.entry_type = entryType
        
        rows.forEach(row=>{
            let newEntry = {
                'account_id' : row.accountId,
                'amount' : row.amount
            }
            journal.entries = [...journal.entries, newEntry]
        })
        console.log(journal)
        const docRes = await fetch('http://127.0.0.1:8000/doc/general', {
            method : 'POST',
            mode : 'cors',
            headers : {
                'Access-Control-Allow-Origin' : 'http://localhost:5173',
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify(journal)
        })
        if (docRes.status === 200) {
            message = `Document ${docNumber} dated ${docDate} saved succesfully.`
            saveSuccess.showModal()
            return true
        } else if (docRes.status === 500) {
            message = 'Error : 500, an internal server error occured, failed to save the document.'
            messageError = true;
            saveSuccess.showModal()
            return false
        } else {
            message = 'An unknown error occured, please try again.'
            messageError = true;
            saveSuccess.showModal()
            return false
        }
    }
</script>

<main>
    <dialog bind:this={savePrompt}>
        <div class="info">
            <span>Save Document?</span>
        </div>
        <div class="actions">
            <button class="ok" on:click={saveDocument}>+ Save</button>
            <button class="cancel" on:click={savePrompt.close()}>- Cancel</button>
        </div>
    </dialog>
    <dialog bind:this={saveSuccess}>
        <div class="info {messageError?'error-message':''}">
            <span>{message}</span>
        </div>
        <div class="actions">
            <div class="actions">
                <button class="ok" on:click={()=>{dispatch('saved'); saveSuccess.close()}}>Close</button>
            </div>
        </div>
    </dialog>
    <div class="document-container">
        <div class="doc-header">
            <span>Document #</span>
            <span>{docNumber}</span>
        </div>
        {#key docNumber}
        <div class="doc-info">
            <div class="group">
                <label for="type">Document Type</label>
                <select name="type" id="type" bind:value={docType}>
                    {#each documentTypes as type}
                        <option value="{type}">{type}</option>
                    {/each}
                </select>
                {#if typeError}
                    <span class="error">This field is required</span>
                {/if}
            </div>
            <div class="group">
                <label for="date">Document Date</label>
                <input type="date" name="date" id="date" bind:value={docDate}>
                {#if dateError}
                    <span class="error">This field is required</span>
                {/if}
            </div>
            <div class="group">
                <label for="account-name">Account Name</label>
                <input type="text" name="masterAccount" id="masterAccount" placeholder="Enter Account Name" list="masterAccounts" autocomplete="true" bind:value={masterAccount}>
                <datalist id="masterAccounts">
                    {#each accounts as account}
                        <option value="{account.name}">{account.name}</option>
                    {/each}
                </datalist>
                {#if masterAccountError}
                    <span class="error">This field is required</span>
                {/if}
            </div>
            <div class="group">
                <label for="entryType">Entry Type</label>
                <select name="entryType" id="enrtyType" bind:value={entryType} on:change={setEntryType}>
                    <option value="" selected></option>
                    <option value="dr">Debit</option>
                    <option value="cr">Credit</option>
                </select>
                {#if entryTypeError}
                    <span class="error">This field is required</span>
                {/if}    
            </div>
        </div>
        {/key}
        <div class="rows">
            <div class="header">
                <span>#</span>
                <span>Account</span>
                <span>Entry Type</span>
                <span>Amount</span>
            </div>
            {#each rows as row (row.sr)}
            <div class="row {rowErrorList.includes(row.sr)?'row-error':''}" id="row-{row.sr}">
                <button class="remove-row" on:click={()=>{removeRow(row.sr)}}>{row.sr}</button>
                <input type="text" name="account-{row.sr}" id="account-{row.sr}" placeholder="Enter Account Name" autocomplete="true" list="accounts" value="{row.accountName}" on:input={(e)=>{setAccount(e, row.sr)}}>
                <datalist id="accounts">
                    {#each accounts as account}
                    <option value="{account.name}">{account.name}</option>
                    {/each}
                </datalist>
                <button style="cursor: default;">{row.entryType}</button>
                <input type="text" placeholder="₹ 0.00" name="amount-{row.sr}" id="amount-{row.sr}" value="{row.amount}" on:input={(e)=>{setAmount(e, row.sr)}} on:change={(e)=>{formatAmount(e)}}>
            </div>
            {/each}
            <button on:click={addRow}>+ Add Row</button>
        </div>
    </div>
</main>

<style>
    main {
        width: 100%;
    }
    dialog {
        position: absolute;
        top: 40%;
        left: 50%;
        width: 600px;
        height: 250px;
        color: var(--button-background);
        background: var(--button-text);
        transform: translate(-50%, -50%);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .info {
        width: 100%;
        height: 60%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .info span {
        font-size: 1.3rem;
        font-weight: 600;
        letter-spacing: 1.2px;
    }
    .actions {
        width: 100%;
        height: 20%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    .actions .ok {
        width: 150px;
        height: 45px;
        font-weight: 600;
        color: white;
        background: var(--color-success);
        box-shadow: var(--box-shadow-strong);
    }
    .actions .cancel {
        width: 150px;
        height: 45px;
        font-weight: 600;
        color: white;
        background: var(--color-danger);
        box-shadow: var(--box-shadow-strong);
    }
    .actions button:active {
        transform: scale(0.98);
    }
    .document-container {
        width: 100%;
        padding: 1rem 1.8rem 1.5rem 1.8rem;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        background: var(--nav-background);
    }
    .document-container .doc-header {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 50px;
    }
    .document-container .doc-header span {
        font-size: 1.5rem;
        font-weight: 600;
    }
    .doc-header span:nth-child(1) {
        padding: 0.5rem 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .doc-header span:nth-child(2) {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        color: var(--button-background);
        background: var(--button-text);
        box-shadow: var(--box-shadow-strong);
    }
    .document-container .doc-info {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        place-items: center;
    }
    .doc-info .group{
        position: relative;
        width: 100%;
        display: grid;
        grid-template-columns: 1fr;
        gap: 1rem;
        box-shadow: var(--box-shadow-strong);
        padding: 1rem;
        border-radius: var(--border-radius);
    }
    .doc-info .group input,
    .doc-info .group select {
        width: 100%;
        height: 40px;
        padding: 0.2rem 1rem;
        font-weight: 500;
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
        background: var(--button-text);
        color: var(--button-background);
    }
    .rows {
        width: 90%;
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        padding: 1rem;
    }
    .rows .header {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--button-background);
        background: var(--button-text);
        margin-bottom: 5px;
    }
    .rows .header,
    .rows .row {
        width: 100%;
        padding: 0.5rem 1rem;
        display: grid;
        grid-template-columns: 1fr 4fr 2fr 4fr;
        gap: 2rem;
        text-align: center;
        border-radius: var(--border-radius);
    }
    .row input {
        padding: 0.2rem 3rem;
        font-weight: 500;
        border: 0;
        outline: 0;
        border-radius: var(--border-radius);
    }
    .row > * {
        color: var(--button-background);
        background: var(--button-text);
        box-shadow: var(--box-shadow-strong);
    }
    .row button:nth-child(1):active {
        transform: scale(0.98);
    }
    .rows > button {
        width: 20%;
        margin-top: 1rem;
        font-size: 1rem;
        font-weight: 600;
        align-self: center;
        background: var(--button-background);
        box-shadow: var(--box-shadow-strong);
        color: var(--button-text);
    }
    .rows > button:active {
        transform: scale(0.98);
    }
    .row .remove-row {
        position: relative;
    }
    .row .remove-row::after {
        content: 'X';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--button-text);
        border-radius: var(--border-radius);
        opacity: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-danger);
        font-weight: 500;
    }
    .row .remove-row:hover::after {
        opacity: 1;
    }
    .error {
        position: absolute;
        width: 100%;
        top: -35px;
        left: 50%;
        padding: 0.1rem 1rem;
        text-align: center;
        transform: translateX(-50%);
        font-weight: 600;
        color: white;
        background: var(--color-danger);
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .row-error {
        position: relative;
    }
    .row-error::after {
        width: 8%;
        content: '* required';
        position: absolute;
        right: -115px;
        top: 50%;
        transform: translateY(-50%);
        background: var(--color-danger);
        border-radius: var(--border-radius);
    }
</style>