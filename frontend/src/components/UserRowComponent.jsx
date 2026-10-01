import { API } from '../utilities/apis.jsx'
import { useNavigate } from 'react-router'

function UserRowComponent({ user, onDeleted, onUpdate }) {
    const navigate = useNavigate()

    const deleteUser = async () => {
        try {
            const response = await fetch(`${API.users}/${encodeURIComponent(user.id)}`, { method: 'DELETE' })
            if (!response.ok) throw new Error(`Failed to delete user: ${response.status}`)
            onDeleted(user.id)
        } catch (error) {
            console.error('Error deleting user:', error)
        }
    }

    return (
        <tr>
            <td className="customer-id">{user.id}</td>
            <td className="customer-name">{user.name}</td>
            <td>{user.email}</td>
            <td className="customer-actions">
                <button type="button" onClick={() => navigate(`/users/${encodeURIComponent(user.id)}/accounts`)}>View accounts</button>
                <button type="button" onClick={() => onUpdate(user)}>Edit</button>
                <button type="button" className="action-danger" onClick={deleteUser}>Delete</button>
            </td>  
        </tr>  
    )
}

export default UserRowComponent