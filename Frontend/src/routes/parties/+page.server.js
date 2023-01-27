/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    const customerRes = await fetch('http://127.0.0.1:8000/cust/all')
    const vendorRes = await fetch('http://127.0.0.1:8000/ven')
    if (customerRes.ok && vendorRes.ok) {
        return {
            customers : await customerRes.json(),
            vendors : await vendorRes.json()
        }
    }
}