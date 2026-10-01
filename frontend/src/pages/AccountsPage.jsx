import {useEffect, useState} from 'react'
import { Link } from 'react-router'
import { API } from '../utilities/apis.jsx'
import UserRowComponent from "../components/UserRowComponent.jsx"
import UpdateUserModal from '../components/UpdateUserModal.jsx'


function AccountsPage() {
    const [users, setUsers] = useState([])
    const [status, setStatus] = useState('loading')
    const [selectedUser, setSelectedUser] = useState(null)

    useEffect(() => {
        const controller = new AbortController()

        async function getAllUsers() {
            try {
                const response = await fetch(API.users, { signal: controller.signal })
                if (!response.ok) throw new Error(`Failed to load users: ${response.status}`)
                setUsers(await response.json())
                setStatus('success')
            } catch (error) {
                if (error.name !== 'AbortError') setStatus('error')
            }
        }

        getAllUsers()
        return () => controller.abort()
    }, [])

    return (
        <main className="accounts-page page-shell">
        <div className="page-heading">
            <div>
                <p className="eyebrow">Account directory</p>
                <h1>Customers</h1>
            </div>
            <Link className="button-primary" to="/create-account">Create account</Link>
        </div>
        {status === 'loading' && <p role="status">Loading customers...</p>}
        {status === 'error' && <p role="alert">Unable to load customers. Please try again later.</p>}
        {status === 'success' && (users.length === 0 ? <p>No customers yet. <Link to="/create-account">Create the first account</Link>.</p> : (
            <div className="directory-table-scroll">
                <table className="directory-table">
                    <thead>
                        <tr>
                            <th scope="col">Customer ID</th>
                            <th scope="col">Name</th>
                            <th scope="col">Email</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <UserRowComponent key={user.id} user={user} onDeleted={deletedId => setUsers(current => current.filter(item => item.id !== deletedId))} onUpdate={setSelectedUser} />
                        ))}
                    </tbody>
                </table>
            </div>
        ))}
        {selectedUser && (
            <UpdateUserModal
                key={selectedUser.id}
                user={selectedUser}
                onClose={() => setSelectedUser(null)}
                onSaved={updatedUser => {
                    setUsers(current => current.map(user => user.id === updatedUser.id ? updatedUser : user))
                    setSelectedUser(null)
                }}
            />
        )}
        </main>
    )
}

export default AccountsPage