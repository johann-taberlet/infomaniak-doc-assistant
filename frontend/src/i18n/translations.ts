export interface Translations {
  appTitle: string
  theme: {
    light: string
    dark: string
    auto: string
  }
  chat: {
    placeholder: string
    emptyState: string
    send: string
    errorMessage: string
  }
  status: {
    thinking: string
    understanding: string
    searching: string
    generating: string
  }
  tts: {
    listen: string
    stop: string
    readAloud: string
  }
}

export const translations: Record<string, Translations> = {
  en: {
    appTitle: 'Infomaniak Doc Assistant',
    theme: {
      light: 'Light',
      dark: 'Dark',
      auto: 'Auto',
    },
    chat: {
      placeholder: 'Ask about kDrive, kMeet, or kChat...',
      emptyState: 'Ask about kDrive, kMeet, or kChat...',
      send: 'Send',
      errorMessage: 'Error: Could not get response. Please try again.',
    },
    status: {
      thinking: 'Thinking',
      understanding: 'Understanding your question',
      searching: 'Searching documentation',
      generating: 'Generating response',
    },
    tts: {
      listen: 'Listen',
      stop: 'Stop',
      readAloud: 'Read aloud',
    },
  },
  fr: {
    appTitle: 'Infomaniak Doc Assistant',
    theme: {
      light: 'Clair',
      dark: 'Sombre',
      auto: 'Auto',
    },
    chat: {
      placeholder: 'Posez une question sur kDrive, kMeet ou kChat...',
      emptyState: 'Posez une question sur kDrive, kMeet ou kChat...',
      send: 'Envoyer',
      errorMessage: 'Erreur : Impossible d\'obtenir une réponse. Veuillez réessayer.',
    },
    status: {
      thinking: 'Réflexion',
      understanding: 'Analyse de votre question',
      searching: 'Recherche dans la documentation',
      generating: 'Génération de la réponse',
    },
    tts: {
      listen: 'Écouter',
      stop: 'Arrêter',
      readAloud: 'Lire à voix haute',
    },
  },
}

export type Language = keyof typeof translations
