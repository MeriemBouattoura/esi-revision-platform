import { NavLink } from 'react-router-dom'
import Icon from './Icons'

const navItems = [
  { to: '/', label: 'Overview', icon: 'grid', end: true },
  { to: '/years', label: 'My curriculum', icon: 'book' },
  { to: '/todos', label: 'To-do list', icon: 'calendar' },
  { to: '/progress', label: 'My progress', icon: 'chart' },
]

export default function Sidebar({ open, onClose, onSignOut }) {
  return (
    <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
      <NavLink to="/" className="brand-lockup" onClick={onClose}>
        <span className="brand-mark">E</span>
        <span className="brand-name">esi<span>revise</span></span>
      </NavLink>
      <div className="nav-caption">WORKSPACE</div>
      <nav className="main-nav" aria-label="Main navigation">
        {navItems.map(({ to, label, icon, end }) => (
          <NavLink key={to} to={to} end={end} onClick={onClose} className={({ isActive }) => `nav-link ${isActive ? 'nav-active' : ''}`}>
            <Icon name={icon} size={19} /><span>{label}</span>
            {label === 'My curriculum' && <span className="nav-count">5</span>}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <div className="sidebar-tip">
          <div className="tip-icon"><Icon name="plus" size={17} /></div>
          <strong>Make today count</strong>
          <p>A little progress each day adds up to big results.</p>
          <NavLink to="/years" onClick={onClose}>Explore curriculum <Icon name="arrow" size={14} /></NavLink>
        </div>
        <button className="nav-link" onClick={onSignOut}><Icon name="logout" size={19} /><span>Sign out</span></button>
      </div>
    </aside>
  )
}
