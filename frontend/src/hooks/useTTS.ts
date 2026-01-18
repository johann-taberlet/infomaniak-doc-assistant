import { useState, useRef, useCallback } from 'react'
import * as ort from 'onnxruntime-web'
import {
  TextToSpeech,
  Style,
  loadTextToSpeechParallel,
  loadVoiceStyle,
  writeWavFile,
  checkWebGPUSupport,
  AVAILABLE_LANGS,
  type ProgressCallback,
} from '../utils/tts'
import { stripMarkdown } from '../utils/text'

export { AVAILABLE_LANGS }

export type TTSStatus = 'idle' | 'loading' | 'ready' | 'generating' | 'playing' | 'error'

interface UseTTSOptions {
  onnxDir?: string
  voiceStylePath?: string
}

interface UseTTSReturn {
  status: TTSStatus
  loadProgress: { modelName: string; current: number; total: number } | null
  error: string | null
  load: () => Promise<boolean>
  speak: (text: string, lang: string) => Promise<void>
  stop: () => void
}

/**
 * Strip language marker from text
 */
function stripLangMarker(text: string): string {
  return text.replace(/\[LANG:\w{2}\]\s*$/, '').trim()
}

export function useTTS(options: UseTTSOptions = {}): UseTTSReturn {
  const {
    onnxDir = '/static/tts/onnx',
    voiceStylePath = '/static/tts/voice_styles/F2.json',
  } = options

  const [status, setStatus] = useState<TTSStatus>('idle')
  const [loadProgress, setLoadProgress] = useState<{
    modelName: string
    current: number
    total: number
  } | null>(null)
  const [error, setError] = useState<string | null>(null)

  const ttsRef = useRef<TextToSpeech | null>(null)
  const styleRef = useRef<Style | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const audioUrlRef = useRef<string | null>(null)

  const load = useCallback(async (): Promise<boolean> => {
    if (status === 'ready' || status === 'loading') {
      return status === 'ready'
    }

    setStatus('loading')
    setError(null)

    try {
      // Configure ONNX Runtime
      ort.env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.23.0/dist/'
      ort.env.wasm.numThreads = 1

      // Check WebGPU support
      const webgpuSupported = await checkWebGPUSupport()
      const executionProvider = webgpuSupported ? 'webgpu' : 'wasm'

      const sessionOptions: ort.InferenceSession.SessionOptions = {
        executionProviders: [executionProvider],
        graphOptimizationLevel: 'all',
      }

      const progressCallback: ProgressCallback = (modelName, current, total) => {
        setLoadProgress({ modelName, current, total })
      }

      const { textToSpeech } = await loadTextToSpeechParallel(
        onnxDir,
        sessionOptions,
        progressCallback
      )
      ttsRef.current = textToSpeech

      // Load voice style
      const style = await loadVoiceStyle([voiceStylePath])
      styleRef.current = style

      setStatus('ready')
      setLoadProgress(null)
      return true
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load TTS')
      setStatus('error')
      return false
    }
  }, [status, onnxDir, voiceStylePath])

  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.currentTime = 0
      audioRef.current = null
    }
    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current)
      audioUrlRef.current = null
    }
    if (status === 'playing') {
      setStatus('ready')
    }
  }, [status])

  const speak = useCallback(
    async (text: string, lang: string) => {
      if (!ttsRef.current || !styleRef.current) {
        const loaded = await load()
        if (!loaded) return
      }

      // Stop any currently playing audio
      stop()

      setStatus('generating')

      try {
        const plainText = stripMarkdown(stripLangMarker(text))

        const { wav } = await ttsRef.current!.call(
          plainText,
          lang,
          styleRef.current!,
          10, // totalStep
          1.05, // speed
          0.3 // silenceDuration
        )

        // Convert to WAV blob
        const wavBuffer = writeWavFile(wav, ttsRef.current!.sampleRate)
        const blob = new Blob([wavBuffer], { type: 'audio/wav' })
        const url = URL.createObjectURL(blob)
        audioUrlRef.current = url

        // Play audio
        const audio = new Audio(url)
        audioRef.current = audio

        setStatus('playing')

        audio.onended = () => {
          URL.revokeObjectURL(url)
          audioUrlRef.current = null
          audioRef.current = null
          setStatus('ready')
        }

        audio.onerror = () => {
          URL.revokeObjectURL(url)
          audioUrlRef.current = null
          audioRef.current = null
          setStatus('ready')
        }

        await audio.play()
      } catch (err) {
        setError(err instanceof Error ? err.message : 'TTS error')
        setStatus('ready')
      }
    },
    [load, stop]
  )

  return {
    status,
    loadProgress,
    error,
    load,
    speak,
    stop,
  }
}
