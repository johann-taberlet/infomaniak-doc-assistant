import type { QuickAction } from '../../types'
import './QuickActions.css'

interface QuickActionsProps {
  actions: QuickAction[]
}

const actionIcons: Record<string, string> = {
  open_docs: '📄',
  contact_support: '💬',
  copy: '📋',
}

export function QuickActions({ actions }: QuickActionsProps) {
  if (!actions.length) return null

  const handleClick = async (action: QuickAction) => {
    if (action.url) {
      window.open(action.url, '_blank', 'noopener,noreferrer')
    } else if (action.action === 'contact_support') {
      window.open('https://www.infomaniak.com/support', '_blank', 'noopener,noreferrer')
    } else if (action.action === 'copy' && action.label) {
      try {
        await navigator.clipboard.writeText(action.label)
      } catch (err) {
        console.error('Failed to copy:', err)
      }
    }
  }

  return (
    <div className="quick-actions">
      {actions.map((action, index) => (
        <button
          key={index}
          className="quick-action-btn"
          onClick={() => handleClick(action)}
        >
          <span className="quick-action-icon">
            {action.icon || actionIcons[action.action || ''] || '→'}
          </span>
          <span className="quick-action-label">{action.label}</span>
        </button>
      ))}
    </div>
  )
}
