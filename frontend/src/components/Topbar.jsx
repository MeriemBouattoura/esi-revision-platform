import { useState } from 'react'
import Icon from './Icons'

function initials(user) {
  const name = user?.name || user?.email || 'Student'
  return name.split(/[\s@.]+/).filter(Boolean).slice(0, 2).map((part) => part[0]).join('').toUpperCase()
}

export default function Topbar({ user, onMenu, onSignOut }) {
  const [menuOpen, setMenuOpen] = useState(false)
  const name = user?.name || 'Student'

  function signOut() {
    setMenuOpen(false)
    onSignOut()
  }

  return (
    <header className="topbar">
      <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={onMenu}><Icon name="menu" /></button>
      <div className="breadcrumb"><span>Workspace</span><span className="crumb-slash">/</span><strong>Overview</strong></div>
      <div className="topbar-right">
        <button className="icon-button search-button" aria-label="Search"><Icon name="search" /></button>
        <button className="icon-button notification-button" aria-label="Notifications"><Icon name="bell" /><span className="notification-dot" /></button>
        <div className="topbar-divider" />
        <div className="user-menu">
          <button className="user-chip" aria-expanded={menuOpen} aria-haspopup="menu" onClick={() => setMenuOpen((open) => !open)}>
            <div className="avatar">{initials(user)}</div>
            <div className="user-chip-copy"><strong>{name}</strong><span>{user?.role === 'admin' ? 'Administrator' : 'Student'}</span></div>
          </button>
          {menuOpen && <div className="user-menu-popover" role="menu">
            <div className="user-menu-email">{user?.email}</div>
            <button role="menuitem" onClick={signOut}><Icon name="logout" size={16} /> Sign out</button>
          </div>}
        </div>
      </div>
    </header>
  )
}
