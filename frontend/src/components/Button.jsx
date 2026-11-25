export default function Button({ variant = 'primary', className = '', ...props }) {
  return <button className={`${variant === 'primary' ? 'primary-button' : 'secondary-button'} ${className}`.trim()} {...props} />
}
