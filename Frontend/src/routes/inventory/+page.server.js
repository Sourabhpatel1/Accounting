/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const inventoryRes = await fetch('http://127.0.0.1:8000/inv/')
    const unitRes = await fetch('http://127.0.0.1:8000/lookup/unit')
    const typeRes = await fetch('http://127.0.0.1:8000/lookup/inventory')

    if (inventoryRes.ok && unitRes.ok && typeRes.ok) {
        return {
            'items' : await inventoryRes.json(),
            'units' : await unitRes.json(),
            'types' : await typeRes.json()
        }
    }
}