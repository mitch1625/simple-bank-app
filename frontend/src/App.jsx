import HomePage from './pages/HomePage.jsx'
import AboutPage from './pages/AboutPage.jsx'
import AccountsPage from './pages/AccountsPage.jsx'
import AccountDetailsPage from './pages/AccountDetailsPage.jsx'
import CreateAccountPage from './pages/CreateAccountPage.jsx'
import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router'
import Header from './components/Header.jsx'

function App() {


  return ( 
    <>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/accounts" element={<AccountsPage />} />
          <Route path="/users/:userId/accounts" element={<AccountDetailsPage />} />
          <Route path="/create-account" element={<CreateAccountPage />} />
        </Routes>
      </Router>
    </>
  )
}

export default App
