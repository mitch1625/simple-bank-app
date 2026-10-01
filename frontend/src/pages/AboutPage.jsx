import { Link } from 'react-router'

function AboutPage() {
    return (
        <main className="about-page">
            <section className="about-intro">
                <div className="page-shell">
                    <p className="eyebrow">About Bank App</p>
                    <h1>Simple tools for everyday banking.</h1>
                    <p>Bank App brings customer records, account information, and transaction activity together in a straightforward workspace.</p>
                </div>
            </section>
            <section className="about-details page-shell" aria-labelledby="about-tools">
                <h2 id="about-tools">One place to manage the essentials</h2>
                <div className="about-columns">
                    <div><h3>Customers</h3><p>View customer details and keep names and email addresses up to date.</p></div>
                    <div><h3>Accounts</h3><p>Create savings or checking accounts and review balances by customer.</p></div>
                    <div><h3>Transactions</h3><p>Make deposits and withdrawals and inspect each account's transaction history.</p></div>
                </div>
                <Link className="button-primary" to="/accounts">Go to accounts</Link>
            </section>
        </main>
    )
}

export default AboutPage