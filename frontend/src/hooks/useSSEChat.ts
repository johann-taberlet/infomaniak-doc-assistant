import { useState, useCallback, useRef } from 'react'
import type { Message, MessageSegment, SSEEvent, Segment, UIComponent } from '../types'

// Debug logging with timestamps
const DEBUG = true
const startTime = Date.now()
const log = (action: string, data?: unknown) => {
  if (!DEBUG) return
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(3)
  console.log(`[${elapsed}s] [useSSEChat] ${action}`, data ?? '')
}

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

export function useSSEChat(options: UseSSEChatOptions = {}): UseSSEChatReturn {
  const [messages, setMessages] = useState<Message[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const sessionIdRef = useRef<string>(generateId())
  const eventSourceRef = useRef<EventSource | null>(null)
  // Collect segments as they arrive (already ordered by backend)
  const segmentsRef = useRef<MessageSegment[]>([])

  // Helper to get full text content from segments
  const getFullContent = (segments: MessageSegment[]): string => {
    return segments
      .filter((s): s is { type: 'text'; content: string } => s.type === 'text')
      .map(s => s.content)
      .join('')
  }

  // Handle incoming segment - update existing or add new
  const handleSegment = useCallback((segment: Segment) => {
    const segmentType = segment.type
    const segmentOrder = 'order' in segment ? segment.order : undefined

    if (segmentType === 'text') {
      log('SEGMENT RECEIVED', { type: 'text', order: segmentOrder, preview: segment.content.slice(0, 30) })
      segmentsRef.current.push({ type: 'text', content: segment.content })
    } else if (segmentType === 'step_guide' && segmentOrder !== undefined) {
      const stepCount = 'steps' in segment ? (segment.steps as unknown[])?.length : 0
      const existingIndex = segmentsRef.current.findIndex(
        s => s.type === 'component' &&
             s.component.type === 'step_guide' &&
             'order' in s.component &&
             (s.component as { order?: number }).order === segmentOrder
      )

      if (existingIndex >= 0) {
        log('SEGMENT RECEIVED', { type: 'step_guide', order: segmentOrder, steps: stepCount, action: 'UPDATE' })
        segmentsRef.current[existingIndex] = { type: 'component', component: segment as unknown as UIComponent }
      } else {
        log('SEGMENT RECEIVED', { type: 'step_guide', order: segmentOrder, steps: stepCount, action: 'NEW' })
        segmentsRef.current.push({ type: 'component', component: segment as unknown as UIComponent })
      }
    } else {
      log('SEGMENT RECEIVED', { type: segmentType, order: segmentOrder })
      segmentsRef.current.push({ type: 'component', component: segment as unknown as UIComponent })
    }
  }, [])

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

    // Track if we received an error (to prevent done from overwriting)
    let receivedError = false

    eventSource.onmessage = (event) => {
      try {
        const data: SSEEvent = JSON.parse(event.data)

        if ('error' in data) {
          // Server-side error - display error message to user
          receivedError = true
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, content: data.error, isError: true }
                : m
            )
          )
          // Close stream immediately on error
          eventSource.close()
          eventSourceRef.current = null
          setIsStreaming(false)
          options.onError?.(new Error(data.error))
        } else if ('done' in data && data.done) {
          // Don't overwrite if we already received an error
          if (receivedError) {
            return
          }

          log('DONE RECEIVED', { segmentCount: segmentsRef.current.length, language: data.language })

          // Stream complete - finalize message
          const finalSegments = [...segmentsRef.current]
          const finalContent = getFullContent(finalSegments)

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
          log('STREAMING ENDED')
          setIsStreaming(false)
          options.onStreamEnd?.(finalMessage)
        } else if ('status' in data) {
          // Status update - show progress to user
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, status: data.status }
                : m
            )
          )
        } else if ('segment' in data) {
          // Handle segment (update or add)
          handleSegment(data.segment)

          // Update message with current segments (clear status as we now have content)
          const currentSegments = [...segmentsRef.current]
          const currentContent = getFullContent(currentSegments)

          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, content: currentContent, segments: currentSegments, status: undefined }
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

      const currentSegments = [...segmentsRef.current]
      const currentContent = getFullContent(currentSegments)

      if (!currentContent) {
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId
              ? { ...m, content: 'Error: Could not get response. Please try again.', isError: true }
              : m
          )
        )
      } else {
        // Keep what we received
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId
              ? { ...m, content: currentContent, segments: currentSegments }
              : m
          )
        )
      }

      options.onError?.(new Error('Stream connection failed'))
    }
  }, [isStreaming, options, handleSegment])

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
