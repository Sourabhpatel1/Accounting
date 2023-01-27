<script>
    import View from "./components/View.svelte";
    import New from "./components/New.svelte";
    
    export let data
    
    let current = 'item'
</script>

<main>
    <nav>
        <div class="tabs">
            <button class="{current==='item'?'active':''}" on:click={()=>{current='item'}}>Inventory Items</button>
            <button class="{current==='add'?'active':''}" on:click={()=>{current='add'}}>Add Items</button>
        </div>
        <div class="save">
            {#if current === 'add'}
                <button>+Add Item</button>
            {/if}
        </div>
    </nav>
    <div class="content">
        {#if current === 'item'}
            <View {data}/>
        {:else if current === 'add'}
            <New {data}/>
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
    } 
    button:active {
        transform: scale(0.98);
    }
    nav {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 1rem;
        background: var(--nav-background);
        box-shadow: var(--box-shadow-strong);
    }
    nav .tabs {
        width: 80%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 2rem;
    }
    nav .tabs button {
        width: 230px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: var(--box-shadow-strong);
        transition: background 0.2s ease;
    }
    nav .tabs button.active {
        background: var(--button-text);
        color: var(--button-background);
    }
    nav .tabs .save {
        width: 20%;
        height: 100%;
    }
    .save button {
        width: 150px;
        height: 40px;
        color: var(--button-background);
        background: var(--color-success);
        box-shadow: var(--box-shadow-strong);
    }
    .content {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: flex-start;
        justify-content: center;
    }
</style>