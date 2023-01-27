<script>
    import { createEventDispatcher } from "svelte";
    export let tab;

    const dispatch = createEventDispatcher()
</script>

<main>
    <div class="form">
        <div class="head">
            <span>Add {tab}</span>
        </div>
        <div class="info">
            <div class="labels">
                <label for="name">Name</label>
                <label for="email">Email</label>
                <label for="countrycode">Country Code</label>
                <label for="phone">Phone</label>
                <label for="address">Address</label>
                <label for="state">State</label>
                <label for="Country">Country</label>
                <label for="pin">Postal Code</label>
                <label for="gst">GST</label>
            </div>
            <div class="fields">
                <input type="text" name="name" id="name">
                <input type="email" name="email" id="email">
                <input type="text" name="countrycode" id="countrycode">
                <input type="text" name="phone" id="phone">
                <input type="text" name="address" id="address">
                <input type="text" name="state" id="state">
                <input type="text" name="country" id="country">
                <input type="text" name="pin" id="pin">
                <input type="text" name="gst" id="gst">
            </div>
        </div>
        <div class="close">
            <button on:click={()=>{dispatch('close')}}>X</button>
        </div>
        <button>+ Save</button>
    </div>
</main>

<style>
    main {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        color: var(--button-background);
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.5);
        z-index: 10;
    }
    .form {
        position: relative;
        width: 50%;
        height: 90%;
        padding: 1rem;
        background: var(--button-text);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        justify-content: flex-start;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow-strong);
    }
    .head {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .head span {
        font-size: 2rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: var(--button-background);
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .form .info {
        width: 80%;
        margin-top: 25px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        place-items: center;
    }
    .labels,
    .fields {
        width: 100%;
        display: grid;
        gap: 1rem;
    }
    .labels label {
        width: 80%;
        height: 40px;
        padding-left: 70px;
        font-size: 1.2rem;
        font-weight: 600;
        margin-left: 20px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .fields input {
        width: 100%;
        height: 40px;
        padding: 0 1rem;
        color: var(--button-background);
        background: var(--button-text);
        border: 1px solid var(--button-background);
        outline: 0;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .close {
        position: absolute;
        top: -15px;
        right: -15px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .close button {
        width: 40px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--button-background);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: var(--color-danger);
    }
    .form > button {
        margin-top: 50px;
        width: 200px;
        height: 40px;
        font-size: 1.2rem;
        font-weight: 500;
        color: var(--button-background);
        background: var(--color-success);
    }
    button:active {
        transform: scale(0.98);
    }
</style>