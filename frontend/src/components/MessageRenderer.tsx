import Markdown from 'react-markdown'
import type { Message, MessageSegment, UIComponent } from '../types'
import type { TTSStatus } from '../hooks/useTTS'
import { SourceCards } from './ui/SourceCards'
import { StepGuide } from './ui/StepGuide'
import { QuickActions } from './ui/QuickActions'
import { PlatformAvailability } from './ui/PlatformAvailability'

const AVAILABLE_LANGS = ['en', 'ko', 'es', 'pt', 'fr'] as const

interface MessageRendererProps {
  message: Message
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
}

function getEffectiveLanguage(message: Message): string {
  // If language is detected and supported, use it
  if (message.language && AVAILABLE_LANGS.includes(message.language as typeof AVAILABLE_LANGS[number])) {
    return message.language
  }
  // Default to English for TTS
  return 'en'
}

function renderUIComponent(component: UIComponent, key?: string) {
  switch (component.type) {
    case 'source_cards':
      return <SourceCards key={key || component.id} sources={component.sources} />
    case 'step_guide':
      return (
        <StepGuide
          key={key || component.id}
          title={component.title}
          steps={component.steps}
        />
      )
    case 'quick_actions':
      return <QuickActions key={key || component.id} actions={component.actions} />
    case 'platform_availability':
      return (
        <PlatformAvailability
          key={key || component.id}
          feature={component.feature}
          platforms={component.platforms}
        />
      )
    default:
      return null
  }
}

function renderSegment(segment: MessageSegment, index: number) {
  if (segment.type === 'text') {
    // Only render non-empty text segments
    if (!segment.content.trim()) return null
    return (
      <div key={`text-${index}`} className="message-content">
        <Markdown>{segment.content}</Markdown>
      </div>
    )
  } else {
    return renderUIComponent(segment.component, `component-${index}`)
  }
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
}: MessageRendererProps) {
  const isAssistant = message.role === 'assistant'
  // Show TTS for any assistant message with content
  const showTTS = isAssistant && message.content.length > 0

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
    if (message.segments && message.segments.length > 0) {
      // Render interleaved segments (text and components in order)
      return message.segments.map(renderSegment)
    }
    // Fallback: render content as single text block
    return (
      <div className="message-content">
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
