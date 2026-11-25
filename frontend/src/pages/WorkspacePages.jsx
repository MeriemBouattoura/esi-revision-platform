import { Link, useLocation } from 'react-router-dom'
import Icon from '../components/Icons'
import { useAuth } from '../context/AuthContext'

const courses = [
  { title: 'Mathematics', topic: 'Algebra & functions', color: 'blue', progress: 68, icon: '∑' },
  { title: 'Physics', topic: 'Mechanics', color: 'purple', progress: 42, icon: 'ϕ' },
  { title: 'Computer Science', topic: 'Data structures', color: 'mint', progress: 81, icon: '⌘' },
]

const upcoming = [
  { day: '24', month: 'NOV', title: 'Revise: Linear equations', course: 'Mathematics', time: '09:30 AM', color: 'blue' },
  { day: '25', month: 'NOV', title: 'Practice: Newton’s laws', course: 'Physics', time: '02:00 PM', color: 'purple' },
  { day: '27', month: 'NOV', title: 'Review: Arrays & lists', course: 'Computer Science', time: '10:00 AM', color: 'mint' },
]

export function OverviewPage() {
  const { user } = useAuth()
  const firstName = (user?.name || user?.full_name || 'there').split(' ')[0]
  return (
    <>
      <div className="welcome-row">
        <div><div className="eyebrow"><span className="eyebrow-dot" /> MONDAY, NOVEMBER 23</div><h1>Good morning, {firstName}<span className="title-period">.</span></h1><p className="page-subtitle">A new week is a fresh chance to make progress.</p></div>
        <Link to="/courses" className="primary-button welcome-action"><Icon name="plus" size={17} /> Explore courses</Link>
      </div>
      <section className="stats-grid" aria-label="Study summary">
        <div className="stat-card"><div className="stat-top"><span className="stat-label">Study time this week</span><span className="stat-icon stat-blue"><Icon name="clock" size={18} /></span></div><div className="stat-value">4.5 <small>hrs</small></div><div className="stat-foot"><span className="stat-trend">↗ 12%</span> vs last week</div><div className="mini-bars" aria-hidden="true">{[35, 54, 43, 74, 51, 82, 30].map((height, i) => <i key={i} style={{ height: `${height}%` }} className={i === 5 ? 'bar-current' : ''} />)}</div></div>
        <div className="stat-card"><div className="stat-top"><span className="stat-label">Current study streak</span><span className="stat-icon stat-amber">✦</span></div><div className="stat-value">3 <small>days</small></div><div className="stat-foot">You’re building a great habit</div><div className="streak-dots"><i className="done">M</i><i className="done">T</i><i className="done">W</i><i>T</i><i>F</i><i>S</i><i>S</i></div></div>
        <div className="stat-card"><div className="stat-top"><span className="stat-label">Topics completed</span><span className="stat-icon stat-green"><Icon name="check" size={18} /></span></div><div className="stat-value">12 <small>topics</small></div><div className="stat-foot">Across all your courses</div><div className="stat-progress"><span /></div></div>
      </section>
      <div className="content-grid">
        <section className="content-card course-card">
          <div className="section-heading"><div><h2>Your courses</h2><p>Keep your learning moving forward</p></div><Link to="/courses" className="text-link">View all <Icon name="arrow" size={15} /></Link></div>
          <div className="course-list">{courses.map((course) => <Link className="course-row" to="/courses" key={course.title}><span className={`course-icon course-${course.color}`}>{course.icon}</span><span className="course-main"><strong>{course.title}</strong><small>{course.topic}</small></span><span className="course-progress"><span className="course-bar"><i className={`fill-${course.color}`} style={{ width: `${course.progress}%` }} /></span><small>{course.progress}%</small></span><Icon name="arrow" size={17} className="course-arrow" /></Link>)}</div>
        </section>
        <section className="content-card agenda-card">
          <div className="section-heading"><div><h2>Coming up</h2><p>Your next study sessions</p></div><Link to="/schedule" className="text-link">Planner <Icon name="arrow" size={15} /></Link></div>
          <div className="agenda-list">{upcoming.slice(0, 2).map((item) => <div className="agenda-row" key={item.title}><div className={`agenda-date date-${item.color}`}><b>{item.day}</b><small>{item.month}</small></div><div className="agenda-info"><strong>{item.title}</strong><small>{item.course}</small></div><span className="agenda-time">{item.time}</span></div>)}</div>
          <Link to="/schedule" className="agenda-bottom"><Icon name="calendar" size={16} /> See your full study plan <Icon name="arrow" size={14} /></Link>
        </section>
      </div>
      <section className="focus-banner"><div className="focus-badge"><span>✦</span></div><div className="focus-copy"><strong>Every session adds up.</strong><p>You’ve already put in 4.5 hours this week. Keep the momentum going!</p></div><Link to="/courses" className="focus-link">Keep learning <Icon name="arrow" size={15} /></Link><div className="focus-decoration" aria-hidden="true">✦</div></section>
    </>
  )
}

