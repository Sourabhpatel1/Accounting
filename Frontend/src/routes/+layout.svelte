<script>
    import '$lib/styles/styles.css'
    import { page } from '$app/stores';

    $: currentPage = $page.route.id
</script>
<svelte:head>
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
</svelte:head>
<main>
    <nav>
        <div class="logo">
            <h4>Accounts</h4>
        </div>
        <div class="tabs">
            <button class="{currentPage === '/dashboard'?'active':''}">
                <a href="/dashboard"><i class='bx bxs-dashboard'></i> Dashboard</a>
            </button>
            <button class="{currentPage === '/coa'?'active':''}">
                <a href="/coa"><i class='bx bxs-wallet'></i> Accounts</a>
            </button>
            <button class="{currentPage === '/ledgers'?'active':''}">
                <a href="/ledgers"><i class='bx bxs-book-open' ></i> Ledgers</a>
            </button>
            <button class="{currentPage === '/journal'?'active':''}">
                <a href="/journal"><i class='bx bxs-book-open' ></i> Journal</a>
            </button>
            <button class="{currentPage === '/purchase'?'active':''}">
                <a href="/purchase"><i class='bx bxs-cart-add' ></i> Purchase</a>
            </button>
            <button class="{currentPage === '/sales'?'active':''}">
                <a href="/sales"><i class='bx bxs-store-alt' ></i> Sales</a>
            </button>
            <button class="{currentPage==='/parties'?'active':''}">
                <a href="/parties"><i class='bx bxs-user-detail'></i> Parties</a>
            </button>
            <button class="{currentPage === '/inventory'?'active':''}">
                <a href="/inventory"><i class='bx bxs-box' ></i> Inventory</a>
            </button>
            <button class="{currentPage === '/payroll'?'active':''}">
                <a href="/payroll"><i class='bx bxs-group' ></i> Payroll</a>
            </button>
        </div>
        <div class="footer">
            <button class="{currentPage === '/settings'?'active':''}">
                <a href="/settings"> <i class='bx bxs-cog' ></i> Settings</a>
            </button>
        </div>
    </nav>
    <section class="content">
        <slot></slot>
    </section>
</main>

<style>
   main {
        position: relative;
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: flex-start;
   } 
   nav {
        position: fixed;
        top: 0;
        height: 100%;
        width: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        background-color: var(--nav-background);
        box-shadow: var(--box-shadow-strong);
   }
   nav .logo {
        width: 100%;
        padding: 0.5rem 1rem;
        text-align: center;
        box-shadow: var(--box-shadow-strong);
        border-radius: var(--border-radius);
        background-color: var(--button-background);
    }
    nav .logo h4 {
        color: var(--button-text);
    }
    nav .tabs {
        box-shadow: var(--box-shadow-strong);
    }
    nav .tabs,
    nav .footer {
        width: 100%;
        margin-top: 0.5rem;
        padding: 2rem 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        gap: 1rem;
        border-radius: var(--border-radius);
    }
    nav .tabs button,
    nav .footer button {
        width: 100%;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 0.3rem 1rem;
        transition: scale 0.1s linear;
        transition: background 0.4s ease-in-out;
    }
    nav .tabs button a,
    nav .footer button a {
        width: 100%;
        height: 100%;
        text-align: left;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 2rem;
        font-size: 1.5rem;
        font-weight: 500;
    }
    .footer {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center !important;
        box-shadow: var(--box-shadow-strong);
    }
    .tabs button:active,
    .footer button:active {
        transform: scale(0.98);
    }
    .tabs button.active,
    .footer button.active {
        color: var(--button-background);
        background-color: var(--button-text);
    }
    section {
        position: relative;
        width: 100%;
        height: 100%;
        margin-left: 300px;
    }
</style>