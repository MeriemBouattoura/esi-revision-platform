import { useState } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'

export default function AppLayout() {
  const [menuOpen, setMenuOpen] = useState(false)
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function signOut() {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="app-shell">
      {menuOpen && <button className="sidebar-backdrop" aria-label="Close navigation" onClick={() => setMenuOpen(false)} />}
      <Sidebar open={menuOpen} onClose={() => setMenuOpen(false)} onSignOut={signOut} />
      <div className="workspace">
        <Topbar user={user} onMenu={() => setMenuOpen(true)} onSignOut={signOut} />
        <main className="page-content"><Outlet /></main>
      </div>
    </div>
  )
}
