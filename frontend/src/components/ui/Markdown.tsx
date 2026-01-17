import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ReactNode } from 'react'

interface MarkdownProps {
  children: string | null | undefined
}

/**
 * Markdown component with GFM (GitHub Flavored Markdown) support.
 * Renders tables, strikethrough, task lists, and other GFM features.
 */
export function Markdown({ children }: MarkdownProps): ReactNode {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]}>
      {children || ''}
    </ReactMarkdown>
  )
}
