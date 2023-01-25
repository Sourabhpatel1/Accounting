<script>
    import New from "./components/New.svelte";
    import View from "./components/View.svelte";
  
    export let data;

    $: docNumber = data.docs.length + 1
    $: accounts = data.accounts
    
    let current = 'new'
    let saveDoc;
    
    const refetchData = async ()=>{
        const docRes = await fetch('http://127.0.0.1:8000/doc/doc')
        if (docRes.ok) {
            data = {
                'docs' : await docRes.json(),
                'accounts' : accounts
            }
        } else {
            console.log(await docRes.json())
        }
    }
    const save = async ()=>{
        saveDoc()
    }
</script>

<main>
    <nav>
        <div class="tabs">
            <button class="{current==='new'?'active':''}" on:click={()=>{current = 'new'}}>New Journal</button>
            <button class="{current==='view'?'active':''}" on:click={()=>{current = 'view'}}>View Journals</button>
        </div>
        <div class="actions">
            {#if current === 'new'}
                <button on:click={save}>+ Save</button>
            {/if}
        </div>
    </nav>
    <div class="content">
        {#key data}
            {#if current === 'new'}
                <New {docNumber} {accounts} bind:startSave={saveDoc} on:saved={()=>{refetchData()}}/>
            {:else if current === 'view'}
                <View docs={data.docs} {accounts}/>
            {/if}
        {/key}
    </div>
</main>

<style>
    main {
        width: 100%;
        height: 100%;
    }
    nav {
        position: sticky;
        top: 0;
        width: 100%;
        padding: 1rem 1rem;
        background: var(--nav-background);
        box-shadow: var(--box-shadow-strong);
        display: flex;
        align-items: center;
        justify-content: space-between;
        z-index: 9;
    }
    nav .tabs {
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 1rem;
    }
    nav .tabs button {
        width: 230px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: var(--box-shadow-strong);
        transition: background 0.2s ease;
    }
    nav .tabs button:active {
        transform: scale(0.98);
    }
    nav .tabs button.active {
        background: var(--button-text);
        color: var(--button-background);
    }
    .actions {
        padding: 0rem 1rem;
    }
    .actions button:nth-child(1) {
        font-size: 1.2rem;
        font-weight: 600;
        color: white;
        background: var(--color-success);
    }
    .actions button:nth-child(1):active {
        transform: scaleX(0.98);
    }
    .content {
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        padding: 1rem;
        
    }
</style>