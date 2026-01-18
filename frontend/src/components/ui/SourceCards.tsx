import type { SourceDocument } from '../../types'
import { stripMarkdown } from '../../utils/text'
import './SourceCards.css'

interface SourceCardsProps {
  sources: SourceDocument[]
}

const productColors: Record<string, string> = {
  kDrive: '#0066cc',
  kMeet: '#00a86b',
  kChat: '#ff6b35',
}

export function SourceCards({ sources }: SourceCardsProps) {
  if (!sources.length) return null

  return (
    <div className="source-cards">
      <div className="source-cards-header">
        <span className="source-cards-icon">📚</span>
        <span className="source-cards-title">Sources</span>
      </div>
      <div className="source-cards-scroll">
        {sources.map((source, index) => (
          <a
            key={source.url}
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="source-card"
          >
            <div className="source-card-header">
              <span
                className="source-card-badge"
                style={{
                  backgroundColor: productColors[source.product] || '#666',
                }}
              >
                {source.product}
              </span>
              <span className="source-card-rank">#{index + 1}</span>
            </div>
            <h4 className="source-card-title">{source.title}</h4>
            <p className="source-card-snippet">{stripMarkdown(source.snippet)}</p>
          </a>
        ))}
      </div>
    </div>
  )
}
