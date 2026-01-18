/**
 * Debug logging utility for streaming animation.
 * Enable by setting VITE_DEBUG_STREAMING=true in .env or localStorage.
 */

const DEBUG_KEY = 'debug_streaming'

export function isStreamingDebugEnabled(): boolean {
  // Check localStorage first (can be toggled at runtime)
  if (typeof localStorage !== 'undefined') {
    const stored = localStorage.getItem(DEBUG_KEY)
    if (stored === 'true') return true
  }
  // Then check env
  return import.meta.env.VITE_DEBUG_STREAMING === 'true'
}

type LogLevel = 'info' | 'warn' | 'state' | 'event'

interface LogEntry {
  timestamp: number
  component: string
  level: LogLevel
  message: string
  data?: Record<string, unknown>
}

// Keep last N entries in memory for inspection
const LOG_BUFFER_SIZE = 200
const logBuffer: LogEntry[] = []

function formatTime(timestamp: number): string {
  const date = new Date(timestamp)
  return `${date.toISOString().slice(11, 23)}`
}

export function streamingLog(
  component: string,
  level: LogLevel,
  message: string,
  data?: Record<string, unknown>
): void {
  if (!isStreamingDebugEnabled()) return

  const entry: LogEntry = {
    timestamp: Date.now(),
    component,
    level,
    message,
    data,
  }

  // Add to buffer
  logBuffer.push(entry)
  if (logBuffer.length > LOG_BUFFER_SIZE) {
    logBuffer.shift()
  }

  // Console output with color coding
  const colors: Record<LogLevel, string> = {
    info: '#888',
    warn: '#f90',
    state: '#0af',
    event: '#0f0',
  }

  const prefix = `%c[${formatTime(entry.timestamp)}] [${component}]`
  const style = `color: ${colors[level]}; font-weight: bold;`

  if (data) {
    console.log(prefix, style, message, data)
  } else {
    console.log(prefix, style, message)
  }
}

// Expose buffer for debugging in console
if (typeof window !== 'undefined') {
  ;(window as unknown as Record<string, unknown>).__streamingLogs = logBuffer
  ;(window as unknown as Record<string, unknown>).__enableStreamingDebug = () => {
    localStorage.setItem(DEBUG_KEY, 'true')
    console.log('Streaming debug enabled. Refresh or wait for next message.')
  }
  ;(window as unknown as Record<string, unknown>).__disableStreamingDebug = () => {
    localStorage.removeItem(DEBUG_KEY)
    console.log('Streaming debug disabled.')
  }
  ;(window as unknown as Record<string, unknown>).__dumpStreamingLogs = () => {
    console.table(
      logBuffer.map(e => ({
        time: formatTime(e.timestamp),
        component: e.component,
        level: e.level,
        message: e.message,
        ...e.data,
      }))
    )
  }
}
