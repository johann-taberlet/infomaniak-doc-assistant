import { Markdown } from './ui/Markdown'
import type { Message } from '../types'
import { AVAILABLE_LANGS, type TTSStatus } from '../hooks/useTTS'
import { StreamingSegments } from './ui/StreamingSegments'
import './ui/Markdown.css'

interface MessageRendererProps {
  message: Message
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
  /** True if this message is currently being streamed */
  isStreaming?: boolean
}

function getEffectiveLanguage(message: Message): string {
  // If language is detected and supported, use it
  if (message.language && AVAILABLE_LANGS.includes(message.language as typeof AVAILABLE_LANGS[number])) {
    return message.language
  }
  // Default to English for TTS
  return 'en'
}

function getTTSButtonContent(status?: TTSStatus): string {
  switch (status) {
    case 'loading':
      return '⏳'
    case 'generating':
      return '⏳'
    case 'playing':
      return '⏹'
    default:
      return '🔊'
  }
}

function getTTSButtonClass(status?: TTSStatus): string {
  const classes = ['tts-button']
  if (status === 'loading' || status === 'generating') {
    classes.push('loading')
  } else if (status === 'playing') {
    classes.push('playing')
  }
  return classes.join(' ')
}

export function MessageRenderer({
  message,
  onTTSRequest,
  ttsStatus,
  isStreaming = false,
}: MessageRendererProps) {
  const isAssistant = message.role === 'assistant'
  // Show TTS for any assistant message with content (not errors)
  const showTTS = isAssistant && message.content.length > 0 && !message.isError

  const isDisabled = ttsStatus === 'loading' || ttsStatus === 'generating'

  const handleTTSClick = () => {
    // Create a message with effective language for TTS
    const messageWithLang: Message = {
      ...message,
      language: getEffectiveLanguage(message),
    }
    onTTSRequest?.(messageWithLang)
  }

  // Render assistant message content - use segments if available
  const renderAssistantContent = () => {
    // Show status or loading indicator while waiting for response
    if (!message.content && (!message.segments || message.segments.length === 0)) {
      const statusText = message.status || 'Thinking'
      return (
        <div className="message-content status-indicator">
          {statusText}<span className="thinking-dots"><span>.</span><span>.</span><span>.</span></span>
        </div>
      )
    }

    // Show error message with distinct styling
    if (message.isError) {
      return (
        <div className="message-content error-content">
          {message.content}
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

  return (
    <div className={`message ${message.role}`}>
      {isAssistant ? (
        <>
          {renderAssistantContent()}
          {showTTS && (
            <button
              className={getTTSButtonClass(ttsStatus)}
              onClick={handleTTSClick}
              title={ttsStatus === 'playing' ? 'Stop' : 'Read aloud'}
              disabled={isDisabled}
            >
              {getTTSButtonContent(ttsStatus)}
            </button>
          )}
        </>
      ) : (
        <div className="message-content">{message.content}</div>
      )}
    </div>
  )
}
