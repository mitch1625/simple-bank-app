import { useEffect, useRef, useState } from 'react'
import { API } from '../utilities/apis.jsx'

function TransactionModal({ accounts, onClose, onSuccess }) {
    const dialogRef = useRef(null)
    const [type, setType] = useState('deposit')
    const [accountId, setAccountId] = useState(accounts[0]?.id || '')
    const [amount, setAmount] = useState('')
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')

    useEffect(() => {
        const dialog = dialogRef.current
        dialog.showModal()
        return () => dialog.close()
    }, [])

    const submit = async (event) => {
        event.preventDefault()
        if (saving) return
        const value = Number(amount)
        if (!Number.isFinite(value) || Math.round(value * 100) <= 0) {
            setError('Enter an amount of at least 0.01.')
            return
        }
        setSaving(true)
        setError('')
        try {
            const response = await fetch(`${API.accounts}/${encodeURIComponent(accountId)}/${type}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: value })
            })
            if (!response.ok) {
                const detail = await response.json()
                throw new Error(typeof detail.detail === 'string' ? detail.detail : 'Transaction failed.')
            }
            onSuccess(await response.json())
        } catch (submitError) {
            setError(submitError.message)
        } finally {
            setSaving(false)
        }
    }

    return (
        <dialog ref={dialogRef} className="transaction-modal" onClose={onClose} onCancel={event => { if (saving) event.preventDefault() }} aria-labelledby="transaction-title">
            <form onSubmit={submit}>
                <h2 id="transaction-title">New Transaction</h2>
                <label htmlFor="transaction-type">Transaction Type</label>
                <select id="transaction-type" value={type} onChange={event => setType(event.target.value)} disabled={saving}>
                    <option value="deposit">Deposit</option>
                    <option value="withdraw">Withdraw</option>
                </select>
                <label htmlFor="transaction-account">Account</label>
                <select id="transaction-account" value={accountId} onChange={event => setAccountId(event.target.value)} required disabled={saving}>
                    {accounts.map(account => <option key={account.id} value={account.id}>{account.accountType} - {account.id}</option>)}
                </select>
                <label htmlFor="transaction-amount">Amount</label>
                <input id="transaction-amount" type="number" min="0.01" step="0.01" value={amount} onChange={event => setAmount(event.target.value)} required disabled={saving} />
                {error && <p role="alert">{error}</p>}
                <div className="transaction-actions">
                    <button type="button" onClick={() => dialogRef.current.close()} disabled={saving}>Cancel</button>
                    <button type="submit" disabled={saving}>{saving ? 'Submitting...' : 'Submit'}</button>
                </div>
            </form>
        </dialog>
    )
}

export default TransactionModal