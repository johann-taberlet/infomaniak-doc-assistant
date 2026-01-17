import { useState, useCallback } from 'react'
import { Chat } from './components/Chat'
import { TTSLoadingModal } from './components/TTSLoadingModal'
import { useTTS, AVAILABLE_LANGS } from './hooks/useTTS'
import type { Message } from './types'
import './App.css'

function App() {
  const [showTTSModal, setShowTTSModal] = useState(false)
  const { status, loadProgress, error, load, speak, stop } = useTTS()

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

  const handleCloseTTSModal = useCallback(() => {
    setShowTTSModal(false)
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>Infomaniak Doc Assistant</h1>
      </header>
      <main className="app-main">
        <Chat onTTSRequest={handleTTSRequest} ttsStatus={status} />
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
