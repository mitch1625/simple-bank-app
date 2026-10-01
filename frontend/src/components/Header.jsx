import { Link, NavLink } from 'react-router'

function Header() {
    return (
        <header className="site-header">
            <div className="site-header-inner page-shell">
                <Link to="/" className="site-brand">Bank<span>App</span><span className="brand-mark" aria-hidden="true">.</span></Link>
                <nav aria-label="Main navigation">
                    <NavLink to="/" end>Home</NavLink>
                    <NavLink to="/accounts">Accounts</NavLink>
                    <NavLink to="/create-account">Create account</NavLink>
                    <NavLink to="/about">About</NavLink>
                </nav>
            </div>
        </header>
    )
} 

export default Header