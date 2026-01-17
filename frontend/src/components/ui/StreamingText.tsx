import { useState, useEffect, useRef } from 'react'
import { Markdown } from './Markdown'
import './Markdown.css'

interface StreamingTextProps {
  content: string
  /** Delay between characters in ms (default: 8) */
  charDelay?: number
  /** Characters to reveal per tick (default: 2) */
  charsPerTick?: number
  /** Called when all text has been displayed */
  onComplete?: () => void
}

/**
 * Displays text with a smooth typewriter effect, character by character.
 */
export function StreamingText({
  content,
  charDelay = 8,
  charsPerTick = 2,
  onComplete,
}: StreamingTextProps) {
  const [displayedLength, setDisplayedLength] = useState(0)
  const onCompleteCalledRef = useRef(false)
  const contentRef = useRef(content)

  // Reset when content changes significantly
  useEffect(() => {
    if (content !== contentRef.current) {
      // If new content is extension of old, don't reset
      if (!content.startsWith(contentRef.current)) {
        setDisplayedLength(0)
        onCompleteCalledRef.current = false
      }
      contentRef.current = content
    }
  }, [content])

  // Animation effect
  useEffect(() => {
    const totalLength = content.length

    // All displayed?
    if (displayedLength >= totalLength) {
      if (!onCompleteCalledRef.current) {
        onCompleteCalledRef.current = true
        onComplete?.()
      }
      return
    }

    // Reveal next characters
    const timer = setTimeout(() => {
      setDisplayedLength(prev => Math.min(prev + charsPerTick, totalLength))
    }, charDelay)

    return () => clearTimeout(timer)
  }, [content, displayedLength, charDelay, charsPerTick, onComplete])

  const displayedText = content.slice(0, displayedLength)

  return (
    <div className="streaming-text">
      <Markdown>{displayedText || '\u00A0'}</Markdown>
    </div>
  )
}
