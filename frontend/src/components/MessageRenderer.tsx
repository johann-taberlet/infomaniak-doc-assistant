import Markdown from 'react-markdown'
import type { Message, UIComponent } from '../types'
import type { TTSStatus } from '../hooks/useTTS'
import { SourceCards } from './ui/SourceCards'
import { StepGuide } from './ui/StepGuide'
import { QuickActions } from './ui/QuickActions'
import { PlatformAvailability } from './ui/PlatformAvailability'

const AVAILABLE_LANGS = ['en', 'ko', 'es', 'pt', 'fr']

interface MessageRendererProps {
  message: Message
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
}

function renderUIComponent(component: UIComponent) {
  switch (component.type) {
    case 'source_cards':
      return <SourceCards key={component.id} sources={component.sources} />
    case 'step_guide':
      return (
        <StepGuide
          key={component.id}
          title={component.title}
          steps={component.steps}
        />
      )
    case 'quick_actions':
      return <QuickActions key={component.id} actions={component.actions} />
    case 'platform_availability':
      return (
        <PlatformAvailability
          key={component.id}
          feature={component.feature}
          platforms={component.platforms}
        />
      )
    default:
      return null
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
  const showTTS =
    isAssistant &&
    message.language &&
    AVAILABLE_LANGS.includes(message.language) &&
    message.content.length > 0

  const isDisabled = ttsStatus === 'loading' || ttsStatus === 'generating'

  return (
    <div className={`message ${message.role}`}>
      {isAssistant ? (
        <>
          <div className="message-content">
            <Markdown>{message.content}</Markdown>
          </div>
          {message.uiComponents?.map(renderUIComponent)}
          {showTTS && (
            <button
              className={getTTSButtonClass(ttsStatus)}
              onClick={() => onTTSRequest?.(message)}
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
