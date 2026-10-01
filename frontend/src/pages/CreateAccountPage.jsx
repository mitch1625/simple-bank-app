
import { useEffect, useState } from 'react'
import { API } from '../utilities/apis.jsx'

async function postJson(url, body) {
    const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    const data = await response.json()
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : `Request failed: ${response.status}`)
    return data
}

function CreateAccountPage() {
    const [mode, setMode] = useState('new')
    const [users, setUsers] = useState([])
    const [usersStatus, setUsersStatus] = useState('loading')
    const [selectedId, setSelectedId] = useState('')
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [accountType, setAccountType] = useState('Savings')
    const [createdUserId, setCreatedUserId] = useState('')
    const [saving, setSaving] = useState(false)
    const [message, setMessage] = useState('')
    const [error, setError] = useState('')
    const selectedUser = users.find(user => user.id === selectedId)

    useEffect(() => {
        if (mode !== 'existing') return
        const controller = new AbortController()
        setUsersStatus('loading')

        async function loadUsers() {
            try {
                const response = await fetch(API.users, { signal: controller.signal })
                if (!response.ok) throw new Error(`Failed to load users: ${response.status}`)
                setUsers(await response.json())
                setUsersStatus('success')
            } catch (loadError) {
                if (loadError.name !== 'AbortError') setUsersStatus('error')
            }
        }

        loadUsers()
        return () => controller.abort()
    }, [mode])

    const submit = async (event) => {
        event.preventDefault()
        if (saving) return
        setSaving(true)
        setError('')
        setMessage('')

        let userId = mode === 'existing' ? selectedId : createdUserId
        try {
            if (mode === 'new' && !userId) {
                const user = await postJson(API.users, { name: name.trim(), email: email.trim() })
                userId = user.id
                setCreatedUserId(userId)
            }
            const account = await postJson(API.accounts, { userId, accountType })
            setMessage(`Account ${account.id} created successfully.`)
            if (mode === 'new') {
                setCreatedUserId('')
                setName('')
                setEmail('')
            }
        } catch (submitError) {
            setError(`${submitError.message}${mode === 'new' && userId ? ' The user was created; retry to create the account.' : ''}`)
        } finally {
            setSaving(false)
        }
    }

    const switchMode = (nextMode) => {
        setMode(nextMode)
        setMessage('')
        setError('')
    }

    return (
        <main className="create-account">
            <h1>Create Account</h1>
            <div className="create-account-modes" role="group" aria-label="User type">
                <button type="button" aria-pressed={mode === 'new'} onClick={() => switchMode('new')} disabled={saving}>New User</button>
                <button type="button" aria-pressed={mode === 'existing'} onClick={() => switchMode('existing')} disabled={saving}>Existing User</button>
            </div>
            <form onSubmit={submit}>
                {mode === 'existing' ? (
                    <>
                        <label htmlFor="account-user">User</label>
                        <select id="account-user" value={selectedId} onChange={event => { setSelectedId(event.target.value); setMessage(''); setError('') }} required disabled={saving || usersStatus !== 'success'}>
                            <option value="">Select a user</option>
                            {users.map(user => <option key={user.id} value={user.id}>{user.name} ({user.email})</option>)}
                        </select>
                        {usersStatus === 'loading' && <p>Loading users...</p>}
                        {usersStatus === 'error' && <p role="alert">Unable to load users.</p>}
                        {usersStatus === 'success' && users.length === 0 && <p>No users available.</p>}
                        <label htmlFor="account-existing-name">Name</label>
                        <input id="account-existing-name" value={selectedUser?.name || ''} readOnly />
                        <label htmlFor="account-existing-id">ID</label>
                        <input id="account-existing-id" value={selectedUser?.id || ''} readOnly />
                    </>
                ) : (
                    <>
                        <label htmlFor="account-new-name">Name</label>
                        <input id="account-new-name" value={name} onChange={event => setName(event.target.value)} required disabled={saving || !!createdUserId} />
                        <label htmlFor="account-new-email">Email</label>
                        <input id="account-new-email" type="email" value={email} onChange={event => setEmail(event.target.value)} required disabled={saving || !!createdUserId} />
                    </>
                )}
                <label htmlFor="account-type">Account Type</label>
                <select id="account-type" value={accountType} onChange={event => setAccountType(event.target.value)} disabled={saving}>
                    <option value="Savings">Savings</option>
                    <option value="Checking">Checking</option>
                </select>
                {error && <p role="alert" className="create-account-error">{error}</p>}
                {message && <p role="status" className="create-account-success">{message}</p>}
                <button type="submit" disabled={saving || (mode === 'existing' && !selectedUser)}>{saving ? 'Creating...' : 'Create Account'}</button>
            </form>
        </main>
    )
}

export default CreateAccountPage