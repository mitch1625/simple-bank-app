import { Link } from 'react-router'
import { ArrowUpRight, Landmark, UsersRound, WalletCards } from 'lucide-react'

function HomePage() {

    return (
        <main>
            <section className="home-hero">
                <div className="home-hero-content page-shell">
                    <p className="eyebrow">Everyday banking</p>
                    <h1>Bank App</h1>
                    <p>Manage customers, accounts, and transactions in one place.</p>
                    <div className="hero-actions">
                        <Link className="button-primary" to="/accounts">View accounts <ArrowUpRight size={18} aria-hidden="true" /></Link>
                        <Link className="button-outline" to="/create-account">Create account</Link>
                    </div>
                </div>
            </section>
            <section className="home-workflows page-shell" aria-labelledby="workflows-title">
                <div className="section-heading">
                    <p className="eyebrow">Your workspace</p>
                    <h2 id="workflows-title">Banking, organized.</h2>
                </div>
                <div className="workflow-grid">
                    <Link to="/accounts" className="workflow-link">
                        <UsersRound size={23} aria-hidden="true" />
                        <span>Customers</span>
                        <ArrowUpRight size={18} aria-hidden="true" />
                    </Link>
                    <Link to="/create-account" className="workflow-link">
                        <WalletCards size={23} aria-hidden="true" />
                        <span>Open an account</span>
                        <ArrowUpRight size={18} aria-hidden="true" />
                    </Link>
                    <Link to="/about" className="workflow-link">
                        <Landmark size={23} aria-hidden="true" />
                        <span>About Bank App</span>
                        <ArrowUpRight size={18} aria-hidden="true" />
                    </Link>
                </div>
            </section>
        </main>
    )
}


export default HomePage