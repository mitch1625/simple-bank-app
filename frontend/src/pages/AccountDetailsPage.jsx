import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { API } from '../utilities/apis.jsx'
import AccountRow from '../components/AccountRow.jsx'
import TransactionModal from '../components/TransactionModal.jsx'
function AccountDetailsPage() {
    const { userId } = useParams()
    const [accounts, setAccounts] = useState([])
    const [status, setStatus] = useState('loading')
    const [transactionOpen, setTransactionOpen] = useState(false)
    const [transactionVersion, setTransactionVersion] = useState(0)

    useEffect(() => {
        const controller = new AbortController()
        setStatus('loading')

        async function loadAccounts() {
            try {
                const response = await fetch(`${API.users}/${encodeURIComponent(userId)}/accounts`, { signal: controller.signal })
                if (!response.ok) throw new Error(`Failed to load accounts: ${response.status}`)
                setAccounts(await response.json())
                setStatus('success')
            } catch (error) {
                if (error.name !== 'AbortError') setStatus('error')
            }
        }

        loadAccounts()
        return () => controller.abort()
    }, [userId])

    return (
        <main className="account-details">
            <h1>Account Details</h1>
            {status === 'success' && accounts.length > 0 && (
                <button type="button" className="new-transaction" onClick={() => setTransactionOpen(true)}>New Transaction</button>
            )}
            {transactionOpen && (
                <TransactionModal
                    accounts={accounts}
                    onClose={() => setTransactionOpen(false)}
                    onSuccess={updatedAccount => {
                        setAccounts(current => current.map(account => account.id === updatedAccount.id ? updatedAccount : account))
                        setTransactionVersion(version => version + 1)
                        setTransactionOpen(false)
                    }}
                />
            )}
            {status === 'loading' && <p>Loading accounts...</p>}
            {status === 'error' && <p role="alert">Unable to load accounts.</p>}
            {status === 'success' && (accounts.length === 0 ? <p>No accounts found.</p> : (
                <div className="account-table-scroll"><table>
                    <thead>
                        <tr>
                            <th>Account ID</th>
                            <th>Balance</th>
                            <th>Account Type</th>
                        </tr>
                    </thead>
                    <tbody>
                        {accounts.map(account => <AccountRow key={account.id} account={account} transactionVersion={transactionVersion} />)}
                    </tbody>
                </table></div>
            ))}
        </main>
    )
}

export default AccountDetailsPage