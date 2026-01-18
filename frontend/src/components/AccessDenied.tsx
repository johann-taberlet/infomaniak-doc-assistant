import './AccessDenied.css'

interface AccessDeniedProps {
  translations: {
    title: string
    message: string
  }
}

export function AccessDenied({ translations }: AccessDeniedProps) {
  return (
    <div className="access-denied">
      <div className="access-denied-content">
        <div className="access-denied-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
        </div>
        <h2>{translations.title}</h2>
        <p>{translations.message}</p>
      </div>
    </div>
  )
}