const pageContent = {
  '/years': { eyebrow: 'YOUR CURRICULUM', title: 'Choose your year', description: 'Pick your study year to explore semesters and modules.', icon: 'book', titleAction: 'Study years' },
  '/todos': { eyebrow: 'YOUR ROUTINE', title: 'To-do list', description: 'Keep track of what you want to revise today.', icon: 'calendar', titleAction: 'Your tasks' },
  '/courses': { eyebrow: 'LEARNING SPACE', title: 'Your courses', description: 'Everything you’re learning, all in one place.', icon: 'book', titleAction: 'Your courses' },
  '/schedule': { eyebrow: 'YOUR ROUTINE', title: 'Study planner', description: 'A little planning makes a big difference.', icon: 'calendar', titleAction: 'Upcoming sessions' },
  '/progress': { eyebrow: 'LOOK HOW FAR YOU’VE COME', title: 'Your progress', description: 'Celebrate the small wins that get you to your goals.', icon: 'chart', titleAction: 'Your learning journey' },
}

export function PlaceholderPage() {
  const { pathname } = useLocation()
  const page = pageContent[pathname]
    || (pathname.startsWith('/years/') ? {
      eyebrow: 'YOUR CURRICULUM', title: 'Choose a semester', description: 'Select S1 or S2 to see your modules.',
      icon: 'calendar', titleAction: 'Available semesters',
    } : pathname.startsWith('/semesters/') ? {
      eyebrow: 'YOUR CURRICULUM', title: 'Choose a module', description: 'Select a module to open its revision space.',
      icon: 'book', titleAction: 'Available modules',
    } : pathname.includes('/modules/') && pathname.endsWith('/stats') ? {
      eyebrow: 'YOUR PROGRESS', title: 'Module statistics', description: 'See how prepared you are for each course.',
      icon: 'chart', titleAction: 'Preparation levels',
    } : pathname.includes('/modules/') && pathname.endsWith('/revision') ? {
      eyebrow: 'REVISION SPACE', title: 'Course documents', description: 'Read course notes or practise with a quiz.',
      icon: 'book', titleAction: 'Revision documents',
    } : pathname.includes('/modules/') ? {
      eyebrow: 'YOUR CURRICULUM', title: 'Module workspace', description: 'Choose revision materials, check your progress, or plan your work.',
      icon: 'book', titleAction: 'Module options',
    } : pathname.includes('/quiz') ? {
      eyebrow: 'PRACTICE', title: 'Quiz practice', description: 'Set up a quiz and test what you know.',
      icon: 'check', titleAction: 'Your quiz',
    } : pathname === '/progress' ? pageContent['/progress'] : pageContent['/courses'])
  const items = pathname === '/schedule' ? upcoming : courses
  return (
    <>
      <div className="welcome-row"><div><div className="eyebrow"><span className="eyebrow-dot" /> {page.eyebrow}</div><h1>{page.title}<span className="title-period">.</span></h1><p className="page-subtitle">{page.description}</p></div></div>
      <section className="content-card placeholder-card">
        <div className="section-heading"><div><h2>{page.titleAction}</h2><p>Here’s what’s on your radar</p></div><span className="placeholder-tag">YOUR SPACE</span></div>
        <div className="placeholder-list">{items.map((item) => <div className="placeholder-row" key={item.title}><span className={`course-icon ${item.color ? `course-${item.color}` : 'course-blue'}`}>{item.icon || item.day}</span><div className="placeholder-row-copy"><strong>{item.title}</strong><small>{item.topic || item.course}</small></div>{item.progress ? <span className="placeholder-progress">{item.progress}% complete</span> : <span className="placeholder-progress">{item.month} {item.day} · {item.time}</span>}</div>)}</div>
      </section>
      <section className="empty-feature"><div className="feature-icon"><Icon name={page.icon} size={22} /></div><div><strong>More tools are on the way</strong><p>This space is ready for your learning journey. Keep checking back as your workspace grows.</p></div></section>
    </>
  )
}
