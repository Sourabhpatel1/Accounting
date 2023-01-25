/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    const docRes = await fetch('http://127.0.0.1:8000/doc/doc')
    const accountsRes = await fetch('http://127.0.0.1:8000/acc/all')
    if (docRes.ok && accountsRes.ok) {
        return {
            'docs' : await docRes.json(),
            'accounts' : await accountsRes.json()
        }
    } else {
        console.log(await docRes.json())
    }
}