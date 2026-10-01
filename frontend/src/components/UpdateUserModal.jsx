import { useEffect, useRef, useState } from 'react'
import { API } from '../utilities/apis.jsx'

function UpdateUserModal({ user, onClose, onSaved }) {
	const dialogRef = useRef(null)
	const [name, setName] = useState(user.name)
	const [email, setEmail] = useState(user.email)
	const [saving, setSaving] = useState(false)
	const [error, setError] = useState('')

	useEffect(() => {
		const dialog = dialogRef.current
		dialog.showModal()
		return () => dialog.close()
	}, [])

	const saveUser = async (event) => {
		event.preventDefault()
		setSaving(true)
		setError('')
		try {
			const response = await fetch(`${API.users}/${encodeURIComponent(user.id)}`, {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name: name.trim(), email: email.trim() })
			})
			if (!response.ok) throw new Error(`Failed to update user: ${response.status}`)
			onSaved(await response.json())
		} catch (saveError) {
			setError('Unable to update user. Please try again.')
		} finally {
			setSaving(false)
		}
	}

	return (
		<dialog ref={dialogRef} className="update-user-modal" onClose={onClose} onCancel={event => { if (saving) event.preventDefault() }} aria-labelledby="update-user-title">
			<form onSubmit={saveUser}>
				<h2 id="update-user-title">Update User</h2>
				<label htmlFor="update-user-name">Name</label>
				<input id="update-user-name" name="name" value={name} onChange={event => setName(event.target.value)} required autoFocus />
				<label htmlFor="update-user-email">Email</label>
				<input id="update-user-email" name="email" type="email" value={email} onChange={event => setEmail(event.target.value)} required />
				{error && <p role="alert">{error}</p>}
				<div className="update-user-actions">
					<button type="button" onClick={() => dialogRef.current.close()} disabled={saving}>Cancel</button>
					<button type="submit" disabled={saving}>{saving ? 'Saving...' : 'Save'}</button>
				</div>
			</form>
		</dialog>
	)
}

export default UpdateUserModal
