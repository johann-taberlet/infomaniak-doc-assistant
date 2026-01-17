import './TTSLoadingModal.css'

interface TTSLoadingModalProps {
  isOpen: boolean
  progress: { modelName: string; current: number; total: number } | null
  error: string | null
  onClose: () => void
}

export function TTSLoadingModal({
  isOpen,
  progress,
  error,
  onClose,
}: TTSLoadingModalProps) {
  if (!isOpen) return null

  const progressPercent = progress
    ? (progress.current / progress.total) * 100
    : 0

  return (
    <div className="tts-loading-modal">
      <div className="tts-loading-content">
        {error ? (
          <>
            <h3>Failed to Load TTS</h3>
            <p className="tts-error">{error}</p>
            <button className="tts-retry-btn" onClick={onClose}>
              Close
            </button>
          </>
        ) : (
          <>
            <h3>Downloading TTS Model</h3>
            <p className="tts-loading-status">
              {progress
                ? `Loading ${progress.modelName} (${progress.current}/${progress.total})...`
                : 'Initializing...'}
            </p>
            <div className="tts-progress-bar">
              <div
                className="tts-progress-fill"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </>
        )}
      </div>
    </div>
  )
}
