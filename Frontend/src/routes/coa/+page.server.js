/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
    try {
        const primaryRes = await fetch('http://127.0.0.1:8000/acc/all/primary')
        const groupRes = await fetch('http://127.0.0.1:8000/acc/all/group')
        const accRes = await fetch('http://127.0.0.1:8000/acc/all')

        if (primaryRes.ok && groupRes.ok && accRes.ok) {
            return {
                'primaryAccounts' : await primaryRes.json(),
                'groupAccounts' : await groupRes.json(),
                'accounts' : await accRes.json()
            }
        }
    } catch (err) {
        console.log(err)
    }
}