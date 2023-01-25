<script>
    export let data;
    
    let current = 'coa'

    $: openPrimary = []
    $: openGroup = []
    
    $: addingGroupTo = ''
    $: addingAccTo = ''

    let addingGroup = false;
    let addingAcc = false;

    const refetchData = async ()=>{
        try {
            const primaryRes = await fetch('http://127.0.0.1:8000/acc/all/primary')
            const groupRes = await fetch('http://127.0.0.1:8000/acc/all/group')
            const accRes = await fetch('http://127.0.0.1:8000/acc/all')

            if (primaryRes.ok && groupRes.ok && accRes.ok) {
                data = {
                    'primaryAccounts' : await primaryRes.json(),
                    'groupAccounts' : await groupRes.json(),
                    'accounts' : await accRes.json()
                }
            }
        } catch (err) {
            console.log(err)
        }
    }

    const activatePrimary = (pId)=>{
        if (!openPrimary.includes(pId)){
            openPrimary = [...openPrimary, pId]
        } else {
            let subGroupAccountIds = []
            openPrimary = openPrimary.filter(id=>{return id !== pId})
            let primaryGroupAccounts = data.groupAccounts.filter(acc=>{
                return acc.primary_account_id === pId
            })
            primaryGroupAccounts.forEach(item=>{
                subGroupAccountIds = [...subGroupAccountIds, item.id]
            })
            subGroupAccountIds.forEach(id=>{
                if(openGroup.includes(id)) {
                    openGroup = openGroup.filter(gid=>{
                        return id !== gid
                    })
                }
            })
            addingGroupTo = '';
            addingAccTo = '';
            addingGroup = false;
            addingAcc = false;
        }
    }
    const activateGroup = (gId)=>{
        if (!openGroup.includes(gId)) {
            openGroup = [...openGroup, gId]
        } else {
            openGroup = openGroup.filter(id=>{return id !== gId})
            addingAccTo = '';
            addingAcc = false;
        }
    }
    const addGroupAccount = (pId, e)=>{
        if (openPrimary.includes(pId)) {
            e.stopPropagation()
        }
        if (addingGroupTo === pId) {
            addingGroup = true;
        }
    }
    const addAccount = (gId, e)=>{
        if (openGroup.includes(gId)) {
            e.stopPropagation()
        }
        if (addingAccTo === gId) {
            addingAcc = true;
        }
    }
    const submitGroupAccount = async (pId, e)=>{
        const inputField = e.target.parentNode.firstChild
        const primaryAccountid = pId

        if (!inputField.value) {
            alert("Group Account Name is required")
            return
        }
        if (!pId) {
            alert("Could Not Determine Primary Account Id")
            return
        }
        const groupRes = await fetch('http://127.0.0.1:8000/acc/group_account', {
            method : 'POST',
            mode: 'cors',
            headers : {
                'Access-Control-Allow-Origin' : 'http://127.0.0.1:5173',
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({
                'name' : inputField.value,
                'primary_account_id' : primaryAccountid
            })
        })
        if (groupRes.ok) {
            alert("Group Account " + inputField.value + " Created Successfully")
            refetchData()
        } else if (groupRes.status === 500) {
            alert("Account name must be unique, Group Account name " + inputField.value + " already exists.")
        } else {
            alert("an unknown error occuredm please ensure that the server is running properly and retry.")
        }
    }
    const submitAccount = async (gId, e)=>{
        const inputField = e.target.parentNode.firstChild
        const groupAccountId = gId

        if (!inputField.value) {
            alert("Account Name is required")
            return
        }
        if (!groupAccountId) {
            alert("Could not determine group account id")
            return
        }
        const accRes = await fetch('http://127.0.0.1:8000/acc/account', {
            method : 'POST',
            mode : 'cors',
            headers : {
                'Access-Control-Allow-Origin' : 'http://127.0.0.1:5173',
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({
                'name' : inputField.value,
                'group_account_id' : groupAccountId
            })
        })
        if (accRes.ok) {
            alert("Account " + inputField.value + " Created Succesfully")
            refetchData()
        } else if (accRes.status === 500) {
            alert("Account name must be unique, Account Name " + inputField.value + " already exists")
        } else {
            alert("an unknown error occuredm please ensure that the server is running properly and retry.")
        }
    }
</script>

<main>
    <nav>
        <button class="{current === 'coa'?'active':''}" on:click={()=>{current = 'coa'}}>Charts of Accounts</button>
    </nav>
    {#key  data}
        <div class="content">
            <h4>Primary Accounts</h4>
            {#each data.primaryAccounts as p_acc (p_acc.id)}
                <div class="primary {openPrimary.includes(p_acc.id)?'open':''}">
                    <button on:click={()=>{activatePrimary(p_acc.id)}}>
                        {p_acc.name}
                        <button on:click={(e)=>{addingGroupTo = p_acc.id; addGroupAccount(p_acc.id, e)}}>+ add group account</button>
                    </button>
                    {#if addingGroup && addingGroupTo === p_acc.id && openPrimary.includes(p_acc.id)}
                        <div class="add">
                            <input type="text" placeholder="Enter Group Account Name">
                            <button on:click={(e)=>{submitGroupAccount(p_acc.id, e)}}>+ add</button>
                            <button on:click={()=>{addingGroup = false; addingGroupTo = ''}}>- cancel</button>
                        </div>
                    {/if}
                    {#if openPrimary.includes(p_acc.id)}
                        <h5>Group Accounts</h5>
                    {/if}
                    {#each data.groupAccounts as g_acc (g_acc.id)}
                        <div class="group {openGroup.includes(g_acc.id)?'open':''}">
                            {#if g_acc.primary_account_id === p_acc.id}
                            <button on:click={()=>{activateGroup(g_acc.id)}}>
                                {g_acc.name}
                                <button on:click={(e)=>{addingAccTo = g_acc.id; addAccount(g_acc.id, e)}}>+ add account</button>
                            </button>
                            {#if addingAcc && addingAccTo === g_acc.id && openGroup.includes(g_acc.id)}
                            <div class="add-acc">
                                <input type="text" placeholder="Enter Account Name">
                                <button on:click={(e)=>{submitAccount(g_acc.id, e)}}>+ add</button>
                                <button on:click={()=>{addingAccTo = ''; addingAcc=false}}>- cancel</button>
                            </div>
                            {/if}
                            <div class="acc">
                                <h6>Accounts</h6>
                                {#each data.accounts as acc (acc.id)}
                                {#if acc.group_account_id === g_acc.id}    
                                <button><span>{acc.name}</span> <span>₹ {acc.balance.toFixed(2)} {acc.balance_type}</span></button>
                                {/if}
                                {/each}
                            </div>
                            {/if}
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
    {/key}
</main>

<style>
    nav {
        width: 100%;
        padding: 1rem 1rem;
        background: var(--nav-background);
        box-shadow: var(--box-shadow-strong);
        display: flex;
        align-items: center;
    }
    nav button {
        width: 230px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: var(--box-shadow-strong);
    }
    nav button.active {
        background: var(--button-text);
        color: var(--button-background);
    }
    .content {
        height: 50%;
        display: flex;
        flex-direction: column;
        padding: 1rem;
    }
    .primary {
        width: 500px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
    }
    .primary > button {
        width: 100%;
        height: 80px;
        font-size: 1.5rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: space-between;
        text-align: left;
    }
    .group {
        width: 400px;
        max-height: 0;
        margin-left: 100px;
        opacity: 0;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        pointer-events: none;
    }
    .group > button {
        width: 100%;
        height: 100%;
        height: 60px;
        margin-top: 5px;
        font-size: 1.2rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: space-between;
        text-align: left;
    }
    .acc {
        opacity: 0;
        max-height: 0;
        width: 300px;
        margin-left: 100px;
        pointer-events: none;
    }
    .acc button {
        width: 100%;
        height: 40px;
        font-weight: 500;
        margin-top: 5px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        text-align: left;
    }
    .primary button button {
        height: 100%;
        opacity: 0;
        font-size: 0.9rem;
        color: var(--button-background);
        background: var(--button-text);
        pointer-events: none;
    }
    .primary button:hover button {
        opacity: 1;
        pointer-events: all;
    }
    .group button button {
        height: 100%;
        opacity: 0;
        background: var(--button-text);
        color: var(--button-background);
        pointer-events: none;
    }
    .group button:hover button {
        opacity: 1;
        pointer-events: all;
    }
    .primary.open .group {
        max-height: 100%;
        opacity: 1;
        pointer-events: all;
    }
    .primary.open .group.open .acc {
        max-height: 100%;
        opacity: 1;
        pointer-events: all;
    }
    .add,
    .add-acc {
        width: calc(100% - 100px);
        margin-top: 5px;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.5rem;
        margin-left: 100px;
    }
    .add input,
    .add-acc input {
        width: 100%;
        height: 40px;
        grid-column: 1/3;
        border-radius: var(--border-radius);
        border: 0;
        outline: 0;
        padding: 0 1rem;
        font-weight: 500;
        box-shadow: var(--box-shadow-strong);
    }
    .add button {
        height: 40px;
    }
    .add button:nth-child(2),
    .add-acc button:nth-child(2) {
        color: white;
        font-weight: 500;
        background: var(--color-success);
    }
    .add button:nth-child(3),
    .add-acc button:nth-child(3) {
        color: white;
        font-weight: 500;
        background: var(--color-danger);
    }
</style>