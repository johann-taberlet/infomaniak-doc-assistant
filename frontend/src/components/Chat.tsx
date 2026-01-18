import { useState, useRef, useEffect, useCallback, type FormEvent } from 'react'
import { useSSEChat } from '../hooks/useSSEChat'
import { MessageRenderer } from './MessageRenderer'
import { SuggestedQuestions } from './SuggestedQuestions'
import type { Message } from '../types'
import type { TTSStatus } from '../hooks/useTTS'
import './Chat.css'

interface ChatTranslations {
  placeholder: string
  emptyState: string
  send: string
  errorMessage: string
}

interface StatusTranslations {
  thinking: string
  understanding: string
  searching: string
  generating: string
}

interface TTSTranslations {
  listen: string
  stop: string
  readAloud: string
}

interface ChatProps {
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
  translations: ChatTranslations
  statusTranslations: StatusTranslations
  ttsTranslations: TTSTranslations
  lang: 'en' | 'fr'
}

export function Chat({ onTTSRequest, ttsStatus, translations, statusTranslations, ttsTranslations, lang }: ChatProps) {
  const [input, setInput] = useState('')
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Track if user manually scrolled up (wheel event, not programmatic scroll)
  const userScrolledUpRef = useRef(false)
  const programmaticScrollRef = useRef(false)
  const lastScrollTopRef = useRef(0)

  const { messages, isStreaming, sendMessage } = useSSEChat({
    onStreamEnd: () => {
      inputRef.current?.focus()
    },
  })

  // Scroll to bottom
  const scrollToBottom = useCallback(() => {
    const container = chatContainerRef.current
    if (!container || userScrolledUpRef.current) return

    programmaticScrollRef.current = true
    container.scrollTo({
      top: container.scrollHeight,
      behavior: 'smooth',
    })
  }, [])

  // Detect manual scroll via wheel event
  const handleWheel = useCallback((e: WheelEvent) => {
    // User scrolled up manually
    if (e.deltaY < 0) {
      userScrolledUpRef.current = true
    }
  }, [])

  // Track scroll position to detect if user scrolled back to bottom
  const handleScroll = useCallback(() => {
    const container = chatContainerRef.current
    if (!container) return

    // Ignore programmatic scrolls
    if (programmaticScrollRef.current) {
      programmaticScrollRef.current = false
      lastScrollTopRef.current = container.scrollTop
      return
    }

    const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight

    // If user scrolled back near bottom, re-enable auto-scroll
    if (distanceFromBottom < 50 && userScrolledUpRef.current) {
      userScrolledUpRef.current = false
    }

    lastScrollTopRef.current = container.scrollTop
  }, [])

  // Attach wheel listener
  useEffect(() => {
    const container = chatContainerRef.current
    if (!container) return

    container.addEventListener('wheel', handleWheel, { passive: true })
    return () => container.removeEventListener('wheel', handleWheel)
  }, [handleWheel])

  // Reset scroll lock when streaming starts (new message)
  useEffect(() => {
    if (isStreaming) {
      userScrolledUpRef.current = false
      scrollToBottom()
    }
  }, [isStreaming, scrollToBottom])

  // Use ResizeObserver on the container itself to detect any content size change
  useEffect(() => {
    const container = chatContainerRef.current
    if (!container) return

    // Observe the container's scroll height changes
    let lastHeight = container.scrollHeight

    const resizeObserver = new ResizeObserver(() => {
      const newHeight = container.scrollHeight
      if (newHeight > lastHeight) {
        lastHeight = newHeight
        scrollToBottom()
      } else if (newHeight !== lastHeight) {
        lastHeight = newHeight
      }
    })

    // Observe the container
    resizeObserver.observe(container)

    // Also use MutationObserver to catch DOM changes that might not trigger resize
    const mutationObserver = new MutationObserver(() => {
      const newHeight = container.scrollHeight
      if (newHeight > lastHeight) {
        lastHeight = newHeight
        scrollToBottom()
      } else if (newHeight !== lastHeight) {
        lastHeight = newHeight
      }
    })

    mutationObserver.observe(container, {
      childList: true,
      subtree: true,
      characterData: true,
    })

    return () => {
      resizeObserver.disconnect()
      mutationObserver.disconnect()
    }
  }, [scrollToBottom])

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isStreaming) return
    sendMessage(input)
    setInput('')
  }

  const handleSuggestionSelect = (question: string) => {
    if (isStreaming) return
    sendMessage(question)
  }

  return (
    <div className="chat">
      <div className="chat-container" ref={chatContainerRef} onScroll={handleScroll}>
        {messages.length === 0 && (
          <div className="chat-empty">
            <p>{translations.emptyState}</p>
          </div>
        )}
        {messages.map((message, index) => (
          <MessageRenderer
            key={message.id}
            message={message}
            onTTSRequest={onTTSRequest}
            ttsStatus={ttsStatus}
            isStreaming={isStreaming && index === messages.length - 1}
            statusTranslations={statusTranslations}
            ttsTranslations={ttsTranslations}
            errorMessage={translations.errorMessage}
          />
        ))}
      </div>
      {messages.length === 0 && (
        <SuggestedQuestions lang={lang} onSelect={handleSuggestionSelect} />
      )}
      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={translations.placeholder}
          disabled={isStreaming}
          autoComplete="off"
        />
        <button type="submit" disabled={isStreaming || !input.trim()}>
          {translations.send}
        </button>
      </form>
    </div>
  )
}
