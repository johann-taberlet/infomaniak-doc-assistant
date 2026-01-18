import { useState, useCallback, useEffect, type ReactNode } from 'react'
import { Markdown } from './ui/Markdown'
import type { Message } from '../types'
import { AVAILABLE_LANGS, type TTSStatus } from '../hooks/useTTS'
import { StreamingSegments } from './ui/StreamingSegments'
import './ui/Markdown.css'

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

interface MessageRendererProps {
  message: Message
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
  /** True if this message is currently being streamed */
  isStreaming?: boolean
  statusTranslations: StatusTranslations
  ttsTranslations: TTSTranslations
  errorMessage: string
}

function isTTSLanguageSupported(message: Message): boolean {
  return !!message.language && AVAILABLE_LANGS.includes(message.language as typeof AVAILABLE_LANGS[number])
}

const SpeakerIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
    <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
    <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
  </svg>
)

const StopIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" stroke="none">
    <rect x="6" y="6" width="12" height="12" rx="2" />
  </svg>
)

const LoadingIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="tts-spinner">
    <path d="M12 2v4" />
    <path d="M12 18v4" />
    <path d="M4.93 4.93l2.83 2.83" />
    <path d="M16.24 16.24l2.83 2.83" />
    <path d="M2 12h4" />
    <path d="M18 12h4" />
    <path d="M4.93 19.07l2.83-2.83" />
    <path d="M16.24 7.76l2.83-2.83" />
  </svg>
)

function getTTSButtonContent(status?: TTSStatus): { icon: ReactNode; className: string } {
  const isLoading = status === 'loading' || status === 'generating'
  if (isLoading) {
    return { icon: <LoadingIcon />, className: 'tts-button loading' }
  }
  if (status === 'playing') {
    return { icon: <StopIcon />, className: 'tts-button playing' }
  }
  return { icon: <SpeakerIcon />, className: 'tts-button' }
}

function translateStatus(backendStatus: string | undefined, translations: StatusTranslations): string {
  if (!backendStatus) return translations.thinking

  const status = backendStatus.toLowerCase()

  // Map backend status strings to translation keys
  if (status.includes('understand')) {
    return translations.understanding
  }
  if (status.includes('search')) {
    return translations.searching
  }
  if (status.includes('generat')) {
    return translations.generating
  }

  return translations.thinking
}

export function MessageRenderer({
  message,
  onTTSRequest,
  ttsStatus,
  isStreaming = false,
  statusTranslations,
  ttsTranslations,
  errorMessage,
}: MessageRendererProps) {
  const isAssistant = message.role === 'assistant'

  // Track when streaming animation is complete (not just backend streaming)
  const [animationComplete, setAnimationComplete] = useState(false)

  // Reset animation state when streaming starts
  useEffect(() => {
    if (isStreaming) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- intentional reset on prop change
      setAnimationComplete(false)
    }
  }, [isStreaming])

  const handleAnimationComplete = useCallback(() => {
    setAnimationComplete(true)
  }, [])

  // Show TTS only if language is supported and all animations are complete
  const hasSegments = message.segments && message.segments.length > 0
  const showTTS = isAssistant &&
    message.content.length > 0 &&
    !message.isError &&
    !isStreaming &&
    isTTSLanguageSupported(message) &&
    (hasSegments ? animationComplete : true)

  const isDisabled = ttsStatus === 'loading' || ttsStatus === 'generating'

  const handleTTSClick = () => {
    // Language is already validated by showTTS condition
    onTTSRequest?.(message)
  }

  // Render assistant message content - use segments if available
  const renderAssistantContent = () => {
    // Show status or loading indicator while waiting for response
    if (!message.content && (!message.segments || message.segments.length === 0)) {
      const statusText = translateStatus(message.status, statusTranslations)
      return (
        <div className="message-content status-indicator">
          {statusText}<span className="thinking-dots"><span>.</span><span>.</span><span>.</span></span>
        </div>
      )
    }

    // Show error message with distinct styling
    if (message.isError) {
      const displayedError = message.isConnectionError ? errorMessage : message.content
      return (
        <div className="message-content error-content">
          {displayedError}
        </div>
      )
    }

    if (message.segments && message.segments.length > 0) {
      // Use StreamingSegments for queued animations
      return (
        <StreamingSegments
          segments={message.segments}
          isStreaming={isStreaming}
          messageId={message.id}
          onAnimationComplete={handleAnimationComplete}
        />
      )
    }

    // Fallback: render content as single text block
    return (
      <div className="message-content markdown-content">
        <Markdown>{message.content}</Markdown>
      </div>
    )
  }

  const ttsButton = getTTSButtonContent(ttsStatus)

  return (
    <div className={`message ${message.role}`}>
      {isAssistant ? (
        <>
          {renderAssistantContent()}
          {showTTS && (
            <div className="tts-button-container">
              <button
                className={ttsButton.className}
                onClick={handleTTSClick}
                title={ttsStatus === 'playing' ? ttsTranslations.stop : ttsTranslations.readAloud}
                disabled={isDisabled}
              >
                {ttsButton.icon}
                <span>{ttsTranslations.listen}</span>
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="message-content">{message.content}</div>
      )}
    </div>
  )
}
