import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { getErrorMessage } from '../api/client'

function Brand() {
  return <Link to="/login" className="auth-brand"><span className="brand-mark">E</span><span className="brand-name">esi<span>revise</span></span></Link>
}

function AuthFrame({ children, title, description, mode }) {
  return (
    <div className="auth-page">
      <div className="auth-left">
        <Brand />
        <div className="auth-panel">
          <div className="eyebrow"><span className="eyebrow-dot" /> YOUR STUDY SPACE</div>
          <h1>{title}</h1>
          <p className="auth-intro">{description}</p>
          {children}
          <div className="auth-switch">
            {mode === 'login' ? <>New to ESI Revise? <Link to="/register">Create an account <span>→</span></Link></> : <>Already have an account? <Link to="/login">Sign in <span>→</span></Link></>}
          </div>
        </div>
        <div className="auth-footer">© {new Date().getFullYear()} ESI Revise <span>·</span> Built for your next big step</div>
      </div>
      <aside className="auth-aside">
        <div className="aside-art" aria-hidden="true">
          <div className="art-glow" />
          <div className="art-card art-card-back"><div className="art-card-line short" /><div className="art-card-line" /><div className="art-card-line medium" /><div className="art-card-check"><span>✓</span> Weekly revision plan</div></div>
          <div className="art-card art-card-front"><div className="art-card-head"><span className="art-book">✦</span><div><b>Study session</b><small>Mathematics · Chapter 04</small></div><span className="art-more">•••</span></div><div className="art-progress-label"><span>Session progress</span><b>72%</b></div><div className="art-progress"><span /></div><div className="art-complete"><span>✓</span><div><b>You're on a roll!</b><small>3 day study streak</small></div></div></div>
          <div className="art-floating art-float-top"><span>✦</span> Focus mode</div>
          <div className="art-floating art-float-bottom"><span>↗</span> Keep it up</div>
        </div>
        <div className="aside-copy"><div className="aside-kicker">SMALL STEPS. BIG MOMENTUM.</div><h2>Your goals are closer<br />than you think.</h2><p>A calmer, clearer way to stay on top of your revision and make every study session count.</p><div className="aside-pagination"><i className="is-current" /><i /><i /></div></div>
      </aside>
    </div>
  )
}

export function LoginPage() {
  const { login, isAuthenticated, loading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (!loading && isAuthenticated) return <Navigate to="/" replace />

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login(form)
      navigate(location.state?.from?.pathname || '/', { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthFrame mode="login" title={<>Welcome<br />back<span className="title-period">.</span></>} description="Pick up where you left off. Your next great study session is just around the corner.">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-error" role="alert">{error}</div>}
        <label htmlFor="email">Email address</label>
        <input id="email" type="email" autoComplete="email" placeholder="you@example.com" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <div className="field-heading"><label htmlFor="password">Password</label><a href="#forgot-password" onClick={(e) => e.preventDefault()}>Forgot password?</a></div>
        <input id="password" type="password" autoComplete="current-password" placeholder="Enter your password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button type="submit" className="primary-button auth-submit" disabled={submitting}>{submitting ? 'Signing in…' : 'Sign in'} <span>→</span></button>
      </form>
    </AuthFrame>
  )
}

export function RegisterPage() {
  const { register, isAuthenticated, loading } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  if (!loading && isAuthenticated) return <Navigate to="/" replace />

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await register(form)
      navigate('/', { replace: true })
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthFrame mode="register" title={<>A fresh start<span className="title-period">.</span></>} description="Create your account and build a study routine that works for you.">
      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="form-error" role="alert">{error}</div>}
        <label htmlFor="name">Your name</label>
        <input id="name" type="text" autoComplete="name" placeholder="How should we call you?" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <label htmlFor="email">Email address</label>
        <input id="email" type="email" autoComplete="email" placeholder="you@example.com" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
        <label htmlFor="password">Password</label>
        <input id="password" type="password" autoComplete="new-password" minLength="8" placeholder="At least 8 characters" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
        <button type="submit" className="primary-button auth-submit" disabled={submitting}>{submitting ? 'Creating account…' : 'Create account'} <span>→</span></button>
        <p className="terms-note">By creating an account, you agree to our <a href="#terms" onClick={(e) => e.preventDefault()}>Terms</a> and <a href="#privacy" onClick={(e) => e.preventDefault()}>Privacy Policy</a>.</p>
      </form>
    </AuthFrame>
  )
}
