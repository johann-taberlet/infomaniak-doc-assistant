import { useState, useCallback, useRef } from 'react'
import type { Message, MessageSegment, SSEEvent } from '../types'

interface UseSSEChatOptions {
  onStreamStart?: () => void
  onStreamEnd?: (message: Message) => void
  onError?: (error: Error) => void
}

interface UseSSEChatReturn {
  messages: Message[]
  isStreaming: boolean
  sendMessage: (content: string) => void
  clearMessages: () => void
}

function generateId(): string {
  return crypto.randomUUID()
}

function stripLangMarker(text: string): string {
  return text.replace(/\[LANG:\w{2}\]\s*$/, '').trim()
}

export function useSSEChat(options: UseSSEChatOptions = {}): UseSSEChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const sessionIdRef = useRef<string>(generateId())
  const eventSourceRef = useRef<EventSource | null>(null)
  // Track segments (interleaved text and components) and current text buffer
  const segmentsRef = useRef<MessageSegment[]>([])
  const textBufferRef = useRef<string>('')

  // Helper to build segments array for message updates
  const buildCurrentSegments = (): MessageSegment[] => {
    const segments = [...segmentsRef.current]
    // Add current text buffer as a segment if non-empty
    if (textBufferRef.current) {
      segments.push({ type: 'text', content: textBufferRef.current })
    }
    return segments
  }

  // Helper to get full text content from segments
  const getFullContent = (segments: MessageSegment[]): string => {
    return segments
      .filter((s): s is { type: 'text'; content: string } => s.type === 'text')
      .map(s => s.content)
      .join('')
  }

  const sendMessage = useCallback((content: string) => {
    if (isStreaming || !content.trim()) return

    // Add user message
    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: content.trim(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsStreaming(true)
    segmentsRef.current = []
    textBufferRef.current = ''
    options.onStreamStart?.()

    // Create assistant message placeholder
    const assistantId = generateId()
    setMessages(prev => [
      ...prev,
      {
        id: assistantId,
        role: 'assistant',
        content: '',
      },
    ])

    // Build URL with query parameters
    const url = `/chat/stream?message=${encodeURIComponent(content)}&session_id=${encodeURIComponent(sessionIdRef.current)}`

    const eventSource = new EventSource(url)
    eventSourceRef.current = eventSource

    eventSource.onmessage = (event) => {
      try {
        const data: SSEEvent = JSON.parse(event.data)

        if ('done' in data && data.done) {
          // Stream complete - finalize segments
          // Flush any remaining text buffer
          if (textBufferRef.current) {
            segmentsRef.current.push({
              type: 'text',
              content: textBufferRef.current,
            })
            textBufferRef.current = ''
          }

          // Add sources at the very end
          if (data.sources) {
            for (const source of data.sources) {
              segmentsRef.current.push({ type: 'component', component: source })
            }
          }

          // Build final message
          const finalSegments = [...segmentsRef.current]
          const rawContent = getFullContent(finalSegments)
          const finalContent = stripLangMarker(rawContent)

          // Strip lang marker from the last text segment
          for (let i = finalSegments.length - 1; i >= 0; i--) {
            if (finalSegments[i].type === 'text') {
              const textSeg = finalSegments[i] as { type: 'text'; content: string }
              textSeg.content = stripLangMarker(textSeg.content)
              break
            }
          }

          const finalMessage: Message = {
            id: assistantId,
            role: 'assistant',
            content: finalContent,
            language: data.language,
            segments: finalSegments.length > 0 ? finalSegments : undefined,
          }

          setMessages(prev =>
            prev.map(m => (m.id === assistantId ? finalMessage : m))
          )

          eventSource.close()
          eventSourceRef.current = null
          setIsStreaming(false)
          options.onStreamEnd?.(finalMessage)
        } else if ('token' in data) {
          // Append token to current text buffer
          textBufferRef.current += data.token
          const currentSegments = buildCurrentSegments()
          const currentContent = getFullContent(currentSegments)

          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, content: currentContent, segments: currentSegments }
                : m
            )
          )
        } else if ('ui_component' in data) {
          // Flush text buffer as a segment, then add component
          if (textBufferRef.current) {
            segmentsRef.current.push({
              type: 'text',
              content: textBufferRef.current,
            })
            textBufferRef.current = ''
          }

          // Add component segment
          segmentsRef.current.push({
            type: 'component',
            component: data.ui_component,
          })

          const currentSegments = buildCurrentSegments()
          const currentContent = getFullContent(currentSegments)

          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, content: currentContent, segments: currentSegments }
                : m
            )
          )
        }
      } catch (e) {
        console.error('Parse error:', e)
      }
    }

    eventSource.onerror = (error) => {
      console.error('EventSource error:', error)
      eventSource.close()
      eventSourceRef.current = null
      setIsStreaming(false)

      const currentSegments = buildCurrentSegments()
      const currentContent = getFullContent(currentSegments)

      if (!currentContent) {
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId
              ? { ...m, content: 'Error: Could not get response. Please try again.' }
              : m
          )
        )
      } else {
        // Keep what we received
        const finalContent = stripLangMarker(currentContent)
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId
              ? { ...m, content: finalContent, segments: currentSegments }
              : m
          )
        )
      }

      options.onError?.(new Error('Stream connection failed'))
    }
  }, [isStreaming, options])

  const clearMessages = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
    setMessages([])
    setIsStreaming(false)
    sessionIdRef.current = generateId()
  }, [])

  return {
    messages,
    isStreaming,
    sendMessage,
    clearMessages,
  }
}
