import { useState, useRef, useEffect, type FormEvent } from 'react'
import { useSSEChat } from '../hooks/useSSEChat'
import { MessageRenderer } from './MessageRenderer'
import type { Message } from '../types'
import type { TTSStatus } from '../hooks/useTTS'
import './Chat.css'

interface ChatProps {
  onTTSRequest?: (message: Message) => void
  ttsStatus?: TTSStatus
}

export function Chat({ onTTSRequest, ttsStatus }: ChatProps) {
  const [input, setInput] = useState('')
  const chatContainerRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const { messages, isStreaming, sendMessage } = useSSEChat({
    onStreamEnd: () => {
      inputRef.current?.focus()
    },
  })

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [messages])

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isStreaming) return
    sendMessage(input)
    setInput('')
  }

  return (
    <div className="chat">
      <div className="chat-container" ref={chatContainerRef}>
        {messages.length === 0 && (
          <div className="chat-empty">
            <p>Ask about kDrive, kMeet, or kChat...</p>
          </div>
        )}
        {messages.map((message, index) => (
          <MessageRenderer
            key={message.id}
            message={message}
            onTTSRequest={onTTSRequest}
            ttsStatus={ttsStatus}
            isStreaming={isStreaming && index === messages.length - 1}
          />
        ))}
      </div>
      <form className="chat-form" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about kDrive, kMeet, or kChat..."
          disabled={isStreaming}
          autoComplete="off"
        />
        <button type="submit" disabled={isStreaming || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  )
}
