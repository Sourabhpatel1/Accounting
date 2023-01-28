/** @type {import('./$types').PageServerLoad} */
export async function load() {
    const salesRes = await fetch('http://127.0.0.1:8000/doc/sales')
    const inventoryRes = await fetch('http://127.0.0.1:8000/inv')
    const unitsRes = await fetch('http://127.0.0.1:8000/lookup/unit')
    const transactionRes = await fetch('http://127.0.0.1:8000/lookup/transaction')
    const inventoryTypeRes = await fetch('http://127.0.0.1:8000/lookup/inventory')
    const customersRes = await fetch('http://127.0.0.1:8000/cust/all')
    const accountsRes = await fetch('http://127.0.0.1:8000/acc/all')
    if (salesRes.ok && inventoryRes.ok && unitsRes.ok && transactionRes.ok && inventoryTypeRes.ok && customersRes.ok && accountsRes.ok) {
        return {
            invoices : await salesRes.json(),
            inventory : await inventoryRes.json(),
            units : await unitsRes.json(),
            transactionTypes : await transactionRes.json(),
            inventoryTypes : await inventoryTypeRes.json(),
            customers : await customersRes.json(),
            accounts : await accountsRes.json()
        }
    }    
}