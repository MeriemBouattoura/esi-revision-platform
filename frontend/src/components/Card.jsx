export default function Card({ className = '', ...props }) {
  return <section className={`content-card ${className}`.trim()} {...props} />
}
