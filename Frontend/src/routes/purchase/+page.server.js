/** @type {import('./$types').PageServerLoad} */
export async function load() {
    const purchaseRes = await fetch('http://127.0.0.1:8000/doc/purchase')
    const inventoryRes = await fetch('http://127.0.0.1:8000/inv')
    const unitsRes = await fetch('http://127.0.0.1:8000/lookup/unit')
    const transactionRes = await fetch('http://127.0.0.1:8000/lookup/transaction')
    const inventoryTypeRes = await fetch('http://127.0.0.1:8000/lookup/inventory')
    const vendorsRes = await fetch('http://127.0.0.1:8000/ven/')
    const accountsRes = await fetch('http://127.0.0.1:8000/acc/all')
    if (purchaseRes.ok && inventoryRes.ok && unitsRes.ok && transactionRes.ok && inventoryTypeRes.ok && vendorsRes.ok && accountsRes.ok) {
        return {
            invoices : await purchaseRes.json(),
            inventory : await inventoryRes.json(),
            units : await unitsRes.json(),
            transactionTypes : await transactionRes.json(),
            inventoryTypes : await inventoryTypeRes.json(),
            vendors : await vendorsRes.json(),
            accounts : await accountsRes.json()
        }
    }    
}