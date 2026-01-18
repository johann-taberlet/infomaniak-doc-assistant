import { useState, useCallback, useMemo, useEffect } from 'react'
import { Chat } from './components/Chat'
import { AccessDenied } from './components/AccessDenied'
import { TTSLoadingModal } from './components/TTSLoadingModal'
import { ThemeToggle } from './components/ThemeToggle'
import { useTTS, AVAILABLE_LANGS } from './hooks/useTTS'
import { useLocale } from './hooks/useLocale'
import type { Message } from './types'
import './App.css'

type TokenStatus = 'checking' | 'valid' | 'invalid'

function App() {
  const [showTTSModal, setShowTTSModal] = useState(false)
  const [tokenStatus, setTokenStatus] = useState<TokenStatus>('checking')
  const { status, loadProgress, error, load, speak, stop } = useTTS()
  const { lang, t } = useLocale()

  // Read token from URL query parameter (computed once on mount)
  const token = useMemo(() => {
    return new URLSearchParams(window.location.search).get('token')
  }, [])

  // Verify token with backend on mount
  useEffect(() => {
    if (!token) {
      setTokenStatus('invalid')
      return
    }

    const apiBase = import.meta.env.VITE_API_URL || ''
    fetch(`${apiBase}/metrics?token=${encodeURIComponent(token)}`)
      .then(response => {
        setTokenStatus(response.ok ? 'valid' : 'invalid')
      })
      .catch(() => {
        // Network error - allow access (backend might not require token)
        setTokenStatus('valid')
      })
  }, [token])

  const handleTTSRequest = useCallback(
    async (message: Message) => {
      if (!message.language || !AVAILABLE_LANGS.includes(message.language as typeof AVAILABLE_LANGS[number])) {
        return
      }

      // If currently playing, stop
      if (status === 'playing') {
        stop()
        return
      }

      // If not loaded, show modal and load
      if (status === 'idle' || status === 'error') {
        setShowTTSModal(true)
        const loaded = await load()
        if (loaded) {
          setShowTTSModal(false)
          await speak(message.content, message.language)
        }
      } else if (status === 'ready') {
        await speak(message.content, message.language)
      }
    },
    [status, load, speak, stop]
  )

  const handleCloseTTSModal = () => {
    setShowTTSModal(false)
  }

  // Show loading while checking token
  if (tokenStatus === 'checking') {
    return (
      <div className="app">
        <div className="app-loading" />
      </div>
    )
  }

  // Show access denied if token is invalid
  if (tokenStatus === 'invalid') {
    return (
      <div className="app">
        <AccessDenied translations={t.accessDenied} />
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>{t.appTitle}</h1>
        <ThemeToggle translations={t.theme} />
      </header>
      <main className="app-main">
        <Chat
          token={token}
          onTTSRequest={handleTTSRequest}
          ttsStatus={status}
          translations={t.chat}
          statusTranslations={t.status}
          ttsTranslations={t.tts}
          lang={lang}
        />
      </main>
      <TTSLoadingModal
        isOpen={showTTSModal && status === 'loading'}
        progress={loadProgress}
        error={error}
        onClose={handleCloseTTSModal}
      />
    </div>
  )
}

export default App
