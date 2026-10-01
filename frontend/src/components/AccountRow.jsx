import { useEffect, useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
import { API } from '../utilities/apis.jsx'

function AccountRow({ account, transactionVersion }) {
    const [expanded, setExpanded] = useState(false)
    const [transactions, setTransactions] = useState([])
    const [transactionStatus, setTransactionStatus] = useState('loading')

    useEffect(() => {
        if (!expanded) return
        const controller = new AbortController()
        setTransactionStatus('loading')

        async function loadTransactions() {
            try {
                const response = await fetch(`${API.accounts}/${encodeURIComponent(account.id)}/transactions`, { signal: controller.signal })
                if (!response.ok) throw new Error(`Failed to load transactions: ${response.status}`)
                setTransactions(await response.json())
                setTransactionStatus('success')
            } catch (error) {
                if (error.name !== 'AbortError') setTransactionStatus('error')
            }
        }

        loadTransactions()
        return () => controller.abort()
    }, [account.id, expanded, transactionVersion])

    return (
        <>
            <tr>
                <td>
                    <button
                        type="button"
                        className="account-expand"
                        aria-label={`${expanded ? 'Collapse' : 'Expand'} transactions for account ${account.id}`}
                        aria-expanded={expanded}
                        title={`${expanded ? 'Collapse' : 'Expand'} transactions`}
                        onClick={() => setExpanded(open => !open)}
                    >
                        {expanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
                    </button>
                    {account.id}
                </td>
                <td>{Number(account.balance).toFixed(2)}</td>
                <td>{account.accountType}</td>
            </tr>
            {expanded && (
                <tr className="account-transactions">
                    <td colSpan={3}>
                        {transactionStatus === 'loading' && <p>Loading transactions...</p>}
                        {transactionStatus === 'error' && <p role="alert">Unable to load transactions.</p>}
                        {transactionStatus === 'success' && (transactions.length === 0 ? <p>No transactions found.</p> : (
                            <table>
                                <thead>
                                    <tr>
                                        <th>Transaction ID</th>
                                        <th>Type</th>
                                        <th>Amount</th>
                                        <th>Date</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {[...transactions]
                                        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
                                        .map(transaction => (
                                        <tr key={transaction.id}>
                                            <td>{transaction.id}</td>
                                            <td>{transaction.txnType === 'withdrawal' ? 'Withdraw' : transaction.txnType === 'deposit' ? 'Deposit' : transaction.txnType}</td>
                                            <td>{Number(transaction.amount).toFixed(2)}</td>
                                            <td>{new Date(transaction.createdAt).toLocaleString()}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ))}
                    </td>
                </tr>
            )}
        </>
    )
}

export default AccountRow