<script>
    import { createEventDispatcher } from "svelte";
    export let tab;

    let name;
    let email;
    let country_code;
    let phone;
    let address;
    let state;
    let country;
    let postal_code;
    let gst = "N/A";

 let fieldError = false;

    const dispatch = createEventDispatcher()
    export const save = async ()=>{
        if (!name || !email || !country_code || !phone || !address || !state || !country || !postal_code){
            fieldError = true;
            return
        }
        
        let urlSuffix = tab==="customers"?'/cust/':tab==='vendors'?'/ven/':null
        const partyRes = await fetch('http://127.0.0.1:8000'+urlSuffix, {
            method:'POST',
            mode:'cors',
            headers:{
                'Access-Control-Allow-Origin':'http://localhost:5173',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                "name": name,
                "email": email,
                "country_code": country_code,
                "phone": Number(phone),
                "address": address,
                "state": state,
                "country": country,
                "postal_code": Number(postal_code),
                "gst": gst
            })
        })
        if (partyRes.ok) {
            alert(`${name} has been added to ${tab} successfully.`)
            dispatch('save')
        } else {
            alert("Something Went Wrong")
        }
    }
</script>

<main>
    <div class="form">
        <div class="head">
            <span>Add {tab}</span>
        </div>
        <span class="{fieldError?'error':''}">Fields Marked with * are required</span>
        <div class="info">
            <div class="labels">
                <label for="name">Name <span>*</span></label>
                <label for="email">Email <span>*</span></label>
                <label for="countrycode">Country Code <span>*</span></label>
                <label for="phone">Phone <span>*</span></label>
                <label for="address">Address <span>*</span></label>
                <label for="state">State <span>*</span></label>
                <label for="Country">Country <span>*</span></label>
                <label for="pin">Postal Code <span>*</span></label>
                <label for="gst">GST</label>
            </div>
            <div class="fields">
                <input type="text" name="name" id="name" bind:value={name}>
                <input type="email" name="email" id="email" bind:value={email}>
                <input type="text" name="countrycode" id="countrycode" bind:value={country_code}>
                <input type="text" name="phone" id="phone" bind:value={phone}>
                <input type="text" name="address" id="address" bind:value={address}>
                <input type="text" name="state" id="state" bind:value={state}>
                <input type="text" name="country" id="country" bind:value={country}>
                <input type="text" name="pin" id="pin" bind:value={postal_code}>
                <input type="text" name="gst" id="gst" bind:value={gst}>
            </div>
        </div>
        <div class="close">
            <button on:click={()=>{dispatch('close')}}>X</button>
        </div>
        <button on:click={save}>+ Save</button>
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
        margin-top: 5px;
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
        height: 50px;
        padding-left: 70px;
        padding: 0.1rem 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        margin-left: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .labels label span {
        color: var(--color-danger);
    }
    .fields input {
        width: 100%;
        height: 50px;
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
    .form > span {
        padding: 0.5rem;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
    }
    .form span.error {
        background: var(--color-danger);
    }
    .form > button {
        margin-top: 20px;
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