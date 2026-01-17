import { useState, useCallback, useRef } from 'react'
import type { Message, UIComponent, SSEEvent } from '../types'

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
  const streamingMessageRef = useRef<string>('')
  const uiComponentsRef = useRef<UIComponent[]>([])

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
    streamingMessageRef.current = ''
    uiComponentsRef.current = []
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
          // Stream complete - add sources at the very end
          const finalContent = stripLangMarker(streamingMessageRef.current)

          // Combine inline components with sources (sources come last)
          const allComponents = [...uiComponentsRef.current]
          if (data.sources) {
            allComponents.push(...data.sources)
          }

          const finalMessage: Message = {
            id: assistantId,
            role: 'assistant',
            content: finalContent,
            language: data.language,
            uiComponents: allComponents.length > 0 ? allComponents : undefined,
          }

          setMessages(prev =>
            prev.map(m => (m.id === assistantId ? finalMessage : m))
          )

          eventSource.close()
          eventSourceRef.current = null
          setIsStreaming(false)
          options.onStreamEnd?.(finalMessage)
        } else if ('token' in data) {
          // Append token
          streamingMessageRef.current += data.token
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, content: streamingMessageRef.current }
                : m
            )
          )
        } else if ('ui_component' in data) {
          // Add inline UI component immediately (not sources)
          uiComponentsRef.current.push(data.ui_component)
          setMessages(prev =>
            prev.map(m =>
              m.id === assistantId
                ? { ...m, uiComponents: [...uiComponentsRef.current] }
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

      if (!streamingMessageRef.current) {
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId
              ? { ...m, content: 'Error: Could not get response. Please try again.' }
              : m
          )
        )
      } else {
        // Keep what we received
        const finalContent = stripLangMarker(streamingMessageRef.current)
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantId ? { ...m, content: finalContent } : m
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
